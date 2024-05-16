import numpy as np
import gemmi
from TEMPy.map_process.map_filters import Filter
from TEMPy.maps.em_map import Map
from TEMPy.protein.mmcif import mmcif_writer


class DensityCalculator:
    """
    Class to calculate electron potential map for a given model
    using the electron scattering factor for neutral atoms.
    Note: Slightly slower than StructureBlurrer that uses gaussian blur
    but this adds atomic B-factors to density calculation
    """

    def __init__(self):
        """
        Nothing to initialise
        """
        pass

    @staticmethod
    def calculate_rho_TEMPy(model=None, densMap=None, rad_cutoff=2.5):
        """
        Calculate density, use this if you have a TEMPy BioPy_Structure and
        an EM map from experiment with pixel spacing less than radius cutoff
        (rad_cutoff default: 2.5 Angstroms). Input map and model are needed.
        Arguments:
            *model*
                TEMPy BioPy_Structure instance
            *densMap*
                TEMPy Map instance with the map grids in which to
                calculate density in
            *radius*
                cutoff radius (density to decrease with radius).
                same for all atoms
        Return:
            A new TEMPy Map instance with dimensions based on the input Map
            filled with calculated density for the model given
        """
        if model is None:
            print("Please provide a model")
            raise ValueError("No input model given.")
        if densMap is None:
            print("Please provide an input map")
            raise ValueError("No input map given.")
        model_len = len(model)
        newMap = densMap.copy()
        newMap.fullMap = newMap.fullMap * 0.0
        dx = int(np.ceil(rad_cutoff / newMap.apix[0]))
        dy = int(np.ceil(rad_cutoff / newMap.apix[1]))
        dz = int(np.ceil(rad_cutoff / newMap.apix[2]))

        for i in range(model_len):
            lims = model.atomList[i].gridpoints_around_atom(
                newMap,
                dx=dx,
                dy=dy,
                dz=dz,
            )
            xg, yg, zg = np.mgrid[
                lims[0] : lims[1],
                lims[2] : lims[3],
                lims[4] : lims[5],
            ]

            xg = xg * newMap.apix[0] + newMap.origin[0]
            yg = yg * newMap.apix[1] + newMap.origin[1]
            zg = zg * newMap.apix[2] + newMap.origin[2]
            indi = np.vstack([xg.ravel(), yg.ravel(), zg.ravel()]).T
            # print(f"indi, {indi}")
            dxyz = indi - np.array(
                [
                    model.atomList[i].get_x(),
                    model.atomList[i].get_y(),
                    model.atomList[i].get_z(),
                ]
            )
            # print(f"dxyz, {dxyz}")
            r_sq = np.sum(np.square(dxyz), axis=1)
            r = np.sqrt(r_sq)
            # print(f"r, {r}")
            new_indi = indi[r <= rad_cutoff]
            new_r_sq = r_sq[r <= rad_cutoff]
            grid_indi = np.round(((new_indi - newMap.origin) / newMap.apix), 0)
            grid_indi = grid_indi.astype(int)
            elem = model.atomList[i].elem
            temp_fac = model.atomList[i].temp_fac
            occ = model.atomList[i].occ
            rho_arr = np.zeros(new_r_sq.shape, dtype=np.float64)
            for j in range(len(new_r_sq)):
                rho_arr[j] = occ * gemmi.Element(elem).c4322.calculate_density_iso(
                    new_r_sq[j], temp_fac
                )
            xi, yi, zi = zip(*grid_indi)
            newMap.fullMap[zi, yi, xi] += rho_arr

        newMap.update_header()
        return newMap

    @staticmethod
    def calculate_rho_GEMMI(
        gemmi_structure=None,
        model_number=0,
        densMap=None,
        offset_model=False,
    ):
        """
        Calculate density, use this to calculate electron potential map from a
        GEMMI structure object. Input map is needed for the headers/dimensions.
        Arguments:
            *gemmi_structure*
                GEMMI structure instnace
            *model_number*
                Index fo the model in GEMMI structure instance,
                Default=0 (first model)
            *densMap*
                TEMPy Map instance with the map grids in which to
                calculate density in
            *offset_model*
                Boolean to offset the model's position with non-zero origin
                Default=False
        Return:
            A new TEMPy Map instance with dimensions based on the input Map
            filled with calculated density for the model given
        """
        if gemmi_structure is None:
            print("Please provide a model")
            raise ValueError("No input model given.")
        dencalc = gemmi.DensityCalculatorE()
        if densMap is None:
            print("Please provide a map")
            raise ValueError("No input map given.")
        else:
            a = densMap.apix[0] * densMap.x_size()
            b = densMap.apix[1] * densMap.y_size()
            c = densMap.apix[2] * densMap.z_size()
            if len(densMap.header) != 0:
                alpha = densMap.header[13]
                beta = densMap.header[14]
                gamma = densMap.header[15]
            else:
                alpha = 90.0
                beta = 90.0
                gamma = 90.0
        # offset model's position from non-zero origin
        model_copy = gemmi_structure
        if offset_model:
            for cra in model_copy[model_number].all():
                cra.atom.pos -= gemmi.Position(
                    densMap.x_origin(), densMap.y_origin(), densMap.z_origin()
                )

        model_copy.cell = gemmi.UnitCell(a, b, c, alpha, beta, gamma)
        model_copy.spacegroup_hm = "P 1"
        # set resolution with the formula (apix * 2 * oversampling)
        # to get same grid size as the input map
        dencalc.rate = 1.5  # oversampling rate
        dencalc.d_min = np.min(densMap.apix) * (2 * dencalc.rate)
        dencalc.set_grid_cell_and_spacegroup(model_copy)
        # use each gemmi function individually to check if the grid
        # size set by gemmi is the same as the input map
        # gemmi.initialize_grid() is default with denser=True
        # resulting in spacing can be smaller or greater than given
        # dencalc.put_model_density_on_grid(model_copy[model_number])
        dencalc.initialize_grid()
        # check for same grid size X,Y,Z
        mapin_shape = (densMap.x_size(), densMap.y_size(), densMap.z_size())
        if not np.array_equal(dencalc.grid.shape, mapin_shape):
            dencalc.grid.set_size(mapin_shape[0], mapin_shape[1], mapin_shape[2])
        # calculate density
        dencalc.add_model_density_to_grid(model_copy[model_number])
        dencalc.grid.symmetrize_sum()
        newMap = densMap.copy()
        newMap.fullMap = newMap.fullMap * 0.0
        # transpose to Z,Y,X
        new_axes = [2, 1, 0]
        data = np.transpose(dencalc.grid, axes=new_axes)
        newMap.fullMap = data.copy()
        newMap.update_header()

        return newMap

    @staticmethod
    def calculate_rho_box(
        model=None,
        densMap=None,
        rad_cutoff=2.5,
        flag_gemmi=False,
        model_number=0,
        centre_of_model=False,
        offset_model=False,
        filename="None",
    ):
        """
        Calculate density and centered (if centre_of_molecule=True) based on the
        given structure within the grid size of the input map given

        Argument:
            *model*
                TEMPy BioPy_structure or GEMMI structure instance
            *densMap*
                TEMPy map instance with the grid size and pixel spacing
                to put model density on
            *rad_cutoff*
                cutoff radius (density to decrease with radius)
            *flag_gemmi*
                Boolean to use GEMMI's DensityCalculatorE() (if flag_gemmi=True)
                If False, density will be calculated similar to
                CLIPPER's implementation
            *model_number*
                Index to model for GEMMI structure instance
                Default=0 for first model
            *centre_of_model*
                Boolean to set centre of box to centre of model (if True)
                Default: False
            *offset_model*
                Boolean to offset the model's position with non-zero origin (if True)
                Will automatically set to True if centre_of_model=True
                Default=False
            *filename*
                filename of the parsed map, or the structure
        Return:
            A new TEMPy map instance with the calculated density centered
            based on the structure with the grid box size given
        """
        if model is None:
            print("Please provide a model")
            raise ValueError("No input model given.")
        if densMap is None:
            print("Please provide a map")
            raise ValueError("No input model given")
        newMap = densMap.copy()
        if centre_of_model:
            if flag_gemmi:
                if not isinstance(model, gemmi.Structure):
                    cif_instance = mmcif_writer(
                        model, model.filename, save_all_metadata=False
                    )
                    structure = cif_instance.gemmi_structure
                else:
                    structure = model
                com_x, com_y, com_z = structure[0].calculate_center_of_mass()
            else:
                com_x = model.CoM.x
                com_y = model.CoM.y
                com_z = model.CoM.z
            x_origin = com_x - (densMap.apix[0] * newMap.x_size() / 2.0)
            y_origin = com_y - (densMap.apix[1] * newMap.y_size() / 2.0)
            z_origin = com_z - (densMap.apix[2] * newMap.z_size() / 2.0)
            full_grid = np.zeros(
                (newMap.z_size(), newMap.y_size(), newMap.x_size()), dtype=np.float64
            )
            newMap = Map(
                full_grid, [x_origin, y_origin, z_origin], densMap.apix, filename
            )
            newMap.update_header()
        else:
            if flag_gemmi:
                if not isinstance(model, gemmi.Structure):
                    cif_instance = mmcif_writer(
                        model, model.filename, save_all_metadata=False
                    )
                    structure = cif_instance.gemmi_structure

        if flag_gemmi:
            # to get the right positions with new map origins
            # offset_model is set to True
            if centre_of_model:
                protmapbox = DensityCalculator.calculate_rho_GEMMI(
                    gemmi_structure=structure,
                    model_number=model_number,
                    densMap=newMap,
                    offset_model=True,
                )
            else:
                protmapbox = DensityCalculator.calculate_rho_GEMMI(
                    gemmi_structure=structure,
                    model_number=model_number,
                    densMap=newMap,
                    offset_model=offset_model,
                )
        else:
            protmapbox = DensityCalculator.calculate_rho_TEMPy(
                model=model,
                densMap=newMap,
                rad_cutoff=rad_cutoff,
            )

        return protmapbox

    @staticmethod
    def map_sharpen_blur(densMap=None, bfactor=0.0, res_cutoff=2.0):
        """
        Sharpen/Blur given map with a global B-factor
        Arguments:
            *densMap*
                TEMPy EM map instance
            *bfactor*
                Global B-factor to apply to map, negative is sharpen,
                positive is blur.
            *res_cutoff*
                resolution cutoff for map sharpening to avoid artifact
                Default: 2.0 Angstrom - this works fine generally
        Return:
            Sharpened/Blurred map with global B-factor given
        """
        if densMap is None:
            print("Please provide a map")
            raise ValueError("No input map given.")
        fltrmap = Filter(densMap)
        ftfltr = fltrmap.bfact_sharpen_blur(
            bfactor=bfactor,
            map_shape=densMap.box_size(),
            keep_shape=False,
            resocut=res_cutoff,
        )
        fltrmap.fourier_filter(ftfltr, inplace=True)
        sharpblur_map = densMap.copy()
        sharpblur_map.fullMap[:] = fltrmap.fullMap[:]
        sharpblur_map.update_header()

        return sharpblur_map
