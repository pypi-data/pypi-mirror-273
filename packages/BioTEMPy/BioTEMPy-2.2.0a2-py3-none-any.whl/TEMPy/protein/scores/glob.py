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

import sys
import math
import itertools

import numpy as np
from scipy import stats
from scipy.ndimage import laplace

from TEMPy.protein.structure_blurrer import StructureBlurrer
from TEMPy.math import fourier, vector

class MapScore:
    def score_maps(self, target_map, sim_map):
        assert_map_equivalent(target_map, sim_map)
        self.score_arrays(target_map.fullMap, sim_map.fullMap)

    def score_arrays(self, target_array, sim_array):
        # Map scores should implement this.
        pass


def map_model_fsc_resolution(
    structure,
    target_map,
    map_resolution,
    mask=None,
    sim_map=None,
    cutoff_correlation=0.5,
    use_highest_resolution=True,
):
    """Calculate the Map-model "resolution" using Fourier Shell Correlation
    (FSC).

    Arguments:
        structure: A model structure instance.
        target_map: A Map instance.
        map_resolution: The resolution of target_map
        mask: A Map instance of a soft-edged mask.
        sim_map: A Map instance of a pre-calculated simulated map, if
            not explicitly supplied it will be calculated automatically
            from the structure instance.
        cutoff_correlation: Threshold correlation used to define the
            model-map "resolution".
        use_highest_resolution: If True, the highest resolution shell
            that crosses the cutoff_correlation threshold is taken.
            Otherwise, the frequency that first crosses the threshold
            is taken.

    Returns:
        Map-model FSC "resolution": The fourier shell frequency
        (in angstroms) where the correlation crosses the stated
        threshold.
    """

    if sim_map is None:
        blurrer = StructureBlurrer(with_vc=True)
        sim_map = blurrer.gaussian_blur_real_space(
            structure,
            map_resolution,
            densMap=target_map,
        )

    fsc = map_model_fsc(
        structure, target_map, map_resolution, mask=mask, sim_map=sim_map
    )

    max_frequency_at_cutoff = fourier.get_fsc_resolution(
        fsc,
        fsc_threshold=cutoff_correlation,
        interpolate_cutoff=False,
        use_highest_resolution=use_highest_resolution,
    )

    return max_frequency_at_cutoff


def map_model_fsc(structure, target_map, map_resolution, mask=None, sim_map=None):
    """Calculate the map-model Fourier Shell Correlation (FSC).

    Arguments:
        structure: A model structure instance.
        target_map: A Map instance.
        map_resolution: The resolution of target_map
        mask: A Map instance of a soft-edged mask.
        sim_map: A Map instance of a pre-calculated simulated map, if
            not explicitly supplied it will be calculated automatically
            from the structure instance

    Returns:
        The map-model FSC as an np.array with shape (2, (N / 2) + 1) for
        an input map with shape (N, N, N). Output has format:
                [[shell frequency (angstroms), correlation]
                            ........
                [shell frequency (angstroms), correlation]]

    """
    if sim_map is None:
        blurrer = StructureBlurrer(with_vc=True)
        sim_map = blurrer.gaussian_blur_real_space(
            structure,
            map_resolution,
            densMap=target_map,
        )

    if mask:
        fsc = fourier.calculate_fsc_with_mask(
            target_map.fullMap,
            sim_map.fullMap,
            mask,
            pixel_size=target_map.apix[0],
        )
    else:
        fsc = fourier.calculate_fsc(
            target_map.fullMap,
            sim_map.fullMap,
            pixel_size=target_map.apix[0],
        )

    return fsc


def map_resolution_FSC(
    half_map1, half_map2, mask=None, fsc_threshold=0.143, use_highest_resolution=True
):
    """Calculate the map resolution from two half-maps using the
    Fourier Shell Correlation.

    Arguments:
        half_map1: Map instance of first half map
        half_map2: Map instance of second half map
        mask: A Map instance of a soft edged mask
        fsc_threshold: Correlation threshold value that defines
            how the map resolution is found.
        use_highest_resolution: If True, takes the highest
            resolution shell that crosses the fsc_threshold, if
            there are multiple crossovers.

    Returns:
        The FSC resolution (in angstroms).

    """
    if mask is not None:
        fsc = fourier.calculate_fsc_with_mask(
            half_map1.fullMap,
            half_map2.fullMap,
            mask.fullMap,
            pixel_size=half_map1.apix[0],
        )
    else:
        fsc = fourier.calculate_fsc(
            half_map1.fullMap,
            half_map2.fullMap,
            pixel_size=half_map1.apix[0],
        )

    resolution = fourier.get_fsc_resolution(
        fsc,
        fsc_threshold=fsc_threshold,
        use_highest_resolution=use_highest_resolution,
        interpolate_cutoff=False,
    )

    return resolution


class MI(MapScore):
    """Calculate the mutual information score between two Map instances.

    Arguments:
        bins1: Number of bins to divide densities into from exp_map.
        bins2: Number of bins to divide densities from sim_map.
    Returns:
        MI scoring object
    """
    # code modified from https://stackoverflow.com/questions/20491028
    def __init__(self, bins1=20, bins2=20):
        self.bins1 = bins1
        self.bins2 = bins2

    def score_arrays(self, target_array, sim_array):
        c_xy, x, y = np.histogram2d(
            target_array.ravel(), sim_array.ravel(), bins=[self.bins1, self.bins2]
        )

        g, _, _, _ = stats.chi2_contingency(c_xy, lambda_="log-likelihood")

        mi_nl = 0.5 * g / c_xy.sum()

        return np.log2(np.exp(mi_nl))


def calculate_alcps(ref_chain, probe_chain):
    """
    Calculate the Arc Length Component Placement Score between two models.
    Generally, this score is calculated between individual chains in a
    structure.

    Inputs:
        ref_chain:
            One of the input structure instances being compared
        probe_chain:
            The other input structure instance being compared
    Output:
        alcps:
            Arc Length Component Placement Score
    """

    diff_vec = ref_chain.CoM - probe_chain.CoM
    r = diff_vec.mod()

    ref_matrix = vector.get_coordinate_mass_array(ref_chain)
    probe_matrix = vector.get_coordinate_mass_array(probe_chain)

    rotation_matrix, _t = vector.get_transform(ref_matrix, probe_matrix)

    theta, n1, n2, n3 = vector._rotmat_to_axisangle(rotation_matrix)
    theta = math.degrees(theta)

    alcps = 2 * math.pi * r * theta / 360

    return alcps


def get_log10_alcps(ref_chain, probe_chain, lowest_value=-2):
    """
    Calculate the log10 of the ALCPS score.

    Inputs:
        ref_chain:
            Reference structure instance
        probe_chain:
            Probe structure instance
        lowest_value:
            Value to use if two structures are perfectly aligned (i.e. if
            alcps = 0) - default value is -2
    Outputs:
        log10(alcps):
            log10 of the ALCPS
        lowest_value:
            returned if ALCPS = 0, default value is -2
    """

    alcps = calculate_alcps(ref_chain, probe_chain)

    if alcps == 0.0:
        return lowest_value
    else:
        return math.log10(alcps)


def get_sm_score(
    struct,
    ncomp,
    template_grid,
    cvol,
    apix,
):
    """Calculate the clash score between chains within a protein model

    The clash score calculates the amount that chains in a protein overlap
    one another. The structure is mapped into discrete bins in 3D space,
    defined by the template_grid input. The score is proportional to the
    number of these bins occupied by more than one of the protein chains.

    Recommended pixel spacing of the template_grid is 3.5 Å.

    Args:
        struct: Structure instance.
        ncomp: Number of chains in the structure.
        template_grid: Map object with empty 3D-grid (filled with zeros).
            This can be calculated using
            :meth:`StructureBlurrer.protMap <TEMPy.protein.structure_blurrer.StructureBlurrer.protMap>`
        cvol: List containing the volume of each chain. This can be
            calculated using
            :meth:`Map._get_component_volumes <TEMPy.maps.em_map.Map._get_component_volumes>`
        apix: Pixel size of template_grid, used for scaling the volume
            calculations.

    Returns:
        The clash score for the structure (close to 0 is good, large
        negative score is bad)
    """
    overlay_maplist = []
    blurrer = StructureBlurrer()

    overlay_maplist = []
    ssplit = struct.split_into_chains()
    for x in ssplit:
        overlay_maplist.append(
            blurrer.make_atom_overlay_map1(
                template_grid,
                x,
            )
        )

    nc = range(ncomp)
    cpair = list(itertools.combinations(nc, 2))
    score = 0.0
    n_overlap_voxel = 0
    overlap_volume = 0.0
    for i in cpair:
        n_overlap_voxel = (
            overlay_maplist[i[0]].fullMap * overlay_maplist[i[1]].fullMap
        ).sum()
        overlap_volume = ((apix.prod()) * n_overlap_voxel) * 2
        clash_percent = float(overlap_volume / (cvol[i[0]] + cvol[i[1]]))
        score = score + clash_percent
    return -(score)


def envelope_score(
    map_target,
    primary_boundary,
    structure_instance,
    norm=True,
):
    """
    Calculate the envelope score between a target Map and a Structure
    Instances.

    Arguments:
        map_target: Target Map Instance.
        primary_boundary: Value specified is calculated with
            primary_boundary of the map object.
        structure_instance: Model structure instance.
        norm: Normalise the score between 0 and 1 if True.

    Returns:
        Envelope score, normalised between 0 and 1 if norm is True

    """
    binMap = map_target.make_bin_map(primary_boundary)
    max_score = float(-2 * np.sum(binMap.fullMap))
    min_score = float(np.sum(binMap.fullMap) - 2 * np.sum(binMap.fullMap + 1))

    blurrer = StructureBlurrer()
    struct_binMap = blurrer.make_atom_overlay_map1(map_target, structure_instance)
    grid = struct_binMap.get_pos(0.9, 1.1)
    for x, y, z in grid:
        g = binMap[z][y][x]
        if g == -1:
            binMap[z][y][x] = 2
        elif g == 0:
            binMap[z][y][x] = -2
    score = float(np.sum(binMap.fullMap))
    if norm:
        norm_score = float((score - min_score) / (max_score - min_score))
        return norm_score
    else:
        return score


def envelope_score_map(
    map_target,
    map_probe,
    map_target_threshold=0,
    map_probe_threshold=0,
    norm=True,
):
    """Calculate the envelope score between two maps

    Arguments:
        map_target, map_probe: Map instance to compare.
        map_target_threshold, map_probe_threshold:
            Map threshold that defines the envelope, or surface, of the
            map. Will be automatically calculated using
            :meth:`self.calculate_map_threshold <TEMPy.protein.scoring_functions.ScoringFunctions.calculate_map_threshold>`
            if not specified.
        norm: Normalise the score between 0 and 1 if True.

    Returns:
        Envelope score, normalised between 0 and 1 if norm is True
    """
    assert_map_equivalent(map_target, map_probe)
    if map_target_threshold == 0:
        map_target_threshold = map_target.calculate_map_threshold()
    if map_probe_threshold == 0:
        map_probe_threshold = map_probe.calculate_map_threshold()

    binMap = map_target.make_bin_map(map_target_threshold)
    max_score = float(-2 * np.sum(binMap.fullMap))
    min_score = float(np.sum(binMap.fullMap) - 2 * np.sum(binMap.fullMap + 1))
    struct_binMap = map_probe.make_bin_map(map_probe_threshold)
    newMap = binMap.fullMap + 2 * struct_binMap.fullMap
    hist_array = np.histogram(newMap, 4)
    score = 2 * hist_array[0][0] - (2 * (hist_array[0][1])) - (hist_array[0][2])
    if norm:
        norm_score = float((score - min_score)) / (max_score - min_score)
        return norm_score
    else:
        return score


def normal_vector_score(
    map_target, map_probe, primary_boundary, secondary_boundary=0.0, Filter=None
):
    """Calculate the Normal Vector Score between two Map surfaces.

    Based on 3SOM algorithm (Ceulemans and Russell, 2004).

    Arguments:
        map_target, map_probe:
            Map instances to compare.
        primary_boundary, secondary_boundary:
            If a filter is selected, just input a contour level as primary
            threshold. Otherwise, need to run get_primary_boundary and
            get_second_boundary based on map target.
        Filter:
            Filter to be applied to inputs maps before calculating score.
                1. Sobel Filter (Filter=='Sobel')
                2. Laplace Filter (Filter=='Laplace')
                3. Minimum Filter (Filter=='Minimum')
                4. Mean Filter (Filter=='Mean')
                5. No filtering (Filter==None)
    Return:
        Normal vector score.
    Raises:
        sys.exit: Input maps do not match in shape, pixel size or origin
    """
    if Filter not in ["Sobel", "Laplace", "Mean", "Minimum", None]:
        print('Incorrect name of filter: %s" % Filter')
        print(
            "Select one of the following Filters if applicable: %s\n"
            % ", ".join(["Sobel", "Laplace"])
        )
        sys.exit()

    scores = []
    assert_map_equivalent(map_target, map_probe)
    assert isinstance(primary_boundary, float)
    assert isinstance(secondary_boundary, float)
    if primary_boundary > secondary_boundary:
        temp_thr = secondary_boundary
        secondary_boundary = primary_boundary
        primary_boundary = temp_thr

    points = np.argwhere(
        (map_target.fullMap > primary_boundary)
        & (map_target.fullMap < secondary_boundary)
    )

    if Filter == "Sobel":
        map1_surface = map_target._sobel_filter_contour(primary_boundary)
        points = np.argwhere(map1_surface.fullMap > (map1_surface.max() / 2.0))
    elif Filter == "Laplace":
        map1_surface = map_target._laplace_filtered_contour(primary_boundary)
        points = np.argwhere(map1_surface.fullMap > (map1_surface.max() / 2.0))
    elif Filter == "Minimum":
        map1_surface = map_target._surface_minimum_filter(float(primary_boundary))
        points = np.argwhere(map1_surface == 1)
    elif Filter == "Mean":
        map1_filter = map_target._surface_features(float(primary_boundary))
        bin_test = [0.0001]
        for ii in range(1, 41):
            bin_test.append(0.025 * ii)
        freq_test = np.histogram(map1_filter.fullMap, bin_test)[0]
        sum_freq = 0.0
        for fr in range(len(freq_test)):
            sum_freq += float(freq_test[fr])
            if sum_freq / np.sum(freq_test) > 0.05 and bin_test[fr + 1] >= 0.3:
                t1 = bin_test[fr + 1]
                break
            if sum_freq / np.numsum(freq_test) > 0.10 or sum_freq > 100000:
                t1 = bin_test[fr + 1]
                break
        points = np.argwhere((map1_filter.fullMap > 0.0) & (map1_filter.fullMap < t1))
    # C++ calculation
    flagc = 1
    try:
        vecnorm_target = map_target._get_normal_vector(points)
        vecnorm_probe = map_probe._get_normal_vector(points)
    except Exception:
        flagc = 0
    if vecnorm_target is None or vecnorm_probe is None:
        flagc = 0
    ct = 0

    if flagc == 1:
        for i in range(len(vecnorm_target)):
            ct += 1
            nvec = vecnorm_target[i]
            ovec = vecnorm_probe[i]
            # add max value for regions of null variation
            if nvec[0] == 0.0 and nvec[1] == 0.0 and nvec[2] == 0.0:
                if ovec[0] == 0.0 and ovec[1] == 0.0 and ovec[2] == 0.0:
                    continue
                else:
                    scores.append(3.14)
                    continue
            else:
                if ovec[0] == 0.0 and ovec[1] == 0.0 and ovec[2] == 0.0:
                    scores.append(3.14)
                    continue
            try:
                dotprod = ovec[0] * nvec[0] + ovec[1] * nvec[1] + ovec[2] * nvec[2]
                den = np.sqrt(nvec[0] ** 2 + nvec[1] ** 2 + nvec[2] ** 2) * np.sqrt(
                    ovec[0] ** 2 + ovec[1] ** 2 + ovec[2] ** 2
                )
                if abs(dotprod - den) < 0.00001:
                    ang = 0.0
                else:
                    ang = math.acos(min(max(dotprod / den, -1.0), 1.0))
                if den == 0.0:
                    print(dotprod, den, nvec, ovec)
                scores.append(abs(ang))
            except ValueError:
                print("Error: Angle could not be calculated: ", nvec, " ", ovec)
        if len(scores) == 0:
            print(
                "There are no points to be scored! The threshold values or"
                " the number of points to be considered needs to be"
                " changed."
            )
            return None
        else:
            if sum(scores) == 0:
                return 0.0
            else:
                return 1 - (sum(scores) / (len(points) * 3.14))
    scores = []
    ct1 = 0
    if flagc == 0:
        for v in points:
            n_vec = map_target.get_normal_vector(v[2], v[1], v[0])
            o_vec = map_probe.get_normal_vector(v[2], v[1], v[0])
            ct1 += 1
            if n_vec.x == -9 and n_vec.y == -9 and n_vec.z == -9:
                if o_vec.x == -9 and o_vec.y == -9 and o_vec.z == -9:
                    continue
                else:
                    scores.append(3.14)
                    continue
            else:
                if o_vec.x == -9 and o_vec.y == -9 and o_vec.z == -9:
                    scores.append(3.14)
                    continue
            try:
                scores.append(abs(n_vec.arg(o_vec)))
            except ValueError:
                print(
                    "Error: Angle between "
                    + str(n_vec)
                    + ", "
                    + str(o_vec)
                    + " for point %d, %d, %d cannot be calculated." % (v.x, v.y, v.z)
                )
    if len(scores) == 0:
        print(
            "There are no points to be scored! The threshold values or "
            "the number of points to be considered needs to be changed."
        )
    else:
        if sum(scores) == 0:
            return 0
        else:
            return 1 - (sum(scores) / (len(points) * 3.14))


def get_partial_DLSF(num_of_points, map_target, map_probe):
    """Calculate the DLSF score between two Map instances.

    The DLSF is similar to the LSF;
    whereas the LSF compares absolute density values,
    the DLSF compares the difference between pairs of values.

    Arguments:
        map_target, map_probe: Map instances to compare.
        num_of_points: Number of significant points.
    Return:
        DLSF score, or string "can't match the map" if Input maps do not
        match in shape, pixel size or origin
    """

    assert_map_equivalent(map_target, map_probe)

    map_target_sig_pairs = map_target._get_random_significant_pairs(int(num_of_points))
    otherMap = map_probe
    score = 0.0
    for p in map_target_sig_pairs:
        z1 = p[0]
        y1 = p[1]
        x1 = p[2]
        z2 = p[3]
        y2 = p[4]
        x2 = p[5]
        dens = p[6]
        prot_dens = otherMap.fullMap[z1][y1][x1] - otherMap.fullMap[z2][y2][x2]
        score += (dens - prot_dens) ** 2
    return score / map_target.fullMap.size


def _CCC_calc(m1, m2):
    arr1 = m1.view(float)
    arr2 = m2.view(float)  # noqa:F841
    nd = len(arr1.shape)
    if nd == 2 and len(arr1.shape)[1] == 0:
        nd = 1
    l = 1  # noqa:E741
    dim = np.zeros(3, dtype=int)
    for i in range(nd):
        l *= arr1.shape[i]  # noqa:E741
        dim[i] = arr1.shape[i]
    corr = 0.0
    numer = 0.0
    var1 = 0.0
    var2 = 0.0
    if nd == 1:
        for z in range(dim[0]):
            numer += arr1[z] * arr2[z]
            var1 += arr1[z] ** 2
            var2 += arr2[z] ** 2
    elif nd == 3:
        for z in range(dim[0]):
            for y in range(dim[1]):
                for x in range(dim[2]):
                    numer += arr1[z, y, x] * arr2[z, y, x]
                    var1 += arr1[z, y, x] ** 2
                    var2 += arr2[z, y, x] ** 2
    corr = numer / math.sqrt(var1 * var2)
    corr = min(1.0, corr)
    corr = max(-1.0, corr)
    return corr


def CCC_map(
    map_target,
    map_probe,
    map_target_threshold=0.0,
    map_probe_threshold=0.0,
    mode=1,
    meanDist=False,
    cmode=True,
):
    """Calculate cross-correlation between two Map instances using one of
    3 methods.

    Args:
        map_target, map_probe: EMMap instance to compare.

        map_target_threshold, map_probe_threshold:
            Map threshold, used to select pixels when calculating CCC with
            method 2. If not specified, will be calculated using
            :meth:`calculate_map_threshold <TEMPy.protein.scoring_functions.ScoringFunctions.calculate_map_threshold>`  # noqa:E501

        mode:
            1. CCC calculation on all pixels in map
            2. CCC only on pixels with density value above respective thresholds
            3. CCC only on pixels within the mask

        meanDist: True if the deviation from mean needs to be calculated

        cmode: If True, use pure python implementation to calculate CCC.
            If False, use numpy implementation.

    Returns:

        CCC, percentage_overlap: The cross correlation score and the
        percentage overlap between the two input maps

    Raises:

        Warning: Will return -1, 0 if the two input maps do not match
            shape, pixel size and origin.
    """
    assert_map_equivalent(map_target, map_probe)
    if not mode == 1:
        if map_target_threshold == 0 and map_probe_threshold == 0:
            map_target_threshold = map_target.calculate_map_threshold()
            map_probe_threshold = map_probe.calculate_map_threshold()
        bin_map1 = map_target.fullMap > float(map_target_threshold)
        bin_map2 = map_probe.fullMap > float(map_probe_threshold)
        minim = np.sum(bin_map1)
        minim2 = np.sum(bin_map2)
        if minim2 < minim:
            minim = minim2
        mask_array = (bin_map1 * bin_map2) > 0
        if not minim == 0.0:
            perc_ovr = float(np.sum(mask_array)) / minim
        else:
            print(
                "No map overlap (Cross correlation score), exiting "
                "score calculation.."
            )
            return -1.0, 0.0
        if perc_ovr < 0.02:
            return -1.0, 0.0
    else:
        perc_ovr = 1.0

    # calculate CCC within volume of overlap
    if mode == 3:
        if np.sum(mask_array) == 0:
            print(
                "No map overlap (Cross correlation score), "
                "exiting score calculation.."
            )
            return -1.0, 0.0
        map1_mask = map_target.fullMap[mask_array]
        map2_mask = map_probe.fullMap[mask_array]
        if meanDist:
            map1_mask = map1_mask - np.mean(map1_mask)
            map2_mask = map2_mask - np.mean(map2_mask)
        if cmode:
            corr = _CCC_calc(
                map1_mask.flatten(),
                map2_mask.flatten(),
            )
        else:
            corr = None
        if corr is None:
            return (
                (
                    np.sum(map1_mask * map2_mask)
                    / np.sqrt(
                        np.sum(np.square(map1_mask)) * np.sum(np.square(map2_mask))
                    )
                ),
                perc_ovr,
            )
        else:
            return corr, perc_ovr

    # calculate CCC for contoured maps based on threshold
    elif mode == 2:
        map1_mask = map_target.fullMap * bin_map1
        map2_mask = map_probe.fullMap * bin_map2
        if meanDist:
            map1_mask = map1_mask - np.mean(map_target.fullMap[bin_map1])
            map2_mask = map2_mask - np.mean(map_probe.fullMap[bin_map2])
            map1_mask = map1_mask * bin_map1
            map2_mask = map2_mask * bin_map2
        else:
            map1_mask = map_target.fullMap * bin_map1
            map2_mask = map_probe.fullMap * bin_map2
        if cmode:
            corr = _CCC_calc(map1_mask, map2_mask)
        else:
            corr = None
        if corr is None:
            return (
                (
                    np.sum(map1_mask * map2_mask)
                    / np.sqrt(
                        np.sum(np.square(map1_mask)) * np.sum(np.square(map2_mask))
                    )
                ),
                perc_ovr,
            )
        else:
            return corr, perc_ovr
    # calculate on the complete map
    if meanDist:
        if cmode:
            corr = _CCC_calc(
                map_target.fullMap - np.mean(map_target.fullMap),
                map_probe.fullMap - np.mean(map_probe.fullMap),
            )
        else:
            corr = None
        if corr is None:
            return (
                (
                    np.sum(
                        (map_target.fullMap - np.mean(map_target.fullMap))
                        * (map_probe.fullMap - np.mean(map_probe.fullMap))
                    )
                    / (
                        np.sqrt(
                            np.sum(
                                np.square(
                                    map_target.fullMap - np.mean(map_target.fullMap)
                                )
                            )
                            * np.sum(
                                np.square(
                                    map_probe.fullMap - np.mean(map_probe.fullMap)
                                )
                            )
                        )
                    )
                ),
                perc_ovr,
            )
        else:
            return corr, perc_ovr
    if cmode:
        corr = _CCC_calc(map_target.fullMap, map_probe.fullMap)
    else:
        corr = None
    if corr is None:
        return (
            np.sum(map_target.fullMap * map_probe.fullMap)
            / np.sqrt(
                np.sum(np.square(map_target.fullMap))
                * np.sum(np.square(map_probe.fullMap))
            ),
            perc_ovr,
        )
    else:
        return corr, perc_ovr


class CCC(MapScore):
    """Calculate cross-correlation between two Map instances.

    Args:
    Returns:
        CCC scoring object
    Raises:
        sys.exit: Input maps do not match in shape, pixel size or origin
    """
    def __init__(self):
        self

    def score_arrays(self, target_array, sim_array):
        target_mean = np.mean(target_array)
        sim_mean = np.mean(sim_array)
        nom = np.sum((target_array - target_mean) * (sim_array - sim_mean))
        denom = np.sqrt(np.sum(np.square(target_array - target_mean)) * np.sum(np.square(sim_array - sim_mean)))
        return nom / denom


class MOC(MapScore):
    """Calculate Manders Overlap Coefficient between two numpy array instances.

    Args:
    Returns:
        MOC scoring object
    """
    def __init__(self):
        self

    def score_arrays(self, target_array, sim_array):
        nom = np.sum(target_array * sim_array)
        denom = np.sqrt(np.sum(np.square(target_array)) * np.sum(np.square(sim_array)))
        return nom / denom




class LSF(MapScore):
    """Calculate least-squares between two Map instances.

    Arguments:
    Return:
        Least-squares scorer
    Raises:
        sys.exit: Input maps do not match in shape, pixel size or origin
    """
    def __init__(self):
        pass

    def score_arrays(self, target, probe):
        return np.square(target - probe).mean()


class LaplaceCCC(MapScore):
    """Calculate CCC between two laplacian filtered Map instances.

    The laplacian filter is an edge detection filter, which computes the
    second derviatives of an image/volume. Using Laplacian filters in
    combination with CCC scoring of cryo EM models  was shown to be more
    accurate than CCC scoring alone for low resolution maps, in
    `(Chacon and Wriggers, 2002) <https://pubmed.ncbi.nlm.nih.gov/11922671/>`_

    Arguments:
        map_target, map_probe: Map instances to compare.

        prefil: 2-tuple of boolean values, one for each map respectively.
            True if Map instance is already Laplacian-filtered. False
            otherwise.
    Return:
        Laplacian cross-correlation score
    Raises:
        sys.exit: Input maps do not match in shape, pixel size or origin
    """
    def __init__(self, prefil=(False, False)):
        self.prefil = prefil
        self.ccc = CCC()

    def score_arrays(self, target, sim):
        if not self.prefil[0]:
            target = laplace(target)
        if not self.prefil[1]:
            sim = laplace(sim)
        return self.ccc.score_arrays(target, sim)


def calculate_overlap_scores(
    map_target, map_probe, map_target_threshold, map_probe_threshold
):
    """Currently broken: np.numsum doesn't exist in current numpy version


    mask maps with 2 cut-off map_target_threshold and
    map_probe_threshold (vol thr.)

    return:
    fraction of overlap with respect to target, and with respect to
    probe
    """

    binmap1 = map_target.fullMap > float(map_target_threshold)
    binmap2 = map_probe.fullMap > float(map_probe_threshold)
    mask_array = (binmap1 * binmap2) > 0

    size1 = np.numsum(binmap1)  # can't find numsum in numpy docs
    size2 = np.numsum(binmap2)
    return float(np.numsum(mask_array)) / size1, float(np.numsum(mask_array)) / size2


def assert_map_equivalent(map_target, map_probe):
    """
    Checks if properties (sampling rate, box size and origin) of two maps
    are equivalent.

    Returns:
        None
    Raises:
        Exception if maps are not equivalent
    """
    if not (np.isclose(map_target.apix, map_probe.apix, atol=1e-6).all()):
        raise Exception("Maps do not have the same box size")

    if map_target.box_size() != map_probe.box_size():
        raise Exception("Maps do not have the same voxel size")

    if not (
        round(map_target.origin[0], 2) == round(map_probe.origin[0], 2)
        and round(map_target.origin[1], 2) == round(map_probe.origin[1], 2)  # noqa:E501
        and round(map_target.origin[2], 2)  # noqa:E501
        == round(map_probe.origin[2], 2)  # noqa:E501
    ):
        raise Exception("Maps do not have the same origin")
