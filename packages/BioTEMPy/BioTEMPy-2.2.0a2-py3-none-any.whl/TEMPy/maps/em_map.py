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
#     Farabella, I., Vasishtan, D., Joseph, A.P., Pandurangan, A.P.,
#     Sahota, H. & Topf, M. (2015). J. Appl. Cryst. 48.
#
# =============================================================================


import datetime
import math
from random import randrange
import sys

import numpy as np
from scipy.ndimage.interpolation import (
    affine_transform,
    map_coordinates,
    shift,
    spline_filter,
)
from scipy.ndimage import (
    generic_filter,
    laplace,
    minimum_filter,
    uniform_filter,
)
from scipy.ndimage.filters import sobel
from scipy.fftpack import (
    fftn,
    fftshift,
)
from scipy.signal import resample
from scipy.spatial import KDTree
from scipy.ndimage.morphology import binary_opening
from scipy.ndimage import measurements
import struct as binary

import TEMPy.math.vector as Vector
from TEMPy.protein.prot_rep_biopy import BioPy_Structure, Atom
import mrcfile


class Map:
    """A class representing information from a density map file.

    Args:
        fullMap: 3D Numpy array containing the EM density
        origin: Origin of the EM map, in [x, y, z] format.
        apix: Pixel size (Å) of the EM map.
        filename: Filename of the parsed map.
        header: Python array, containing the header information, ordered based
            on the
            `mrc header format <https://www.ccpem.ac.uk/mrc_format/mrc2014.php>`_.
        ext_header: Information present in the extended header, as per the
            `mrc header format <https://www.ccpem.ac.uk/mrc_format/mrc2014.php>`_
            , if present.

    Returns:
        Map Instance.

    :ivar Map.fullMap: 3D Numpy array containing the EM density
    :ivar Map.origin: Origin of the EM map, in [x, y, z] format.
    :ivar Map.apix: Pixel size (Å) of the EM map.
    :ivar Map.filename: Filename of the parsed map.
    :ivar Map.header: Python array, containing the header information, ordered
        based on the
        `mrc header format <https://www.ccpem.ac.uk/mrc_format/mrc2014.php>`_.
    :ivar Map.ext_header: Information present in the extended header, as per
        the
        `mrc header format <https://www.ccpem.ac.uk/mrc_format/mrc2014.php>`_
        , if present.

    """

    def __init__(
            self,
            fullMap,
            origin,
            apix,
            filename,
            header=[],
            ext_header=[]
    ):
        self.header = header
        self.origin = origin
        self.apix = apix
        self.filename = filename
        self.fullMap = fullMap
        self.ext_header = ext_header

    def __repr__(self):
        box_size = list(self.box_size())
        box_size.reverse()
        string1 = 'Obtained from ' + self.filename + '\n'
        string2 = 'Origin: [{:.3f} {:.3f} {:.3f}]\n'.format(
            self.origin[0], self.origin[1], self.origin[2]
        )
        string3 = 'Box size (x,y,z): ' + str(box_size) + '\n'
        string4 = 'Grid spacing: [{:.3f} {:.3f} {:.3f}]\n'.format(
            self.apix[0], self.apix[1], self.apix[2])
        string5 = (
                'Min, max, mean, std: %.3f, %.3f, %.3f, %.3f\n' %
                (
                    self.min(),
                    self.max(),
                    self.mean(),
                    self.std()
                )
        )
        return string1 + string2 + string3 + string4 + string5

    def x_origin(self):
        """
        Returns:
            x-coordinate of the origin."""
        return self.origin[0]

    def y_origin(self):
        """
        Returns:
            y-coordinate of the origin."""
        return self.origin[1]

    def z_origin(self):
        """
        Returns:
            z-coordinate of the origin."""
        return self.origin[2]

    def copy(self):
        """
        Returns:
            copy of the Map Instance.
        """
        copy = Map(
            self.fullMap.copy(),
            self.origin[:],
            self.apix,
            self.filename,
            self.header[:],
            self.ext_header[:]
        )
        return copy

    def getMap(self):
        """
        Returns:
            Numpy array containing the map density data.
        """
        return self.fullMap

    def box_size(self):
        """
        Returns:
            Size of the map array, in Numpy (Z, Y, X) format. """
        return self.fullMap.shape

    def x_size(self):
        """
        Returns:
            Size of the map array in x direction.
        """
        return self.fullMap.shape[2]

    def y_size(self):
        """
        Returns:
            Size of the map array in y direction."""
        return self.fullMap.shape[1]

    def z_size(self):
        """
        Returns:
            Size of the map array in z direction.
        """
        return self.fullMap.shape[0]

    def map_size(self):
        """
        Returns:
            Number of voxels in the fullMap array. """
        return self.fullMap.size

    def __getitem__(self, index):
        """
        Allows direct indexing of the map array from the Map instance.
        ie. map[2][2][1] instead of map.fullMap[2][2][1]
        """
        return self.fullMap[index]

    def _shift_density(self, offset):
        self.fullMap = self.fullMap + float(offset)

    def scale_map(self, scaling):
        """ Scaling Map by scaling factor

        Returns:
            new Map instance
         """
        sc = 1. / scaling
        c_sh = self.pixel_centre() * (1 - sc)
        newMap = self.copy()
        newMap.fullMap = affine_transform(
            self.fullMap,
            np.diag([sc, sc, sc]),
            offset=[c_sh.z, c_sh.y, c_sh.x]
        )
        return newMap

    def _crop_box(self, c, f):
        """
        Crop a map in place based on a threshold
        Arguments:
            *c*
                map threshold
            *f*
                factor to relax threshold
        Returns:
        """
        minval = float(c) - (float(f) * self.std())
        axis_diff = []
        for i in range(3):
            ct1 = 0
            try:
                while (self.fullMap[0] < minval).all():
                    self.fullMap = np.delete(self.fullMap, 0, 0)
                    ct1 += 1
            except (IndexError, ValueError):
                pass
            axis_diff.append(ct1)
            ct2 = 0
            try:
                while (self.fullMap[self.fullMap.shape[0] - 1] < minval).all():
                    self.fullMap = np.delete(self.fullMap, -1, 0)
                    ct2 += 1
            except (IndexError, ValueError):
                pass
            self.fullMap = np.transpose(self.fullMap, (2, 0, 1))
        ox = self.origin[0] + axis_diff[1] * self.apix[0]
        oy = self.origin[1] + axis_diff[2] * self.apix[1]
        oz = self.origin[2] + axis_diff[0] * self.apix[2]
        self.origin = (ox, oy, oz)

    def _alignment_box(self, map2, s):
        (ox, oy, oz) = (
            self.origin[0],
            self.origin[1],
            self.origin[2]
        )
        (o1x, o1y, o1z) = (
            map2.origin[0],
            map2.origin[1],
            map2.origin[2]
        )
        offset = (
            o1x - ox,
            o1y - oy,
            o1z - oz
        )
        (m1x, m1y, m1z) = (
            ox + self.fullMap.shape[2] * self.apix[2],
            oy + self.fullMap.shape[1] * self.apix[1],
            oz + self.fullMap.shape[0] * self.apix[0]
        )
        (m2x, m2y, m2z) = (
            o1x + map2.fullMap.shape[2] * map2.apix[2],
            o1y + map2.fullMap.shape[1] * map2.apix[1],
            o1z + map2.fullMap.shape[0] * map2.apix[0]
        )
        (nx, ny, nz) = (o1x, o1y, o1z)
        if offset[0] > 0:
            nx = ox
        if offset[1] > 0:
            ny = oy
        if offset[2] > 0:
            nz = oz

        (lz, ly, lx) = (
            (m2z-nz) / float(s[2]),
            (m2y-ny) / float(s[1]),
            (m2x-nx) / float(s[0])
        )
        if m2x < m1x:
            lx = (m1x - nx) / float(s[0])
        if m2y < m1y:
            ly = (m1y - ny) / float(s[1])
        if m2z < m1z:
            lz = (m1z - nz) / float(s[2])
        gridshape = (int(lz), int(ly), int(lx))
        new_origin = (nx, ny, nz)
        return gridshape, new_origin

    def _interpolate_to_grid(self, grid, s, ori):
        new_map = self.copy()
        (ox, oy, oz) = (
            self.origin[0],
            self.origin[1],
            self.origin[2],
        )
        (o1x, o1y, o1z) = (
            float(ori[0]),
            float(ori[1]),
            float(ori[2])
        )
        scale = s / self.apix
        offset = (
            o1x - ox,
            o1y - oy,
            o1z - oz
        )

        gridshape = grid
        new_map.origin = (o1x, o1y, o1z)
        grid_indices = np.indices(gridshape)
        z_ind = grid_indices[0]
        z_ind.ravel()
        y_ind = grid_indices[1]
        y_ind.ravel()
        x_ind = grid_indices[2]
        x_ind.ravel()
        z_ind = ((offset[2]) / self.apix[2]) + scale[2] * z_ind
        y_ind = ((offset[1]) / self.apix[1]) + scale[1] * y_ind
        x_ind = ((offset[0]) / self.apix[0]) + scale[0] * x_ind
        new_array = map_coordinates(
            self.fullMap,
            [z_ind, y_ind, x_ind],
            cval=self.min(),
        )
        new_map.fullMap = new_array.reshape(gridshape)
        new_map.origin = (o1x, o1y, o1z)
        new_map.apix = s
        return new_map

    def _downsample_apix(self, spacing):
        apix_ratio = (
            round(self.header[10] / self.header[7], 2) / spacing,
            round(self.header[11] / self.header[8], 2) / spacing,
            round(self.header[12] / self.header[9], 2) / spacing
        )
        grid_shape = (
            int(round(self.z_size() * apix_ratio[2])),
            int(round(self.y_size() * apix_ratio[1])),
            int(round(self.x_size() * apix_ratio[0]))
        )
        try:
            newmap = self._interpolate_to_grid1(
                grid_shape,
                spacing,
                self.origin
            )
        except:  # noqa:E722
            newmap = self._interpolate_to_grid(
                grid_shape,
                spacing,
                self.origin
            )
        return newmap

    def downsample_map(self, spacing, grid_shape=None):
        apix_ratio = self.apix / spacing
        if grid_shape is None:
            grid_shape = (
              int(round(self.z_size() * apix_ratio[2])),
              int(round(self.y_size() * apix_ratio[1])),
              int(round(self.x_size() * apix_ratio[0]))
            )
        emmap_1 = self._interpolate_to_grid(
          grid_shape,
          spacing,
          self.origin
        )
        return emmap_1

    def _peak_density(self):
        """
        Find background peak and sigma (for values beyond the peak)

        Returns:
            peak, average and sigma (beyond peak)
        """
        freq, bins = np.histogram(self.fullMap, 1000)
        ind = np.nonzero(freq == np.amax(freq))[0]
        peak = None
        ave = np.mean(self.fullMap)
        sigma = np.std(self.fullMap)

        for i in ind:
            val = (bins[i] + bins[i + 1]) / 2.
            if val < float(ave) + float(sigma):
                peak = val
        if peak is None:
            peak = ave
        sigma1 = None
        if peak is not None:
            mask_array = self.fullMap[self.fullMap > peak]
            sigma1 = np.sqrt(
                np.mean(
                    np.square(mask_array - peak)
                )
            )

        return peak, ave, sigma1

    def _sobel_surface_mask(self, c):
        """ Apply sobel filter on binned density maps

        Args:
            c: Threshold that defines the maps surface.

        Returns:
            Sobel filtered Map instance
        """

        newmap = self.copy()
        binmap = newmap.fullMap > float(c)
        sx = sobel(binmap, 0, mode='constant')
        sy = sobel(binmap, 1, mode='constant')
        sz = sobel(binmap, 2, mode='constant')
        newmap.fullMap = np.sqrt(sx * sx + sy * sy + sz * sz)
        newmap.fullMap = binmap * newmap.fullMap
        return newmap

    def _sobel_filter_contour(self, c):
        """Apply sobel filter on density maps above contour

        Args:
            c: Threshold that defines the maps surface.

        Returns:
            Sobel filtered Map instance
        """

        newmap = self.copy()
        binmap = newmap.fullMap > c
        newmap.fullMap = binmap * newmap.fullMap
        sx = sobel(newmap.fullMap, 0, mode='constant')
        sy = sobel(newmap.fullMap, 1, mode='constant')
        sz = sobel(newmap.fullMap, 2, mode='constant')
        newmap.fullMap = np.sqrt(sx * sx + sy * sy + sz * sz)
        return newmap

    def _sobel_filter_map_all(self):
        """ Apply sobel filter on self

        Returns:
            Sobel filtered Map instance
        """
        newmap = self.copy()
        sx = sobel(newmap.fullMap, 0, mode='constant')
        sy = sobel(newmap.fullMap, 1, mode='constant')
        sz = sobel(newmap.fullMap, 2, mode='constant')
        newmap.fullMap = np.sqrt(sx * sx + sy * sy + sz * sz)
        return newmap

    def _laplace_filtered_contour(self, c):
        """
        Apply Laplacian filter on density maps above contour

        Returns:
            new Map instance
        """
        newmap = self.copy()
        binmap = newmap.fullMap > float(c)
        newmap.fullMap = binmap * newmap.fullMap
        newmap.fullMap = laplace(newmap.fullMap)
        return newmap

    def _surface_minimum_filter(self, c):
        """
        contour the map
        get the footprint array corresponding to 6 neighbors of a voxel
        apply minimum filter to return surface voxels with zeros in
        select those voxels with zeros filled in after applying minimum filter
        """
        binmap = self.fullMap > float(c)
        fp = self._grid_footprint()
        binmap_surface = minimum_filter(
            binmap * 1,
            footprint=fp,
            mode='constant',
            cval=0.0
        )
        binmap_surface = ((binmap * 1 - binmap_surface) == 1) * 1

        return binmap_surface

    def _surface_features(
            self,
            c,
            window=21,
            itern=1
    ):
        newmap = self.copy()
        binmap = self.fullMap > float(c)
        newmap.fullMap = binmap * 1.0
        for i in range(itern):
            newmap.fullMap = uniform_filter(
                newmap.fullMap,
                size=window,
                mode='constant',
                cval=0.0
            )
            newmap.fullMap = newmap.fullMap*binmap
            binmap = newmap.fullMap > 0.0
            minval = newmap.fullMap[binmap].min()
            newmap.fullMap = newmap.fullMap - minval + (0.001 * minval)
            newmap.fullMap = newmap.fullMap * binmap
            newmap.fullMap = newmap.fullMap / float(newmap.fullMap.max())
        return newmap

    def _soft_mask(
            self,
            c=None,
            window=5,
            itern=3
    ):
        newmap = self.copy()
        if c is not None:
            newmap.fullMap = newmap.fullMap * (newmap.fullMap > float(c))
        binmap = newmap.fullMap != 0
        footprint_sph = self._make_spherical_footprint(window)
        for i in range(itern):
            newmap.fullMap = generic_filter(
                newmap.fullMap,
                np.mean,
                footprint=footprint_sph,
                mode='constant',
                cval=0.0
            )
        newmap.fullMap[binmap] = self.fullMap[binmap]
        return newmap.fullMap

    def _std_neigh(self, c=None, window=6):
        newmap = self.copy()
        if c is not None:
            newmap.fullMap = newmap.fullMap * (newmap.fullMap > float(c))
        footprint_sph = self._make_spherical_footprint(window)
        newmap.fullMap = generic_filter(
            newmap.fullMap,
            np.std,
            footprint=footprint_sph,
            mode='constant',
            cval=0.0
        )
        return newmap

    def _mean_neigh(
            self,
            c=None,
            window=6,
            itr=1
    ):
        newmap = self.copy()
        if c is not None:
            newmap.fullMap = newmap.fullMap * (newmap.fullMap > float(c))
        footprint_sph = self._make_spherical_footprint(window)
        for i in range(itr):
            newmap.fullMap = generic_filter(
                newmap.fullMap,
                np.mean,
                footprint=footprint_sph,
                mode='constant',
                cval=0.0,
            )
        return newmap

    def _map_digitize(
            self,
            cutoff,
            nbins,
            left=False
    ):
        try:
            from numpy import digitize
        except ImportError:
            print('Numpy Digitize missing, try v1.8')
        binMap = self.copy()
        bins = []
        step = (self.fullMap.max() - float(cutoff)) / nbins
        ini = float(cutoff) + (0.000001 * step)
        if left:
            ini = float(cutoff) - (0.000001 * step)
        bins.append(ini)
        for ii in range(1, nbins + 1):
            bins.append(float(cutoff) + ii * step)
        if bins[-1] < self.fullMap.max():
            bins = bins[:-1]
            bins.append(self.fullMap.max())

        for z in range(len(self.fullMap)):
            for y in range(len(self.fullMap[z])):
                binMap.fullMap[z][y] = digitize(self.fullMap[z][y], bins)
        return binMap

    def _map_depth(self, c):
        newmap = self.copy()
        binmap = self.fullMap > float(c)
        newmap.fullMap = binmap * 1.0
        for i in range(3):
            newmap.fullMap = uniform_filter(
                newmap.fullMap,
                size=21,
                mode='constant',
                cval=0.0,
            )
            newmap.fullMap = newmap.fullMap * binmap
            binmap = newmap.fullMap > 0.0
            minval = newmap.fullMap[binmap].min()
            newmap.fullMap = newmap.fullMap - minval + 0.001
            newmap.fullMap = newmap.fullMap * binmap
            newmap.fullMap = newmap.fullMap / float(newmap.fullMap.max())
        return newmap

    def _label_patches(self, c, prob=0.2):
        fp = self._grid_footprint()
        binmap = self.fullMap > float(c)
        label_array, labels = measurements.label(
            self.fullMap * binmap,
            structure=fp
        )
        sizes = measurements.sum(binmap, label_array, range(labels + 1))
        if labels < 10:
            m_array = sizes < 0.05 * sizes.max()
            ct_remove = np.sum(m_array)
            remove_points = m_array[label_array]
            label_array[remove_points] = 0
            return (
                (label_array > 0) * (self.fullMap * binmap),
                labels - ct_remove + 1
            )

        freq, bins = np.histogram(sizes[1:], 20)

        m_array = np.zeros(len(sizes))
        ct_remove = 0
        for i in range(len(freq)):
            fr = freq[i]
            s2 = bins[i + 1]
            s1 = bins[i]
            p_size = float(fr) / float(np.sum(freq))
            if s2 < 10 or p_size > prob:
                m_array = m_array + ((sizes >= s1) & (sizes < s2))
                ct_remove += 1
        m_array = m_array > 0
        remove_points = m_array[label_array]

        label_array[remove_points] = 0
        return (
            (label_array > 0) * (self.fullMap * binmap),
            labels - ct_remove
        )

    def _grid_footprint(self):
        a = np.zeros((3, 3, 3))
        a[1, 1, 1] = 1
        a[0, 1, 1] = 1
        a[1, 0, 1] = 1
        a[1, 1, 0] = 1
        a[2, 1, 1] = 1
        a[1, 2, 1] = 1
        a[1, 1, 2] = 1

        return a

    def _make_spherical_footprint(self, ln):
        rad_z = np.arange(np.floor(ln / 2.0) * -1, np.ceil(ln / 2.0))
        rad_y = np.arange(np.floor(ln / 2.0) * -1, np.ceil(ln / 2.0))
        rad_x = np.arange(np.floor(ln / 2.0) * -1, np.ceil(ln / 2.0))

        rad_x = rad_x**2
        rad_y = rad_y**2
        rad_z = rad_z**2
        dist = np.sqrt(rad_z[:, None, None] + rad_y[:, None] + rad_x)
        return (dist <= np.floor(ln / 2.0)) * 1

    def _map_binary_opening(self, c, it=1):
        """
        current position can be updated based on neighbors only
        threshold can be 1*std() to be safe?
        """
        fp = self._grid_footprint()
        fp[1, 1, 1] = 0
        self.fullMap = self.fullMap * (self.fullMap > float(c))
        self.fullMap = self.fullMap * binary_opening(
            self.fullMap > float(c),
            structure=fp,
            iterations=it
        )

    def resize_map(self, new_size):
        """ Resize Map instance by cropping/padding (with zeros) the box.

        Args:
            new_size: 3-tuple (x,y,z) giving the box size.

        Returns:
            Map instance with new box size.
        """
        newMap = self.copy()
        newMap.fullMap = np.zeros(new_size)
        min_box = [
            min(x, y) for x, y in zip(newMap.box_size(), self.box_size())
        ]
        newMap.fullMap[
            :min_box[0],
            :min_box[1],
            :min_box[2]
        ] = self.fullMap[
                :min_box[0],
                :min_box[1],
                :min_box[2]
            ]
        return newMap

    def _mut_normalise(self):
        if self.fullMap.std() == 0:
            pass
        else:
            self.fullMap -= self.fullMap.mean()
            self.fullMap /= self.fullMap.std()
        return self

    def normalise(self):
        """Returns: 0-mean normalised Map instance. """
        return self.copy()._mut_normalise()

    def normalise_to_1_minus1(self, in_place=False):
        """
        """
        if not in_place:
            map = self.copy()
        else:
            map = self

        data = map.fullMap
        normalised_data = (np.divide(
                                    (data - data.min()),
                                    (data.max() - data.min())) * 2) - 1
        map.fullMap = normalised_data

        return map

    def pad_map(self, nx, ny, nz):
        """ Pad a map (in place) by specified number of voxels along each
        dimension.

        Args:
            nx,ny,nz: Number of voxels to pad in each dimension.
        Returns:
            Padded Map instance
        """
        gridshape = (
            self.fullMap.shape[0] + nz,
            self.fullMap.shape[1] + ny,
            self.fullMap.shape[2] + nx
        )
        new_array = np.zeros(gridshape)
        new_array.fill(self.fullMap.min())
        oldshape = self.fullMap.shape
        indz, indy, indx = (
            round((gridshape[0] - oldshape[0]) / 2.),
            round((gridshape[1] - oldshape[1]) / 2.),
            round((gridshape[2] - oldshape[2]) / 2.)
        )
        self.origin = (
            self.origin[0] - self.apix[0] * indx,
            self.origin[1] - self.apix[1] * indy,
            self.origin[2] - self.apix[2] * indz
        )
        new_array[
            indz:indz + oldshape[0],
            indy:indy + oldshape[1],
            indx:indx + oldshape[2]
        ] = self.fullMap
        self.fullMap = new_array

    def get_cropped_box_around_atom(self, atom, new_box_size):
        """Returns a new Map object with specified shape centred on the CA
        of a specific atom.

        Args:
            atom: An Atom (or subclass) instance.
            new_box_size: List, tuple or np.ndarray with shape (3,)
                defining the shape for the new Map object

        Returns:
              Map Instance for the cropped out density.
        """

        x = int(round((atom.x - self.origin[0])/self.apix[0], 0))
        y = int(round((atom.y - self.origin[1])/self.apix[1], 0))
        z = int(round((atom.z - self.origin[2])/self.apix[2], 0))

        if np.isclose(new_box_size, self.fullMap.shape).all():
            print("WARNING: Cropped box size is equal to, or bigger than, the "
                  "original box size.")
            return self.copy()
        else:
            return self.get_cropped_box([z, y, x], new_box_size)

    def get_cropped_box(self, centroid, new_box_size):
        """Returns a new Map object with specified shape centred an
        arbitrary point.

        Note: centroid and new_box_size should follow numpy indexing
        rules, i.e. follow [z, y, x] convention.

        Args:
            centroid: List, tuple or np.ndarray with shape (3,)
                defining the central point in the Map to crop around.
                Must be (i, j, k) coordinates, i.e. an index into
                the Map.fullMap ndarray.
            new_box_size: List, tuple or np.ndarray with shape (3,)
                defining the shape for the new Map object

        Returns:
              Map Instance for the cropped out density.
        """
        new_box_size = np.array(new_box_size)
        map_np_array = self.fullMap
        box_size = self.fullMap.shape

        half_mask_left = np.floor(new_box_size / 2).astype(np.int64)
        half_mask_right = np.ceil(new_box_size / 2).astype(np.int64)

        # check we're not indexing outside limits
        if centroid[0] - half_mask_left[0] < 0:
            centroid[0] = half_mask_left[0]
        if centroid[2] - half_mask_left[2] < 0:
            centroid[2] = half_mask_left[2]
        if centroid[1] - half_mask_left[1] < 0:
            centroid[1] = half_mask_left[1]

        if centroid[0] + half_mask_right[0] >= box_size[0]:
            centroid[0] = box_size[0] - half_mask_right[0]
        if centroid[2] + half_mask_right[2] >= box_size[2]:
            centroid[2] = box_size[2] - half_mask_right[2]
        if centroid[1] + half_mask_right[1] >= box_size[1]:
            centroid[1] = box_size[1] - half_mask_right[1]

        top_left = [
                    centroid[0] - half_mask_left[0],
                    centroid[1] - half_mask_left[1],
                    centroid[2] - half_mask_left[2],
                    ]
        bottom_right = [
                    centroid[0] + half_mask_right[0],
                    centroid[1] + half_mask_right[1],
                    centroid[2] + half_mask_right[2],
                    ]
        cropped_map = map_np_array[
                                    top_left[0]:bottom_right[0],
                                    top_left[1]:bottom_right[1],
                                    top_left[2]:bottom_right[2],
                                    ]
        new_origin = self.origin + ((np.flip(centroid - half_mask_left)) * self.apix)
        return Map(cropped_map, new_origin, self.apix, self.filename,)

    def rotate_by_axis_angle(
            self,
            x,
            y,
            z,
            angle,
            CoM,
            rad=False,
    ):
        """ Rotate map around pivot, given by CoM, using Euler angles.

        Args:
            x,y,z: Axis to rotate about, ie. x,y,z =  0,0,1 rotates the Map
                round the xy-plane.
            angle: Angle (in radians if rad == True, else in degrees) of
                rotation.
            CoM: Centre of mass around which map will be rotated.

        Returns:
            Rotated Map instance
        """

        m = Vector.axis_angle_to_matrix(
            x,
            y,
            z,
            angle,
            rad,
        )
        newCoM = CoM.matrix_transform(m.T)
        offset = CoM - newCoM
        newMap = self.matrix_transform(
            m,
            offset.x,
            offset.y,
            offset.z,
        )
        return newMap

    def rotate_by_euler(
            self,
            x,
            y,
            z,
            CoM,
            rad=False
    ):
        """Rotate map around pivot, given by CoM, using Euler angles.

        Args:
            x,y,z: Euler angles (in radians if rad == True, else in degrees)
                used to rotate map.
            CoM: Centre of mass around which map will be rotated.
            *x, y, z*
                translation in angstroms.

        Returns:
            Rotated Map instance
        """
        m = Vector.euler_to_matrix(
            x,
            y,
            z,
            rad,
        )
        newCoM = CoM.matrix_transform(m.T)
        offset = CoM - newCoM
        newMap = self.matrix_transform(
            m,
            offset.x,
            offset.y,
            offset.z,
        )
        return newMap

    def _box_transform(self, mat):
        """ Calculate box dimensions after rotation

        Args:
            mat: Input rotation matrix
        Returns:
            New box shape in format x, y, z
        """
        v1 = Vector.Vector(
            self.origin[0],
            self.origin[1],
            self.origin[2],
        )
        v2 = Vector.Vector(
            self.origin[0] + (self.apix[0] * self.x_size()),
            self.origin[1],
            self.origin[2],
        )
        v3 = Vector.Vector(
            self.origin[0] + (self.apix[0] * self.x_size()),
            self.origin[1] + (self.apix[1] * self.y_size()),
            self.origin[2],
        )
        v4 = Vector.Vector(
            self.origin[0] + (self.apix[0] * self.x_size()),
            self.origin[1] + (self.apix[1] * self.y_size()),
            self.origin[2] + (self.apix[2] * self.z_size()),
        )
        v5 = Vector.Vector(
            self.origin[0],
            self.origin[1] + (self.apix[0] * self.y_size()),
            self.origin[2],
        )
        v6 = Vector.Vector(
            self.origin[0],
            self.origin[1],
            self.origin[2] + (self.apix[1] * self.z_size()),
        )
        v7 = Vector.Vector(
            self.origin[0],
            self.origin[1] + (self.apix[1] * self.y_size()),
            self.origin[2] + (self.apix[2] * self.z_size()),
        )
        v8 = Vector.Vector(
            self.origin[0] + (self.apix[0] * self.x_size()),
            self.origin[1],
            self.origin[2] + (self.apix[2] * self.z_size())
        )

        v1 = v1.matrix_transform(mat)
        v2 = v2.matrix_transform(mat)
        v3 = v3.matrix_transform(mat)
        v4 = v4.matrix_transform(mat)
        v5 = v5.matrix_transform(mat)
        v6 = v6.matrix_transform(mat)
        v7 = v7.matrix_transform(mat)
        v8 = v8.matrix_transform(mat)

        max_x = 0
        max_y = 0
        max_z = 0
        ltmp = [
            v1,
            v2,
            v3,
            v4,
            v5,
            v6,
            v7,
            v8,
        ]
        for i in range(8):
            for j in range(i, 8):
                if abs(ltmp[i].x - ltmp[j].x) > max_x:
                    max_x = abs(ltmp[i].x - ltmp[j].x)
                if abs(ltmp[i].y - ltmp[j].y) > max_y:
                    max_y = abs(ltmp[i].y - ltmp[j].y)
                if abs(ltmp[i].z - ltmp[j].z) > max_z:
                    max_z = abs(ltmp[i].z - ltmp[j].z)
        output_dimension = Vector.Vector(max_x, max_y, max_z)
        return output_dimension

    def _rotation_offset(
            self,
            mat,
            CoM1,
            CoM2,
    ):
        newCoM = CoM2.matrix_transform(mat)
        offset = CoM1 - newCoM
        return offset

    def rotate_by_matrix(self, mat, CoM):
        """Rotate map around pivot, given by CoM, using a rotation matrix

        Args:
            mat: 3x3 matrix used to rotate map.
            CoM: Rotation pivot, usually the centre of mass around which
                map will be rotated.

        Returns:
            Rotated Map instance
        """
        newCoM = CoM.matrix_transform(mat.T)
        offset = CoM - newCoM
        newMap = self.matrix_transform(
            mat,
            offset.x,
            offset.y,
            offset.z,
        )
        return newMap

    def _matrix_transform_offset(
            self,
            mat,
            shape,
            x=0,
            y=0,
            z=0,
    ):
        newMap = self.copy()
        off_x = float(x / self.apix[0])
        off_y = float(y / self.apix[1])
        off_z = float(z / self.apix[2])
        newMap.fullMap = newMap.fullMap.swapaxes(0, 2)
        newMap.fullMap = affine_transform(
            newMap.fullMap,
            mat,
            offset=(off_x, off_y, off_z),
            output_shape=shape,
            cval=(self.min())
        )
        newMap.fullMap = newMap.fullMap.swapaxes(0, 2)
        return newMap

    def matrix_transform(
            self,
            mat,
            x=0,
            y=0,
            z=0,
    ):
        """" Apply affine transform to the map.

        Arguments:
            mat: Affine 3x3 transformation matrix
            shape: New box dimensions
            x, y, z: Translation in angstroms in respective plane.

        Returns:
            Transformed Map instance
        """
        newMap = self.copy()
        mat = mat.T
        off_x = x / self.apix[0]
        off_y = y / self.apix[1]
        off_z = z / self.apix[2]
        x_o = -self.x_origin() / self.apix[0]
        y_o = -self.y_origin() / self.apix[1]
        z_o = -self.z_origin() / self.apix[2]

        off_x += x_o - mat[0, 0] * x_o - mat[0, 1] * y_o - mat[0, 2] * z_o
        off_y += y_o - mat[1, 0] * x_o - mat[1, 1] * y_o - mat[1, 2] * z_o
        off_z += z_o - mat[2, 0] * x_o - mat[2, 1] * y_o - mat[2, 2] * z_o

        off_x = float(off_x)
        off_y = float(off_y)
        off_z = float(off_z)

        newMap.fullMap = newMap.fullMap.swapaxes(0, 2)
        newMap.fullMap = affine_transform(
            newMap.fullMap,
            mat,
            offset=(off_x, off_y, off_z),
            cval=self.min()
        )
        newMap.fullMap = newMap.fullMap.swapaxes(0, 2)
        return newMap

    def change_origin(self, x_origin, y_origin, z_origin):
        """ Change the origin of the map.

        Arguments:
            x_origin, y_origin, z_origin: New origin co-ordinate.

        Returns:
            Map instance with new origin
        """
        newMap = self.copy()
        newMap.origin = (x_origin, y_origin, z_origin)
        return newMap

    def shift_origin(self, x_shift, y_shift, z_shift):
        """ Shift the Map origin.

        Arguments:
            x_shift, y_shift, z_shift: Shift (in voxels) applied to origin in
                respective plane.

        Returns:
            Map instance with new origin.
        """

        newMap = self.copy()
        newMap.origin = (
            self.origin[0] + x_shift,
            self.origin[1] + y_shift,
            self.origin[2] + z_shift
        )
        return newMap

    def translate(
            self,
            x,
            y,
            z,
    ):
        """ Translate the map.

        Args:
            x, y, z: Translation (in A) applied to the map in respective plane.

        Returns:
            Shifted Map instance
        """
        sh = np.array([
            z / self.apix[2],
            y / self.apix[1],
            x / self.apix[0],
        ])
        newMap = self.copy()
        newMap.fullMap = shift(
            newMap.fullMap,
            sh,
            cval=self.min()
        )
        return newMap

    def origin_change_maps(self, MapRef):
        """ Translate Map such that the origin is moved to the origin of a
        reference Map.

        Args:
            MapRef: Reference Map

        Returns:
            Translated Map instance
        """
        newMap = self.copy()
        origin_shift = [
            y - x for x, y in
            zip(newMap.origin, MapRef.origin)
        ]
        newMap.translate(
            origin_shift[0],
            origin_shift[1],
            origin_shift[2],
        )
        newMap.origin = MapRef.origin[:]
        return newMap

    def threshold_map(self, minDens, maxDens):
        """Create a Map instance containing only density values between the
        specified min and max values.

        Args:
            minDens: Minimum density threshold
            maxDens: Maximum density threshold

        Returns:
            Thresholded Map instance
        """
        newMap1 = self.fullMap.copy()
        newMap1 = newMap1 * (newMap1 < maxDens) * (newMap1 > minDens)
        newMap = self.copy()
        newMap.fullMap = newMap1
        return newMap

    def _find_level(self, vol):
        """
        Get the level corresponding to volume.
        Arguments:
            *vol*
                volume within the contour

        Returns:
            level corresponding to volume
        """
        c1 = self.fullMap.min()
        vol_calc = float(vol) * 2
        it = 0
        flage = 0
        while (vol_calc - float(vol)) / (self.apix.prod()) > 10 and flage == 0:
            mask_array = self.fullMap >= c1
            dens_freq, dens_bin = np.histogram(self.fullMap[mask_array], 1000)
            sum_freq = 0.0
            for i in range(len(dens_freq)):
                sum_freq += dens_freq[-(i + 1)]
                dens_level = dens_bin[-(i + 2)]
                vol_calc = sum_freq*(self.apix.prod())
                if vol_calc > float(vol):
                    sel_level = dens_level
                    it += 1
                    if sel_level <= c1:
                        flage = 1
                    c1 = sel_level
                    if it == 3:
                        flage = 1
                    break
        return sel_level

    def _rotate_interpolate_to_grid(
            self,
            mat,
            gridshape,
            spacing_i,
            spacing_f,
            cort,
            fill=None,
            origin=None
    ):
        """
        rotate a map and interpolate to new grid.

        Arguments:
            *mat*
                rotation matrix
            *gridshape*
                new grid shape (z,y,x)
            *spacing_i*
                initial grid spacing
            *spacing_f*
                new grid spacing
            *cort*
                centre of rotation

        Returns:
            level corresponding to volume
        """
        nz = int(gridshape[0])
        ny = int(gridshape[1])
        nx = int(gridshape[2])
        map_centre = self.centre()
        if origin is None:
            origin = (
                map_centre.x - (nx * spacing_f) / 2.0,
                map_centre.y - (ny * spacing_f) / 2.0,
                map_centre.z - (nz * spacing_f) / 2.0,
            )
        orif = np.array(origin).view(float)  # noqa:F841
        orii = np.array(self.origin).view(float)  # noqa:F841
        nzi = int(self.fullMap.shape[0])  # noqa:F841
        nyi = int(self.fullMap.shape[1])  # noqa:F841
        nxi = int(self.fullMap.shape[2])  # noqa:F841
        si = float(spacing_i)  # noqa:F841
        sf = float(spacing_f)  # noqa:F841
        cor = np.array(cort).astype(float)  # noqa:F841
        new_grid = np.zeros(gridshape, dtype=float)
        if not fill == 0.0:
            new_grid.fill(self.min())
        maparray = self.fullMap.view(float)  # noqa:F841
        # rotation matrix transpose
        matt = (np.array(mat).T).astype(float)  # noqa:F841
        # /*calculate offset*/
        corfx = orif[0]+(nx*sf)/2.0
        corfy = orif[1]+(ny*sf)/2.0
        corfz = orif[2]+(nz*sf)/2.0
        crx = matt[0, 0] * corfx + matt[0, 1] * corfy + matt[0, 2] * corfz
        cry = matt[1, 0] * corfx + matt[1, 1] * corfy + matt[1, 2] * corfz
        crz = matt[2, 0] * corfx + matt[2, 1] * corfy + matt[2, 2] * corfz
        offx = cor[0] - crx
        offy = cor[1] - cry
        offz = cor[2] - crz
        for z in range(nz):
            for y in range(ny):
                for x in range(nx):
                    # /*reverse rotation*/
                    xf = orif[0]+(sf/2.0)+x*sf
                    yf = orif[1]+(sf/2.0)+y*sf
                    zf = orif[2]+(sf/2.0)+z*sf
                    xi = matt[0, 0]*xf + matt[0, 1]*yf + matt[0, 2]*zf
                    yi = matt[1, 0]*xf + matt[1, 1]*yf + matt[1, 2]*zf
                    zi = matt[2, 0]*xf + matt[2, 1]*yf + matt[2, 2]*zf
                    # /*add offset*/
                    xi = xi + offx
                    yi = yi + offy
                    zi = zi + offz
                    # /*array coordinates*/
                    xi = (xi - (orii[0]+(si/2.0)))/si
                    yi = (yi - (orii[1]+(si/2.0)))/si
                    zi = (zi - (orii[2]+(si/2.0)))/si
                    # /*find bounds*/
                    x0 = np.floor(xi)
                    y0 = np.floor(yi)
                    z0 = np.floor(zi)
                    x1 = np.ceil(xi)
                    y1 = np.ceil(yi)
                    z1 = np.ceil(zi)
                    # noqa: E501 /*std::cout << xf << ' ' << xi << ' ' << x0 << ' ' << x1 << ' ' << offx << std::endl*/
                    if (
                            (x0 >= 0 and y0 >= 0 and z0 >= 0) and
                            (x1 < nxi and y1 < nyi and z1 < nzi)
                    ):
                        ma000 = maparray[z0, y0, x0]
                        ma100 = maparray[z1, y0, x0]
                        ma010 = maparray[z0, y1, x0]
                        ma001 = maparray[z0, y0, x1]
                        ma110 = maparray[z1, y1, x0]
                        ma011 = maparray[z0, y1, x1]
                        ma101 = maparray[z1, y0, x1]
                        ma111 = maparray[z1, y1, x1]
                        new_grid[z, y, x] = ma000*(1-(xi-x0))*(1-(yi-y0))*(1-(zi-z0))+ma001*(xi-x0)*(1-(yi-y0))*(1-(zi-z0))+ma010*(1-(xi-x0))*(yi-y0)*(1-(zi-z0))+ma100*(1-(xi-x0))*(1-(yi-y0))*(zi-z0)+ma101*(xi-x0)*(1-(yi-y0))*(zi-z0)+ma110*(1-(xi-x0))*(yi-y0)*(zi-z0)+ma011*(xi-x0)*(yi-y0)*(1-(zi-z0))+ma111*(xi-x0)*(yi-y0)*(zi-z0)  # noqa: E501
        self.fullMap = new_grid
        self.origin = origin

    def _interpolate_to_grid(  # noqa:F811
            self,
            gridshape,
            s,
            ori,
            order_spline=3,
            fill='min'
    ):
        """
        Spline interpolation to a grid.

        Arguments:
            *gridshape*
                shape of new grid array (z,y,x)
            *s*
                new grid spacing
            *ori*
                origin of the new grid
            *order_spine*
                order of the spline used for interpolation

        Returns:
            Interpolated map
        """
        (ox, oy, oz) = (
            self.origin[0],
            self.origin[1],
            self.origin[2],
        )
        (o1x, o1y, o1z) = (
            float(ori[0]),
            float(ori[1]),
            float(ori[2])
        )
        scale = s / self.apix
        offset = (o1x - ox, o1y - oy, o1z - oz)

        new_map_origin = (o1x, o1y, o1z)
        grid_indices = np.indices(gridshape)
        z_ind = grid_indices[0]
        z_ind.ravel()
        y_ind = grid_indices[1]
        y_ind.ravel()
        x_ind = grid_indices[2]
        x_ind.ravel()
        z_ind = ((offset[2]) / self.apix[2]) + scale[2] * z_ind
        y_ind = ((offset[1]) / self.apix[1]) + scale[1] * y_ind
        x_ind = ((offset[0]) / self.apix[0]) + scale[0] * x_ind
        if order_spline > 1:
            filtered_array = spline_filter(self.fullMap, order=order_spline)
        else:
            filtered_array = self.fullMap
        if fill == 'zero':
            fillval = 0.0
        else:
            fillval = self.min()
        new_array = map_coordinates(
            filtered_array,
            [z_ind, y_ind, x_ind],
            cval=fillval,
            order=order_spline,
            prefilter=False,
        )
        new_map = Map(
            new_array.reshape(gridshape),
            new_map_origin,
            s,
            self.filename,
            self.header[:],
        )

        new_map.origin = np.array([o1x, o1y, o1z], dtype=np.float32)
        new_map.apix = s
        return new_map

    def _interpolate_to_grid1(
            self,
            gridshape,
            s,
            ori,
            fill='min',
            bound=False,
    ):
        """
        Spline interpolation to a grid.
        Arguments:

            *gridshape*
                shape of new grid array (z,y,x)
            *s*
                new grid spacing
            *ori*
                origin of the new grid
            *order_spine*
                order of the spline used for interpolation

        Returns:
            interpolated map
        """
        (ox, oy, oz) = (
            self.origin[0],
            self.origin[1],
            self.origin[2],
        )
        (o1x, o1y, o1z) = (
            float(ori[0]),
            float(ori[1]),
            float(ori[2]),
        )
        scale = s / self.apix
        offset = (o1x - ox, o1y - oy, o1z - oz)

        new_map_origin = (o1x, o1y, o1z)

        # axis coordinates of new grid
        z_ind = np.arange(gridshape[0])
        y_ind = np.arange(gridshape[1])
        x_ind = np.arange(gridshape[2])
        # find coordinates relative to old grid
        z_ind = ((offset[2]) / self.apix[2]) + scale[2] * z_ind
        y_ind = ((offset[1]) / self.apix[1]) + scale[1] * y_ind
        x_ind = ((offset[0]) / self.apix[0]) + scale[0] * x_ind
        # get indices of points inside the old grid
        z_mask_ind = (((np.nonzero((z_ind >= 0) & (z_ind < self.fullMap.shape[0] - 1))[0]) * 1).astype(int))  # noqa:E501
        y_mask_ind = ((np.nonzero((y_ind >= 0) & (y_ind < self.fullMap.shape[1]-1))[0])*1).astype(int)  # noqa:E501
        x_mask_ind = ((np.nonzero((x_ind >= 0) & (x_ind < self.fullMap.shape[2]-1))[0])*1).astype(int)  # noqa:E501
        # indices of boundaries
        z_mask_ind1 = np.nonzero(
            (z_ind >= self.fullMap.shape[0]-1) &
            (z_ind < self.fullMap.shape[0])
        )[0]
        y_mask_ind1 = np.nonzero(
            (y_ind >= self.fullMap.shape[1]-1) &
            (y_ind < self.fullMap.shape[1])
        )[0]
        x_mask_ind1 = np.nonzero(
            (x_ind >= self.fullMap.shape[2]-1) &
            (x_ind < self.fullMap.shape[2])
        )[0]
        z_mask_ind0 = np.nonzero(
            (z_ind < 0) & (z_ind > -1)
        )[0]
        y_mask_ind0 = np.nonzero(
            (y_ind < 0) & (y_ind > -1)
        )[0]
        x_mask_ind0 = np.nonzero(
            (x_ind < 0) & (x_ind > -1)
        )[0]
        # searchsorted/floor
        # get the bound int coordinates
        # searchsorted gives right bounds of orig array. substract 1 to get
        # lower bound
        k_z = np.searchsorted(
            np.arange(self.fullMap.shape[0], dtype=float),
            z_ind - 1,
            side='right',
        )
        k_y = np.searchsorted(
            np.arange(self.fullMap.shape[1], dtype=float),
            y_ind - 1,
            side='right',
        )
        k_x = np.searchsorted(
            np.arange(self.fullMap.shape[2], dtype=float),
            x_ind - 1,
            side='right',
        )
        # new_grid
        new_grid = np.zeros((gridshape))
        # extract lower bounds from original grid
        # check coordinate range
        x_grid1 = k_x[x_mask_ind].astype(int)
        y_grid1 = k_y[y_mask_ind].astype(int)
        z_grid1 = k_z[z_mask_ind].astype(int)
        # faster option (array broadcasting - operations on different sizes)
        # indices from orig array
        tmp_grid = np.zeros(
            (
                len(z_grid1),
                len(y_grid1),
                len(x_grid1)
            ),
            dtype=int,
        )
        z_gridL = (tmp_grid + z_grid1[..., np.newaxis, np.newaxis]).flatten()
        y_gridL = (tmp_grid + y_grid1[..., np.newaxis]).flatten()
        x_gridL = (tmp_grid + x_grid1).flatten()
        assert (
                len(z_grid1) == len(z_mask_ind) and
                len(y_grid1) == len(y_mask_ind) and
                len(x_grid1) == len(x_mask_ind)
        )
        # target array indices
        z_grid = (tmp_grid + z_mask_ind[..., np.newaxis, np.newaxis]).flatten()
        y_grid = (tmp_grid + y_mask_ind[..., np.newaxis]).flatten()
        x_grid = (tmp_grid + x_mask_ind).flatten()
        # fill with minimum value/zero
        if not fill == 'zero':
            new_grid.fill(self.min())
        # interpolate
        nx = int(len(x_grid1))  # noqa:F841
        ny = int(len(y_grid1))   # noqa:F841
        nz = int(len(z_grid1))  # noqa:F841
        maparray = self.fullMap.view(float)  # noqa:F841
        xind = x_ind.view(float)  # noqa:F841
        yind = y_ind.view(float)  # noqa:F841
        zind = z_ind.view(float)  # noqa:F841
        # int k,j,i;
        # int k1,j1,i1;
        # for z in range(nz):
        #     for y in range(ny):
        #         for  x in range(nx):
        #             k1 = z_grid1[z]
        #             j1 = y_grid1[y]
        #             i1 = x_grid1[x]
        #             k = z_mask_ind[z]
        #             j = y_mask_ind[y]
        #             i = x_mask_ind[x]
        #             float ma000 = maparray[k1,j1,i1]
        #             float ma100 = maparray[k1+1,j1,i1]
        #             float ma010 = maparray[k1,j1+1,i1]
        #             float ma001 = maparray[k1,j1,i1+1]
        #             float ma110 = maparray[k1+1,j1+1,i1]
        #             float ma011 = maparray[k1,j1+1,i1+1]
        #             float ma101 = maparray[k1+1,j1,i1+1]
        #             float ma111 = maparray[k1+1,j1+1,i1+1]
        #             float indx = xind[i];
        #             float indy = yind[j];
        #             float indz = zind[k];
        # noqa: E501  new_grid[k,j,i] = ma000* (1-(indx-i1))* (1-(indy-j1))* (1-(indz-k1)) +ma001*(indx-i1)*(1-(indy-j1))*(1-(indz-k1))+ma010*(1-(indx-i1))*(indy-j1)*(1-(indz-k1))+ma100*(1-(indx-i1))*(1-(indy-j1))*(indz-k1)+ma101*(indx-i1)*(1-(indy-j1))*(indz-k1)+ma110*(1-(indx-i1))*(indy-j1)*(indz-k1)+ma011*(indx-i1)*(indy-j1)*(1-(indz-k1))+ma111*(indx-i1)*(indy-j1)*(indz-k1);
        new_grid[z_grid, y_grid, x_grid] = (1.-(x_ind[x_grid]-x_gridL))*(1-(y_ind[y_grid]-y_gridL))*(1-(z_ind[z_grid]-z_gridL))*self.fullMap[z_gridL, y_gridL, x_gridL]+self.fullMap[z_gridL, y_gridL, x_gridL+1]*(x_ind[x_grid]-x_gridL)*(1-(y_ind[y_grid]-y_gridL))*(1-(z_ind[z_grid]-z_gridL))+self.fullMap[z_gridL, y_gridL+1, x_gridL]*(1.-(x_ind[x_grid]-x_gridL))*(y_ind[y_grid]-y_gridL)*(1-(z_ind[z_grid]-z_gridL))+self.fullMap[z_gridL+1, y_gridL, x_gridL]*(1.-(x_ind[x_grid]-x_gridL))*(1-(y_ind[y_grid]-y_gridL))*(z_ind[z_grid]-z_gridL)+self.fullMap[z_gridL+1, y_gridL, x_gridL+1]*(x_ind[x_grid]-x_gridL)*(1-(y_ind[y_grid]-y_gridL))*(z_ind[z_grid]-z_gridL)+self.fullMap[z_gridL+1, y_gridL+1, x_gridL]*(1.-(x_ind[x_grid]-x_gridL))*(y_ind[y_grid]-y_gridL)*(z_ind[z_grid]-z_gridL)+self.fullMap[z_gridL, y_gridL+1, x_gridL+1]*(x_ind[x_grid]-x_gridL)*(y_ind[y_grid]-y_gridL)*(1-(z_ind[z_grid]-z_gridL))+self.fullMap[z_gridL+1, y_gridL+1, x_gridL+1]*(x_ind[x_grid]-x_gridL)*(y_ind[y_grid]-y_gridL)*(z_ind[z_grid]-z_gridL)  # noqa:E501

        if bound is True:
            # note that the boundary interpolations are done just along one
            # axis - to save time - not accurate
            # boundary interpolations
            for el in x_mask_ind1:
                new_grid[z_grid, y_grid, el] = (
                        (1 - (x_ind[el] - k_x[el])) *
                        self.fullMap[z_gridL, y_gridL, k_x[el]] +
                        (x_ind[el] - k_x[el]) *
                        self.min()
                )
            for el in y_mask_ind1:
                new_grid[z_grid, el, x_grid] = (
                    (1-(y_ind[el]-k_y[el])) *
                    self.fullMap[z_gridL, k_y[el], x_gridL] +
                    (y_ind[el] - k_y[el]) * self.min()
                )
            for el in z_mask_ind1:
                new_grid[el, y_grid, x_grid] = (
                        (1 - (z_ind[el] - k_z[el])) *
                        self.fullMap[k_z[el], y_gridL, x_gridL] +
                        (z_ind[el] - k_z[el]) * self.min()
                )
            k_x[x_mask_ind0] = -1.
            k_y[y_mask_ind0] = -1.
            k_z[z_mask_ind0] = -1.
            for el in x_mask_ind0:
                new_grid[z_grid, y_grid, el] = (
                    (1 - (x_ind[el] - (-1))) *
                    self.min() +
                    (x_ind[el] - (-1)) *
                    self.fullMap[z_gridL, y_gridL, 0]
                )
            for el in y_mask_ind0:
                new_grid[z_grid, el, x_grid] = (
                    (1 - (y_ind[el] - (-1))) *
                    self.min() +
                    (y_ind[el] - (-1)) *
                    self.fullMap[z_gridL, 0, x_gridL]
                )
            for el in z_mask_ind0:
                new_grid[el, y_grid, x_grid] = (
                    (1-(z_ind[el]-(-1))) *
                    self.min() +
                    (z_ind[el] - (-1)) *
                    self.fullMap[0, y_gridL, x_gridL]
                )

        # interpolate
        new_map = Map(
            new_grid,
            new_map_origin,
            s,
            self.filename,
            self.header[:]
        )

        new_map.origin = (o1x, o1y, o1z)
        new_map.apix = s
        return new_map

    # TODO: this code gives an error when called as it stands,
    # so there must be some inconsistency in it. To be checked
    def _check_overlap(
            c1,
            c2,
            mat,
            cor,
            maxG
    ):
        """
        Check whether transformation of a map overlaps with another.
        Note that for maps with large differences in x,y,z dimensions,
        some non-overlapping boxes may be returned but this is quick way
        to check for overlap without using the grids.

        Arguments:
            *c1*
                box centre of map1
            *c2*
                box centre of map2
            *mat*
                transformation matrix
            *cor*
                centre of rotation
            *maxG*
                maximum of the dimensions of the maps, in Angstrom

        Returns:
            True/False
        """
        mat1 = np.matrix([
            [c2[0]],
            [c2[1]],
            [c2[2]],
        ])
        mat2 = np.matrix([
            mat[0][:-1],
            mat[1][:-1],
            mat[2][:-1]
        ])
        c2_t = mat2 * mat1
        c2_t[0] = c2_t[0] + mat[0][-1] + (float(cor[0]) - c2_t[0])
        c2_t[1] = c2_t[1] + mat[1][-1] + (float(cor[1]) - c2_t[1])
        c2_t[2] = c2_t[2] + mat[2][-1] + (float(cor[2]) - c2_t[2])
        dist = math.sqrt(
            math.pow(c2_t[0] - c1[0], 2) +
            math.pow(c2_t[1] - c1[1], 2) +
            math.pow(c2_t[2] - c1[2], 2)
        )
        if dist < maxG / 2.0:
            return True
        else:
            return False

    def _mask_contour(self, thr, mar=0.0):
        """
        Mask backgound beyond contour (in place)
        """
        if mar != 0.0:  # TODO: NEVER CHECK FOR EQUALITY WITH FLOATS
            level = thr - (mar * self.fullMap.std())
        else:
            level = thr
        minVal = self.min()
        a = np.ma.masked_less(self.fullMap, level, copy=True)
        self.fullMap = np.ma.filled(a, minVal)

    def _make_fourier_shell(self, fill=1.0):
        """
        For a given grid, make a grid with sampling frequencies as distance
        from centre
        Returns:
          grid with sampling frequencies
        """
        rad_z = (
            np.arange(
                np.floor(self.z_size() / 2.0) * -1,
                np.ceil(self.z_size() / 2.0)
            ) / float(np.floor(self.z_size()))
        )
        rad_y = (
            np.arange(
                np.floor(self.y_size() / 2.0) * -1,
                np.ceil(self.y_size()/2.0)
            ) / float(np.floor(self.y_size()))
        )
        rad_x = (
            np.arange(
                np.floor(self.x_size()/2.0) * -1,
                np.ceil(self.x_size()/2.0)
            ) / float(np.floor(self.x_size()))
        )

        rad_x = rad_x**2
        rad_y = rad_y**2
        rad_z = rad_z**2

        dist = np.sqrt(rad_z[:, None, None] + rad_y[:, None] + rad_x)
        return dist

    def _get_maskArray(self, densValue):
        """
        ADDED by APP to use with SSCCC score
        """
        mask_array = np.ma.masked_less_equal(self.fullMap, densValue)
        return np.ma.getmask(mask_array)

    def _get_maskMap(self, maskArray):
        """
        ADDED by APP to use with SSCCC score
        """
        newMap = self.copy()
        newMap.fullMap *= 0
        masked_newMAP = np.ma.masked_array(
            self.fullMap,
            mask=maskArray,
            fill_value=0
        )
        newMap.fullMap = masked_newMAP.filled()
        return newMap

    def make_bin_map(self, cutoff):
        """ Make a binarised version of Map, where values above cutoff = 1 and
        below cutoff = 0.

        Args:
            cutoff: Cutoff density value

        Returns:
            Binarised Map instance
        """
        # TODO: get rid of the copy here
        binMap = self.copy()
        binMap.fullMap = (self.fullMap > float(cutoff)) * -1
        return binMap

    def _make_clash_map(self, apix=np.ones(3)):
        """
        NOTE: NEEED TO BE CHECKED.

        Return an empty Map instance with set Angstrom per pixel sampling
        (default is 1)

        Returns:
            new Map instance
        """
        grid = np.zeros(
            (
                int(self.box_size()[0] * self.apix[0] / apix[0]),
                int(self.box_size()[1] * self.apix[1] / apix[1]),
                int(self.box_size()[2] * self.apix[2] / apix[2])
            )
        )
        clashMap = self.copy()
        clashMap.fullMap = grid
        clashMap.apix = apix
        return clashMap

    def resample_by_apix(self, new_apix):
        """ Resample the map to a new pixel size.

        Args:
            new_apix: New Angstrom per pixel sampling

        Returns:
            Resampled Map instance
        """
        new_map = self.copy()
        apix_ratio = self.apix/new_apix
        new_map.fullMap = resample(
            new_map.fullMap,
            self.z_size() * apix_ratio[2],
            axis=0
        )
        new_map.fullMap = resample(
            new_map.fullMap,
            self.y_size() * apix_ratio[1],
            axis=1
        )
        new_map.fullMap = resample(
            new_map.fullMap,
            self.x_size() * apix_ratio[0],
            axis=2
        )
        new_map.apix = (self.apix * self.box_size()) / new_map.box_size()
        return new_map

    def resample_by_box_size(self, new_box_size):
        """ Resample the map based on new box size.

        Args:
            new_box_size: New box dimensions in (Z, Y, X) format

        Returns:
            Resampled Map instance
        """
        new_map = self.copy()
        new_map.fullMap = resample(new_map.fullMap, new_box_size[0], axis=0)
        new_map.fullMap = resample(new_map.fullMap, new_box_size[1], axis=1)
        new_map.fullMap = resample(new_map.fullMap, new_box_size[2], axis=2)
        new_map.apix = (self.apix * self.box_size()[2]) / new_box_size[2]
        return new_map

    def fourier_transform(self):
        """ Apply Fourier transform on the density map.

        The zero frequency component is in the centre of the spectrum.

        Returns:
            Fourier Transformed Map instance.
        """
        new_map = self.copy()
        new_map.fullMap = fftshift(fftn(self.fullMap))
        return new_map

    def laplace_filtered(self):
        """ Laplacian filter Map.

        Returns:
            Laplacian filtered Map instance
        """
        new_map = self.copy()
        new_map.fullMap = laplace(self.fullMap)
        return new_map

    def get_vectors(self):
        """ Retrieve all non-zero density points as Vector instances.

        Returns:
            Numpy array:
                An array of 2-tuple (
                :class:`Vector Instance <TEMPy.math.vector.Vector>` with
                respect to origin, and density value)
        """
        a = []
        for z in range(len(self.fullMap)):
            for y in range(len(self.fullMap[z])):
                for x in range(len(self.fullMap[z][y])):
                    if self.fullMap[z][y][x] != 0:
                        a.append(
                            (
                                Vector.Vector(
                                    (x * self.apix[0]) + self.origin[0],
                                    (y * self.apix[1]) + self.origin[1],
                                    (z * self.apix[2]) + self.origin[2],
                                ),
                                self.fullMap[z][y][x]
                            )
                        )
        return np.array(a)

    def get_line_between_points(self, point1, point2):
        """Return an array of float values representing a line of density values
        between two points on the map.

        Args:
            point1, point2: Vector instances defining one of the line to
                extract density values.

        Returns:
            Numpy array:
                Array of density values along the defined line.
       """
        v1 = point1.minus(
            Vector.Vector(
                self.origin[0],
                self.origin[1],
                self.origin[2],
            )
        ).times(1.0 / self.apix)
        v2 = point2.minus(
            Vector.Vector(
                self.origin[0],
                self.origin[1],
                self.origin[2],
            )
        ).times(1.0 / self.apix)
        v3 = v2.minus(v1)
        noOfPoints = int(round(2 * v3.mod() / self.apix))
        points = []
        for x in range(0, noOfPoints+1):
            p = v1.plus(v3.times(float(x) / noOfPoints))
            points.append(self.fullMap[p.z][p.y][p.x])
        return np.array(points)

    def _get_com_threshold(self, c):
        """
        Return Vector instance of the centre of mass of the map.
        """
        newmap = self.copy()
        binmap = self.fullMap > float(c)
        newmap.fullMap = binmap * self.fullMap

        total_x_moment = 0.0
        total_y_moment = 0.0
        total_z_moment = 0.0
        total_mass = 0.0
        min_mass = newmap.min()
        vectorMap = np.argwhere(newmap.fullMap)
        for v in vectorMap:
            m = newmap.fullMap[v[0]][v[1]][v[2]] + min_mass
            total_mass += m
            total_x_moment += m * (self.origin[0] + v[2] * self.apix[0])
            total_y_moment += m * (self.origin[1] + v[1] * self.apix[1])
            total_z_moment += m * (self.origin[2] + v[0] * self.apix[2])
        x_CoM = total_x_moment / total_mass
        y_CoM = total_y_moment / total_mass
        z_CoM = total_z_moment / total_mass
        return Vector.Vector(x_CoM, y_CoM, z_CoM)

    def get_com(self):
        """
        Returns:
            the centre of mass as a
            :class:`Vector instance <TEMPy.math.vector.Vector>`
        """
        total_x_moment = 0.0
        total_y_moment = 0.0
        total_z_moment = 0.0
        total_mass = 0.0
        min_mass = self.min()
        vectorMap = self.get_vectors()
        for v in vectorMap:
            m = v[1] + min_mass
            total_mass += m
            total_x_moment += m * v[0].x
            total_y_moment += m * v[0].y
            total_z_moment += m * v[0].z
        x_CoM = total_x_moment / total_mass
        y_CoM = total_y_moment / total_mass
        z_CoM = total_z_moment / total_mass
        return Vector.Vector(x_CoM, y_CoM, z_CoM)

    def pixel_centre(self):
        """
        Returns:
            :class:`Vector instance <TEMPy.math.vector.Vector>` of the centre
            of the map in pixels.
        """
        x_centre = self.x_size() / 2
        y_centre = self.y_size() / 2
        z_centre = self.z_size() / 2
        return Vector.Vector(x_centre, y_centre, z_centre)

    def centre(self):
        """
        Returns:
            :class:`Vector instance <TEMPy.math.vector.Vector>` of the centre
            of the map in Angstroms.
        """
        x_centre = self.origin[0] + (self.apix[0] * self.x_size() / 2)
        y_centre = self.origin[1] + (self.apix[1] * self.y_size() / 2)
        z_centre = self.origin[2] + (self.apix[2] * self.z_size() / 2)
        return Vector.Vector(x_centre, y_centre, z_centre)

    def mean(self):
        """
        Returns:
            Mean density value of map.
        """
        return self.fullMap.mean()

    def median(self):
        """
        Returns:
            Median density value of map.
        """
        return np.median(self.fullMap)

    def std(self):
        """
        Returns:
            Standard deviation of density values in map.
        """
        return self.fullMap.std()

    def min(self):
        """
        Returns:
            Minimum density value of the map.
        """
        return self.fullMap.min()

    def max(self):
        """
        Returns:
            Maximum density value of the map.
        """
        return self.fullMap.max()

    def vectorise_point(
            self,
            x,
            y,
            z
    ):
        """Get a Vector instance for a specific voxel coordinate (index) of the
        map.

        Args:
            x, y, z: Co-ordinate of the density point to be vectorised.

        Returns:
            :class:`Vector instance <TEMPy.math.vector.Vector>` for the point,
            in angstrom units, relative to the origin.
        """
        v_x = (self.apix[0] * x) + self.origin[0]
        v_y = (self.apix[1] * y) + self.origin[1]
        v_z = (self.apix[2] * z) + self.origin[2]
        return Vector.Vector(v_x, v_y, v_z)

    def get_significant_points(self):
        """ Retrieve all points with a density greater than one standard
        deviation above the mean.

        Returns:
            Numpy array:
                An array of 4-tuple (indices of the voxels in z, y, x format
                and density value)
        """
        sig_points = []
        boo = self.fullMap > (self.fullMap.mean() + self.fullMap.std())
        for z in range(self.z_size()):
            for y in range(self.y_size()):
                for x in range(self.x_size()):
                    if boo[z][y][x]:
                        sig_points.append(
                            np.array([z, y, x, self.fullMap[z][y][x]])
                        )
        return np.array(sig_points)

    def _get_random_significant_pairs(self, amount):
        """
        Return an array of tuple pairs of significant points randomly chosen
        from 'get_significant_points' function.
        For use with the DCCF and DLSF scoring functions.

        Arguments:
            *amount*
                number of significant point pairs to return.
        """
        sig_points = self.get_significant_points()
        sig_pairs = []
        size = len(sig_points)
        for r in range(amount):
            fst = sig_points[randrange(size)]
            snd = sig_points[randrange(size)]
            new_value = np.array(
                [
                    fst[0],
                    fst[1],
                    fst[2],
                    snd[0],
                    snd[1],
                    snd[2],
                    fst[3] - snd[3],
                ]
            )
            sig_pairs.append(new_value)
        return np.array(sig_pairs)

    def makeKDTree(self, minDens, maxDens):
        """ Make a k-dimensional tree for points in the Map within specified
        density thresholds.

        The KD-Tree can be used for quick nearest neighbour look-ups.

        Args:
            minDens: Minimum density value to include in k-dimensional tree.
            maxDens: Maximum density value to include in k-dimensional tree.

        Returns:
            Scipy KDTree containing all relevant points.
        """
        maplist = self.get_pos(minDens, maxDens)
        if len(maplist) != 0:
            return KDTree(maplist)

    def get_pos(self, minDens, maxDens):
        """Find the index for all voxels in the Map whose density values fall
        within the specified thresholds.

        Args:
            minDens: Minimum density threshold.
            maxDens: Maximum density threshold.

        Returns:
            An array of 3-tuples (indices of the voxels in x,y,z format)
        """
        a = []
        for z in range(len(self.fullMap)):
            for y in range(len(self.fullMap[z])):
                for x in range(len(self.fullMap[z][y])):
                    if (
                            (self.fullMap[z][y][x] > minDens) and
                            (self.fullMap[z][y][x] < maxDens)
                    ):
                        a.append((x, y, z))
        return np.array(a)

    def _get_normal_vector(self, points):
        arr = points.view(int)  # noqa:F841
        vecnorm = np.zeros((len(points), 3), dtype=float)
        nps = len(points)  # noqa:F841
        xsize = int(self.x_size())  # noqa:F841
        ysize = int(self.y_size())  # noqa:F841
        zsize = int(self.z_size())  # noqa:F841
        mat = self.fullMap.view(float)  # noqa:F841

        for v in range(len(points)):
            x = arr[v, 2]
            y = arr[v, 1]
            z = arr[v, 0]
            xa = ya = za = 0.0
            flag = 0
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    for k in range(z-1, z+2):
                        if (i == x) and (j == y) and (z == k):
                            continue
                        elif (i < 0) or (j < 0) or (k < 0):
                            continue
                        elif (i > xsize-1) or (j > ysize-1) or (k > zsize-1):
                            continue
                        else:
                            if mat[k, j, i] > mat[z, y, x]:
                                # sum of unit vectors
                                mod = math.sqrt((i-x)**2+(j-y)**2+(k-z)**2)
                                if mod != 0.0:
                                    xa += (i-x)/mod
                                    ya += (j-y)/mod
                                    za += (k-z)/mod
                                flag = 1
                            elif mat[k, j, i] < mat[z, y, x]:
                                flag = 1
            if flag != 0:
                # unit average
                mod = math.sqrt(xa**2+ya**2+za**2)
                if mod != 0.0:
                    vecnorm[v, 0] = xa/mod
                    vecnorm[v, 1] = ya/mod
                    vecnorm[v, 2] = za/mod
                else:
                    vecnorm[v, 0] = 0.0
                    vecnorm[v, 1] = 0.0
                    vecnorm[v, 2] = 0.0
        return vecnorm

    def get_normal_vector(
            self,
            x_pos,
            y_pos,
            z_pos,
    ):
        """Calculate the normal vector at the point specified.

        Point calculated using 3SOM algorithm used by Ceulemans H. & Russell
        R.B. (2004).

        Args:
            x_pos, y_pos, z_pos: Voxel in map on which to calculate normal
                vector.
        Returns:
            :class:`Vector instance <TEMPy.math.vector.Vector>`:
                The Normal vector at the point specified.
        """
        flag = 0
        internal_vecs = []
        for x in range(x_pos - 1, x_pos + 2):
            for y in range(y_pos - 1, y_pos + 2):
                for z in range(z_pos - 1, z_pos + 2):
                    if (x_pos, y_pos, z_pos) == (x, y, z):
                        pass
                    elif x < 0 or y < 0 or z < 0:
                        pass
                    elif (
                            x > self.x_size()-1 or
                            y > self.y_size()-1 or
                            z > self.z_size()-1
                    ):
                        pass
                    else:
                        if (
                                self.fullMap[z][y][x] >
                                self.fullMap[z_pos][y_pos][x_pos]
                        ):
                            internal_vecs.append(
                                Vector.Vector(
                                    x - x_pos,
                                    y - y_pos,
                                    z - z_pos
                                ).unit()
                            )
                            flag = 1
                        elif (
                                self.fullMap[z][y][x] <
                                self.fullMap[z_pos][y_pos][x_pos]
                        ):
                            flag = 1

        sub_vector = Vector.Vector(0, 0, 0)
        for v in internal_vecs:
            sub_vector = sub_vector + v
        if len(internal_vecs) == 0 and flag == 0:
            return Vector.Vector(-9.0, -9.0, -9.0)
        return sub_vector.unit()

    def represent_normal_vectors(self, min_threshold, max_threshold):
        """ Create a Structure instance representing normal vectors of density
        points specified.

        Args:
            min_threshold, max_threshold: Minimum/maximum values to include
                in normal vector representation.
        Returns:
            Structure Instance
        """
        atomList = []
        m = self.copy()
        print(m.origin)
        for x in range(1, (m.box_size()[0]-1)):
            for y in range(1, (m.box_size()[1]-1)):
                for z in range(1, (m.box_size()[2]-1)):
                    if (
                            m.fullMap[z][y][x] > min_threshold and
                            m.fullMap[z][y][x] < max_threshold
                    ):
                        n_vec = m.get_normal_vector(x, y, z)
                        n_vec = n_vec.unit()
                        pos_vec = Vector.Vector(
                            (x * m.apix[0]) + m.origin[0],
                            (y * m.apix[1]) + m.origin[1],
                            (z * m.apix[2]) + m.origin[2],
                        )
                        a = Atom('H', [pos_vec.x, pos_vec.y, pos_vec.z])

                        x = pos_vec.x + n_vec.x
                        y = pos_vec.y + n_vec.y
                        z = pos_vec.z + n_vec.z
                        b = Atom('H', [x, y, z])

                        x = pos_vec.x + 2 * n_vec.x
                        y = pos_vec.y + 2 * n_vec.y
                        z = pos_vec.z + 2 * n_vec.z
                        c = Atom('H', [x, y, z])
                        atomList.append(a)
                        atomList.append(b)
                        atomList.append(c)
        try:
            s = BioPy_Structure(atomList)
        except ZeroDivisionError:
            return atomList
        s.renumber_atoms()
        return s

    def get_point_map(self, min_thr, percentage=0.2):
        """ Calculates the amount of points to use for the
        :meth:`Normal vector score <TEMPy.protein.scoring_functions.ScoringFunctions.normal_vector_score>`
        and :meth:`Chamfer distance <TEMPy.protein.scoring_functions.ScoringFunctions.chamfer_distance>`
        score.

        Minimum number of returned points is 100.

        Arguments:
            min_thr: Minimum threshold, recommended to get value by running
                the :meth:`get_primary_boundary <TEMPy.maps.em_map.Mapget_primary_boundary>`
                on target map.
            percentage: Percentage of the protein volume.

        Returns:
            Number of points for Chamfer and Normal Vector scores.
        """
        new_map = self.copy()
        prot_size = 1. * (new_map.fullMap > min_thr).sum()
        points = max(100, round(prot_size * percentage))
        return points

    def get_primary_boundary(
            self,
            molWeight,
            low,
            high,
            vol_factor=1.21,
    ):
        """Estimates a threshold value to create an envelope that encapsulates
        a volume expected for a protein with a certain molecular size.

        The estimation uses a recursive algorithm, so some parameters can be
        set as approximate guesses.

        NOTE: when used to calculated the NV score this value should be
        calculated for the experimental map.

        Args:
            molWeight: molecular weight of all molecules in model. Can be
                calculated using
                :meth:`get_prot_mass_from_atoms <TEMPy.protein.prot_rep_biopy.get_prot_mass_from_atoms>`.
            low: Minimum threshold to consider. Can be a crude first guess
                e.g. :meth:`Map.min <TEMPy.maps.em_map.Map.min`
            high: Minimum threshold to consider. Can be a crude first guess
                e.g. :meth:`Map.min <TEMPy.maps.em_map.Map.min`
            vol_factor: Approximate value for cubic Angstroms per Dalton for
                globular proteins. Value used in Chimera
                (Petterson et al, 2004), taken from Harpaz 1994, is 1.21.
                Other recommended volume factor are 1.5 (1.1-1.9) cubic
                Angstroms per Dalton in EMAN Volume/mass conversions assume a
                density of 1.35 g/ml (0.81 Da/A3) (~1.23A3/Da)

        Returns:
            float:
                Primary boundary density value
        """
        new_map = self.copy()
        if np.sum(new_map.fullMap == low) > new_map.fullMap.size / 10:
            all_dens = new_map.fullMap.flatten()
            all_dens = set(all_dens)
            all_dens = sorted(all_dens)
            l_ind = all_dens.index(low)
            low = all_dens[l_ind+1]
        if high - low < 0.0000002 or high < low:
            est_weight = int(
                np.sum(new_map.fullMap > low) *
                new_map.apix.prod() /
                (vol_factor * 1000)
            )
            print(
                'Exact molecular weight cannot be found. Approx. weight of '
                + str(est_weight) + ' used instead.'
            )
            return low
        thr = low + (high - low) / 2
        this_weight = int(
            np.sum(new_map.fullMap > thr) *
            new_map.apix.prod() /
            (vol_factor * 1000)
        )
        if this_weight == int(molWeight):
            return thr
        elif this_weight > molWeight:
            return new_map.get_primary_boundary(molWeight, thr, high)
        elif this_weight < molWeight:
            return new_map.get_primary_boundary(molWeight, low, thr)

    def _get_second_boundary_outward(
            self,
            primary_boundary,
            noOfPoints,
            low,
            high,
            err_percent=1,
    ):
        """
        PRIVATE FUNCTION to calculate the second bound density value.
        Searching from primary boundary outward.
        For a given boundary value, it calculates the second bound density
        value such that a specified number of points whose density values fall
        between the defined boundaries. Uses recursive algorithm.
        Arguments:
           *primary_boundary*
               primary threshold, normally given by get_primary_boundary method
               based on protein molecular weight.
           *noOfPoints*
               Number of points to use in the normal vector score - try
               first with 10% (maybe 5%better) of the number of points in the
               map ( round((self.map_size())*0.1)
           *low, high*
               minimum and maximum values between which the threshold will be
               taken. low should be equal to the value returned by the
               get_primary_boundary() method and high is the maximum density
               values in map.
           *err_percent*
                 default value of 1. Allowed to find a secondary boundary that
                 includes a 1% error.

        Returns:
             outward secondary boundary density value

        """
        if high - low < 0.0000002 or high < low:
            print(
                'Non optimal number of pixels to match. Try changing this '
                'value or increasing the size of err_percent '
            )
            return 1j

        thr = low + (high - low) / 2
        this_no_of_points = np.sum(
            (self.fullMap < thr) * (self.fullMap > primary_boundary)
        )
        if abs(this_no_of_points - noOfPoints) < err_percent * noOfPoints/100.:
            return thr
        elif this_no_of_points < noOfPoints:
            return self._get_second_boundary_outward(
                primary_boundary,
                noOfPoints,
                thr,
                high
            )
        elif this_no_of_points > noOfPoints:
            return self._get_second_boundary_outward(
                primary_boundary,
                noOfPoints,
                low,
                thr,
            )

    def _get_second_boundary_inward(
            self,
            primary_boundary,
            noOfPoints,
            low,
            high,
            err_percent=1
    ):
        """
        PRIVATE FUNCTION to calculate the second bound density value.
        Searching from primary boundary inward.
        For a given boundary value, it calculates the second bound density
        value such that a specified number of points whose density values fall
        between the defined boundaries. Uses recursive algorithm.

        Arguments:
            *primary_boundary*
                primary threshold, normally given by get_primary_boundary
                method based on protein molecular weight.
            *noOfPoints*
                Number of points to use in the normal vector score - try first
                with 10% (maybe 5%better) of the number of points in the map
                ( round((self.map_size())*0.1)
            *low, high*
                minimum and maximum values between which the threshold will be
                taken. low should be equal to the value returned by the
                get_primary_boundary() method and high is the maximum density
                values in map.
            *err_percent*
                default value of 1. Allowed to find a secondary boundary that
                includes a 1% error.

        Returns:
             outward secondary boundary density value
            """
        if high - low < 0.0000002 or high < low:
            print(
                'Non optimal number of pixels to match. Try changing this'
                'value or increasing the size of err_percent '
            )
            return 1j

        thr = high - (high - low) / 2
        this_no_of_points = np.sum(
            (self.fullMap < thr) * (self.fullMap > primary_boundary)
        )
        if abs(this_no_of_points - noOfPoints) < err_percent * noOfPoints/100.:
            return thr
        elif this_no_of_points < noOfPoints:
            return self._get_second_boundary_inward(
                primary_boundary,
                noOfPoints,
                thr,
                high,
            )
        elif this_no_of_points > noOfPoints:
            return self._get_second_boundary_inward(
                primary_boundary,
                noOfPoints,
                low,
                thr,
            )

    def get_second_boundary(
            self,
            primary_boundary,
            noOfPoints,
            low,
            high,
            err_percent=1,
    ):
        """
        Calculate the second bound density value. For a given boundary value,
        it calculates the second bound density value such that a specified
        number of points whose density values fall between the defined
        boundaries. Uses recursive algorithm.

        Arguments:
            *primary_boundary*
                primary threshold, normally given by get_primary_boundary
                method based on protein molecular weight.
            *noOfPoints*
                Number of points to use in the normal vector score - try
                first with 10% (maybe 5%better) of the number of points in
                the map ( round((self.map_size())*0.1)
            *low, high*
                minimum and maximum values between which the threshold will be
                taken.
                low should be equal to the value returned by the
                get_primary_boundary() method and high is the maximum density
                values in map.
            *err_percent*
                default value of 1. Allowed to find a secondary boundary that
                includes a 1% error.

        Returns:
            secondary boundary density value
        """
        bou = self._get_second_boundary_outward(
            primary_boundary,
            noOfPoints,
            low,
            high,
            err_percent,
        )
        if bou == 1j:
            bou = self._get_second_boundary_inward(
                primary_boundary,
                noOfPoints,
                low,
                high,
                err_percent,
            )
        return bou

    def _shrink_map(self, sd=2.):
        pass

    def _write_to_xplor_file(self, xplorFileName):
        """
        OBSOLETE PRIVATE FUNCTION

        xplorFileName = name of file to write to. Note that this function
        does not automatically append a .xplor suffix.
        """
        xplor = '\n 1 !NTITLE\n'
        xplor += 'REMARKS '+'"' + xplorFileName + '"' + '    written by ME!\n'
        xplor += (
                self._pad_grid_line_no(self.z_size()) +
                self._pad_grid_line_no(0) +
                self._pad_grid_line_no(self.z_size()-1) +
                self._pad_grid_line_no(self.y_size()) +
                self._pad_grid_line_no(0) +
                self._pad_grid_line_no(self.y_size()-1) +
                self._pad_grid_line_no(self.x_size()) +
                self._pad_grid_line_no(0) +
                self._pad_grid_line_no(self.x_size()-1) + '\n'
        )

        xplor += (
                self._convert_point_to_string(self.apix[2] * self.z_size()) +
                self._convert_point_to_string(self.apix[1] * self.y_size()) +
                self._convert_point_to_string(self.apix[0] * self.x_size())
        )

        xplor += (
                self._convert_point_to_string(90.0) +
                self._convert_point_to_string(90.0) +
                self._convert_point_to_string(90.0) + '\n'
        )
        xplor += 'ZYX\n'
        flatList = self.fullMap.flatten()
        blockSize = self.z_size() * self.y_size()
        blockNo = 0
        offset = 0
        for point in range(len(flatList)):
            if point - offset % 6 == 0 and point % blockSize != 0:
                xplor += '\n'
            if point % blockSize == 0:
                xplor += '\n' + self._pad_grid_line_no(blockNo) + '\n'
                blockNo += 1
                offset = point % 6
            xplor += self._convert_point_to_string(np.real(flatList[point]))
        xplor += '\n   -9999'
        f = open(xplorFileName, 'w')
        f.write(xplor)
        f.close()

    def _write_to_situs_file(self, situsFileName):
        """
        One day I will do this.
        """
        pass

    def old_write_to_MRC_file(self, mrcfilename, imod=False):
        """ Write out Map instance as an MRC file

        Old implementation that uses Python write(filename, 'wb') to write
        binary data. Extended header not saved using this implementation.

        Arguments:
            mrcfilename: Filename for the output mrc file
        """
        h = self.update_header(binarise=True)
        maparray = np.array(self.fullMap, dtype='float32')
        f = open(mrcfilename, 'wb')
        f.write(h)
        f.write(maparray.tostring())
        f.close()

    def write_to_MRC_file(self, mrcfilename, overwrite=True):
        """ Write out Map instance as an MRC file

        Uses `mrcfile <https://mrcfile.readthedocs.io/en/latest/usage_guide.html>`_
        library for file writing.

        Arguments:
            mrcfilename: Filename for the output mrc file
        """
        label = 'Created by TEMPy on: ' + str(datetime.date.today())
        fullMap_f32 = self.fullMap.astype('float32')

        with mrcfile.new(mrcfilename, overwrite=overwrite) as mrc:
            mrc.set_data(fullMap_f32)

            # Write out modern MRC files which prefer origin over
            # nstart fields.
            mrc.header.nxstart = 0
            mrc.header.nystart = 0
            mrc.header.nzstart = 0

            # These are determined by density array
            mrc.header.mx = self.x_size()
            mrc.header.my = self.y_size()
            mrc.header.mz = self.z_size()

            # TEMPy should produce maps which have x,y,z ordering
            mrc.header.mapc = 1
            mrc.header.mapr = 2
            mrc.header.maps = 3

            mrc.header.cellb.alpha = 90
            mrc.header.cellb.beta = 90
            mrc.header.cellb.gamma = 90

            mrc.header.ispg = self.header[22]
            mrc.header.extra1 = self.header[24]
            mrc.header.extra2 = self.header[27]

            mrc.header.origin.x = self.origin[0]
            mrc.header.origin.y = self.origin[1]
            mrc.header.origin.z = self.origin[2]

            mrc.header.label[0] = label

            mrc.voxel_size = tuple(self.apix)

            mrc.header.exttyp = self.header[25]
            mrc.set_extended_header(np.array(self.ext_header))

    def update_header(self, binarise=False):
        """ Updates all entries in :code:`Map.header`.

        Args:
            binarse: If True, returns binary version of map header data.
                Used in old MRC writing function.

        Returns:
            Binary version of :code:`Map.header` if :code:`binarise == True`
        """
        nx = np.int32(self.x_size())
        ny = np.int32(self.y_size())
        nz = np.int32(self.z_size())
        mode = np.int32(2)
        nxstart = 0
        nystart = 0
        nzstart = 0

        mx = nx
        my = ny
        mz = nz
        xlen = np.float32(nx * self.apix[0])
        ylen = np.float32(ny * self.apix[1])
        zlen = np.float32(nz * self.apix[2])
        alpha = np.int32(90)
        beta = np.int32(90)
        gamma = np.int32(90)
        mapc = np.int32(1)
        mapr = np.int32(2)
        maps = np.int32(3)
        amin = np.float32(self.min())
        amax = np.float32(self.max())
        amean = np.float32(self.mean())
        ispg = np.int32(0)
        if len(self.header) > 24:
            ispg = np.int32(self.header[22])
        nsymbt = np.int32(0)
        extra = b'\x00'*10
        xorigin = np.float32(self.origin[0])
        yorigin = np.float32(self.origin[1])
        zorigin = np.float32(self.origin[2])
        mapword = b'MAP '
        if sys.byteorder == 'little':
            byteorder = 0x00004444
        else:
            byteorder = 0x11110000
        rms = np.float32(self.std())
        nlabels = np.int32(1)
        label0 = (
            b'Created by TEMpy on: ' +
            str(datetime.date.today()).encode('ascii') +
            b'\x00'*49
        )
        otherlabels = b'\x00'*720

        self.header = [
            nx,
            ny,
            nz,
            mode,
            nxstart,
            nystart,
            nzstart,
            mx,
            my,
            mz,
            xlen,
            ylen,
            zlen,
            alpha,
            beta,
            gamma,
            mapc,
            mapr,
            maps,
            amin,
            amax,
            amean,
            ispg,
            nsymbt,
            extra,
            xorigin,
            yorigin,
            zorigin,
            mapword,
            byteorder,
            rms,
            nlabels,
            label0,
            otherlabels,
        ]

        if binarise:
            fm_string = '=10l6f3l3f2l100s3f4slfl80s720s'
            return binary.pack(fm_string, *self.header)

    def _pad_grid_line_no(self, no):
        """
        Private function to help write data to map files.
        """
        s = str(no)
        spaces = ''
        for x in range(8-len(s)):
            spaces += ' '
        s = spaces + s
        return s

    def _convert_point_to_string(self, point):
        """
        Private function to help write data to map files.
        """
        exp = 0
        sign = ''
        if abs(point) < 0.0001:
            point = 0.0
        if point >= 0:
            sign = '+'
        else:
            sign = '-'
        while abs(point) >= 10.0:
            point /= 10.0
            exp += 1
        pointString = str(point)
        if len(pointString) < 7:
            for x in range(len(pointString), 7):
                pointString += '0'
        elif len(pointString) > 7:
            pointString = pointString[:7]
        pointString += 'E' + sign + '0' + str(exp)
        return ' ' + pointString

    def _get_component_volumes(
            self,
            struct,
            apix,
            blurrer,
    ):
        """
        Private function for check on Map instance.
        Return a a list containing the volume of the individual components
        based on a grid with voxel size set to apix

        Arguments:
            *struct*
                Structure object containing one or more chains.
            *apix*
                voxel size of the grid.
            *blurrer*
                Instance of a StructureBlurrer class.

        Returns:
            Return a a list containing the volume of the individual components
        """
        mapCoM = self.get_com()
        ssplit = struct.split_into_chains()
        temp_grid = self._make_clash_map(apix)

        overlay_maplist = []
        cvol = []
        for x in ssplit:
            tx = mapCoM[0] - x.CoM[0]
            ty = mapCoM[1] - x.CoM[1]
            tz = mapCoM[2] - x.CoM[2]
            x.translate(tx, ty, tz)
            overlay_maplist.append(
                blurrer.make_atom_overlay_map1(temp_grid, x)
            )
        for y in overlay_maplist:
            cvol.append(y.fullMap.sum() * (apix.prod()))
        return cvol

    def map_rotate_by_axis_angle(
            self,
            x,
            y,
            z,
            angle,
            CoM,
            rad=False,
    ):
        """Rotate Map instance around pivot point.

        Arguments:
            angle: Angle (in radians if rad == True, else in degrees) of
                rotation
            x,y,z: Axis to rotate about, ie. x,y,z =  0,0,1 rotates the Map
                round the xy-plane.
            CoM: Point around which map will be rotated.

        Returns:
            Rotated Map instance
        """
        m = Vector.axis_angle_to_matrix(
            x,
            y,
            z,
            angle,
            rad,
        )
        newCoM = CoM.matrix_transform(m.T)
        offset = CoM - newCoM

        newMap = self.matrix_transform(
            m,
            offset.x,
            offset.y,
            offset.z,
        )
        return newMap
