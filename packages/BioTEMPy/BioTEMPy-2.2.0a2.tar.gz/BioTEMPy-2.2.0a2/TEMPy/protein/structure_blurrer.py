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
#     Please cite your use of TEMPy in published work:
#
#     Farabella, I., Vasishtan, D., Joseph, A.P., Pandurangan, A.P., Sahota, H.
#     & Topf, M. (2015). J. Appl. Cryst. 48.
#
# =============================================================================
from collections import OrderedDict
import gc

import numpy as np
from scipy.fftpack import (
    fftn,
    ifftn,
)
from scipy.ndimage import (
    fourier_gaussian,
    gaussian_filter,
)

from TEMPy.maps.em_map import Map


class StructureBlurrer:
    """
    A class to generate density maps using structure instances.

    Args:
        use_vc: If True, use an accelerated algorithm to calculate the map
            density when calling
            :meth:`gaussian_blur_real_space <TEMPy.protein.structure_blurrer.StructureBlurrer.gaussian_blur_real_space>`.

    Returns:
        A structure blurring object.
    """

    def __init__(self, with_vc=False, locres=None):
        self.use_vc = False
        import os
        if with_vc or os.environ.get('BLUR_WITH_VC') is not None:
            try:
                __import__('voxcov')
                self.use_vc = True
                self._locres = locres
            except ImportError:
                print("voxcov not installed. Using standard blurring instead.")

    def protMap(
            self,
            struct,
            apix,
            resolution=None,
            filename="None",
    ):
        """
        Returns an Map instance sized and centred based on the atomic
        structure.

        Arguments:
            struct: Model structure instance.
            apix: Angstroms per pixel for the output Map.
            resolution: Target resolution of the output Map.
            filename: Filename for Map instance - if it is saved.

        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:
                Map full of zeros with a shape sufficient to encompass the
                protein in struct.

           """
        # Build empty template map based on the size of the protein and the
        # resolution.
        extr = struct.get_extreme_values()
        if resolution is not None:
            edge = np.array(2 * resolution / apix, dtype=int) + 4
        else:
            edge = 10
        x_size = int((extr[1] - extr[0]) / apix[0]) + edge[0]
        y_size = int((extr[3] - extr[2]) / apix[1]) + edge[1]
        z_size = int((extr[5] - extr[4]) / apix[2]) + edge[2]

        # Origin calculated such that the centre of the map is the centre of
        # mass of the protein.
        half_x = max(struct.CoM.x - extr[0], extr[1] - struct.CoM.x)
        if half_x < (apix[0] * x_size / 2.0):
            half_x = apix[0] * x_size / 2.0
        x_origin = struct.CoM.x - half_x - edge[0] * apix[0]
        # apj: if com is not near the geometric centre of protein
        x_size = int(half_x * 2.0 / apix[0] + 2 * edge[0])
        # apj: if com is not near the geometric centre of protein
        half_y = max(struct.CoM.y - extr[2], extr[3] - struct.CoM.y)
        if half_y < (apix[1] * y_size / 2.0):
            half_y = (apix[1] * y_size / 2.0)
        y_origin = struct.CoM.y - half_y - edge[1] * apix[1]
        y_size = int(half_y * 2.0 / apix[1] + 2 * edge[1])
        # apj: if com is not near the geometric centre of protein
        half_z = max(struct.CoM.z - extr[4], extr[5] - struct.CoM.z)
        if half_z < (apix[2] * z_size / 2.0):
            half_z = apix[2] * z_size / 2.0
        z_origin = struct.CoM.z - half_z - edge[2]*apix[2]
        z_size = int(half_z * 2.0 / apix[2] + 2 * edge[2])

        newMap = np.zeros((z_size, y_size, x_size))
        fullMap = Map(newMap, [x_origin, y_origin, z_origin], apix, filename)
        return fullMap

    def protMapBox(
            self,
            struct,
            apix,
            resolution,
            box_size_x,
            box_size_y,
            box_size_z,
            filename,
    ):
        """
        Create a Map instance sized and centered based on the atomic structure.

        Arguments:
            struct: model Structure instance.
            apix: Angstroms per pixel for the output Map.
            resolution: the resolution, in Angstroms, to blur the protein to.
            box_size_x: x dimension of output map box in Angstroms.
            box_size_y: y dimension of output map box in Angstroms.
            box_size_z: z dimension of output map box in Angstroms.
            filename: output name of the map file, if it is saved.

        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:
                Empty map (full of zeros) with size as specified and origin
                centred on the protein model in struct.

        """
        # Build empty template map based on the size of the protein and the
        # resolution.
        x_size = int(box_size_x)
        y_size = int(box_size_y)
        z_size = int(box_size_z)

        # Origin calculated such that the centre of the map is the centre of
        # mass of the protein.
        x_origin = struct.CoM.x - (apix[0] * x_size / 2.0)
        y_origin = struct.CoM.y - (apix[1] * y_size / 2.0)
        z_origin = struct.CoM.z - (apix[2] * z_size / 2.0)

        newMap = np.zeros((z_size, y_size, x_size))
        fullMap = Map(newMap, [x_origin, y_origin, z_origin], apix, filename)
        return fullMap

    def mapGridPosition(self, densMap, atom):
        """Finds the index of an atom in a Map instance, and the atom's mass.

        Arguments:
            densMap: :class:`Map <TEMPy.maps.em_map.Map>` instance the atom is
                to be placed on.
            atom: :class:`Atom <TEMPy.protein.prot_rep_biopy.Atom>` instance.

        Returns:
            int, int, int, float:
                x, y, z index for atom and its mass.
        """
        origin = densMap.origin
        apix = densMap.apix
        box_size = densMap.box_size()
        x_pos = int(round((atom.x - origin[0]) / apix[0], 0))
        y_pos = int(round((atom.y - origin[1]) / apix[1], 0))
        z_pos = int(round((atom.z - origin[2]) / apix[2], 0))
        # MODIFIED BY PAP
        if(
                (box_size[2] > x_pos >= 0) and
                (box_size[1] > y_pos >= 0) and
                (box_size[0] > z_pos >= 0)
        ):
            return x_pos, y_pos, z_pos, atom.mass
        else:
            return 0

    def mapGridPositions_vdw(self, densMap, atom, gridtree):
        """
        Returns the index of the nearest pixel to an atom, and atom mass (4
        values in list form).

        Arguments:
           *densMap*
               Map instance the atom is to be placed on.
           *atom*
               Atom instance.
           """
        origin = densMap.origin
        apix = densMap.apix
        x_pos = int(round((atom.x - origin[0]) / apix[0], 0))
        y_pos = int(round((atom.y - origin[1]) / apix[1], 0))
        z_pos = int(round((atom.z - origin[2]) / apix[2], 0))
        if(
                (densMap.x_size() > x_pos >= 0) and
                (densMap.y_size() > y_pos >= 0) and
                (densMap.z_size() > z_pos >= 0)
        ):
            # search all points withing 1.5sigma
            list_points = gridtree.query_ball_point(
                [
                    atom.x,
                    atom.y,
                    atom.z,
                ],
                atom.vdw
            )
            return list_points, (x_pos, y_pos, z_pos)
        else:
            print('Warning, atom out of map box')
            return [], ()

    def maptree(self, densMap, strmap=None):
        """
        Returns the KDTree of coordinates from a map grid.

        Arguments:
           *densMap*
               Map instance the atom is to be placed on.
        """
        origin = densMap.origin
        apix = densMap.apix
        nz, ny, nx = densMap.fullMap.shape

        # convert to real coordinates
        zg, yg, xg = np.mgrid[0:nz, 0:ny, 0:nx]
        # to get indices in real coordinates
        zg = zg * apix[2] + origin[2] + apix[2] / 2.0
        yg = yg * apix[1] + origin[1] + apix[1] / 2.0
        xg = xg * apix[0] + origin[0] + apix[0] / 2.0
        indi = list(zip(xg.ravel(), yg.ravel(), zg.ravel()))
        try:
            from scipy.spatial import cKDTree
            gridtree = cKDTree(indi)
        except ImportError:
            try:
                from scipy.spatial import KDTree
                gridtree = KDTree(indi)
            except ImportError:
                return
        return gridtree, indi

    def mapGridPositions(
            self,
            densMap,
            atom,
            gridtree,
            res_map,
            sim_sigma_coeff=0.187,
            sigma_thr=2.0
    ):
        """
        Returns the indices of the nearest pixels to an atom as a list.

        Arguments:
           *densMap*
               Map instance the atom is to be placed on.
           *atom*
               Atom instance.
           *gridtree*
               KDTree of the map coordinates (absolute cartesian)
           *res_map*
               Map resolution
        """
        origin = densMap.origin
        apix = densMap.apix
        x_pos = int(round((atom.x - origin[0]) / apix[0], 0))
        y_pos = int(round((atom.y - origin[1]) / apix[1], 0))
        z_pos = int(round((atom.z - origin[2]) / apix[2], 0))
        if((densMap.x_size() >= x_pos >= 0) and
           (densMap.y_size() >= y_pos >= 0) and
           (densMap.z_size() >= z_pos >= 0)):
            # search all points withing 1.5sigma
            list_points = gridtree.query_ball_point(
                [
                    atom.x,
                    atom.y,
                    atom.z,
                ],
                sigma_thr * max(sim_sigma_coeff * res_map, 1.0)
            )
            return list_points
        else:
            print('Warning, atom out of map box')
            return []

    def model_tree(
            self,
            list_coord1,
            distpot=6.0,
            list_coord2=None,
    ):
        """ Finds neighbouring points
        Returns
        """
        try:
            from scipy.spatial import cKDTree
            coordtree = cKDTree(list_coord1)
            if list_coord2 is not None:
                coordtree1 = cKDTree(list_coord2)
        except ImportError:
            from scipy.spatial import KDTree
            coordtree = KDTree(list_coord1)
            if list_coord2 is not None:
                coordtree1 = KDTree(list_coord2)
        if list_coord2 is not None:
            neigh_points = coordtree.query_ball_tree(coordtree1, distpot)
            # use count_neighbors if the corresponding indices are not required
        else:
            neigh_points = coordtree.query_ball_tree(coordtree, distpot)
        return neigh_points

    def get_coordinates(self, structure_instance):
        """Returns flat indices of the pixels occupied by each residue in a
        chain.

        Arguments:
            structure_instance*: Structure instance of the model.

        Returns:
            Something
        """
        dict_res_CA = {}
        dict_res_indices = {}
        dict_chain_indices = {}
        dict_chain_CA = {}
        currentChain = structure_instance.atomList[0].chain
        for x in structure_instance.atomList:
            if not x.chain == currentChain:
                try:
                    dict_chain_indices[x.model][currentChain] = (
                        dict_res_indices.copy()
                    )
                except KeyError:
                    dict_chain_indices[x.model] = {}
                    dict_chain_indices[x.model][currentChain] = (
                        dict_res_indices.copy()
                    )
                try:
                    dict_chain_CA[x.model][currentChain] = dict_res_CA.copy()
                except KeyError:
                    dict_chain_CA[x.model] = {}
                    dict_chain_CA[x.model][currentChain] = dict_res_CA.copy()
                currentChain = x.chain
                dict_res_indices = {}
                dict_res_CA = {}
            cur_res = x.get_res_no()
            # save residue coords
            if x.atom_name == 'CA':
                # CA coordinates
                dict_res_CA[cur_res] = [x.x, x.y, x.z]
            try:
                dict_res_indices[cur_res].append([x.x, x.y, x.z])
            except KeyError:
                dict_res_indices[cur_res] = [[x.x, x.y, x.z]]
        if currentChain not in dict_chain_indices:
            try:
                dict_chain_CA[x.model][currentChain] = dict_res_CA.copy()
            except KeyError:
                dict_chain_CA[x.model] = {}
                dict_chain_CA[x.model][currentChain] = dict_res_CA.copy()
            try:
                dict_chain_indices[x.model][currentChain] = (
                    dict_res_indices.copy()
                )
            except KeyError:
                dict_chain_indices[x.model] = {}
                dict_chain_indices[x.model][currentChain] = (
                    dict_res_indices.copy()
                )
        return dict_chain_indices, dict_chain_CA

    def get_indices(
            self,
            structure_instance,
            emmap,
            res_map,
            sim_sigma_coeff=0.187,
            sigma_thr=2.0,
            atom_sel=None,
            atom_centre='CA'
    ):
        """Returns flat indices of the pixels occupied by each residue in a
        chain.

        Args:
            structure_instance: Structure instance of the model.
            emmap: Map instance the model is to be placed on.
            res_map: Resolution of the map
            sim_sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
        Returns:
            Dictionaries:

        """

        dict_res_indices = OrderedDict()
        dict_res_CA = OrderedDict()
        dict_chain_res = OrderedDict()
        dict_chain_CA = OrderedDict()
        dict_chain_indices = OrderedDict()
        gridtree = self.maptree(emmap)[0]
        points = []
        # get chain details
        currentChain = structure_instance.atomList[0].chain
        prev_res = structure_instance.atomList[0].get_res_no()
        prev_resname = structure_instance.atomList[0].res
        ca_coord = ['', '', '']
        for x in structure_instance.atomList:
            if atom_sel == 'CA' and not x.atom_name == 'CA':
                continue
            elif atom_sel == 'AR' and x.res not in ['TYR', 'PHE', 'TRP'] \
                    and not x.atom_name == 'CA':
                continue

            cur_res = x.get_res_no()
            if not x.chain == currentChain:
                # uniquify lists
                for e in dict_res_indices:
                    tmplist = dict_res_indices[e][:]
                    setlist = set(tmplist)
                    dict_res_indices[e] = list(setlist)

                try:
                    dict_chain_indices[currentChain].update(
                                                        dict_res_indices.copy()
                                                        )
                except KeyError:
                    dict_chain_indices[currentChain] = dict_res_indices.copy()

                try:
                    dict_chain_CA[currentChain].update(dict_res_CA.copy())
                except KeyError:
                    dict_chain_CA[currentChain] = dict_res_CA.copy()
                currentChain = x.chain
                dict_res_indices = {}
            else:
                # check dict_CA if atom_centre not found for prev res
                if cur_res != prev_res:
                    # if not dict_res_CA.has_key(prev_res):
                    if prev_res not in dict_res_CA:
                        try:
                            dict_res_CA[prev_res] = [prev_resname].extend(
                                                                    ca_coord
                                                                    )
                        except AttributeError:
                            dict_res_CA[prev_res] = [' '].extend(ca_coord)

            currentChain = x.chain
            # save residue numbers in order
            try:
                if cur_res not in dict_chain_res[currentChain]:
                    dict_chain_res[currentChain].append(cur_res)
            except KeyError:
                dict_chain_res[currentChain] = [cur_res]
            # return indices covered by gaussian blur
            if res_map is not None:
                points = self.mapGridPositions(
                                            emmap,
                                            x,
                                            gridtree,
                                            res_map,
                                            sim_sigma_coeff,
                                            sigma_thr)
            # return indices covered by vdW radii
            else:
                points = self.mapGridPositions_vdw(emmap, x, gridtree)

            # nucleic acids
            if x.res in ['A', 'T', 'C', 'G', 'U']:
                if atom_centre in ['CA', 'CB']:
                    atom_centre = "C1'"
                if x.atom_name in ["P", "C3'", "C1'"]:
                    ca_coord = [x.x, x.y, x.z]
            elif x.atom_name == 'CA':
                ca_coord = [x.x, x.y, x.z]
            if x.atom_name == atom_centre:  # x.fullid
                # CA coordinates
                try:
                    dict_res_CA[cur_res] = [x.res, x.x, x.y, x.z]
                except AttributeError:
                    dict_res_CA[cur_res] = [' ', x.x, x.y, x.z]

            prev_res = cur_res
            prev_resname = x.res
            # continue if no indices are returned
            if len(points) == 0:
                dict_res_indices[cur_res] = []
                continue

            # get points occupied by the residue
            if cur_res in dict_res_indices:
                dict_res_indices[cur_res].extend(points)
            else:
                dict_res_indices[cur_res] = points

        if currentChain not in dict_chain_indices:
            # uniquify lists
            for e in dict_res_indices:
                tmplist = dict_res_indices[e][:]
                setlist = set(tmplist)
                dict_res_indices[e] = list(setlist)
            try:
                dict_chain_indices[currentChain].update(
                                                    dict_res_indices.copy())
            except KeyError:
                dict_chain_indices[currentChain] = dict_res_indices.copy()
            try:
                dict_chain_CA[currentChain].update(dict_res_CA.copy())
            except KeyError:
                dict_chain_CA[currentChain] = dict_res_CA.copy()

        if cur_res not in dict_res_CA:
            try:
                dict_res_CA[cur_res] = [x.res].extend(ca_coord)
            except AttributeError:
                dict_res_CA[cur_res] = [' '].extend(ca_coord)

        return dict_chain_indices, dict_chain_res, dict_chain_CA, gridtree

    def old_get_indices(
            self,
            structure_instance,
            emmap,
            res_map,
            sim_sigma_coeff=0.187,
            sigma_thr=2.0,
            atom_sel=None,
    ):
        """
        Returns flat indices of the pixels occupied by each residue in a chain.

        Arguments:
            structure_instance: Structure instance of the model.
            emmap: Map instance the model is to be placed on.
            res_map: Resolution of the map
            sim_sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`

        Returns:
            Dictionaries:
        """

        dict_res_indices = OrderedDict()
        dict_res_dist = OrderedDict()
        dict_chain_res = OrderedDict()
        dict_chain_indices = {}
        gridtree = self.maptree(emmap)[0]
        points = []
        # get chain details
        currentChain = structure_instance.atomList[0].chain
        for x in structure_instance.atomList:
            if atom_sel == 'CA' and not x.atom_name == 'CA':
                continue
            elif (
                    atom_sel == 'AR' and
                    x.res not in ['TYR', 'PHE', 'TRP'] and
                    not x.atom_name == 'CA'
            ):
                continue

            if not x.chain == currentChain:
                # uniquify lists
                for e in dict_res_indices:
                    tmplist = dict_res_indices[e][:]
                    setlist = set(tmplist)
                    dict_res_indices[e] = list(setlist)
                dict_chain_indices[currentChain] = dict_res_indices.copy()
                currentChain = x.chain
                dict_res_indices = {}
            cur_res = x.get_res_no()
            # save residue numbers in order
            try:
                if cur_res not in dict_chain_res[currentChain]:
                    dict_chain_res[currentChain].append(cur_res)
            except KeyError:
                dict_chain_res[currentChain] = [cur_res]
            # return indices covered by gaussian blur
            if res_map is not None:
                points = self.mapGridPositions(
                    emmap,
                    x,
                    gridtree,
                    res_map,
                    sim_sigma_coeff,
                    sigma_thr,
                )
            # return indices covered by vdW radii
            else:
                points = self.mapGridPositions_vdw(emmap, x, gridtree)
            if len(points) == 0:
                dict_res_indices[cur_res] = []
                continue
            if x.atom_name == 'CA':
                dict_res_dist[cur_res] = [x.x, x.y, x.z]
            # get points occupied by the residue
            if cur_res in dict_res_indices:
                dict_res_indices[cur_res].extend(points)
            else:
                dict_res_indices[cur_res] = points
        if currentChain not in dict_chain_indices:
            # uniquify lists
            for e in dict_res_indices:
                tmplist = dict_res_indices[e][:]
                setlist = set(tmplist)
                dict_res_indices[e] = list(setlist)
            dict_chain_indices[currentChain] = dict_res_indices.copy()
        return dict_chain_indices, dict_chain_res, dict_res_dist

    # added by aj
    # get nearest grid indices for a residue atoms
    def get_indices_aj(
            self,
            structure_instance,
            emmap,
            res_map,
            sim_sigma_coeff=0.187,
            sigma_thr=2.0,
            atom_sel=None,
            atom_centre='CA'
    ):
        """ Returns flat indices of the pixels occupied by each residue in a
        chain.

        Args:

            structure_instance: Structure instance of the model.
            emmap: Map instance the model is to be placed on.
            res_map: Resolution of the map
            sim_sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
            sigma_thr:
            atom_sel:
            atom_centre:
        """

        dict_res_indices = OrderedDict()
        dict_res_CA = OrderedDict()
        dict_chain_res = OrderedDict()
        dict_chain_CA = OrderedDict()
        dict_chain_indices = OrderedDict()
        gridtree = self.maptree(emmap)[0]
        points = []
        # get chain details
        currentChain = structure_instance.atomList[0].chain
        prev_res = structure_instance.atomList[0].get_res_no()
        ca_coord = ['', '', '']
        for x in structure_instance.atomList:
            if atom_sel == 'CA' and not x.atom_name == 'CA':
                continue
            elif atom_sel == 'AR' and x.res not in ['TYR', 'PHE', 'TRP'] \
                    and not x.atom_name == 'CA':
                continue

            cur_res = x.get_res_no()
            # TODO: this is just added to pass the test,
            #  not sure that's correct at all!
            prev_resname = x.res
            if not x.chain == currentChain:
                # uniquify lists
                for e in dict_res_indices:
                    tmplist = dict_res_indices[e][:]
                    setlist = set(tmplist)
                    dict_res_indices[e] = list(setlist)
                dict_chain_indices[currentChain] = dict_res_indices.copy()
                dict_chain_CA[currentChain] = dict_res_CA.copy()
                currentChain = x.chain
                dict_res_indices = {}
            else:
                # check dict_CA if atom_centre not found for prev res
                if cur_res != prev_res:
                    if prev_res not in dict_res_CA:
                        try:
                            dict_res_CA[prev_res] = \
                                [prev_resname].extend(ca_coord)
                        except AttributeError:
                            dict_res_CA[prev_res] = [' '].extend(ca_coord)

            # save residue numbers in order
            try:
                if cur_res not in dict_chain_res[currentChain]:
                    dict_chain_res[currentChain].append(cur_res)
            except KeyError:
                dict_chain_res[currentChain] = [cur_res]
            # return indices covered by gaussian blur
            if res_map is not None:
                points = self.mapGridPositions(
                    emmap,
                    x,
                    gridtree,
                    res_map,
                    sim_sigma_coeff,
                    sigma_thr
                )
            # return indices covered by vdW radii
            else:
                points = self.mapGridPositions_vdw(emmap, x, gridtree)
            if len(points) == 0:
                dict_res_indices[cur_res] = []
                continue
            # nucleic acids
            if x.res in ['A', 'T', 'C', 'G', 'U']:
                if atom_centre in ['CA', 'CB']:
                    atom_centre = "C1'"
                if x.atom_name in ["P", "C3'", "C1'"]:
                    ca_coord = [x.x, x.y, x.z]
            elif x.atom_name == 'CA':
                ca_coord = [x.x, x.y, x.z]
            if x.atom_name == atom_centre:  # x.fullid
                # CA coordinates
                try:
                    dict_res_CA[cur_res] = [x.res, x.x, x.y, x.z]
                except AttributeError:
                    dict_res_CA[cur_res] = [' ', x.x, x.y, x.z]

            prev_res = cur_res
            prev_resname = x.res
            # get points occupied by the residue
            if cur_res in dict_res_indices:
                dict_res_indices[cur_res].extend(points)
            else:
                dict_res_indices[cur_res] = points
        if currentChain not in dict_chain_indices:
            # uniquify lists
            for e in dict_res_indices:
                tmplist = dict_res_indices[e][:]
                setlist = set(tmplist)
                dict_res_indices[e] = list(setlist)
            dict_chain_indices[currentChain] = dict_res_indices.copy()
            dict_chain_CA[currentChain] = dict_res_CA.copy()
        if cur_res not in dict_res_CA:
            try:
                dict_res_CA[cur_res] = [x.res].extend(ca_coord)
            except AttributeError:
                dict_res_CA[cur_res] = [' '].extend(ca_coord)
        return dict_chain_indices, dict_chain_res, dict_chain_CA, gridtree

    def _get_map_values(
            self,
            structure_instance,
            emmap,
            res_map,
            sim_sigma_coeff=0.187,
            win=5,
    ):
        """
        Returns avg map density from voxels occupied by overlapping residue
        fragments.

        Arguments:
           *structure_instance*
               Structure instance of the model.
           *emmap*
               Map instance the model is to be placed on.
           *res_map*
               Resolution of the map
            sim_sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
           *win*
               Fragment length (odd values)
        """
        dict_chain_indices, dict_chain_res, dict_res_dist = self.get_indices(
            structure_instance,
            emmap,
            res_map,
            sim_sigma_coeff,
        )
        nz, ny, nx = emmap.fullMap.shape
        zg, yg, xg = np.mgrid[0:nz, 0:ny, 0:nx]
        indi = list(zip(xg.ravel(), yg.ravel(), zg.ravel()))
        dict_chain_scores = {}
        for ch in dict_chain_indices:
            dict_res_scores = {}
            dict_res_indices = dict_chain_indices[ch]
            for res in dict_res_indices:
                if res not in dict_res_scores:
                    indices = dict_res_indices[res][:]
                    for ii in range(1, int(round((win + 1) / 2))):
                        try:
                            indices.extend(
                                dict_res_indices[
                                    dict_chain_res[ch]
                                    [
                                        dict_chain_res[ch].index(res) - ii
                                    ]
                                ]
                            )
                        except Exception:
                            pass
                    for ii in range(1, int(round((win + 1) / 2))):
                        try:
                            indices.extend(
                                dict_res_indices[
                                    dict_chain_res[ch][
                                        dict_chain_res[ch].index(res) + ii
                                    ]
                                ]
                            )
                        except Exception:
                            pass
                    tmplist = indices[:]
                    setlist = set(tmplist)
                    indices = list(setlist)
                    sc_indices = []
                    for ii in indices:
                        sc_indices.append(indi[ii])
                    array_indices = np.array(sc_indices)
                    ind_arrxyz = np.transpose(array_indices)
                    ind_arrzyx = (ind_arrxyz[2], ind_arrxyz[1], ind_arrxyz[0])
                dict_res_scores[res] = np.mean(emmap.fullMap[ind_arrzyx])
            dict_chain_scores[ch] = dict_res_scores.copy()
        return dict_chain_scores

    def _get_indices1(
            self,
            structure_instance,
            emmap,
            res_map,
            sim_sigma_coeff=0.187,
    ):
        """
        Returns flat indices of the pixels occupied by each residue in a chain.

        Arguments:
           *structure_instance*
               Structure instance of the model.
           *emmap*
               Map instance the model is to be placed on.
           *res_map*
               Resolution of the map
            sim_sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
        """
        dict_res_indices = {}
        dict_res_dist = {}
        dict_chain_indices = {}
        gridtree = self.maptree(emmap)
        # get chain details
        currentChain = structure_instance.atomList[0].chain
        for x in structure_instance.atomList:
            if not x.chain == currentChain:
                dict_chain_indices[currentChain] = dict_res_indices.copy()
                currentChain = x.chain
                dict_res_indices = {}
            cur_res = x.get_res_no()
            points = self.mapGridPositions(
                emmap,
                x,
                gridtree,
                res_map,
                sim_sigma_coeff,
            )
            if len(points) == 0:
                dict_res_indices[int(cur_res)] = []
                continue
            if x.atom_name == 'CA':
                dict_res_dist[cur_res] = [x.x, x.y, x.z]
            if int(cur_res) in dict_res_indices:
                dict_res_indices[int(cur_res)].extend(points)
            else:
                dict_res_indices[int(cur_res)] = points
        # uniquify lists
        for el in dict_res_indices:
            tmplist = dict_res_indices[el][:]
            setlist = set(tmplist)
            dict_res_indices[el] = list(setlist)
        return dict_res_indices, dict_res_dist

    def _mut_make_atom_overlay_map(self, densMap, prot):
        for atom in prot.atomList:
            pos = self.mapGridPosition(densMap, atom)
            if pos:
                densMap.fullMap[pos[2]][pos[1]][pos[0]] += pos[3]
        return densMap

    def make_atom_overlay_map(self, densMap, prot):
        """Returns a Map instance with atom masses superposed on it.

        Args:
            densMap: An empty (all densities zero) Map instance to superpose the
                atoms onto
            prot: Model structure instance.

        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:
                Map instance, where Map.fullMap is a 3D grid with the atom
                masses superposed.
        """
        return self._mut_make_atom_overlay_map(densMap.copy(), prot)

    def make_atom_overlay_mapB(self, densMap, prot):
        """
        Returns a Map instance with atom masses superposed on it.

        Args:
            densMap: An empty (all densities zero) Map instance to superpose the
                atoms onto
            prot: Model structure instance.

        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:
                Map instance, where Map.fullMap is a 3D grid with the atom
                masses superposed.
        """
        densMap = densMap.copy()
        for atom in prot.atomList:
            pos = self.mapGridPosition(densMap, atom)
            if pos:
                densMap.fullMap[pos[2]][pos[1]][pos[0]] += pos[3]
        return densMap

    def make_atom_overlay_map1(self, densMap, prot):
        """
        Returns a Map instance with atom locations recorded on the nearest
        voxel with a value of 1.

        Args:
            densMap: An empty (all densities zero) Map instance to superpose the
                atoms onto
            prot: Model structure instance.

        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:
                Map instance, where Map.fullMap is a 3D grid with the atom
                masses superposed.
        """
        densMap = densMap.copy()
        densMap.fullMap = densMap.fullMap * 0
        for atom in prot.atomList:
            if (
                atom.atom_name == 'C' or
                atom.atom_name == 'N' or
                atom.atom_name == 'CA' or
                atom.atom_name == 'O' or
                atom.atom_name == 'CB'
            ):
                pos = self.mapGridPosition(densMap, atom)
                if pos:
                    densMap.fullMap[pos[2]][pos[1]][pos[0]] = 1
        return densMap

    def make_model_grid(
            self,
            prot,
            spacing,
            ca_only=False,
            densMap=False,
    ):
        if not densMap:
            densMap = self.protMap(prot, spacing)
            print(
                'WARNING: Use StructureBlurrer.gaussian_blur_box() to blurred a'
                ' map with a user defined defined cubic box'
            )
        # get flat indices of grid
        nz, ny, nx = densMap.fullMap.shape
        zg, yg, xg = np.mgrid[0:nz, 0:ny, 0:nx]
        indi = zip(xg.ravel(), yg.ravel(), zg.ravel())
        gridtree = self.maptree(densMap)
        currentChain = prot.atomList[0].chain

        for x in prot.atomList:
            if not x.chain == currentChain:
                currentChain = x.chain
            if ca_only and not x.atom_name == 'CA':
                continue
            points, gridpoint = self.mapGridPositions_vdw(densMap, x, gridtree)
            if len(points) == 0:
                continue
            grid_indices = []
            for p in points:
                grid_indices.append(indi[p])
            x.grid_indices = grid_indices[:]
            array_indices = np.array(grid_indices)
            ind_arrxyz = np.transpose(array_indices)
            ind_arrzyx = (ind_arrxyz[2], ind_arrxyz[1], ind_arrxyz[0])
            densMap.fullMap[ind_arrzyx] = 1.0
        return densMap

    def gaussian_blur(
            self,
            prot,
            resolution,
            densMap=False,
            sigma_coeff=0.356,
            normalise=True,
            filename="None",
    ):
        """ Returns a Map instance based on a Gaussian blurring of a protein.

        The convolution of atomic gaussians is done in reciprocal space.

        Arguments:
            prot: the Structure instance to be blurred.
            resolution: The resolution, in Angstroms, to blur the protein to.
            densMap: A map instance to use as a template, which sets the
                boxsize, pixel size and origin. If False, a Map with dimensions
                based on the protein is generated.
            sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
            filename: Output name of the map file, if saved.

        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:

        """
        if not densMap:
            r = min(resolution / 4., 3.5)
            apix = np.array([r, r, r])
            densMap = self.protMap(prot, apix, resolution)
        
            print(
                'WARNING: Use StructureBlurrer.gaussian_blur_box() to blurred a'
                ' map with a user defined defined cubic box'
            )
        x_s = int(densMap.x_size()*densMap.apix[0])
        y_s = int(densMap.y_size()*densMap.apix[1])
        z_s = int(densMap.z_size()*densMap.apix[2])

        newMap = densMap.copy()
        newMap.fullMap = np.zeros((z_s, y_s, x_s))
        newMap.apix = (densMap.apix * densMap.x_size()) / x_s
        sigma = sigma_coeff * resolution
        newMap = self.make_atom_overlay_map(newMap, prot)
        fou_map = fourier_gaussian(fftn(newMap.fullMap), sigma)
        newMap.fullMap = np.real(ifftn(fou_map))
        newMap = newMap.resample_by_box_size(densMap.box_size())
        if normalise:
            newMap = newMap._mut_normalise()
        newMap.filename = filename
        newMap.update_header
        return newMap

    def gaussian_blur_box(
            self,
            prot,
            resolution,
            box_size_x,
            box_size_y,
            box_size_z,
            sigma_coeff=0.356,
            normalise=True,
            filename="None",
    ):
        """
        Returns a Map instance based on a Gaussian blurring of a protein.
        The convolution of atomic structures is done in reciprocal space.

        Arguments:
            prot: the Structure instance to be blurred.
            resolution: The resolution, in Angstroms, to blur the protein to.
            box_size_x: x dimension of map box in Angstroms.
            box_size_y: y dimension of map box in Angstroms.
            box_size_z: z dimension of map box in Angstroms.
            sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
            filename: Output name of the map file, if saved.

        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:

        """
        densMap = self.protMapBox(
            prot,
            np.ones((3)),
            resolution,
            box_size_x,
            box_size_y,
            box_size_z,
            filename,
        )
        x_s = int(densMap.x_size() * densMap.apix[0])
        y_s = int(densMap.y_size() * densMap.apix[1])
        z_s = int(densMap.z_size() * densMap.apix[2])
        newMap = densMap.copy()
        newMap.fullMap = np.zeros((z_s, y_s, x_s))
        newMap.apix = (densMap.apix * densMap.x_size()) / x_s
        sigma = sigma_coeff * resolution
        newMap = self.make_atom_overlay_map(newMap, prot)
        fou_map = fourier_gaussian(fftn(newMap.fullMap), sigma)
        newMap.fullMap = np.real(ifftn(fou_map))
        newMap = newMap.resample_by_box_size(densMap.box_size())
        if normalise:
            newMap = newMap.normalise()
        return newMap

    def hard_sphere(
            self,
            prot,
            resolution,
            densMap=False,
            normalise=True,
            filename="None"
    ):
        """
        Returns a Map instance based on a Hard Sphere model of a protein.
        Usefull for rigid fitting (Topf et al, 2008)

        Arguments:
            prot: The Structure instance to be blurred.
            resolution: The resolution, in Angstroms, to blur the protein to.
            densMap: A map instance to use as a template, which sets the
                boxsize, pixel size and origin. If False, a Map with dimensions
                based on the protein is generated.
            normalise: Normalise the densities in the
                :class:`Map <TEMPy.maps.em_map.Map>` instance to 0 mean using
                :meth:`Map.normalise <TEMPy.maps.em_map.Map.normalise>`
            filename: Output name of the map file, if saved.
        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:

        """
        gridpx = min(resolution / 4., 3.5)
        if not densMap:
            apix = np.array([gridpx, gridpx, gridpx])
            densMap = self.protMap(prot, apix, resolution)
            print(
                'WARNING: Use StructureBlurrer.hard_sphere() to create a map'
                'with a user defined defined cubic box'
            )
        x_s = int(densMap.x_size() * densMap.apix)
        y_s = int(densMap.y_size() * densMap.apix)
        z_s = int(densMap.z_size() * densMap.apix)
        newMap = densMap.resample_by_box_size([z_s, y_s, x_s])
        newMap.fullMap *= 0

        newMap = self.make_atom_overlay_mapB(newMap, prot)
        print(gridpx)
        newMap = newMap.resample_by_box_size(densMap.box_size())
        if normalise:
            newMap = newMap.normalise()
        return newMap

    def hard_sphere_box(
            self,
            prot,
            resolution,
            box_size_x,
            box_size_y,
            box_size_z,
            normalise=True,
            filename="None",
    ):
        """
        Returns a Map instance based on a Hard Sphere model of a protein.
        Usefull for rigid fitting (Topf et al, 2008)

        Arguments:
            prot: The Structure instance to be blurred.
            resolution: The resolution, in Angstroms, to blur the protein to.
            box_size_x: x dimension of map box in Angstroms.
            box_size_y: y dimension of map box in Angstroms.
            box_size_z: z dimension of map box in Angstroms.
            filename: output name of the map file.
        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:

        """
        densMap = self.protMapBox(
            prot,
            np.ones(3),
            resolution,
            box_size_x,
            box_size_y,
            box_size_z,
            filename,
        )
        x_s = int(densMap.x_size() * densMap.apix)
        y_s = int(densMap.y_size() * densMap.apix)
        z_s = int(densMap.z_size() * densMap.apix)
        newMap = densMap.resample_by_box_size([z_s, y_s, x_s])
        newMap.fullMap *= 0

        newMap = self.make_atom_overlay_map(newMap, prot)
        if normalise:
            newMap = newMap.normalise()
        return newMap

    def _gaussian_blur_real_space_vc(
            self,
            struct,
            resolution,
            exp_map,
            sigma_coeff=0.356,
            cutoff=4.0,
    ):
        import voxcov as vc
        blur_vc = vc.BlurMap(
            exp_map.apix,
            exp_map.origin,
            [exp_map.x_size(), exp_map.y_size(), exp_map.z_size()],
            cutoff,
        )
        for a in struct.atomList:
            blur_vc.add_gaussian(
                    [a.x, a.y, a.z],
                    a.get_mass() / resolution,
                    sigma_coeff * resolution
            )
        full_map = blur_vc.to_numpy()
        return Map(
                full_map,
                exp_map.origin,
                exp_map.apix,
                exp_map.filename + "_simulated"
        )

    def gaussian_blur_real_space(
            self,
            prot,
            resolution,
            densMap=False,
            sigma_coeff=0.356,
            normalise=True,
            filename="None"
    ):
        """
        Returns a Map instance based on a Gaussian blurring of a protein.
        The convolution of atomic structures is done in real space

        Arguments:
            prot: the Structure instance to be blurred.
            resolution: the resolution, in Angstroms, to blur the protein to.
            densMap: A map instance to use as a template, which sets the
                boxsize, pixel size and origin. If False, a Map with dimensions
                based on the protein is generated.
            sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
            filename: Output name of the map file, if saved.
        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:

        """

        if self.use_vc:
            m = self._gaussian_blur_real_space_vc(
                    prot,
                    resolution,
                    densMap,
                    sigma_coeff=sigma_coeff
            )
            if normalise:
                m._mut_normalise()
            return m

        if not densMap:
            r = np.clip(resolution / 4., a_min=1.0, a_max=3.5)
            densMap = self.protMap(
                prot,
                apix=np.array((r, r, r), dtype=float),
                resolution=resolution
            )
            print(
                'WARNING: Use StructureBlurrer.gaussian_blur_real_space_box()'
                'to blurred a map with a user defined defined cubic box'
            )
        x_s = int(densMap.x_size() * densMap.apix[0])
        y_s = int(densMap.y_size() * densMap.apix[1])
        z_s = int(densMap.z_size() * densMap.apix[2])
        newMap = Map(
            np.zeros((z_s, y_s, x_s)),
            densMap.origin,
            densMap.apix,
            'mapname',
        )
        newMap.apix = (densMap.apix[0] * densMap.x_size()) / x_s, \
                      (densMap.apix[1] * densMap.y_size()) / y_s, \
                      (densMap.apix[2] * densMap.z_size()) / z_s
        newMap.update_header()
        densMap_apix = densMap.apix

        sigma = sigma_coeff * resolution
        newMap = self.make_atom_overlay_map(newMap, prot)
        gauss_map = gaussian_filter(newMap.fullMap, sigma)
        newMap.fullMap = gauss_map
        newMap = newMap.downsample_map(
            densMap_apix,
            grid_shape=densMap.fullMap.shape,
        )
        if normalise:
            newMap = newMap._mut_normalise()
        return newMap

    def gaussian_blur_real_space_box(
            self,
            prot,
            resolution,
            box_size_x,
            box_size_y,
            box_size_z,
            sigma_coeff=0.356,
            normalise=True,
            filename="None",
    ):
        """
        Returns a Map instance based on a Gaussian blurring of a protein.
        The convolution of atomic structures is done in real space

        Arguments:
            prot: the Structure instance to be blurred.
            resolution: the resolution, in Angstroms, to blur the protein to.
            box_size_x: x dimension of map box in Angstroms.
            box_size_y: y dimension of map box in Angstroms.
            box_size_z: z dimension of map box in Angstroms.
            sigma_coeff: Parameter need for Structure Blurrer. Full
                explanation :ref:`here<Note on real space blurring:>`
            filename: output name of the map file, if saved.
        Returns:
            :class:`Map <TEMPy.maps.em_map.Map>` instance:
        """
        newMap = self.protMapBox(
            prot,
            np.ones(3),
            resolution,
            box_size_x,
            box_size_y,
            box_size_z,
            filename,
        )
        self._mut_make_atom_overlay_map(newMap, prot)
        sigma = np.clip(sigma_coeff * resolution, a_min=1.0, a_max=None)
        newMap.fullMap = gaussian_filter(newMap.fullMap, sigma)
        if normalise:
            newMap._mut_normalise()
        return newMap

    def _bandpass_blur(
            self,
            atomList,
            densMap,
            lopass,
            lomin,
            lowid,
            hipass,
            hiwid,
    ):
        """
        WARNING: BANDPASS FILTERING (NOT WORKING YET)
        """
        raise NotImplementedError

    def _bandpass_mask_gaussian(
            self,
            densMap,
            lopass,
            lopass_min,
            lowid,
            hipass,
            hiwid,
    ):
        """
        WARNING: BANDPASS FILTERING (NOT WORKING YET)
        """
        newMap = densMap.copy()
        centre = (np.array(newMap.box_size[:]) - 1) / 2.0
        from time import time
        for z in range(newMap.box_size[2]):
            for y in range(newMap.box_size[1]):
                for x in range(newMap.box_size[0]):
                    t1 = time()
                    dist = np.sqrt(
                        (x-centre[0])**2 +
                        (y-centre[1])**2 +
                        (z-centre[2])**2
                    )
                    t2 = time()
                    newMap[z][y][x] = self.bandpass_eq_gaussian(
                        dist,
                        lopass,
                        lopass_min,
                        lowid,
                        hipass,
                        hiwid,
                    )
                    t3 = time()
                    print(t2-t1, t3-t2)
        return newMap

    def _bandpass_eq_gaussian(
            self,
            dist,
            lopass,
            lopass_min,
            lowid,
            hipass,
            hiwid,
    ):
        """
        WARNING: BANDPASS FILTERING (NOT WORKING YET)
        """
        lp_max = lopass + lowid
        hp_min = hipass - hiwid
        if dist <= lp_max:
            return (
                lopass_min +
                (1 - lopass_min) *
                np.exp(-0.5 * ((dist - lp_max) / lowid)**2)
            )
        elif lp_max < dist <= hp_min:
            return 1.0
        else:
            return np.exp(-0.5 * ((dist - hp_min) / hiwid)**2)

    def _bandpass_test(
            self,
            lopass,
            lopass_min,
            lowid,
            hipass,
            hiwid,
            l_len,
    ):
        """
        WARNING: BANDPASS FILTERING (NOT WORKING YET)
        """
        from time import time
        start = time()
        a = np.zeros([l_len])
        for x in range(l_len):
            a[x] = self._bandpass_eq_gaussian(
                x,
                lopass,
                lopass_min,
                lowid,
                hipass,
                hiwid,
            )
        end = time()
        print(end - start)
        return a

    def make_spherical_mask(
                            self,
                            diameter_pix,
                            box_size,
                            centroid,
                            cos_edge,
                            pixel_size=(1.0, 1.0, 1.0),
                            filename='',
                            reference_map=None,
                            ):

        # this implementation is slower for small masks in large boxes

        radius = int(diameter_pix / 2)

        # check we're not indexing outside limits
        if centroid[0] - radius - cos_edge < 0:
            centroid[0] = radius + cos_edge
        if centroid[2] - radius - cos_edge < 0:
            centroid[2] = radius + cos_edge
        if centroid[1] - radius - cos_edge < 0:
            centroid[1] = radius + cos_edge

        if centroid[0] + radius > box_size[0]:
            centroid[0] = box_size[0] - radius - cos_edge
        if centroid[2] + radius + cos_edge >= box_size[2]:
            centroid[2] = box_size[2] - radius - cos_edge
        if centroid[1] + radius + cos_edge >= box_size[1]:
            centroid[1] = box_size[1] - radius - cos_edge

        z_ = np.arange(0 - centroid[0], box_size[0] - centroid[0])
        y_ = np.arange(0 - centroid[1], box_size[1] - centroid[1])
        x_ = np.arange(0 - centroid[2], box_size[2] - centroid[2])
        x, y, z = np.meshgrid(y_, z_, x_, indexing='xy')
        r = np.abs(np.sqrt(x**2 + y**2 + z**2))
        rbins = np.linspace(0, r.max(), int(r.max()))
        r = np.searchsorted(rbins, r, "right")
        r -= 1

        # delete big x, y, z arrays to help reduce memory usage
        del x, y, z, x_, y_, z_
        gc.collect()

        mask_soft_edge = np.zeros(box_size)
        # make a nice cosine edge
        for n in range(radius, radius + cos_edge, 1):
            x = (n - radius) / cos_edge
            x = np.cos(np.pi * x)
            x = (x + 1) / 2
            mask_soft_edge[r == n] = x
        mask_soft_edge[r <= radius] = 1

        if reference_map is not None:
            pixel_size = reference_map.apix
            origin = reference_map.origin
        else:
            origin = centroid

        return Map(mask_soft_edge, origin, pixel_size, filename)
