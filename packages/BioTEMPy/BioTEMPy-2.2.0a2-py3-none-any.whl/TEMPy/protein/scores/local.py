# =============================================================================
#     This file is part of TEMPy.
#
#     TEMPy is a software designed to help the user in the manipulation
#     and analyses of macromolecular assemblies using 3D electron microscopy
#     maps.
#
#     Copyright  2015 Birkbeck College University of London.
#
#     Authors: Maya Topf, Daven Vasishtan, Arun Prasad Pandurangan,
#     Irene Farabella, Agnel-Praveen Joseph, Harpal Sahota
#
#     This software is made available under GPL V3 license
#     http://www.gnu.org/licenses/gpl-3.0.html
#
#
#     Please cite your use of TEMPy in published work:
#
#     Farabella, I., Vasishtan, D., Joseph, A.P., Pandurangan, A.P., Sahota, H.
#     & Topf, M. (2015). J. Appl. Cryst. 48.
#
# =============================================================================

from collections import OrderedDict

import numpy as np
import pyfftw

from . import base_classes, glob
from TEMPy.protein.blur import StructureBlurrer, GlobalBlurrer
from TEMPy.math import fourier
from TEMPy.maps.em_map import Map


class FastSMOC(base_classes._AbstractSlidingScore):
    """A faster version of the sliding window SMOC score.

    Unlike the original algorithm, this ones is optimized in the
    following ways:

    * lazily determines required voxels saving space and time.
    * The sliding-window calculation is performed in time proportional
      only to chain size and not window size.

    This method does not offer all the bells and whistles of old SMOC
    function such as rigid body parameters.  However, two alternative
    methods are provided for dealing with SMOC scores for unmodelled
    regions.

    The function `score_chain_contig`, will score all contigs in a
    chain where each window only contains residues belonging to the
    contig.

    The function `score_chain_span` mimicks the old SMOC behaviour.
    Windows ignore contigs boundaries (they 'span' them), thus residues
    in windows may be physically distant.

    In general, the consider using the `score_chain_contig` method.


    Args:
        struct (:class:`BioPy_Structure <TEMPy.protein.prot_rep_biopy.BioPy_Structure>`): Model to score
        exp_map (:class:`EMMap <TEMPy.maps.em_map.Map>`): Experimental density map
        resolution (float): The resolution of the experimental map
        sigma_coeff (float, optional): The sigma coefficient for simulating the map. Defaults to 0.225.
        sigma_threshold (float, optional): The sigma threshold determines the radius around the atoms to consider. Defaults to 2.5.
        sim_map (EMMap, optional): A simulated map to use instead of generating one.
    Returns:
        FastSMOC object
    """

    def __init__(
        self,
        struct,
        exp_map,
        resolution,
        sigma_coeff=0.225,
        sigma_threshold=2.5,
        sim_map=None,
    ):
        radius = sigma_threshold * max(sigma_coeff * resolution, 1.0)
        if sim_map is None:
            sim_map = GlobalBlurrer(resolution).blur_structure(struct, exp_map)
        moc = base_classes._MOCAccumulator(exp_map, sim_map, radius)
        super().__init__(struct, moc)


class SlidingMI(base_classes._AbstractSlidingScore):
    """ """

    def __init__(self, struct, exp_map, res_or_blurrer, radius, no_bins=20):
        self.exp_map = exp_map
        self.radius = radius
        self.no_bins = no_bins
        if isinstance(res_or_blurrer, StructureBlurrer):
            blurrer = res_or_blurrer
        else:
            blurrer = GlobalBlurrer(res_or_blurrer)
        sim_map = blurrer.blur_structure(struct, exp_map)
        mi = base_classes._MIAccumulator(exp_map, sim_map, radius, no_bins, no_bins)
        super().__init__(struct, mi)


def LoQFit(
    structure,
    target_map,
    resolution_map_target,
    sim_map=None,
    max_res=18.0,
    verbose=True,
    half_map_1=None,
    half_map_2=None,
):
    """Calculate the LoQFit score for each residue in a model.

    The LoQFit score is essentially a local implementation of the
    map-model FSC. More information can be found here:
    https://www.biorxiv.org/content/10.1101/2022.06.08.495259v1

    Arguments:
        structure: Model structure instance
        target_map: Experimental Map instance
        resolution_map_target: The resolution of the target map
        sim_map: Pre-calculated simulated map - will be calculated
            automatically if not supplied
        max_res: The maximum allowed LoQFit score for any residue, this
            parameter prevents
        verbose: If True, prints a progress bar and warnings
        half_map_1: A map instance of a half-map from reconstruction of the
            target map. If supplied (with second half map), this will be
            used to normalise the LoQFit score
        half_map_2: A map instance of the second half map from
            target_map reconstruction.

    Returns:
        The LoQFit score for each residue in structure instance.
        The output is a dictionary with keys:
              (chain_id, residue_number)
        where each value is the LoQFit score for a given residue. If
        half_map_1 and half_map_2 arguments are supplied the LoQFit
        score will be normalised based on the local resolution.
    """
    print(
        f"Calculating LoQFit score for model {structure.filename} into "
        f"map {target_map.filename}"
    )

    # set up some stuff
    target_map.apix = np.array(target_map.apix)
    blurrer = GlobalBlurrer(resolution_map_target)

    if sim_map is None:
        sim_map = blurrer.blur_structure(structure, target_map)
    fsc_threshold = 0.5
    sim_map.normalise_to_1_minus1(in_place=True)
    target_map.normalise_to_1_minus1(in_place=True)

    # approximate mask sphere diameter
    sphere_diameter_angstroms = resolution_map_target * 5
    sphere_diameter_pixels = int(sphere_diameter_angstroms / target_map.apix[0])

    # ensure that parameters are sensible i.e. not a 1 pixel wide mask
    if sphere_diameter_pixels < 6:
        sphere_diameter_pixels = 6
    cos_edge = int(round(sphere_diameter_pixels / 3))
    if cos_edge < 10:
        cos_edge = 10

    if half_map_1 is not None and half_map_2 is not None:
        interpolate_cutoff = False
        normalise_with_half_map = True
        half_map_1.origin = target_map.origin
        half_map_2.origin = target_map.origin
    else:
        interpolate_cutoff = True
        normalise_with_half_map = False

    # get an appropriate box size to crop from main map
    # will be 2^n, 3^n or 5^n size where n is the number required for
    # the minimum box size needed to encompass entire mask in box
    mask_dims = fourier.get_fft_optimised_box_size(
        sphere_diameter_pixels + (2 * cos_edge), target_map.fullMap.shape
    )

    if mask_dims == [0, 0, 0]:
        mask = Map(
            np.ones(target_map.fullMap.shape),
            target_map.origin,
            target_map.apix,
            target_map.filename,
        )
        mask_dims = mask.fullMap.shape
    else:
        centre_of_mask_map = [mask_dims[0] / 2, mask_dims[1] / 2, mask_dims[2] / 2]
        mask = blurrer.make_spherical_mask(
            sphere_diameter_pixels, mask_dims, centre_of_mask_map, cos_edge
        )

    # save scores for each chain and res
    dict_res_scores = OrderedDict()
    chains = structure.split_into_chains()
    number_of_residues = structure.number_of_residues()

    # set up pyfftw for very fast ffts
    input1 = pyfftw.empty_aligned(mask_dims, dtype="float64")
    fftw_object1 = fourier.get_pyfftw_object(mask_dims)
    fftw_object2 = fourier.get_pyfftw_object(mask_dims)

    # precompute these to speed up calculations
    qbins, labelled_shells = fourier.get_labelled_shells(input1.shape)

    warnings = []
    res_no = 0

    for chain in chains:
        for atom in chain.atomList:
            if atom.atom_name == "CA" or atom.atom_name == "C1'":
                pass
            else:
                continue

            cropped_map_1 = target_map.get_cropped_box_around_atom(
                atom,
                mask_dims,
            ).fullMap
            cropped_map_2 = sim_map.get_cropped_box_around_atom(
                atom,
                mask_dims,
            ).fullMap
            fsc = fourier.calculate_fsc_with_mask(
                cropped_map_1,
                cropped_map_2,
                mask.fullMap,
                pixel_size=target_map.apix[0],
                labelled_shells=labelled_shells,
                qbins=qbins,
                fftw_object1=fftw_object1,
                fftw_object2=fftw_object2,
            )

            # find highest frequency shell with 0.5 correlation
            freq_at_corr_cutoff = fourier.get_fsc_resolution(
                fsc,
                fsc_threshold=fsc_threshold,
                interpolate_cutoff=interpolate_cutoff,
                use_highest_resolution=True,
            )

            # freq_at_cutoff can = 0 if correlation never drops below 0.5
            if freq_at_corr_cutoff < min(target_map.apix) * 2:
                freq_at_corr_cutoff = min(target_map.apix) * 2
                warnings.append(
                    f"Warning: FSC at residue {atom.res_no} in"
                    f" chain {atom.chain} never falls below "
                    f"0.5. LoQFit score for this residue set "
                    f"to {freq_at_corr_cutoff}. This is NOT "
                    f"expected and NOT an indication of a "
                    f"good fit between map and model."
                )

            # If there is poor correlation in low resolution shells the
            # freq_at_cutoff can be ridiculously high (i.e. >100 angstroms)
            # which ruins the scaling when the score is plotted
            if freq_at_corr_cutoff > max_res:
                warnings.append(
                    f"Warning: Residue {atom.res_no} in chain "
                    f"{atom.chain} has local resolution of "
                    f" {freq_at_corr_cutoff}, which is set "
                    f"to {max_res}"
                )
                freq_at_corr_cutoff = max_res

            if normalise_with_half_map:
                crop_hmap_1 = half_map_1.get_cropped_box_around_atom(
                    atom,
                    mask_dims,
                )
                crop_hmap_2 = half_map_2.get_cropped_box_around_atom(
                    atom,
                    mask_dims,
                )
                fsc = fourier.calculate_fsc_with_mask(
                    crop_hmap_1.fullMap,
                    crop_hmap_2.fullMap,
                    mask.fullMap,
                    pixel_size=target_map.apix[0],
                    labelled_shells=labelled_shells,
                    qbins=qbins,
                    fftw_object1=fftw_object1,
                    fftw_object2=fftw_object2,
                )
                local_res = fourier.get_fsc_resolution(
                    fsc,
                    fsc_threshold=0.5,
                    interpolate_cutoff=False,
                    use_highest_resolution=True,
                )
                freq_at_corr_cutoff = freq_at_corr_cutoff / local_res

            dict_res_scores[(atom.chain, int(atom.res_no))] = freq_at_corr_cutoff

            res_no += 1
            if verbose:
                zfill_len = len(str(number_of_residues))
                print(
                    f"\rProcessed residue {str(res_no).zfill(zfill_len)}"
                    f"/{number_of_residues}",
                    sep="",
                    end="",
                    flush=True,
                )

    if verbose:
        print("")
        for warning in warnings:
            print(warning)

    return dict_res_scores


def local_resolution(
    half_map_1,
    half_map_2,
    structure=None,
    protein_mask=None,
    verbose=True,
    fsc_threshold=0.5,
):
    """Calculate the local resolution using the local FSC method.

    Arguments:
        half_map_1: A map instance of the first half-map.
        half_map_2: A map instance of the second half map.
        structure: Model structure instance. If defined, the
            local resolution is calculated at the CA atom
            for each residue in the structure only.
        protein_mask: A Map instance of a mask. If defined, the
            local resolution is calculated at each point within
            the mask only.
        verbose: If True, prints a progress bar and warnings
        fsc_threshold: Correlation threshold value that defines
            how the map resolution is found.

    Returns:
        The local resolution at each position in the map, or as
        defined by the structure instance or mask. The output
        is a dictionary where each key has the format:
                        (z, y, x)
        where z, y, x is a 3D-index from the half maps, and the
        value is the local resolution (in angstroms).
    """
    print(
        f"Calculating Local Resolution for half map:"
        f"{half_map_1.filename} and map {half_map_2.filename}"
    )

    # set up some stuff
    apix = np.array(half_map_1.apix)[0]
    map_res = glob.map_resolution_FSC(half_map_1, half_map_2)
    blurrer = StructureBlurrer()

    # approximate mask sphere diameter
    sphere_diameter_angstroms = map_res * 7
    sphere_diameter_pixels = int(sphere_diameter_angstroms / apix)

    # ensure that parameters are sensible i.e. not a 1 pixel wide mask
    if sphere_diameter_pixels < 6:
        sphere_diameter_pixels = 6
    cos_edge = int(round(sphere_diameter_pixels / 3))
    if cos_edge < 10:
        cos_edge = 10

    # get an appropriate box size to crop from main map
    # will be 2^n, 3^n or 5^n size where n is the number required for
    # the minimum box size needed to encompass entire mask in box
    mask_dims = fourier.get_fft_optimised_box_size(
        sphere_diameter_pixels + (cos_edge * 2),
        half_map_1.fullMap.shape,
    )

    if mask_dims == [0, 0, 0]:
        mask = Map(
            np.ones(half_map_1.fullMap.shape),
            half_map_1.origin,
            half_map_1.apix,
            half_map_1.filename,
        )
        mask_dims = mask.fullMap.shape
    else:
        centre_of_mask_map = [mask_dims[0] / 2, mask_dims[1] / 2, mask_dims[2] / 2]
        mask = blurrer.make_spherical_mask(
            sphere_diameter_pixels, mask_dims, centre_of_mask_map, cos_edge
        )

    # save scores for each chain and res
    dict_res_scores = OrderedDict()

    # set up pyfftw for very fast ffts
    input1 = pyfftw.empty_aligned(mask_dims, dtype="float64")

    fftw_object1 = fourier.get_pyfftw_object(mask_dims)
    fftw_object2 = fourier.get_pyfftw_object(mask_dims)

    qbins, labelled_shells = fourier.get_labelled_shells(input1.shape)

    # get coordinates where local FSC should be calculated
    if structure is not None:
        coordinates = structure.get_CAonly().get_atom_zyx_map_indexes(half_map_1)
    elif protein_mask is not None:
        (z, y, x) = np.where(protein_mask.fullMap > 0)
        coordinates = np.stack((z, y, x), axis=-1)
    else:
        (z, y, x) = np.where(half_map_1.fullMap < np.inf)
        coordinates = np.stack((z, y, x), axis=-1)

    warnings = []
    n = 0

    for coordinate in coordinates:

        cropped_map_1 = half_map_1.get_cropped_box(
            coordinate,
            mask_dims,
        )
        cropped_map_2 = half_map_2.get_cropped_box(
            coordinate,
            mask_dims,
        )

        fsc = fourier.calculate_fsc_with_mask(
            cropped_map_1.fullMap,
            cropped_map_2.fullMap,
            mask.fullMap,
            pixel_size=apix,
            labelled_shells=labelled_shells,
            qbins=qbins,
            fftw_object1=fftw_object1,
            fftw_object2=fftw_object2,
        )

        # find highest frequency shell with 0.5 correlation
        freq_at_corr_cutoff = fourier.get_fsc_resolution(
            fsc,
            fsc_threshold=fsc_threshold,
            interpolate_cutoff=False,
            use_highest_resolution=True,
        )

        # FSC can go below nyquist frequency when shells never drop
        # below 0.5 correlation and freq_at_corr_cutoff still equals 0
        if freq_at_corr_cutoff < min(half_map_1.apix) * 2:
            freq_at_corr_cutoff = min(half_map_1.apix) * 2
            warnings.append(
                f"Warning: FSC at coordinate {coordinate}"
                f" never falls below 0.5. SLRS "
                f"score for this residue set to "
                f"{freq_at_corr_cutoff}. This is NOT "
                f"expected and NOT an indication of a good "
                f"fit between map and model."
            )

        dict_res_scores[tuple(coordinate)] = freq_at_corr_cutoff

        n += 1
        if verbose:
            zfill_len = len(str(len(coordinates)))
            print(
                f"\rProcessed residue {str(n).zfill(zfill_len)}" f"/{len(coordinates)}",
                sep="",
                end="",
                flush=True,
            )

    if verbose:
        print("")
        for warning in warnings:
            print(warning)

    return dict_res_scores
