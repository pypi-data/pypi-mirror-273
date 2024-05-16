# =============================================================================
#     This file is part of TEMPy.
#     It describes the implementation of Assembly class for the purpose of
#     fitting multiple component into the assembly map
#
#     TEMPy is a software designed to help the user in the manipulation
#     and analyses of macromolecular assemblies using 3D electron microscopy
#     maps.
#
#     Copyright 2010-2014 TEMPy Inventors and Birkbeck College University of
#     London.
#     The TEMPy Inventors are: Maya Topf, Daven Vasishtan,
#     Arun Prasad Pandurangan, Irene Farabella, Agnel-Praveen Joseph,
#     Harpal Sahota
#
#
#     TEMPy is available under Public Licence.
#
#     Please cite your use of TEMPy in published work:
#
#     Vasishtan D, Topf M. (2011) J Struct Biol 174:333-343.
#     Scoring functions for cryoEM density fitting.
#     Pandurangan AP, Vasishtan D, Topf M. (2015) Structure 23:2365-2376.
#     GAMMA-TEMPy: Simultaneous fitting of components in 3D-EM Maps of their
#     assembly using genetic algorithm.
# =============================================================================

from TEMPy.protein.structure_blurrer import StructureBlurrer
from TEMPy.math.vq import get_VQ_points


class Assembly:
    """
    A class to represent multi-subunit component and its corresponding density
    map.
    """

    def __init__(self, struct_list):
        """
        A constructor to initialise the assembly object.

        Arguments:
           *struct_list*
               A list of BioPy_Structure objects.
        """
        self.struct_list = struct_list
        self.initMapList = []
        self.mapList = []

    def build_maps(
            self,
            resolution: float,
            template_map,
            sig_coeff: float=0.356  # noqa: E252
    ) -> None:
        """
        Build list of maps corresponding to the protein components in the
        structList.

        Arguments:
           *resolution*
               Desired resolution of the density map in Angstrom units.
            *template_map*
                A map object that will be uesd as the template to build maps of
                for the individual maps. Usually the input map used for the
                assembly fitting.
            *sigma_coeff*
                the sigma value (multiplied by the resolution) that controls
                the width of the Gaussian. Default values is 0.356.
        """
        sb = StructureBlurrer()
        for x in self.struct_list:
            self.mapList.append(
                sb.gaussian_blur_real_space(
                    x,
                    resolution,
                    template_map, sig_coeff
                )
            )
            self.initMapList.append(self.mapList[-1].copy())

    def randomise_structs(
            self,
            max_trans,
            max_rot,
            v_grain: int=30,  # noqa: E252
            rad: bool=False  # noqa: E252
    ) -> None:
        """
        Randomise the position and orientation of the protein components in the
        structList.

        Arguments:
            *max_trans*
                Maximum translation permitted
            *max_rot*
                Maximum rotation permitted (in degree if rad=False)
            *v_grain*
                Graning Level for the generation of random vetors (default=30)
        """

        for x in self.struct_list:
            x.randomise_position(max_trans, max_rot, v_grain, rad)

    def randomise_structs_and_maps(
            self,
            max_trans,
            max_rot,
            v_grain: int=30,  # noqa: E252
            rad: bool=False  # noqa: E252
    ) -> None:
        """
        Randomise the position and orientation of the protein components and
        its corresponding map objects.

        Arguments:
            *max_trans*
                Maximum translation permitted
            *max_rot*
                Maximum rotation permitted (in degree if rad=False)
            *v_grain*
                Graning Level for the generation of random vectors (default=30)
        """

        if len(self.mapList) != len(self.struct_list):
            print('Maps not built yet')
        else:
            for x in range(len(self.struct_list)):
                com = self.struct_list[x].CoM.copy()
                rx, ry, rz, ra, tx, ty, tz = self.struct_list[x].randomise_position(  # noqa: E501
                    max_trans,
                    max_rot,
                    v_grain,
                    rad,
                    verbose=True,
                )
                self.mapList[x] = self.mapList[x].rotate_by_axis_angle(
                    rx,
                    ry,
                    rz,
                    ra,
                    com
                )
                self.mapList[x] = self.mapList[x].translate(tx, ty, tz)

    def reset_structs(self) -> None:
        """
        Translate the list of structure objects back into initial position.
        """

        for x in self.struct_list:
            x.reset_position()

    def reset_maps(self) -> None:
        """
        Undo all the transformations applied to the list of map objects and
        restore it to its original state.
        """

        for x in range(len(self.mapList)):
            self.mapList[x] = self.initMapList[x].copy()

    def reset_all(self) -> None:
        """
        Reset the map and structure objects to is initial state.
        """

        self.reset_maps()
        self.reset_structs()

    def move_map_and_prot_by_aa(
            self,
            index,
            rx,
            ry,
            rz,
            ra,
            tx,
            ty,
            tz
    ) -> None:
        """
        Translate and rotate the structure and map objects in the assembly
        around its centre given an axis and angle.

        Arguments:
            *index*
                Index of the structure and map list.
            *rx,ry,rz*
                Axis to rotate about, ie. rx,ry,rz =  0,0,1 rotates the
                structure and map round the xy-plane.
            *ra*
                Angle (in degrees) to rotate map.
            *tx,ty,tz*
                Distance in Angstroms to move structure and map in respective
                x, y, and z directions.
        """

        com = self.struct_list[index].CoM.copy()
        self.struct_list[index].rotate_by_axis_angle(
            rx,
            ry,
            rz,
            ra,
            tx,
            ty,
            tz
        )
        self.mapList[index] = self.mapList[index].rotate_by_axis_angle(
            rx,
            ry,
            rz,
            ra,
            com
        )
        self.mapList[index] = self.mapList[index].translate(tx, ty, tz)

    def move_map_and_prot_by_euler(
            self,
            index,
            rx,
            ry,
            rz,
            tx,
            ty,
            tz
    ) -> None:
        """
        Translate and rotate the structure and map objects in the assembly
        around its centre using Euler angles.

        Arguments:
            *index*
                Index of the structure and map list.
            *rx,ry,rz*
                Axis to rotate about, ie. rx,ry,rz =  0,0,1 rotates the
                structure and map round the xy-plane.
            *ra*
                Angle (in degrees) to rotate map.
            *tx,ty,tz*
                Distance in Angstroms to move structure and map in respective
                x, y, and z directions.
        """

        com = self.struct_list[index].CoM.copy()
        self.struct_list[index].rotate_by_euler(
            rx,
            ry,
            rz,
            0,
            0,
            0
        )
        self.struct_list[index].translate(tx, ty, tz)
        self.mapList[index] = self.mapList[index].rotate_by_euler(
            rx,
            ry,
            rz,
            com
        )
        self.mapList[index] = self.mapList[index].translate(tx, ty, tz)

    def move_map_and_prot_by_mat(
            self,
            index,
            mat,
            tx,
            ty,
            tz
    ) -> None:
        """
        Translate and rotate the structure and map objects around pivot given
        by CoM using a translation vector and a rotation matrix respectively.

        Arguments:
            *mat*
                3x3 matrix used to rotate structure and map objects.
            *tx,ty,tz*
                Distance in Angstroms to move structure and map in respective
                x, y, and z directions.
        """

        com = self.struct_list[index].CoM.copy()
        self.struct_list[index].rotate_by_mat(mat)
        self.struct_list[index].translate(tx, ty, tz)
        self.mapList[index] = self.mapList[index].rotate_by_matrix(mat, com)
        self.mapList[index] = self.mapList[index].translate(tx, ty, tz)

    def move_map_and_prot_by_quat(
            self,
            index,
            tx,
            ty,
            tz,
            q_param,
            mat
    ) -> None:
        """
        Translate the structure objects using a translation vector and rotate
        it using a quaternion object.
        Translate and rotate the map objects around pivot given by CoM using a
        translation vector and a rotation matrix respectively.

        Arguments:
            *index*
                Index of the structure and map list.
            *tx,ty,tz*
                Distance in Angstroms to move structure and map in respective
                x, y, and z directions.
            *q_param*
                Is a list of type [w, x, y, z] which represents a quaternion
                vector used for rotation
            *mat*
                3x3 matrix used to rotate structure and map objects.
        """
        com = self.struct_list[index].CoM.copy()
        self.struct_list[index].rotate_by_quaternion(q_param)
        self.struct_list[index].translate(tx, ty, tz)
        self.mapList[index] = self.mapList[index].rotate_by_matrix(mat, com)
        self.mapList[index] = self.mapList[index].translate(tx, ty, tz)

    def combine_structs(self):
        """
        Used to combine the list of structure objects into a single structure
        object
        """

        if len(self.struct_list) > 1:
            return self.struct_list[0].combine_structures(self.struct_list[1:])
        elif len(self.struct_list) == 1:
            return self.struct_list[0].copy()
        else:
            print('No structures found')

    def combine_maps(self):
        """
        Used to combine the list of map objects into a single map object
        """

        if len(self.mapList) > 1:
            new_map = self.mapList[0].copy()
            for x in self.mapList[1:]:
                new_map.fullMap += x.fullMap
            return new_map
        elif len(self.struct_list) == 1:
            return self.mapList[0].copy()
        else:
            print('No maps found')

    def make_vq_points(
            self,
            threshold,
            no_of_points,
            lap_fil,
            epochs: int=300  # noqa: E252
    ):
        """"
        Cluster the density maps in the assembly object into n points using
        vector quantisation algorithm.

        Arguments:
            *threshold*
                voxels with density above this value are used in the VQ run.
            *no_of_points*
                Number of Vector quantisation points to output.
            *lap_fil*
                True if you want to Laplacian filter the map first, False
                otherwise. Note that filtering the map change the density
                values of the map, which is relevant for the threshold
                parameter.
            *epochs*
                Number of iterations to run the Vector quantisation algorithm.
                Default is set to 300

        Return:
            A list of vector objects containing the vector quatisation points
        """

        vq = []
        if len(self.mapList) > 0:
            for s in range(len(self.mapList)):
                vq.append(
                    get_VQ_points(
                        self.mapList[s],
                        threshold,
                        no_of_points[s],
                        epochs,
                        None,
                        lap_fil
                    )
                )
        return vq

    def write_all_to_files(self, template_name):
        """
        Write the all the strucrure and map objects separately to a pdb and
        mrc formatted file respectively.

        Arguments:
            *templateName*
                A string representing the prefix of the file name
        """

        for x in range(len(self.struct_list)):
            self.struct_list[x].write_to_PDB(
                f'{template_name}{str(x)}.pdb'
            )
            if len(self.mapList) > 0:
                self.mapList[x].write_to_MRC_file(
                    f'{template_name}{str(x)}.mrc'
                )
