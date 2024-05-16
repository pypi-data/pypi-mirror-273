
import copy
import functools
import os
import sys

import numpy as np
from scipy.ndimage import (
    generic_filter,
    map_coordinates,
    measurements,
)

try:
    import TEMPy.math.vector as Vector
    TEMPy_flag = True
except ImportError:
    TEMPy_flag = False

try:
    import mrcfile
    mrcfile_flag = True
except ImportError:
    mrcfile_flag = False


class TEMPyException(Exception):
    """ Custom Exception for TEMPy import """
    pass


def TEMPycheck(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if TEMPy_flag:
            raise TEMPyException(
                """
                TEMPy required for this function\n
                Cannot import TEMPy!
                """
            )
        else:
            return func(self, *args, **kwargs)
    return wrapper


class MapEdit(object):

    def __init__(self, mapobject, datacopy=True):
        if type(mapobject) is MapEdit:
            if not datacopy:
                self.__dict__ = mapobject.__dict__.copy()
            else:
                self.__dict__ = copy.deepcopy(mapobject.__dict__.copy())
        else:
            super(MapEdit, self).__init__()
            # map data and header details
            # add other attributes?
            self.mrc = mapobject
            self.class_name = self.mrc.__class__.__name__
            if datacopy:
                self.reinitialize(inplace=False)
            else:
                self.reinitialize(inplace=True)

    def shape(self):
        return self.fullMap.shape

    def x_origin(self):
        """
         x-coordinate of the origin.
        """
        return self.origin[0]

    def y_origin(self):
        """
        y-coordinate of the origin.
        """
        return self.origin[1]

    def z_origin(self):
        """
        z-coordinate of the origin.
        """
        return self.origin[2]

    def box_size(self):
        """
        size of the map array, in ZYX format.
        """
        return self.fullMap.shape

    def x_size(self):
        """
        size of the map array in x direction.
        """
        return self.fullMap.shape[2]

    def y_size(self):
        """
        size of the map array in y direction.
        """
        return self.fullMap.shape[1]

    def z_size(self):
        """
        size of the map array in z direction.
        """
        return self.fullMap.shape[0]

    def min(self):
        return np.amin(self.fullMap)

    def max(self):
        return np.amax(self.fullMap)

    def std(self):
        return np.std(self.fullMap)

    def copy(self, deep=True, detach=True):
        '''
        Copy contents to a new object
        '''
        # create MapEdit object
        copymap = MapEdit(self.mrc)

        # detach from initial mrc mapfile
        if detach:
            copymap.mrc = None
        # copy data and header
        copymap.origin = copy.deepcopy(self.origin)

        if deep:
            copymap.fullMap = self.fullMap.copy()
        else:
            copymap.fullMap = self.fullMap

        copymap.apix = copy.deepcopy(self.apix)
        copymap.dim = copy.deepcopy(self.dim)

        return copymap

    def data_copy(self):
        """
        Copy data (not to modify inplace)
        """
        if self.class_name == 'MrcFile':
            self.fullMap = self.mrc.data.copy()
        elif self.class_name == 'Map':
            self.fullMap = self.mrc.fullMap.copy()

    def reinitialize_data(self, inplace=False):
        """
        Initialize or re-initialize data
        """
        if inplace:
            if self.class_name == 'MrcFile':
                self.fullMap = self.mrc.data
            elif self.class_name == 'Map':
                self.fullMap = self.mrc.fullMap
        else:
            self.data_copy()

    def reinitialize_header(self):
        """
        Initialize or re-initialize header
        """
        if self.class_name == 'MrcFile':
            self.origin = self.mrc.header.origin.item()
            self.apix = self.mrc.voxel_size.item()
            self.dim = self.mrc.header.cella.item()
        elif self.class_name == 'Map':
            self.origin = tuple(self.mrc.origin)
            self.apix = (
                round(self.mrc.header[10] / self.mrc.header[7], 2),
                round(self.mrc.header[11] / self.mrc.header[8], 2),
                round(self.mrc.header[12] / self.mrc.header[9], 2)
            )
            self.dim = (
                self.x_size() * self.apix[0],
                self.y_size() * self.apix[1],
                self.z_size() * self.apix[2]
            )
        else:
            sys.exit(
                "Only MrcFile and TEMPY Map objects currently supported"
            )

    def reinitialize(self, inplace=False):
        """
        Initialize/re-initialize data/header
        """
        self.reinitialize_data(inplace=inplace)
        self.reinitialize_header()

    def update_header(self):
        """
        Update map header records to current values
        """
        if self.class_name == 'MrcFile':
            # origin
            self.mrc.header.origin.x = self.origin[0]
            self.mrc.header.origin.y = self.origin[1]
            self.mrc.header.origin.z = self.origin[2]
            # dimensions
            self.mrc.header.cella.x = self.dim[0]
            self.mrc.header.cella.y = self.dim[1]
            self.mrc.header.cella.z = self.dim[2]
            # voxel_size
            if type(self.apix) is float:
                self.mrc.voxel_size = (
                            self.apix, self.apix, self.apix)
            else:
                self.mrc.voxel_size = self.apix
        elif self.class_name == 'Map':
            # origin
            self.mrc.origin[0] = self.origin[0]
            self.mrc.origin[1] = self.origin[1]
            self.mrc.origin[2] = self.origin[2]
            # tempy takes a single voxel_size - should be x,y,z in new version
            self.mrc.apix = self.apix[0]

    @staticmethod
    def compare_tuple(tuple1, tuple2):
        for val1, val2 in zip(tuple1, tuple2):
            if type(val2) is float:
                if round(val1, 2) != round(val2, 2):
                    return False
            else:
                if val1 != val2:
                    return False
        return True

    def update_data(self):
        """
        Update data array
        """
        if self.class_name == 'MrcFile':
            if compare_tuple(self.fullMap.shape, self.mrc.data.shape):  # noqa:501 TODO: Fix
                self.mrc.data[:] = self.fullMap
            else:
                self.mrc.set_data(self.fullMap)
        elif self.class_name == 'Map':
            self.mrc.fullMap[:] = self.fullMap

    def set_data_header(self):
        """
        Update data and header with current values
        """
        self.update_data()
        self.update_header()

    def close(self):
        if self.class_name == 'MrcFile':
            self.mrc.close()
        elif self.class_name == 'Map':
            self.mrc.fullMap = None

    def update_newmap_header(self, newmap):
        """
        Update newmap header to current values
        """
        if newmap.__class__.__name__ == 'MrcFile':
            # origin
            newmap.header.origin.x = self.origin[0]
            newmap.header.origin.y = self.origin[1]
            newmap.header.origin.z = self.origin[2]
            # dimensions
            newmap.header.cella.x = self.dim[0]
            newmap.header.cella.y = self.dim[1]
            newmap.header.cella.z = self.dim[2]
            # voxel_size
            newmap.voxel_size = self.apix
        elif newmap.__class__.__name__ == 'Map':
            # corigin
            newmap.origin[0] = self.origin[0]
            newmap.origin[1] = self.origin[1]
            newmap.origin[2] = self.origin[2]
            # cvoxel_size
            newmap.apix = self.apix[0]

    def update_newmap_data(self, newmap):
        """
        Update new map data array
        """
        if newmap.__class__.__name__ == 'MrcFile':
            if str(self.fullMap.dtype) == 'float64':
                newmap.set_data(
                    self.fullMap.astype(
                        'float32',
                        copy=False
                    )
                )
            else:
                newmap.set_data(self.fullMap)
        elif newmap.__class__.__name__ == 'Map':
            newmap.fullMap[:] = self.fullMap

    def set_newmap_data_header(self, newmap):
        """
        Update data and header with current values
        """
        self.update_newmap_data(newmap)
        self.update_newmap_header(newmap)

    def set_dim_apix(self, apix):
        """
        Set dimensions (Angstroms) given voxel size
        """
        self.apix = apix
        self.dim = (
            self.x_size() * self.apix[0],
            self.y_size() * self.apix[1],
            self.z_size() * self.apix[2]
        )

    def set_apix_dim(self, dim):
        """
        Set voxel size given dimensions (Angstroms) of Grid
        """
        self.dim = dim
        self.apix = (
            np.around(self.dim[0] / self.x_size(), decimals=3),
            np.around(self.dim[1] / self.y_size(), decimals=3),
            np.around(self.dim[2] / self.z_size(), decimals=3)
        )

    def set_apix_tempy(self):
        """
        Set apix to single float value for using TEMPy functions
        """
        if isinstance(self.apix, tuple):
            if self.apix[0] == self.apix[1] == self.apix[2]:
                self.apix = self.apix[0]
            else:
                self.downsample_apix(max(self.apix), inplace=True)
                self.apix = self.apix[0]

    def set_apix_as_tuple(self):
        if not isinstance(self.apix, tuple):
            self.apix = (self.apix, self.apix, self.apix)

    def fix_origin(self):
        """
        Set origin record based on nstart if non-zero
        """
        if self.origin[0] == 0. and self.origin[1] == 0. and \
                self.origin[2] == 0.:
            if self.class_name == 'MrcFile':
                if self.mrc.header.nxstart != 0 or \
                    self.mrc.header.nystart != 0 or \
                        self.mrc.header.nzstart != 0:
                    if isinstance(self.apix, tuple):
                        # origin
                        self.origin = (
                                        self.mrc.header.nxstart * self.apix[0],
                                        self.mrc.header.nystart * self.apix[1],
                                        self.mrc.header.nzstart * self.apix[2])
                    else:
                        self.origin = (
                                        self.mrc.header.nxstart * self.apix,
                                        self.mrc.header.nystart * self.apix,
                                        self.mrc.header.nzstart * self.apix)
            elif self.class_name == 'Map':
                nstart_index = self.mrc.header[4:7]
                if nstart_index[0] != 0 or \
                    nstart_index[1] != 0 or \
                        nstart_index[2] != 0:
                    if isinstance(self.apix, tuple):
                        # origin
                        self.origin = (
                                        nstart_index[0] * self.apix[0],
                                        nstart_index[1] * self.apix[1],
                                        nstart_index[2] * self.apix[2])
                    else:
                        self.origin[0] = (
                                            nstart_index[0] * self.apix,
                                            nstart_index[1] * self.apix,
                                            nstart_index[2] * self.apix)

    def crop_box(
            self,
            contour=None,
            factor_sigma=0.0,
            ext=None,
            inplace=False,
            nd=3
    ):
        """
        Crop a map based on a threshold
        Arguments:
            *contour*
                map threshold
            *factor_sigma*
                factor to relax threshold
            *ext*
                padding to keep
        """
        # self.reinitialize_data(inplace)
        # crop based on the give n contour and factor_sigma
        if not factor_sigma == 0.0:
            minval = (
                float(contour) -
                (float(factor_sigma) * self.fullMap.std())
            )
        else:
            minval = float(contour)
        if ext is None:
            ext = 10

        map_data = self.fullMap
        list_indices = []
        for i in range(nd):
            ct1 = 0
            try:
                while (np.nanmax(map_data[ct1]) < minval):
                    ct1 += 1
            except IndexError:
                pass

            ct2 = 0
            try:
                while (np.nanmax(map_data[-1-ct2]) < minval):
                    ct2 += 1
            except IndexError:
                pass
            map_data = np.transpose(map_data, (2, 0, 1))
            # TODO, substracting 1 is not necessary?
            list_indices.append([ct1 - 1, ct2 - 1])

        zs, ze = (
            max(0, list_indices[0][0] - ext),
            min(
                self.fullMap.shape[0] - list_indices[0][1] + ext,
                self.fullMap.shape[0]
            )
        )
        # x axis
        xs, xe = (
            max(0, list_indices[1][0] - ext),
            min(
                self.fullMap.shape[2] - list_indices[1][1] + ext,
                self.fullMap.shape[2]
            )
        )
        # y axis
        ys, ye = (
            max(0, list_indices[2][0] - ext),
            min(
                self.fullMap.shape[1]-list_indices[2][1] + ext,
                self.fullMap.shape[1])
            )

        ox = self.origin[0] + xs * self.apix[0]
        oy = self.origin[1] + ys * self.apix[1]
        oz = self.origin[2] + zs * self.apix[2]

        # cropped data, save a copy to get a contiguous memory block
        # delete the reference
        del map_data
        if inplace:
            # new origin
            self.origin = (ox, oy, oz)
            self.fullMap = self.fullMap[zs:ze, ys:ye, xs:xe]
            # set dimensions for new shape
            self.set_dim_apix(self.apix)
        else:
            newmap = self.copy(deep=False)
            newmap.origin = (ox, oy, oz)
            newmap.fullMap = np.copy(self.fullMap[zs:ze, ys:ye, xs:xe])
            newmap.set_dim_apix(self.apix)
            return newmap

    def pad_map(
            self,
            nx,
            ny,
            nz,
            inplace=False
    ):
        """
        Pad a map (in place) with specified increments along each dimension.
        Arguments:
            *nx,ny,nz*
               Number of slices to pad in each dimension.
        Return:
            new Map instance
        """
        gridshape = (
            self.fullMap.shape[0] + nz,
            self.fullMap.shape[1] + ny,
            self.fullMap.shape[2] + nx
        )
        input_dtype = str(self.fullMap.dtype)
        new_array = np.zeros(gridshape, dtype=input_dtype)
        new_array.fill(self.fullMap.min())

        oldshape = self.fullMap.shape
        indz, indy, indx = (
            int(round((gridshape[0] - oldshape[0]) / 2.)),
            int(round((gridshape[1] - oldshape[1]) / 2.)),
            int(round((gridshape[2] - oldshape[2]) / 2.))
        )
        new_array[
            indz:indz + oldshape[0],
            indy:indy + oldshape[1],
            indx:indx + oldshape[2]
        ][:] = self.fullMap

        if inplace:
            self.fullMap = new_array
            self.origin = (
                self.origin[0] - self.apix[0] * indx,
                self.origin[1] - self.apix[1] * indy,
                self.origin[2] - self.apix[2] * indz
            )
            self.set_dim_apix(self.apix)
        else:
            newmap = self.copy(deep=False)
            newmap.fullMap = new_array
            newmap.origin = (
                self.origin[0] - self.apix[0] * indx,
                self.origin[1] - self.apix[1] * indy,
                self.origin[2] - self.apix[2] * indz
            )
            newmap.set_dim_apix(self.apix)
            return newmap

    def interpolate_to_grid(
            self,
            new_gridshape,
            new_spacing,
            new_origin,
            inplace=False
    ):
        """
        Interpolate to a new map grid given new shape, spacing and origin
        """
        if not isinstance(new_spacing, tuple):
            new_spacing = (new_spacing, new_spacing, new_spacing)
        ox, oy, oz = (self.origin[0], self.origin[1], self.origin[2])
        o1x, o1y, o1z = (
            float(new_origin[0]),
            float(new_origin[1]),
            float(new_origin[2])
        )
        scale = (
            float(new_spacing[0]) / self.apix[0],
            float(new_spacing[1]) / self.apix[1],
            float(new_spacing[2]) / self.apix[2]
        )
        offset = (o1x-ox, o1y-oy, o1z-oz)

        gridshape = new_gridshape
        grid_indices = np.indices(gridshape, dtype=np.uint16)
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
            mode='nearest',
        )

        if inplace:
            self.fullMap = new_array.reshape(gridshape)
            self.origin = (o1x, o1y, o1z)
            self.set_dim_apix(new_spacing)
        else:
            newmap = self.copy(deep=False)
            newmap.fullMap = new_array.reshape(gridshape)
            newmap.origin = (o1x, o1y, o1z)
            newmap.set_dim_apix(new_spacing)
            return newmap

    def downsample_apix(self, new_spacing, inplace=False):
        """
        Downsample map based on voxel size
        """
        apix_ratio = (
            self.apix[0]/new_spacing,
            self.apix[1]/new_spacing,
            self.apix[2]/new_spacing
        )
        grid_shape = (
            int(round(self.z_size() * apix_ratio[2])),
            int(round(self.y_size() * apix_ratio[1])),
            int(round(self.x_size() * apix_ratio[0]))
        )

        if inplace:
            self.interpolate_to_grid(
                                    grid_shape,
                                    new_spacing,
                                    self.origin,
                                    inplace=inplace
                                    )
        else:
            return self.interpolate_to_grid(
                                    grid_shape,
                                    new_spacing,
                                    self.origin,
                                    inplace=inplace
                                    )

    def shift_density(self, offset, inplace=False):
        """
        Shift density given an offset
        """
        if inplace:
            self.fullMap[:] = self.fullMap + float(offset)
        else:
            newmap = self.copy()
            newmap.fullMap[:] = self.fullMap + float(offset)
            return newmap

    def threshold_map(self, contour=0.0, inplace=False):
        """
        Threshold map at a given contour.
        """
        if inplace:
            self.fullMap[:] = self.fullMap * (self.fullMap > contour)
        else:
            newmap = self.copy()
            newmap.fullMap[:] = self.fullMap * (self.fullMap > contour)
            return newmap

    def apply_mask(self, mask_array=None, inplace=False):
        """
        Mask map with a binary mask.
        """
        if mask_array is not None:
            if inplace:
                self.fullMap[:] = self.fullMap * mask_array
            else:
                newmap = self.copy()
                newmap.fullMap[:] = self.fullMap * mask_array
                return newmap

    def get_sigma_map(self, window=5):
        newmap = self.copy(deep=False)
        footprint_sph = self.make_spherical_footprint(window)
        newmap.fullMap = generic_filter(
            newmap.fullMap,
            np.std,
            footprint=footprint_sph,
            mode='constant',
            cval=0.0
        )
        return newmap

    def find_background_peak(self, arr, iter=2):
        """
        Function taken from ccpem TEMPy - written by Agnel
        """

        lbin = np.amin(arr)
        rbin = np.amax(arr)
        ave = np.mean(arr)
        sigma = np.std(arr)
        for it in range(iter):
            if it == 0:
                data = arr
            else:
                data = arr[(arr >= lbin) & (arr <= rbin)]

            freq, bins = np.histogram(data, 100)
            ind = np.nonzero(freq == np.amax(freq))[0]
            peak = None
            for i in ind:
                val = (bins[i] + bins[i + 1]) / 2.
                if val < float(ave) + float(sigma):
                    peak = val
                    lbin = bins[i]
                    rbin = bins[i + 1]
            if peak is None:
                break
        return peak, ave

    def peak_density(self):
        """

        Find background peak and sigma (for values beyond the peak)

        Return:
            peak, average and sigma (beyond peak)

        """
        peak, ave = self.find_background_peak(self.fullMap)
        if peak is None:
            peak = ave
        sigma1 = None
        if peak is not None:
            mask_array = self.fullMap[self.fullMap > peak]
            mask_array[:] = mask_array - peak
            mask_array[:] = np.square(mask_array)
            sigma1 = np.mean(mask_array)
            sigma1 = np.sqrt(sigma1)
        else:
            peak = ave
            sigma1 = np.mean(self.fullMap)  # not tested
        del mask_array

        return peak, ave, sigma1

    def calculate_map_contour(self, sigma_factor=1.5):
        zeropeak, ave, sigma = self.peak_density()
        if zeropeak is not None:
            contour = zeropeak + (sigma_factor * sigma)
        else:
            contour = 0.0
        return contour

    def find_level(self, vol):
        """
        Get the level corresponding to volume.
        Arguments:
            *vol*
                volume within the contour
        Return:
            level corresponding to volume
        """

        c1 = self.fullMap.min()
        vol_calc = float(vol) * 2
        it = 0
        flage = 0
        while (
                (vol_calc - float(vol)) /
                (self.apix[0] * self.apix[1] * self.apix[2]) > 10
                and flage == 0
        ):
            mask_array = self.fullMap >= c1
            dens_freq, dens_bin = histogram(self.fullMap[mask_array], 1000)  # noqa: F821,E501 TODO: Fix
            sum_freq = 0.0
            for i in range(len(dens_freq)):
                sum_freq += dens_freq[-(i + 1)]
                dens_level = dens_bin[-(i + 2)]
                vol_calc = sum_freq * (
                        self.apix[0] * self.apix[1] * self.apix[2]
                )
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

    def map_digitize(
                    self,
                    contour=None,
                    nbins=10,
                    left=False,
                    right=True,
                    inplace=False
                    ):
        """
        Divide density into bins (store bin indices in grid)
            Arguments:
                *contour*
                    map threshold
                    None by default
                *nbins*
                    number of bins
                *right*
                    right closed?
                    False by default
        """
        try:
            from numpy import digitize
        except ImportError as err:
            if not err.args:
                err.args = ('',)
            err.args += ('Numpy Digitize missing, try v1.8 or above',)
            raise

        # self.reinitialize_data(inplace)
        if contour is None:
            contour = np.amin(self.fullMap)
        bins = []
        step = (self.fullMap.max() - float(contour))/nbins

        # > contour value
        if left:
            ini = float(contour) - (0.000001*step)
        elif right:
            ini = float(contour)
        else:
            ini = float(contour) + (0.000001*step)

        bins.append(ini)
        for ii in range(1, nbins + 1):
            bins.append(float(contour) + ii * step)
        if bins[-1] < self.fullMap.max():
            bins = bins[:-1]
            bins.append(self.fullMap.max())

        if not inplace:
            newmap = self.copy()

        for z in range(len(self.fullMap)):
            for y in range(len(self.fullMap[z])):
                if inplace:
                    self.fullMap[z][y] = digitize(
                                            self.fullMap[z][y],
                                            bins,
                                            right=right
                                            )
                else:
                    newmap.fullMap[z][y] = digitize(
                                            self.fullMap[z][y],
                                            bins,
                                            right=right
                                            )
        if not inplace:
            return newmap

    def move_map(self, newori, inplace=False):
        if inplace:
            self.origin = newori
        else:
            newmap = self.copy(deep=False)
            newmap.origin = newori
            return newmap

    def grid_footprint(self):
        """
        Generate a footprint array for local neighborhood (6 faces)
        """
        a = np.zeros((3, 3, 3))
        a[1, 1, 1] = 1
        a[0, 1, 1] = 1
        a[1, 0, 1] = 1
        a[1, 1, 0] = 1
        a[2, 1, 1] = 1
        a[1, 2, 1] = 1
        a[1, 1, 2] = 1

        return a

    def make_spherical_footprint(self, diameter):
        """
        Get spherical footprint of a given diameter
        """
        rad_z = np.arange(
            np.floor(diameter / 2.0) * -1,
            np.ceil(diameter / 2.0)
        )
        rad_y = np.arange(
            np.floor(diameter / 2.0) * -1,
            np.ceil(diameter / 2.0)
        )
        rad_x = np.arange(
            np.floor(diameter / 2.0) * -1,
            np.ceil(diameter / 2.0)
        )

        rad_x = rad_x**2
        rad_y = rad_y**2
        rad_z = rad_z**2
        dist = np.sqrt(rad_z[:, None, None] + rad_y[:, None] + rad_x)
        return (dist <= np.floor(diameter / 2.0)) * 1

    def size_patches(self, contour):
        """
        Get sizes or size distribution of isolated densities
            Arguments:
                *contour*
                    map threshold
            Return:
                array of sizes
        """
        fp = self.grid_footprint()
        binmap = self.fullMap > float(contour)
        label_array, labels = measurements.label(
            self.fullMap * binmap,
            structure=fp
        )
        sizes = measurements.sum(binmap, label_array, range(labels + 1))
        return sizes

    @TEMPycheck
    def box_transform(self, mat):
        """
        Calculate box dimensions after rotation

        Arguments:
                *mat*
                        Input rotation matrix
        Return:
                new box shape
        """
        # Box corners
        v1 = Vector.Vector(
            self.origin[0],
            self.origin[1],
            self.origin[2]
        )
        v2 = Vector.Vector(
            self.origin[0] + (self.apix[0] * self.x_size()),
            self.origin[1],
            self.origin[2]
        )
        v3 = Vector.Vector(
            self.origin[0] + (self.apix[0] * self.x_size()),
            self.origin[1] + (self.apix[1] * self.y_size()),
            self.origin[2]
        )
        v4 = Vector.Vector(
            self.origin[0] + (self.apix[0] * self.x_size()),
            self.origin[1] + (self.apix[1] * self.y_size()),
            self.origin[2] + (self.apix[2] * self.z_size())
        )
        v5 = Vector.Vector(
            self.origin[0],
            self.origin[1] + (self.apix[1] * self.y_size()),
            self.origin[2]
        )
        v6 = Vector.Vector(
            self.origin[0],
            self.origin[1],
            self.origin[2] + (self.apix[2] * self.z_size())
        )
        v7 = Vector.Vector(
            self.origin[0],
            self.origin[1] + (self.apix[1] * self.y_size()),
            self.origin[2] + (self.apix[2] * self.z_size())
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
        ltmp = [v1, v2, v3, v4, v5, v6, v7, v8]
        # New ouput shape
        for i in range(8):
            for j in range(i, 8):
                if abs(ltmp[i].x - ltmp[j].x) > max_x:
                    max_x = abs(ltmp[i].x - ltmp[j].x)
                if abs(ltmp[i].y - ltmp[j].y) > max_y:
                    max_y = abs(ltmp[i].y - ltmp[j].y)
                if abs(ltmp[i].z - ltmp[j].z) > max_z:
                    max_z = abs(ltmp[i].z - ltmp[j].z)
        output_dimension = (max_x, max_y, max_z)
        return output_dimension

    @staticmethod
    def fancy_index_as_slices(values, indices):
        out = np.array([])
        vals = values.ravel()
        inds = indices.ravel()
        s = np.sort(np.where(inds))
        v_sorted = vals[s][:]
        i_sorted = inds[s][:]
        searches = np.searchsorted(
            i_sorted,
            np.arange(0, i_sorted[-1] + 2)
        )
        for i in range(len(searches) - 1):
            st = searches[i]
            nd = searches[i + 1]
            out.append(v_sorted[st:nd])
        return np.array(out)


if __name__ == '__main__':
    mapfile = '/Users/agnel/data/map_model/6oej/emd_3908.map'
    mrcobj = mrcfile.open(mapfile, mode='r+')
    mrcmap = MapEdit(mrcobj)
    ftfilter = mrcmap.tanh_lowpass(0.1, fall=0.25)
    map_name = os.path.basename(os.path.splitext(mapfile)[0])
    map_dir = os.path.dirname(os.path.abspath(mapfile))
    newmap = mrcfile.new(
        os.path.join(map_dir, map_name + '_modified.mrc'),
        overwrite=True
    )
    mrcmap.mrcfile_newmap_data_update(newmap)
    mrcmap.mrcfile_newmap_header_update(newmap)
    newmap.close()
