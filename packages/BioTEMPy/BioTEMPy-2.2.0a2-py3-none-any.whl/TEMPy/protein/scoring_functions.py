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

import itertools
import math
import sys
import gc
import warnings

import numpy as np
from scipy.fftpack import (
    ifftn,
    fftshift,
    ifftshift,
)
from scipy.spatial import KDTree
from scipy import stats
import pyfftw

from TEMPy.protein.structure_blurrer import StructureBlurrer
from TEMPy.protein.rigid_body_parser import RBParser
from TEMPy.math import vector
from TEMPy.maps.em_map import Map
from TEMPy.math import fourier


def _MI_C_helper(
        arr1,
        arr2,
        layers1=20,
        layers2=20,
        N=0,
        lc1=0.0,
        lc2=0.0):
    ly1 = int(layers1)  # noqa:F841
    ly2 = int(layers2)  # noqa:F841
    # input 3D arrays
    nz = int(arr1.shape[0])  # noqa:F841
    ny = int(arr1.shape[1])  # noqa:F841
    nx = int(arr1.shape[2])  # noqa:F841
    # min and max to set left and right bound
    ma1 = np.ma.masked_less_equal(arr1, lc1, copy=False)
    min1 = float(ma1.min())
    max1 = float(ma1.max())

    ma2 = np.ma.masked_less_equal(arr2, lc2, copy=False)
    min2 = float(ma2.min())
    max2 = float(ma2.max())

    min1 = float(min1 - ((max1 - min1) / layers1) * 0.0001)
    min2 = float(min2 - ((max2 - min2) / layers2) * 0.0001)
    # bin width
    step1 = (max1-min1) / float(layers1)  # noqa:F841
    step2 = (max2-min2) / float(layers2)  # noqa:F841
    # histogram freq in bins
    freq1 = np.zeros(layers1, dtype=float)  # noqa:F841
    freq2 = np.zeros(layers2, dtype=float)  # noqa:F841
    comb_freq = np.zeros((layers1, layers2), dtype=float)  # noqa:F841

    s1 = 0
    s2 = 0
    p1 = 0.0
    p2 = 0.0
    pcomb = 0.0
    Hxy = 0.0
    Hy = 0.0
    Hx = 0.0
    # /*long index = 0;
    # long indexend = nz * ny * nx;
    # while (index < indexend){
    #     va1  = arr1[index];
    #     va2 = arr2[index];*/
    # /* use 3d array loop */
    for z in range(nz):
        for y in range(ny):
            for x in range(nx):
                va1 = arr1[z, y, x] ** 2
                va2 = arr2[z, y, x] ** 2
                i = 0
                for i in range(ly1):
                    if (
                            (va1 > (min1 + i * step1)) and
                            (va1 <= (min1 + (i + 1) * step1))
                    ):
                        freq1[i] += 1.0
                        s1 += 1
                        break
                if i == ly1:
                    i = i-1
                for j in range(ly2):
                    if (
                            (va2 > (min2+j * step2)) and
                            (va2 <= (min2+(j+1) * step2))
                    ):
                        freq2[j] += 1.0
                        s2 += 1
                        comb_freq[i, j] += 1.0
                        break
    for i in range(ly1):
        p1 = freq1[i] / s1
        # /*std::cout << s1 << ' ' << s2 << std::endl;*/
        for j in range(ly2):
            p2 = freq2[j] / s2
            pcomb = comb_freq[i, j] / s1
            if (pcomb != 0.0):
                Hxy += (-pcomb*np.log2(pcomb))
            if ((i == 0) and (p2 != 0.0)):
                Hy += (-p2*np.log2(p2))
        if (p1 != 0.0):
            Hx += (-p1*np.log2(p1))
    P, e1, e2 = np.histogram2d(ma1.ravel(), ma2.ravel(), bins=20)
    P /= P.sum()
    p1 = P.sum(axis=0)
    p2 = P.sum(axis=1)
    p1 = p1[p1 > 0]
    p2 = p2[p1 > 0]
    P = P[P > 0]
    Hx_ = (-p1 * np.log2(p1)).sum()
    Hy_ = (-p2 * np.log2(p2)).sum()
    Hxy_ = (-P * np.log2(P)).sum()
    t2 = Hx_ + Hy_ - Hxy_  # noqa: F841
    import pdb
    pdb.set_trace()
    # /*std::cout << Hxy << ' ' << Hx << ' ' << Hy << ' ' << std::endl;*/
    if (N == 1):
        if (Hxy != 0.0):
            return (Hx+Hy)/Hxy
        else:
            return 0.0
    else:
        return Hx+Hy-Hxy


def _MI_C_helper_new(
        arr1,
        arr2,
        layers1=20,
        layers2=20,
        N=0,
        lc1=0.0,
        lc2=0.0):
    ma1 = np.ma.masked_less_equal(arr1, lc1, copy=False)
    ma2 = np.ma.masked_less_equal(arr2, lc2, copy=False)

    P, xe, ye = np.histogram2d(
        ma1.ravel(),
        ma2.ravel(),
        bins=(layers1, layers2)
    )
    P /= P.sum()
    p1 = P.sum(axis=0)
    p2 = P.sum(axis=1)
    p1 = p1[p1 > 0]
    p2 = p2[p2 > 0]
    P = P[P > 0]
    Hx_ = (-p1 * np.log2(p1)).sum()
    Hy_ = (-p2 * np.log2(p2)).sum()
    Hxy_ = (-P * np.log2(P)).sum()
    return Hx_ + Hy_ - Hxy_


class ScoringFunctions:
    """Class implementing most TEMPy scoring functions.

    Args:
        None.

    Returns:
        A ScoringFunction object. See
    """
    def __init__(self):
        warnings.warn("ScoringFunctions class is deprecated, call scoring "
            "functions directly using TEMPy.protein.scores module.",
            category=DeprecationWarning, stacklevel=1)
        pass

    def _overlap_map_samebox(self, map1, map2):
        """ Is this function used somewhere - candidate for deletion?

        volume overlap within 2 maps with same box size

        Return:
           % of overlap
        """
        binmap1 = map1.fullMap > 0.0
        binmap2 = map2.fullMap > 0.0
        mask_array = (binmap1 * binmap2) > 0.0
        return[
            np.count_nonzero(binmap1),
            np.count_nonzero(binmap2),
            np.count_nonzero(mask_array),
            mask_array.size
        ]

    def calculate_overlap_scores(
                                self,
                                map_target,
                                map_probe,
                                map_target_threshold,
                                map_probe_threshold
                                ):
        """
            mask maps with 2 cut-off map_target_threshold and
            map_probe_threshold (vol thr.)

            return:
            fraction of overlap with respect to target, with respect to
            probe and with respect to the total (union)
        """
        if not self.mapComparison(map_target, map_probe):
            raise ValueError(
                f"Could not calculate scores for input maps with pixel sizes {map_target.apix}, {map_probe.apix},"
                f" shapes {map_target.box_size()}, {map_probe.box_size()} and "
                f"origins {map_target.origin}, {map_probe.origin}."
            )
        binmap1 = map_target.fullMap > float(map_target_threshold)
        binmap2 = map_probe.fullMap > float(map_probe_threshold)
        mask_array = (binmap1 * binmap2) > 0

        size1 = np.sum(binmap1)
        size2 = np.sum(binmap2)
        return (
            float(np.sum(mask_array)) / size1,
            float(np.sum(mask_array)) / size2,
            float(np.sum(mask_array)) / (size1 + size2),
        )

    def _overlap_map_array(
            self,
            map_target,
            map_target_threshold,
            map_probe,
            map_probe_threshold,
    ):
        """Helper function for mutual information calculation.

        Masks maps using unique cutoff for each (map_target_threshold and
        map_probe_threshold) and returns a final mask which is True where
        both maps are above their respective thresholds.

        Args:
            map_target, map_probe: Input Map instance
            map_target_threshold, map_probe_threshold: Threshold used to mask
            respective map instance

        Returns:
            mask_array: Mask which is true where both maps are above their
            respective thresholds.
        """
        binmap1 = map_target.fullMap > float(map_target_threshold)
        binmap2 = map_probe.fullMap > float(map_probe_threshold)
        mask_array = (binmap1 * binmap2) > 0
        return mask_array

    def calculate_map_threshold(self, map_target):
        """Calculates map threshold as mean value + (2 * map standard deviation)

        Args:
            map_target: Map instance

        Returns:
            float: Threshold value
        """
        # NOTE: MOVE TO TEMPy.maps.em_map.Map??
        try:
            peak, ave, sigma = map_target._peak_density()
            vol_threshold = float(ave) + (2.0 * float(sigma))
        except Exception:
            if len(map_target.header) == 0:
                amean = map_target.mean()
                rms = map_target.std()
                vol_threshold = float(amean) + (1.5 * float(rms))
            else:
                amean = map_target.mean()
                rms = map_target.std()
                vol_threshold = float(amean) + (1.5 * float(rms))
        return vol_threshold

    def mapComparison(self, map_target, map_probe):
        """
        Checks if properties (sampling rate, box size and origin) of two maps
        are equal.

        Args:
            map_target, map_probe
                Map instance to compare.

        Returns:
            True if the map properties are the same between two maps, False
            otherwise.
        """
        if (
                np.isclose(map_target.apix,
                           map_probe.apix,
                           atol=1E-6).all() and
                map_target.box_size() == map_probe.box_size()
        ):
            if (
                    round(map_target.origin[0], 2) == round(map_probe.origin[0], 2) and  # noqa:E501
                    round(map_target.origin[1], 2) == round(map_probe.origin[1], 2) and  # noqa:E501
                    round(map_target.origin[2], 2) == round(map_probe.origin[2], 2)  # noqa:E501
            ):
                return True
            else:
                return False
        else:
            return False

    def _failed_match(self):
        # should implement TEMPy errors for more elegant error handling
        print(
            'Warning: can\'t match the map at the moment,'
            'use map with same box size.'
        )
        sys.exit()

    def scale_median(self, arr1, arr2):
        """Scale one list/array of scores with respect to another based on
        distribution around median.

        Arguments:
            arr1, arr2: Array/list of scores

        Returns:
            Scaled arr1, based on the values in arr2
        """
        nparr1 = np.array(arr1)
        nparr2 = np.array(arr2)
        med_dev_1 = np.median(np.absolute(nparr1 - np.median(nparr1)))
        med_dev_2 = np.median(np.absolute(nparr2 - np.median(nparr2)))
        if med_dev_1 == 0.0:
            scale_factor = 0.0
        else:
            scale_factor = med_dev_2 / med_dev_1
        shift_factor = np.median(nparr2) - (scale_factor * np.median(nparr1))

        # TODO: find a better way to avoid outliers in general
        if (max(nparr1) - min(nparr1)) > 0.1:
            scaled_arr = ((scale_factor * nparr1 + shift_factor) + nparr2) / 2.
        else:
            scaled_arr = nparr2
        return scaled_arr

    def _CCC_calc(self, m1, m2):
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
                numer += arr1[z]*arr2[z]
                var1 += arr1[z]**2
                var2 += arr2[z]**2
        elif nd == 3:
            for z in range(dim[0]):
                for y in range(dim[1]):
                    for x in range(dim[2]):
                        numer += arr1[z, y, x]*arr2[z, y, x]
                        var1 += arr1[z, y, x]**2
                        var2 += arr2[z, y, x]**2
        corr = numer/math.sqrt(var1*var2)
        corr = min(1.0, corr)
        corr = max(-1.0, corr)
        return corr

    def CCC_map(
            self,
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
        if self.mapComparison(map_target, map_probe):
            if not mode == 1:
                if map_target_threshold == 0 and map_probe_threshold == 0:
                    map_target_threshold = self.calculate_map_threshold(
                        map_target
                    )
                    map_probe_threshold = self.calculate_map_threshold(
                        map_probe
                    )
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
                        'No map overlap (Cross correlation score), exiting '
                        'score calculation..'
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
                        'No map overlap (Cross correlation score), '
                        'exiting score calculation..'
                    )
                    return -1.0, 0.0
                map1_mask = map_target.fullMap[mask_array]
                map2_mask = map_probe.fullMap[mask_array]
                if meanDist:
                    map1_mask = map1_mask - np.mean(map1_mask)
                    map2_mask = map2_mask - np.mean(map2_mask)
                if cmode:
                    corr = self._CCC_calc(
                        map1_mask.flatten(),
                        map2_mask.flatten(),
                    )
                else:
                    corr = None
                if corr is None:
                    return (
                        (
                            np.sum(map1_mask * map2_mask) /
                            np.sqrt(
                                np.sum(np.square(map1_mask)) *
                                np.sum(np.square(map2_mask))
                            )
                        ),
                        perc_ovr
                    )
                else:
                    return corr, perc_ovr

            # calculate CCC for contoured maps based on threshold
            elif mode == 2:
                map1_mask = map_target.fullMap * bin_map1
                map2_mask = map_probe.fullMap * bin_map2
                if meanDist:
                    map1_mask = (
                            map1_mask -
                            np.mean(map_target.fullMap[bin_map1])
                    )
                    map2_mask = (
                            map2_mask -
                            np.mean(map_probe.fullMap[bin_map2])
                    )
                    map1_mask = map1_mask * bin_map1
                    map2_mask = map2_mask * bin_map2
                else:
                    map1_mask = map_target.fullMap * bin_map1
                    map2_mask = map_probe.fullMap * bin_map2
                if cmode:
                    corr = self._CCC_calc(map1_mask, map2_mask)
                else:
                    corr = None
                if corr is None:
                    return (
                        (
                            np.sum(map1_mask * map2_mask) /
                            np.sqrt(
                                np.sum(np.square(map1_mask)) *
                                np.sum(np.square(map2_mask))
                            )
                        ),
                        perc_ovr
                    )
                else:
                    return corr, perc_ovr
            # calculate on the complete map
            if meanDist:
                if cmode:
                    corr = self._CCC_calc(
                        map_target.fullMap - np.mean(map_target.fullMap),
                        map_probe.fullMap - np.mean(map_probe.fullMap)
                    )
                else:
                    corr = None
                if corr is None:
                    return (
                        (
                            np.sum(
                                (
                                    map_target.fullMap -
                                    np.mean(map_target.fullMap)
                                ) *
                                (
                                    map_probe.fullMap -
                                    np.mean(map_probe.fullMap)
                                )
                            ) /
                            (
                                np.sqrt(
                                    np.sum(
                                        np.square(
                                            map_target.fullMap -
                                            np.mean(map_target.fullMap)
                                        )
                                    ) *
                                    np.sum(
                                        np.square(
                                            map_probe.fullMap -
                                            np.mean(map_probe.fullMap)
                                        )
                                    )
                                )
                            )
                        ),
                        perc_ovr
                    )
                else:
                    return corr, perc_ovr
            if cmode:
                corr = self._CCC_calc(map_target.fullMap, map_probe.fullMap)
            else:
                corr = None
            if corr is None:
                return (
                    np.sum(map_target.fullMap * map_probe.fullMap) /
                    np.sqrt(
                        np.sum(np.square(map_target.fullMap)) *
                        np.sum(np.square(map_probe.fullMap))
                    ),
                    perc_ovr
                )
            else:
                return corr, perc_ovr
        else:
            print('@@@ Maps could not be matched')
            return -1., 0.

    def CCC(self, map_target, map_probe):
        """Calculate cross-correlation between two Map instances.

        Args:
            map_target, map_probe
                Map instance to compare.
        Returns:
            CCC score
        Raises:
            sys.exit: Input maps do not match in shape, pixel size or origin
        """
        if self.mapComparison(map_target, map_probe):
            return (
                map_target.normalise().getMap()*map_probe.normalise().getMap()
            ).mean()
        else:
            self._failed_match()

    def LSF(self, map_target, map_probe):
        """Calculate least-squares between two Map instances.

        Arguments:
            map_target, map_probe: Map instance to compare.
        Return:
            Least-squares value
        Raises:
            sys.exit: Input maps do not match in shape, pixel size or origin
        """
        if self.mapComparison(map_target, map_probe):
            map_target, map_probe = map_target, map_probe
        else:
            self._failed_match()
        return ((map_target.getMap() - map_probe.getMap())**2).mean()

    def laplace_CCC(
            self,
            map_target,
            map_probe,
            prefil=(False, False)
    ):
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

        if self.mapComparison(map_target, map_probe):
            # I don't understand this - can we replace it with pass?
            _, _ = map_target, map_probe  # noqa:F841
        else:
            self._failed_match()

        if not prefil[0]:
            map_target = map_target.laplace_filtered()
        if not prefil[1]:
            map_probe = map_probe.laplace_filtered()
        map_target = map_target.normalise()
        map_probe = map_probe.normalise()
        return self.CCC(map_target, map_probe)

    def normal_vector_score(
            self,
            map_target,
            map_probe,
            primary_boundary,
            secondary_boundary=0.0,
            Filter=None,
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
        if Filter not in ['Sobel', 'Laplace', 'Mean', 'Minimum', None]:
            print('Incorrect name of filter: %s" % Filter')
            print(
                'Select one of the following Filters if applicable: %s\n' %
                ', '.join(['Sobel', 'Laplace'])
            )
            sys.exit()

        scores = []
        if not self.mapComparison(map_target, map_probe):
            self._failed_match()
        assert isinstance(primary_boundary, float)
        assert isinstance(secondary_boundary, float)
        if primary_boundary > secondary_boundary:
            temp_thr = secondary_boundary
            secondary_boundary = primary_boundary
            primary_boundary = temp_thr

        points = np.argwhere(
            (map_target.fullMap > primary_boundary) &
            (map_target.fullMap < secondary_boundary)
        )

        if Filter == 'Sobel':
            map1_surface = map_target._sobel_filter_contour(primary_boundary)
            points = np.argwhere(
                map1_surface.fullMap > (map1_surface.max() / 2.0)
            )
        elif Filter == 'Laplace':
            map1_surface = map_target._laplace_filtered_contour(
                primary_boundary
            )
            points = np.argwhere(
                map1_surface.fullMap > (map1_surface.max() / 2.0)
            )
        elif Filter == 'Minimum':
            map1_surface = map_target._surface_minimum_filter(
                float(primary_boundary)
            )
            points = np.argwhere(map1_surface == 1)
        elif Filter == 'Mean':
            map1_filter = map_target._surface_features(float(primary_boundary))
            bin_test = [0.0001]
            for ii in range(1, 41):
                bin_test.append(0.025 * ii)
            freq_test = np.histogram(map1_filter.fullMap, bin_test)[0]
            sum_freq = 0.0
            for fr in range(len(freq_test)):
                sum_freq += float(freq_test[fr])
                if (
                        sum_freq / np.sum(freq_test) > 0.05 and
                        bin_test[fr+1] >= 0.3
                ):
                    t1 = bin_test[fr+1]
                    break
                if (
                        sum_freq / np.numsum(freq_test) > 0.10 or
                        sum_freq > 100000
                ):
                    t1 = bin_test[fr+1]
                    break
            points = np.argwhere(
                (map1_filter.fullMap > 0.0) & (map1_filter.fullMap < t1)
            )
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
                if (
                        nvec[0] == 0. and
                        nvec[1] == 0. and
                        nvec[2] == 0.
                ):
                    if (
                            ovec[0] == 0. and
                            ovec[1] == 0. and
                            ovec[2] == 0.0
                    ):
                        continue
                    else:
                        scores.append(3.14)
                        continue
                else:
                    if (
                            ovec[0] == 0. and
                            ovec[1] == 0. and
                            ovec[2] == 0.
                    ):
                        scores.append(3.14)
                        continue
                try:
                    dotprod = (
                            ovec[0] *
                            nvec[0] +
                            ovec[1] *
                            nvec[1] +
                            ovec[2] *
                            nvec[2]
                    )
                    den = (
                            np.sqrt(nvec[0]**2 + nvec[1]**2 + nvec[2]**2) *
                            np.sqrt(ovec[0]**2 + ovec[1]**2 + ovec[2]**2)
                    )
                    if abs(dotprod - den) < 0.00001:
                        ang = 0.0
                    else:
                        ang = math.acos(min(max(dotprod / den, -1.0), 1.0))
                    if den == 0.0:
                        print(dotprod, den, nvec, ovec)
                    scores.append(abs(ang))
                except ValueError:
                    print(
                        'Error: Angle could not be calculated: ',
                        nvec,
                        ' ',
                        ovec
                    )
            if len(scores) == 0:
                print(
                    'There are no points to be scored! The threshold values or'
                    ' the number of points to be considered needs to be'
                    ' changed.'
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
                if (
                    n_vec.x == -9 and
                    n_vec.y == -9 and
                    n_vec.z == -9
                ):
                    if (
                        o_vec.x == -9 and
                        o_vec.y == -9 and
                        o_vec.z == -9
                    ):
                        continue
                    else:
                        scores.append(3.14)
                        continue
                else:
                    if (
                        o_vec.x == -9 and
                        o_vec.y == -9 and
                        o_vec.z == -9
                    ):
                        scores.append(3.14)
                        continue
                try:
                    scores.append(abs(n_vec.arg(o_vec)))
                except ValueError:
                    print(
                        'Error: Angle between ' +
                        str(n_vec) +
                        ', ' +
                        str(o_vec) +
                        ' for point %d, %d, %d cannot be calculated.' %
                        (v.x, v.y, v.z)
                    )
        if len(scores) == 0:
            print(
                'There are no points to be scored! The threshold values or '
                'the number of points to be considered needs to be changed.'
            )
        else:
            if sum(scores) == 0:
                return 0
            else:
                return 1 - (sum(scores) / (len(points) * 3.14))

    def get_partial_DLSF(
            self,
            num_of_points,
            map_target,
            map_probe
    ):
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

        if not self.mapComparison(map_target, map_probe):
            return "can't Match the map"

        map_target_sig_pairs = map_target._get_random_significant_pairs(
            int(num_of_points)
        )
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
            prot_dens = (
                otherMap.fullMap[z1][y1][x1] - otherMap.fullMap[z2][y2][x2]
            )
            score += (dens - prot_dens)**2
        return score / map_target.fullMap.size

    def _MI(self, map_target, map_probe, layers=20):
        """Calculate the mutual information score between two Maps.

        Old version of the score?

        Arguments:
            map_target, map_probe: Map instances to compare.

            layers: Number of layers used to bin the map. Default is 20 as in
                Shatsky et al., 2008.
        Return: MI score
        Raises:
            sys.exit: Input maps do not match in shape, pixel size or origin
        """

        if self.mapComparison(map_target, map_probe):
            m1, m2 = map_target, map_probe
        else:
            self._failed_match()
        score = 0
        m1_levels = (m1.max() - m1.min()) / layers
        m2_levels = (m2.max() - m2.min()) / layers
        for x in range(layers):
            for y in range(layers):
                m1_level_map = (
                        (m1.getMap() >= m1.min() + (x * m1_levels)) *
                        (m1.getMap() <= m1.min() + ((x + 1) * m1_levels))
                )
                m2_level_map = (
                        (m2.getMap() >= m2.min() + (y * m2_levels)) *
                        (m2.getMap() <= m2.min() + ((y + 1) * m2_levels))
                )
                comb_level_map = m1_level_map*m2_level_map
                p_m1 = float(m1_level_map.sum())/m1_level_map.size
                p_m2 = float(m2_level_map.sum())/m2_level_map.size
                p_comb = float(comb_level_map.sum())/comb_level_map.size
                if p_comb == 0:
                    mi_score = 0.0
                else:
                    mi_score = p_comb * math.log(p_comb / (p_m1 * p_m2), 2)
                score += mi_score
        return score

    def _MI_C(
            self,
            m1,
            m2,
            layers1=20,
            layers2=20,
            N=0,
            lc1=0.0,
            lc2=0.0,
    ):
        arr1 = (m1).view(float)
        arr2 = (m2).view(float)
        return _MI_C_helper_new(arr1, arr2, layers1, layers2, N, lc1, lc2)

    def MI(
            self,
            map_target,
            map_probe,
            map_target_threshold=0.0,
            map_probe_threshold=0.0,
            mode=1,
            layers1=None,
            layers2=None,
            weight=False,
            cmode=True,
    ):
        """Calculate the mutual information score between two Map instances.

        Arguments:
            map_target, map_probe: Map instance to compare.
            map_target_threshold, map_probe_threshold: Threshold used for
                contouring
            mode:
                1. use complete map for calculation
                3. use overlap region for calculation
            layers1: Number of layers used to bin map_target. If None, value
                is calculated based on Sturges, 1926 method.
            layers2: Number of layers used to bin map_probe. If None, value
                is calculated based on Sturges, 1926 method.
            weight: If True: normalised MI (Studholme et al.) is used to
                account for overlap of 'contours'
            cmode:
        Returns:
            MI score
        Raises:
            sys.exit: Input maps do not match in shape, pixel size or origin
        """
        if not self.mapComparison(map_target, map_probe):
            self._failed_match()
        if map_target_threshold == 0.0:
            map_target_threshold = self.calculate_map_threshold(map_target)
        if map_probe_threshold == 0.0:
            map_probe_threshold = self.calculate_map_threshold(map_probe)
        # calculation on the complete map
        if mode == 1:
            if weight:
                wt = 1
            else:
                wt = 0
            if layers1 is None:
                layers1 = 20
            if layers2 is None:
                layers2 = 20
            min1 = (
                    np.amin(map_target.fullMap) -
                    0.00001 *
                    (np.amax(map_target.fullMap) - np.amin(map_target.fullMap))
            )
            min2 = (
                    np.amin(map_probe.fullMap) -
                    0.00001 *
                    (np.amax(map_probe.fullMap) - np.amin(map_probe.fullMap))
            )
            if cmode:
                mic = self._MI_C(
                    map_target.fullMap,
                    map_probe.fullMap,
                    layers1,
                    layers2,
                    wt,
                    min1,
                    min2
                )
            else:
                mic = None
            if mic is not None:
                return mic
            # digitize whole map based on layers
            map1_bin = map_target._map_digitize(
                map_target.min(),
                layers1,
                True,
            )
            map2_bin = map_probe._map_digitize(map_probe.min(), layers2, True)
            bins1 = []
            for i in range(layers1+2):
                bins1.append(i)
            bins2 = []
            for i in range(layers2+2):
                bins2.append(i)
            # calculate frequency of bins
            map1_freq = np.histogram(map1_bin.fullMap, bins1)[0][1:]
            map2_freq = np.histogram(map2_bin.fullMap, bins2)[0][1:]
        elif mode == 3:
            mask_array = self._overlap_map_array(
                map_target,
                map_target_threshold,
                map_probe,
                map_probe_threshold
            )
            if np.sum(mask_array) == 0:
                print(
                    'No map overlap (Mutual information score), exiting score '
                    'calculation..'
                )
                return 0.0
            # sturges rule provides a way of calculating number of bins :
            # 1 + math.log(number of points)
            if layers1 is None:
                try:
                    layers1 = int(1 + math.log(np.sum(mask_array), 2))
                except ValueError:
                    print(
                        'No map overlap (Mutual information score), '
                        'exiting score calculation..'
                    )
                    return 0.0
            if layers2 is None:
                try:
                    layers2 = int(1 + math.log(np.sum(mask_array), 2))
                except ValueError:
                    print(
                        'No map overlap (Mutual information score), exiting '
                        'score calculation..'
                    )
                    return 0.0
            layers1 = max(layers1, 15)
            layers2 = max(layers2, 15)
            if weight:
                wt = 1
            else:
                wt = 0
            if cmode:
                mic = self._MI_C(
                    np.array(map_target.fullMap * mask_array),
                    np.array(map_probe.fullMap * mask_array),
                    layers1,
                    layers2,
                    wt,
                )
            else:
                mic = None
            if mic is not None:
                return mic
            # digitize masked map based on layers
            map1_bin = map_target.copy()
            map2_bin = map_probe.copy()
            map1_bin.fullMap = map1_bin.fullMap * mask_array
            map2_bin.fullMap = map2_bin.fullMap * mask_array
            map1_bin = map1_bin._map_digitize(
                map_target.fullMap[mask_array].min(),
                layers1,
                True
            )
            map2_bin = map2_bin._map_digitize(
                map_probe.fullMap[mask_array].min(),
                layers2,
                True
            )
            # make sure the outside region is filled with zeros
            map1_bin.fullMap = map1_bin.fullMap * mask_array
            map2_bin.fullMap = map2_bin.fullMap * mask_array
            # background frequencies from the whole map
            bins1 = []
            for i in range(layers1 + 2):
                bins1.append(i)
            bins2 = []
            for i in range(layers2 + 2):
                bins2.append(i)
            # calculate frequency of bins
            map1_freq = np.histogram(map1_bin.fullMap, bins1)[0][1:]
            map2_freq = np.histogram(map2_bin.fullMap, bins2)[0][1:]

        score = 0.0
        total = 0

        if np.sum(map1_freq) == 0:
            print(
                'No map overlap (Mutual information score), exiting score '
                'calculation..'
            )
            return 0.0
        if np.sum(map2_freq) == 0:
            print(
                'No map overlap (Mutual information score), exiting score '
                'calculation..'
            )
            return 0.0
        list_overlaps = []
        for x in range(layers1):
            mask_array = map1_bin.fullMap == float(x+1)
            overlap_freq = np.histogram(
                map2_bin.fullMap[mask_array], bins2
            )[0][1:]
            total += float(np.sum(overlap_freq))
            list_overlaps.append(overlap_freq)

        if total == 0:
            print(
                'No map overlap (Mutual information score), exiting score '
                'calculation..'
            )
            return 0.0
        enter = 0
        Hxy = 0.0
        Hx = 0.0
        Hy = 0.0
        mi_score = 0.0
        p_comb = 0.0
        for x in range(layers1):
            p_m1 = map1_freq[x]/float(np.sum(map1_freq))
            for y in range(layers2):
                enter = 1
                p_comb = list_overlaps[x][y]/total
                p_m2 = map2_freq[y] / float(np.sum(map2_freq))
                if p_comb == 0:
                    mi_score = 0.0

                else:
                    Hxy += -p_comb * math.log(p_comb, 2)
                score += mi_score
                if x == 0 and not p_m2 == 0.0:
                    Hy += (-p_m2 * math.log(p_m2, 2))
            if not p_m1 == 0.0:
                Hx += (-p_m1 * math.log(p_m1, 2))
        if enter == 1:
            if weight:
                if Hxy == 0.0:
                    return 0.0
                return (Hx + Hy) / Hxy
            return Hx + Hy - Hxy
        else:
            return None

    def MI_new(self, exp_map, sim_map, bins1=20, bins2=20, normalise=False):
        """
        Taken from https://stackoverflow.com/questions/20491028/optimal-way-to-compute-pairwise-mutual-information-using-numpy
        """

        c_xy, x, y = np.histogram2d(exp_map.fullMap.ravel(),
                            sim_map.fullMap.ravel(),
                            bins=[bins1, bins2])

        g, _, _, _ = stats.chi2_contingency(c_xy, lambda_='log-likelihood')

        mi_nl = 0.5 * g / c_xy.sum()

        return np.log2(np.exp(mi_nl))

    def _hausdorff_list(
            self,
            primary_boundary,
            secondary_boundary,
            kdtree,
            map_probe,
    ):
        """
        This is for the chamdef distance def chamfer_distance, min max density
        value that define the surface of the protein

        Arguments:
            *kdtree*
                (there are 2 of them in numpy one Cbased on py-based, the
                latter is better, ctrl) this have to be one of the input.
                kdtree from map_target
            *primary_boundary, secondary_boundary*
                need to run get_primary_boundary and get_second_boundary for
                map_probe

            NOTE: if you keep the kdtree as parametre out os less time
            consuming as building it takes time.
        """
        points = map_probe.get_pos(primary_boundary, secondary_boundary)
        return kdtree.query(points)[0]

    def chamfer_distance(
            self,
            map_target,
            map_probe,
            primary_boundary,
            secondary_boundary,
            kdtree=None,
    ):
        """Calculate the chamfer distance Score between two Map instances.

        Currently unstable and not recommended for use.

        Arguments:
            map_target, map_probe: Map instances to compare.
            primary_boundary: Threshold that defined the EM map surface, based
                on the volume of the protein model. Can be calculated using
                :meth:`Map.makeKDTree <TEMPy.maps.em_map.Map.get_primary_boundary>`
            secondary_boundary: The second bound density point.
                Can be calculated using
                :meth:`Map.makeKDTree <TEMPy.maps.em_map.Map.get_second_boundary>`
            kdtree: Precalculated kdtree. If None, KDTree is constructed using
                :meth:`Map.makeKDTree <TEMPy.maps.em_map.Map.makeKDTree>`
        """
        if self.mapComparison(map_target, map_probe):
            m1, m2 = map_target, map_probe
        else:
            self._failed_match()
        if kdtree:
            return self._hausdorff_list(
                primary_boundary, secondary_boundary, kdtree, m2
            ).mean()
        else:
            print(m1, primary_boundary, secondary_boundary)
            kdtree = m1.makeKDTree(primary_boundary, secondary_boundary)
            if kdtree is None:
                print('Error. No points selected, change boundary parameters.')
                sys.exit()
            else:
                return self._hausdorff_list(
                    primary_boundary,
                    secondary_boundary,
                    kdtree,
                    m2
                ).mean()

    def _surface_distance_score(
            self,
            map_target,
            map_probe,
            map_target_threshold1=0.0,
            map_probe_threshold=0.0,
            Filter=None,
            map_target_threshold2=0.0,
            weight=False
    ):
        """
        Calculate the chamfer distance Score between two Map instances.

        Arguments:
            *map_target, map_probe*
                EMMap instances to compare.
            *map_target_threshold1*
                contour threshold of the target map.
                This value is used the primary boundary if
                map_target_threshold2 is given.
            *map_probe_threshold*
                contour threshold for the probe map.
            *Filter*
                definition of the surface:
                    1) None : surface defined by known boundaries -
                              map_target_threshold1 & map_target_threshold2
                    If the boundaries are not known and target&probe map
                    contour levels are known:
                        2) Std : to define the boundaries, contour level +- 5%
                                 sigma is calculated. 5%sigma is used to limit
                                 the number of points picked as surface. For
                                 small maps, higher values (eg: 10%sigma)
                                 can be used.
                        3) Mean: a mean filter is applied on the binary contour
                                 mask over a long window. The resulting mask
                                 has values between 0 and 1. Points with values
                                 less than 0.3 is used to represent surface.
                                 As the average is calculated on a long window,
                                 highly exposed surface points have very low
                                 values and partially exposed surfaces/grooves
                                 have relatively higher values.
                                 This definition is useful especially when the
                                 map surface has many features/projections.
                        4) Minimum: a minimum filter is applied on a binary
                                    contour mask to locate surface points.
                                    Voxels surrounded by points outside the
                                    contour (zeroes) are detected as surface.
                                    Voxels surrounded by points outside the
                                    contour (zeroes) are detected as surface.
                        5) Sobel: sobel filter is applied on the map to detect
                                  high density gradients. Before applying the
                                  sobel filter, it is important to reduce the
                                  noise density and large variations
                                  (gradients) in the noise region.
            *weight*
                If set true, the distances between the surface points is
                normalized in a way similar to GDT (Zemla 2007)
                calculation for atomic co-ordinate alignments.
        """
        # check if both maps are on the same grid
        if not self.mapComparison(map_target, map_probe):
            print('@@@ Maps could not be matched')
            return -999.
        # if the boundaries are known, calculate the kdtree
        if Filter is None:
            kdtree = map_target.makeKDTree(
                map_target_threshold1,
                map_target_threshold2
            )
            probe_points = map_probe.get_pos(
                map_target_threshold1,
                map_target_threshold2
            )
        elif Filter == 'Std':
            target_points = np.argwhere(
                (map_target.fullMap > (
                        float(map_target_threshold1)-(map_target.std()*0.10))
                 ) &
                (map_target.fullMap < (
                        float(map_target_threshold1)+(map_target.std()*0.10))
                 )
            )
            probe_points = np.argwhere(
                (map_probe.fullMap > (
                        float(map_probe_threshold)-(map_probe.std()*0.10))
                 ) &
                (map_probe.fullMap < (
                        float(map_probe_threshold)+(map_probe.std()*0.10))
                 )
            )
            if len(target_points) < len(probe_points):
                probe_points1 = np.copy(target_points)
                target_points = np.copy(probe_points)
                probe_points = np.copy(probe_points1)
            if len(target_points) == 0 or len(probe_points) == 0:
                print('Surface detection failed (Std filter), exiting..')
                return None
            try:
                from scipy.spatial import cKDTree
                try:
                    kdtree = cKDTree(target_points)
                except RuntimeError:
                    return None
            except ImportError:
                try:
                    kdtree = KDTree(target_points)
                except RuntimeError:
                    return None
        elif Filter == 'Mean':
            map1_filter = map_target._surface_features(
                float(map_target_threshold1)
            )
            map2_filter = map_probe._surface_features(
                float(map_probe_threshold)
            )
            """
            define surface based on the filtered mask values.
            points with values less than 0.3 are usually preferred. But in
            some cases like viruses, most surface points are highly exposed
            and a large number of points are returned and the calculation
            becomes slow.
            Hence an additional filter is added: the maximum allowed points
            is 10% of box size.
            The minimum number of points is kept as 7%. This mode is less
            sensitive to the number of surface points chosen
            as the extent of exposure is used for defining surface. Hence
            thick surface is not usually required.
            calculate frequencies in bins for filtered mask.
            The smaller the bins, more precise will be the calculation of
            points allowed based on percent of points chosen.
            As this is just an additional filter and doesn't affect the
            calculations drastically, 40 bins are used to calculate
            frequencies.
            """
            bin_test = [0.0001]
            for ii in range(1, 41):
                bin_test.append(0.025 * ii)
            freq_test = np.histogram(map1_filter.fullMap, bin_test)[0]
            map1_filled = np.sum(map1_filter.fullMap > 0)

            sum_freq = 0.0
            for fr in range(len(freq_test)):
                sum_freq += float(freq_test[fr])
                if sum_freq / map1_filled > 0.05 and bin_test[fr+1] >= 0.3:
                    t1 = bin_test[fr+1]
                    break
                if sum_freq / map1_filled > 0.10 or sum_freq > 200000:
                    t1 = bin_test[fr+1]
                    break
            sum_freq = 0.0
            freq_test = np.histogram(map2_filter.fullMap, bin_test)[0]
            map2_filled = np.sum(map2_filter.fullMap > 0)
            for fr in range(len(freq_test)):
                sum_freq += float(freq_test[fr])
                if sum_freq/map2_filled > 0.05 and bin_test[fr+1] >= 0.3:
                    t2 = bin_test[fr+1]
                    break
                if sum_freq/map2_filled > 0.10 or sum_freq > 200000:
                    t2 = bin_test[fr+1]
                    break
            # t1 and t2 are the selected levels based on filtered values and
            # percent of points
            target_points = np.argwhere(
                (map1_filter.fullMap > 0.0) & (map1_filter.fullMap <= t1)
            )
            probe_points = np.argwhere(
                (map2_filter.fullMap > 0.0) & (map2_filter.fullMap <= t2)
            )
            if len(target_points) == 0 or len(probe_points) == 0:
                print('Surface detection failed (Mean filter), exiting..')
                return None
            if len(target_points) < len(probe_points):
                probe_points1 = np.copy(target_points)
                target_points = np.copy(probe_points)
                probe_points = np.copy(probe_points1)
            try:
                from scipy.spatial import cKDTree
                try:
                    kdtree = cKDTree(target_points)
                except RuntimeError:
                    return None
            except ImportError:
                try:
                    kdtree = KDTree(target_points)
                except RuntimeError:
                    return None
        elif Filter == 'Minimum':
            map1_surface = map_target._surface_minimum_filter(
                float(map_target_threshold1)
            )
            map2_surface = map_probe._surface_minimum_filter(
                float(map_probe_threshold)
            )
            # select the surface points represented by the mask
            target_points = np.argwhere(map1_surface == 1)
            probe_points = np.argwhere(map2_surface == 1)
            if len(target_points) == 0 or len(probe_points) == 0:
                print('Surface detection failed (Minimum filter), exiting..')
                return None
            if len(target_points) + len(probe_points) > 250000:
                return None
            if len(target_points) < len(probe_points):
                probe_points1 = np.copy(target_points)
                target_points = np.copy(probe_points)
                probe_points = np.copy(probe_points1)
            try:
                from scipy.spatial import cKDTree
                try:
                    kdtree = cKDTree(target_points)
                except RuntimeError:
                    return None
            except ImportError:
                try:
                    kdtree = KDTree(target_points)
                except RuntimeError:
                    return None
        elif Filter == 'Sobel':
            map1_surface = map_target._sobel_filter_contour(
                float(map_target_threshold1)
            )
            map2_surface = map_probe._sobel_filter_contour(
                float(map_probe_threshold)
            )

            target_points = np.argwhere(
                map1_surface.fullMap > map1_surface.max() / float(2)
            )
            probe_points = np.argwhere(
                map2_surface.fullMap > map2_surface.max() / float(2)
            )
            if len(target_points) == 0 or len(probe_points) == 0:
                print('Surface detection failed (Sobel filter), exiting..')
                return None
            if len(target_points) < len(probe_points):
                probe_points1 = np.copy(target_points)
                target_points = np.copy(probe_points)
                probe_points = np.copy(probe_points1)
            try:
                from scipy.spatial import cKDTree
                try:
                    kdtree = cKDTree(target_points)
                except RuntimeError:
                    return None
            except ImportError:
                try:
                    kdtree = KDTree(target_points)
                except RuntimeError:
                    return None
        distances = kdtree.query(probe_points)[0]
        if len(distances) == 0:
            return None
        if not weight:
            if not np.mean(distances) <= 0.05:
                return 1 / np.mean(distances)
            else:
                return 1/0.05

        x = int(30.0 / map_target.apix)
        if np.amin(distances) < x / 2:
            distances = distances - np.amin(distances)
        bins = []
        i = 0
        while i <= float(x):
            bins.append(i * 1.0)
            i += 1
        num_distances = len(distances)
        overlap_freq = np.histogram(distances, bins)[0]
        for fr_i in range(len(overlap_freq)):
            if overlap_freq[fr_i] > np.amax(overlap_freq) / 3.:
                break
        total_ext = fr_i
        bins = bins[fr_i:]
        if cl:  # noqa:F821
            points_cl = probe_points
            if len(points_cl) == 0:
                return None, None
            try:
                kdtree = cKDTree(points_cl)
            except Exception:
                return None, None
            neighbors_num = 20
            distance_lim = 3.0
            neigh = kdtree.query(
                points_cl,
                k=neighbors_num,
                distance_upper_bound=distance_lim,
            )[1]

            cl_weight = (
                    np.numsum(np.sum(neigh < len(neigh), axis=1) > 17) /
                    float(len(probe_points))
            )
            distances_align = distances
            distances_sel = distances_align[
                np.sum(neigh < len(neigh), axis=1) > 17
            ]
            distances = distances_sel[:]

        overlap_freq = np.histogram(distances, bins)[0]
        total = total_ext
        cumul_freq = 0.0
        enter = 0
        sum_sc = 0.0
        for i in range(len(overlap_freq)):
            w = len(overlap_freq) - (i)
            try:
                cumul_freq += overlap_freq[i]
            except IndexError:
                pass
            try:
                perc_equiv = float(cumul_freq) / num_distances
            except ZeroDivisionError:
                print('Distance weighting failed!!. Check surface defined')
                return None, None
            sum_sc = sum_sc + ((w) * perc_equiv)
            total += (w)
            enter = 1
        score = float(sum_sc) / total
        if cl:  # noqa:F821
            if enter == 1:
                if len(distances_sel) == 0.0:
                    return 0.0
                if np.mean(distances_sel) == 0.0:
                    return 0.0
                if cl_weight == 0.0:
                    return 0.0
                return score
            else:
                return None, None
        if enter == 1:
            if np.mean(distances) <= 0.05:
                return 1.0
            if np.mean(distances) == 0.0:
                return 1.0
            return score
        else:
            return None, None

    def envelope_score(
            self,
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
        min_score = float(np.sum(binMap.fullMap)-2 * np.sum(binMap.fullMap+1))

        blurrer = StructureBlurrer()
        struct_binMap = blurrer.make_atom_overlay_map1(
            map_target,
            structure_instance
        )
        grid = struct_binMap.get_pos(0.9, 1.1)
        for x, y, z in grid:
            g = binMap[z][y][x]
            if g == -1:
                binMap[z][y][x] = 2
            elif g == 0:
                binMap[z][y][x] = -2
        score = float(np.sum(binMap.fullMap))
        if norm:
            norm_score = float((score-min_score) / (max_score-min_score))
            return norm_score
        else:
            return score

    def envelope_score_map(
            self,
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
        if self.mapComparison(map_target, map_probe):
            if map_target_threshold == 0:
                map_target_threshold = self.calculate_map_threshold(map_target)
            if map_probe_threshold == 0:
                map_probe_threshold = self.calculate_map_threshold(map_probe)

        binMap = map_target.make_bin_map(map_target_threshold)
        max_score = float(-2 * np.sum(binMap.fullMap))
        min_score = float(
            np.sum(binMap.fullMap)-2 * np.sum(binMap.fullMap + 1)
        )
        struct_binMap = map_probe.make_bin_map(map_probe_threshold)
        newMap = binMap.fullMap + 2 * struct_binMap.fullMap
        hist_array = np.histogram(newMap, 4)
        score = (
                2 *
                hist_array[0][0] -
                (2 * (hist_array[0][1])) -
                (hist_array[0][2])
        )
        if norm:
            norm_score = float((score - min_score)) / (max_score - min_score)
            return norm_score
        else:
            return score

    def _percent_overlap(
            self,
            map_target,
            map_probe,
            map_target_threshold,
            map_probe_threshold,
            flagsize=0,
    ):
        """Calculate the fraction of overlap between two map grids.

        Arguments:
            map_target, map_probe: Map instance to compare.
            map_target_threshold, map_probe_threshold:
                map contour thresholds for map_target and map_probe.
        Return:
            Percent overlap with respect to smaller grid
        """
        if self.mapComparison(map_target, map_probe):
            binmap1 = map_target.fullMap > float(map_target_threshold)
            binmap2 = map_probe.fullMap > float(map_probe_threshold)
            minim = len(map_target.fullMap[binmap1])
            if len(map_probe.fullMap[binmap2]) < minim:
                minim = len(map_probe.fullMap[binmap2])
            maskmap = (binmap1 * binmap2) > 0
            if flagsize == 1:
                return np.sum(maskmap), np.sum(binmap1), np.sum(binmap2)
            if not minim == 0.0:
                return float(len(map_target.fullMap[maskmap]))/minim
            else:
                print('Check map contour!!')
                return 0.0
        else:
            print('@@@ Maps could not be matched')
            return -1.0

    def SCCC(
            self,
            map_target,
            resolution_densMap,
            sigma_map,
            structure_instance,
            rigid_body_structure,
            write=False,
            c_mode=False,
    ):
        """Calculate local cross-correlation for a segment of a protein model

        Segments are defined using a rigid-body structure instance, which can
        be generated using `RIBFIND <https://ribfind.ismb.lon.ac.uk/>`_.
        The CCC is calculated using
        :meth:`CCC_map <TEMPy.protein.scoring_functions.ScoringFunctions.CCC_map>`.

        Implementation discussed in more detail at the following reference:
            * `Pandurangan et al., J Struct Biol. 2013 Dec 12 <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3988922/>`_

        Args:
            map_target: Map Instance.
            resolution_densMap: Resolution of the input map.
            sigma_map: Parameter need for Structure Blurrer. Full explanation
                :ref:`here<Note on real space blurring:>`
            structure_instance: Structure instance to compare
            rigid_body_structure: Rigid-body Structure instance that defines
                the segment.
            write: If True, a string is returned with format :code:`f'SCCC for segment {SCCC_score}'`
            c_mode: No longer in use
        Returns:
            float if :code:`write=False`, else string:
                SCCC Score
        """
        blurrer = StructureBlurrer()
        scorer = ScoringFunctions()
        outline = ""
        resolution_densMap = float(resolution_densMap)
        whole_fit_map = blurrer.gaussian_blur(
            structure_instance,
            resolution_densMap,
            densMap=map_target,
            sigma_coeff=sigma_map,
            normalise=True,
        )
        sim_map = blurrer.gaussian_blur(
            rigid_body_structure,
            resolution_densMap,
            densMap=map_target,
            sigma_coeff=sigma_map,
            normalise=True,
        )
        minDens = sim_map.std()
        sim_mask_array = sim_map._get_maskArray(minDens)
        mask_emMap = map_target._get_maskMap(sim_mask_array)
        mask_simMap = whole_fit_map._get_maskMap(sim_mask_array)
        sse_lccf, ov = scorer.CCC_map(mask_emMap, mask_simMap, cmode=c_mode)
        if write is True:
            outline += 'SCCC for segment %f\n' % (sse_lccf)
            return outline
        return sse_lccf

    def SCCC_LAP(
            self,
            map_target,
            resolution_densMap,
            sigma_map,
            structure_instance,
            rigid_body_structure,
            write=False,
    ):
        """Calculate the Laplacian filtered cross correlation for a segment of
        a protein model.

        Segments are defined using a rigid-body structure instance, which can
        be generated using `RIBFIND <https://ribfind.ismb.lon.ac.uk/>`_.
        Score calculated using
        :meth:`laplace_CCC <TEMPy.protein.scoring_functions.ScoringFunctions.laplace_CCC>`

        Arguments:
            map_target: Map Instance.
            resolution_densMap: Resolution of the map instance.
            sigma_map: Parameter need for Structure Blurrer. Full explanation
                :ref:`here<Note on real space blurring:>`
            structure_instance: Structure instance to compare
            rigid_body_structure: Rigid-body Structure instance.
            write: If True, a string is returned with format
                :code:`f'SCCC_LAP for segment {SCCC_LAP_score}'`
        Return:
            float if :code:`write=False`, else string:
                SCCC_LAP score
        """
        blurrer = StructureBlurrer()
        scorer = ScoringFunctions()
        outline = ""
        resolution_densMap = float(resolution_densMap)
        whole_fit_map = blurrer.gaussian_blur(
            structure_instance,
            resolution_densMap,
            densMap=map_target,
            sigma_coeff=sigma_map,
            normalise=True,
        )
        sim_map = blurrer.gaussian_blur(
            rigid_body_structure,
            resolution_densMap,
            densMap=map_target,
            sigma_coeff=sigma_map,
            normalise=True,
        )
        minDens = sim_map.std()
        sim_mask_array = sim_map._get_maskArray(minDens)
        mask_emMap = map_target._get_maskMap(sim_mask_array)
        mask_simMap = whole_fit_map._get_maskMap(sim_mask_array)
        sse_lccf = scorer.laplace_CCC(mask_emMap, mask_simMap)
        if write is True:
            outline += 'SCCC for segment %f\n' % (sse_lccf)
            return outline
        return sse_lccf

    def SCCC_MI(
            self,
            map_target,
            resolution_densMap,
            sigma_map,
            structure_instance,
            rigid_body_structure,
            write=False,
    ):
        """Calculate the mutual information score for a segment of a protein
        model.

        Segments are defined using a rigid-body structure instance, which can
        be generated using `RIBFIND <https://ribfind.ismb.lon.ac.uk/>`_.
        The score for the segment is calculated using
        :meth:`MI <TEMPy.protein.scoring_functions.ScoringFunctions.MI>`

        Arguments:
            map_target: Map Instance.
            resolution_densMap: Resolution of the map instance.
            sigma_map: Parameter need for Structure Blurrer. Full explanation
                :ref:`here<Note on real space blurring:>`
            structure_instance: Structure instance to compare
            rigid_body_structure: Rigid-body Structure instance.
            write: If True, a string is returned with format
                :code:`f'SCCC_LAP for segment {SCCC_LAP_score}'`
        Return:
            float if :code:`write=False`, else string:
                SCCC_MI score
        """
        blurrer = StructureBlurrer()
        scorer = ScoringFunctions()
        outline = ""
        resolution_densMap = float(resolution_densMap)
        whole_fit_map = blurrer.gaussian_blur(
            structure_instance,
            resolution_densMap,
            densMap=map_target,
            sigma_coeff=sigma_map,
            normalise=True
        )
        sim_map = blurrer.gaussian_blur(
            rigid_body_structure,
            resolution_densMap,
            densMap=map_target,
            sigma_coeff=sigma_map,
            normalise=True
        )
        minDens = sim_map.std()
        sim_mask_array = sim_map._get_maskArray(minDens)
        mask_emMap = map_target._get_maskMap(sim_mask_array)
        mask_simMap = whole_fit_map._get_maskMap(sim_mask_array)
        sse_lccf = scorer.MI(mask_emMap, mask_simMap)
        if write is True:
            outline += 'SCCC for segment %f\n' % (sse_lccf)
            return outline
        return sse_lccf

    def get_sccc(
            self,
            map_target,
            structure_instance,
            rigid_body_file,
            resolution,
            sigma_map=0.187
    ):
        """Read rigid body file and calculate sccc scores for each rigid body

        Args:
            map_target: Map instance
            structure_instance: Model structure instance
            rigid_body_file: Path to rigid body file
            resolution: Resolution of map instance
            sigma_map: Parameter need for Structure Blurrer. Full explanation
                :ref:`here<Note on real space blurring:>`

        Returns:
            Two dictionaries; dict_chain_scores, dict_rigid_scores
                * dict_chain_scores is a dictionary with keys equal to chain
                  labels (e.g. :code:`['A', 'B', 'C']`). Each value is another
                  dictionary, with keys as residue number for each residue in a
                  rigid body, and values the CCC score for that residue.

                * dict_rigid_scores is a dictionary with keys equal to each
                  rigid body (string?? not sure) and values the CCC score for
                  that body.

        """
        dict_rbf = RBParser.get_rigid_body_str_instances(
            rigid_body_file,
            structure_instance,
        )
        dict_chain_details = structure_instance.get_dict_str()
        dict_chain_scores = {}
        dict_rigid_scores = {}
        minscore = 1.0
        maxscore = -1.0
        for ch in dict_chain_details:
            dict_res_scores = {}
            for res in dict_chain_details[ch]:
                dict_res_scores[res] = -2.0
            if ch not in dict_rbf:
                continue
            for rb in dict_rbf[ch]:
                res_list = []
                for seg in dict_rbf[ch][rb][0]:
                    try:
                        for r in range(int(seg[0]), int(seg[1]) + 1):
                            res_list.append(r)
                    except TypeError:
                        continue
                score_SCCC = self.SCCC(
                    map_target,
                    resolution,
                    sigma_map,
                    structure_instance,
                    dict_rbf[ch][rb][1]
                )
                if rb not in dict_rigid_scores:
                    dict_rigid_scores[rb] = score_SCCC
                    if score_SCCC < minscore:
                        minscore = score_SCCC
                    if score_SCCC > maxscore:
                        maxscore = score_SCCC
                for res in res_list:
                    dict_res_scores[res] = score_SCCC

            dict_chain_scores[ch] = dict_res_scores

        minscore = max(minscore - (maxscore - minscore) / 5., -1.0)
        for ch in dict_chain_scores:
            for res in dict_chain_scores[ch]:
                if dict_chain_scores[ch][res] == -2.0:
                    dict_chain_scores[ch][res] = minscore

        return dict_chain_scores, dict_rigid_scores

    def calc_moc(
            self,
            indices,
            map_probe,
            map_target,
    ):
        map_target_mask = map_target.fullMap[indices]
        map_probe_mask = map_probe.fullMap[indices]
        num = np.sum(map_target_mask * map_probe_mask)
        den = np.sqrt(
            np.sum(np.square(map_target_mask)) *
            np.sum(np.square(map_probe_mask))
        )
        if den == 0.0:
            return -1.0
        return num / den

    def calc_ccc(
            self,
            indices,
            map_probe,
            map_target
    ):
        map_target_mask = map_target.fullMap[indices]
        map_target_mask = map_target_mask - float(
            map_target_mask.sum()/len(map_target_mask)
        )
        map_probe_mask = map_probe.fullMap[indices]
        map_probe_mask = map_probe_mask - float(
            map_probe_mask.sum()/len(map_probe_mask)
        )
        num = np.sum(map_target_mask * map_probe_mask)
        den = np.sqrt(
            np.sum(np.square(map_target_mask)) *
            np.sum(np.square(map_probe_mask))
        )
        if den == 0.0:
            return -1.0
        return num / den

    def indices_smoc(
            self,
            score_indices,
            grid_indices
    ):
        tmplist = score_indices[:]
        setlist = set(tmplist)
        indices = list(setlist)
        sc_indices = []
        for ii in indices:
            sc_indices.append(grid_indices[ii])
        array_indices = np.array(sc_indices)
        ind_arrxyz = np.transpose(array_indices)
        ind_arrzyx = (ind_arrxyz[2], ind_arrxyz[1], ind_arrxyz[0])
        return ind_arrzyx

    def set_score_as_bfactor(
            self,
            structure_instance,
            dict_scores,
            default=0.0,
            chid=None,
            outfile='score.pdb',
    ):
        # include scores as b-factor records
        for x in structure_instance.atomList:
            cur_chain = x.chain
            cur_res = x.get_res_no()
            if cur_chain in dict_scores:
                try:
                    x.temp_fac = "{0:.2f}".format(
                        float(dict_scores[cur_chain][cur_res])
                    )
                except (KeyError, IndexError):
                    print('Residue missing: ', cur_res, chid)
                    x.temp_fac = default
            else:
                x.temp_fac = default
        structure_instance.write_to_PDB(outfile)

    def smoc_score_rigid_bodies(
            self,
            dict_res_indices,
            rigid_body_file,
            ch,
            indi,
            map_target,
            sim_map
    ):
        dict_res_scores = {}
        dict_rbf = RBParser.read_rigid_body_file(rigid_body_file)
        chainid_set = ch
        if len(ch) == 0:
            chainid_set = '-'
        if chainid_set in dict_rbf:
            for rb in dict_rbf[chainid_set]:
                # each rigid body
                indices = []
                res_list = []
                for seg in dict_rbf[chainid_set][rb]:
                    try:
                        for r in range(int(seg[0]), int(seg[1]) + 1):
                            indices.extend(dict_res_indices[r])
                            res_list.append(r)
                    except TypeError:
                        continue
                # minimum value set as 0 here (assuming only positive values!)
                if len(indices) == 0:
                    for res in res_list:
                        dict_res_scores[res] = 0.0  # -0.99
                    continue
                try:
                    ind_arrzyx = self.indices_smoc(indices, indi)
                    smoc = self.calc_moc(ind_arrzyx, sim_map, map_target)
                except IndexError:
                    smoc = 0.0
                # save scores
                for res in res_list:
                    dict_res_scores[res] = smoc
        return dict_res_scores

    def smoc_get_indices_fragment_window(self, dict_res_indices,
                                         dict_chain_res, ch, res,
                                         win):
        indices = dict_res_indices[res][:]
        # consider residues on both sides. NOTE: wont work for insertion codes!
        # need to rewite res numbers to avoid insertion codes
        for ii in range(1, int(round((win + 1) / 2))):
            try:
                res_idx = dict_chain_res[ch].index(res) - ii
                if res_idx < 0:
                    continue
                # get prev residue indices
                indices.extend(
                    dict_res_indices[
                        dict_chain_res[ch]
                        [
                            res_idx
                        ]
                    ]
                )
            except (KeyError, IndexError):
                pass
        for ii in range(1, int(round((win + 1) / 2))):
            try:
                indices.extend(
                    dict_res_indices[
                        dict_chain_res[ch]
                        [
                            dict_chain_res[ch].index(res) + ii
                        ]
                    ]
                )
            except (IndexError, KeyError):
                pass
        return indices

    def smoc_get_indices_sphere(self, gridtree, coord, dist=5.0):
        list_points = gridtree.query_ball_point(
            [coord[0], coord[1], coord[2]],
            dist
        )
        return list_points

    def SMOC(self,
             map_target,
             resolution_densMap,
             structure_instance=None,
             win=11,
             rigid_body_file=None,
             sim_map=None,
             sigma_map=0.225,
             write=False,
             c_mode=True,
             sigma_thr=2.5,
             fragment_score=True,
             dist=5.0,
             atom_centre='CA',
             calc_metric='smoc',
             get_coord=True
             ):
        """Calculate the local Mander's Overlap for each residue in a protein
        model

        SMOC can be calculated in two ways:

            * **SMOCf**: The SMOC score is calculated for residues adjacent in
              sequence, using a sliding and overlapping window.
            * **SMOCd**: Pixels are scored in a spherical radius around each
              residue

        Arguments:
            map_target: Target Map Instance.
            resolution_densMap: Resolution of the target map.
            structure_instance: Model structure instance.
            win: Overlapping Window length to calculate the score
            rigid_body_file: Path to rigid-body file.
            sim_map: Precomputed simulated map. If :code:`None`, sim_map is
                calculated automatically.
            sigma_map: Parameter need for Structure Blurrer. Full explanation
                :ref:`here<Note on real space blurring:>`
            write: Deprecated, not used.
            c_mode: Deprecated, not used.
            sigma_thr: Parameter used to label pixels near each atom in the
                model. Explained in further detail
                :meth:`here <TEMPy.protein.structure_blurrer.StructureBlurrer.get_indices>`
            fragment_score: If True, use SMOCf method. If False, use SMOCd
                method.
            dist: Deprecated, not used.
            atom_centre: Which atom type should be considered the centre of
                residues.
            calc_metric: Which method to use for calculating the local score at
                each residue. Can be :code:`"smoc"` or :code:`"sccc"`
            get_coord: Return additional dict_chain_CA dictionary.

        Returns:
            Dictionary:
                The dictionaries dict_chain_scores, dict_chain_res.
                    dict_chain_CA is returned additionally if get_coord = True

                * dict_chain_scores: 2D dictionary containing the SMOC scores
                  for each residue. Keys are chain_label for first dictionary
                  and residue_number for second dictionary, e.g.:
                  :code:`dict_chain_scores[chain_label][residue_number] = SMOC_score`

                * dict_chain_res: Dictionary with chain labels (e.g.
                  :code:`"A"`) as keys and a list of all residue numbers for
                  a given chain as values.

                * dict_chain_CA: 2D dictionary containing a list for each
                  residue, containing the amino acid type of each residue and
                  its 3D coordinates. Keys are chain_label for first dictionary
                  and residue_number for second dictionary, e.g.:
                  :code:`dict_chain_CA[chain_label][residue_number] = residue_info`
                  where, :code:`residue_info = [residue_type, x, y, z]`
        """
        blurrer = StructureBlurrer()
        if sim_map is None:
            sim_map = blurrer.gaussian_blur_real_space(
                                                    structure_instance,
                                                    resolution_densMap,
                                                    densMap=map_target,
                                                    sigma_coeff=sigma_map,
                                                    normalise=True)
        # mask out background
        try:
            peak, ave, sigma = sim_map.peak_density()
            if peak >= ave - sigma and peak < (ave + 5 * sigma):
                sim_map.fullMap = sim_map.fullMap * (sim_map.fullMap > peak)
        except:  # noqa: E722
            pass

        dict_chain_indices, dict_chain_res, dict_chain_CA, gridtree = \
            blurrer.get_indices(
                                structure_instance,
                                map_target,
                                resolution_densMap,
                                sim_sigma_coeff=sigma_map,
                                sigma_thr=sigma_thr,
                                atom_centre=atom_centre)
        del structure_instance
        gc.collect()
        # get details of map
        nz, ny, nx = map_target.fullMap.shape
        zg, yg, xg = np.mgrid[0:nz, 0:ny, 0:nx]
        # x y,z coordinates of the grid
        indi = list(zip(xg.ravel(), yg.ravel(), zg.ravel()))

        list_sccc = []
        # save scores for each chain and res
        dict_chain_scores = OrderedDict()
        for ch in dict_chain_indices:
            dict_res_scores = OrderedDict()
            dict_res_indices = dict_chain_indices[ch]
            # multi-chain rigid body parser
            if rigid_body_file is not None:
                dict_res_scores = self.smoc_score_rigid_bodies(
                                                dict_res_indices,
                                                rigid_body_file,
                                                ch,
                                                indi,
                                                map_target,
                                                sim_map)
            # for residues not in rigid bodies
            for res in dict_res_indices:
                # if not dict_res_scores.has_key(res):
                if res not in dict_res_scores:
                    if fragment_score:
                        try:
                            indices = self.smoc_get_indices_fragment_window(
                                                    dict_res_indices,
                                                    dict_chain_res,
                                                    ch,
                                                    res,
                                                    win)
                        except TypeError:
                            indices = []
                        # unusual cases
                        if len(indices) > 0 and len(indices) < 10:
                            try:
                                dict_res_scores[res] = \
                                    dict_res_scores[dict_chain_res[ch][dict_chain_res[ch].index(res)-1]]  # noqa: E501
                                try:
                                    dict_res_scores[res] = \
                                        (dict_res_scores[res] +
                                            dict_res_scores[dict_chain_res[ch][dict_chain_res[ch].index(res)+1]])/2.0  # noqa: E501
                                except (IndexError, KeyError):
                                    pass
                            except (IndexError, KeyError):
                                try:
                                    dict_res_scores[res] = \
                                        dict_res_scores[dict_chain_res[ch][dict_chain_res[ch].index(res)+1]]  # noqa: E501
                                except (IndexError, KeyError):
                                    dict_res_scores[res] = 0.0
                            continue
                    else:
                        indices = dict_res_indices[res][:]
                        # for lower resolutions calculate score in a sphere
                        if resolution_densMap > 3.5:
                            dist = 1.0*resolution_densMap
                            try:
                                indices_local = \
                                    self.smoc_get_indices_sphere(
                                                    gridtree,
                                                    dict_chain_CA[ch][res][1:],
                                                    dist=dist)
                                indices.extend(indices_local)
                            except (TypeError, KeyError):
                                pass

                    if len(indices) == 0:
                        print('Score calculation failed for: ', ch, res)
                        smoc = -1.0
                    else:
                        try:
                            ind_arrzyx = self.indices_smoc(indices, indi)
                            if calc_metric == 'smoc':
                                smoc = self.calc_moc(
                                                        ind_arrzyx,
                                                        sim_map,
                                                        map_target)
                            elif calc_metric == 'sccc':
                                smoc = self.calc_ccc(
                                                    ind_arrzyx,
                                                    sim_map,
                                                    map_target)
                        except IndexError:
                            smoc = 0.0
                    dict_res_scores[res] = smoc
                    # error in score calculation
                    if smoc == -1.0:
                        dict_res_scores[res] = 0.0
                        try:
                            dict_res_scores[res] = \
                                dict_res_scores[dict_chain_res[ch][dict_chain_res[ch].index(res)-1]]  # noqa: E501
                            try:
                                dict_res_scores[res] = \
                                    (dict_res_scores[res] +
                                        dict_res_scores[dict_chain_res[ch][dict_chain_res[ch].index(res)+1]])/2.0  # noqa: E501
                            except (IndexError, KeyError):
                                pass
                        except (IndexError, KeyError):
                            try:
                                dict_res_scores[res] = \
                                    dict_res_scores[dict_chain_res[ch][dict_chain_res[ch].index(res)+1]]  # noqa: E501
                            except (IndexError, KeyError):
                                dict_res_scores[res] = 0.0
                        continue

                    list_sccc.append(smoc)
            dict_chain_scores[ch] = OrderedDict()
            dict_chain_scores[ch] = dict_res_scores
        del gridtree
        del dict_chain_indices

        gc.collect()
        if get_coord:
            return dict_chain_scores, dict_chain_res, dict_chain_CA
        else:
            del dict_chain_CA
            return dict_chain_scores, dict_chain_res

    def _SMOC1(  # can we delete this?
            self,
            map_target,
            resolution_densMap,
            structure_instance,
            win=11,
            rigid_body_file=None,
            sigma_map=0.225,
            write=False,
    ):
        """
        Calculate Local cross correlation (Mander's Overlap)
        It is a local Overlap Coefficient calculated on atoms in sliding
        residue windows along the chain.

        Arguments:
            *map_target*
                Target Map Instance.
            *resolution_densMap*
                Parameter need for Structure Blurrer.
                Resolution of the target map.
            *structure_instance*
                Model structure instance.
            *win*
                Overlapping Window length to calculate the score
            *rigid_body_file*
                Rigid-body file.
            sigma_map: Parameter need for Structure Blurrer. Full explanation
                :ref:`here<Note on real space blurring:>`
        Return:
            Dictionary of smoc scores for residues in the chain
        """
        blurrer = StructureBlurrer()
        sim_map = blurrer.gaussian_blur_real_space(
            structure_instance,
            resolution_densMap,
            densMap=map_target,
            sigma_coeff=sigma_map,
            normalise=True,
        )
        peak, ave, sigma = sim_map._peak_density()
        # NOTE: filter background
        _, dict_res_indices, dict_res_dist = blurrer.get_indices(
            structure_instance,
            map_target,
            resolution_densMap
        )
        # get details of map
        # origin = map_target.origin
        # apix = map_target.apix
        # box_size = map_target.box_size()
        nz, ny, nx = map_target.fullMap.shape
        zg, yg, xg = np.mgrid[0:nz, 0:ny, 0:nx]
        indi = zip(xg.ravel(), yg.ravel(), zg.ravel())

        # save rigid body details
        dict_rf_res = {}
        dict_rf_sc = {}
        res_list = []
        rb_list = []
        list_sccc = []
        # save scores for each res
        dict_res_scores = {}
        r_ct = 0
        if rigid_body_file is not None:
            inp = open(rigid_body_file, 'r')
            for ln in inp:
                if ln[0] != '#':
                    score_indices = []
                    lrb = ln.split()
                    if len(lrb) == 0:
                        continue
                    r_ct += 1
                    res_list = []
                    rb_pairs = []
                    # get scores for each res and each rigid body
                    for i in range(max((len(lrb) / 2) - 1, 1)):
                        rb_pairs.append([int(lrb[2 * i]), int(lrb[2 * i + 1])])
                        # NOTE: wont work for insertion codes
                        for r in range(int(lrb[2 * i]), int(lrb[2*i + 1]) + 1):
                            score_indices.extend(dict_res_indices[r])
                            res_list.append(r)
                    rb_list.append(lrb)
                    dict_rf_res[r_ct] = rb_pairs
                    if len(score_indices) == 0:
                        dict_rf_sc[r_ct] = 0.0
                        for res in res_list:
                            dict_res_scores[res] = 0.0
                        continue

                    tmplist = score_indices[:]
                    setlist = set(tmplist)
                    score_indices = list(setlist)
                    sc_indices = []
                    for ii in score_indices:
                        sc_indices.append(indi[ii])
                    array_indices = np.array(sc_indices)
                    ind_arrxyz = np.transpose(array_indices)

                    ind_arrzyx = (ind_arrxyz[2], ind_arrxyz[1], ind_arrxyz[0])
                    sccc = self.calc_moc(ind_arrzyx, sim_map, map_target)
                    dict_rf_sc[r_ct] = sccc
                    # save scores
                    for res in res_list:
                        dict_res_scores[res] = sccc
                        list_sccc.append(sccc)
            inp.close()
        # for residues not in rigid bodies: consider pentapeptides
        for res in dict_res_indices:
            if res in dict_res_scores:
                indices = dict_res_indices[res][:]
                # consider residues on both sides. NOTE: wont work for
                # insertion codes!
                # need to rewite res numbers to avoid insertion codes
                for ii in range(1, int(round((win + 1) / 2))):
                    try:
                        indices.extend(dict_res_indices[res - ii])
                    except Exception:
                        pass
                for ii in range(1, int(round((win + 1) / 2))):
                    try:
                        indices.extend(dict_res_indices[res + ii])
                    except Exception:
                        pass

                tmplist = indices[:]
                setlist = set(tmplist)
                indices = list(setlist)
                sc_indices = []
                for ii in indices:
                    sc_indices.append(indi[ii])
                if len(indices) == 0:
                    dict_res_scores[res] = 0.0
                    continue
                array_indices = np.array(sc_indices)
                ind_arrxyz = np.transpose(array_indices)
                ind_arrzyx = (ind_arrxyz[2], ind_arrxyz[1], ind_arrxyz[0])
                sccc = self.calc_moc(ind_arrzyx, sim_map, map_target)
                dict_res_scores[res] = sccc
                list_sccc.append(sccc)
        return dict_res_scores

    def _get_shell(self, dist1, maxlevel, step, x):
        # indices between upper and lower shell bound
        return np.argwhere((dist1 < min(maxlevel, x + step)) & (dist1 >= x))

        # match power spectra for two maps
    def _amplitude_match(
            self,
            map_1,
            map_2,
            shellmin,
            shellmax,
            step=0.005,
            c1=0,
            c2=0,
            reso=None,
            lpfiltb=False,
            lpfilta=False,
            ref=False,
    ):
        """
        Scale amplitudes to the average in each resolutions shell

        Arguments:
            *step : shell width (1/A)
        """
        # fourier transform: use pyfftw if available
        pyfftw_flag = 1
        try:
            import pyfftw
        except ImportError:
            pyfftw_flag = 0
        try:
            if pyfftw_flag == 0:
                raise ImportError
            inputa1 = pyfftw.n_byte_align_empty(
                map_1.fullMap.shape,
                16,
                'complex128',
            )
            outputa1 = pyfftw.n_byte_align_empty(
                map_1.fullMap.shape,
                16,
                'complex128',
            )
            # fft planning, set planning_timelimit or flags to make it faster
            fft = pyfftw.FFTW(
                inputa1,
                outputa1,
                direction='FFTW_FORWARD',
                axes=(0, 1, 2),
                flags=['FFTW_ESTIMATE'],
            )
            inputa1[:, :, :] = map_1.fullMap[:, :, :]
            fft()
            ft1 = Map(
                fftshift(outputa1),
                map_1.origin,
                map_1.apix,
                map_1.filename,
                map_1.header[:],
            )
        except Exception:
            # use numpy fft instead
            ft1 = map_1.fourier_transform()
        try:
            if pyfftw_flag == 0:
                raise ImportError
            inputa2 = pyfftw.n_byte_align_empty(
                map_2.fullMap.shape,
                16,
                'complex128',
            )
            outputa2 = pyfftw.n_byte_align_empty(
                map_2.fullMap.shape,
                16,
                'complex128',
            )
            fft = pyfftw.FFTW(
                inputa2,
                outputa2,
                direction='FFTW_FORWARD',
                axes=(0, 1, 2),
                flags=['FFTW_ESTIMATE'],
            )
            inputa2[:, :, :] = map_2.fullMap[:, :, :]
            fft()
            ft2 = Map(
                fftshift(outputa2),
                map_2.origin,
                map_2.apix,
                map_2.filename,
                map_2.header[:],
            )
        except Exception:
            ft2 = map_2.fourier_transform()
        # low pass filter before scaling
        if reso is not None:
            cutoff1 = map_1.apix / float(reso)
            cutoff2 = map_2.apix / float(reso)
            if lpfiltb and not lpfilta:
                ft1._tanh_lowpass(cutoff1, fall=0.2, ftmap=True)
                ft2._tanh_lowpass(cutoff2, fall=0.2, ftmap=True)
        # size1 = max(map_1.x_size(),map_1.y_size(),map_1.z_size())
        dist1 = map_1._make_fourier_shell(1)/map_1.apix[0]
        # size2 = max(map_2.x_size(), map_2.y_size(), map_2.z_size())
        dist2 = map_2._make_fourier_shell(1) / map_2.apix[0]
        ft1_avg = []
        ft2_avg = []
        ft1_avg_new = []
        lfreq = []
        # select max spatial frequency to iterate to. low resolution map
        maxlevel = 0.5 / np.max((map_1.apix[0], map_2.apix[0]), axis=0)
        # loop over freq shells, shellwidth=0.005
        # for x in arange(0,maxlevel+step,step):
        nc = 0
        x = 0.0
        highlevel = x + step
        while (x < maxlevel):
            # print x,highlevel, maxlevel
            # indices between upper and lower shell bound
            fshells1 = ((dist1 < min(maxlevel, highlevel)) & (dist1 >= x))
            # radial average
            shellvec1 = ft1.fullMap[fshells1]
            # indices between upper and lower shell bound
            fshells2 = ((dist2 < min(maxlevel, highlevel)) & (dist2 >= x))
            # radial average
            shellvec2 = ft2.fullMap[fshells2]
            abs1 = abs(shellvec1)
            abs2 = abs(shellvec2)
            ns1 = len(np.nonzero(abs1)[0])
            ns2 = len(np.nonzero(abs2)[0])
            if ns1 < 10 or ns2 < 10:
                nc += 1
                highlevel = min(maxlevel, x + (nc + 1) * step)
                x = max(0.0, x - nc * step)
                continue
            else:
                nc = 0
            mft1 = np.mean(abs1)
            mft2 = np.mean(abs2)
            if mft1 == 0.0 and mft2 == 0.0:
                continue
            # sq of radial avg amplitude
            ft1_avg.append(np.log10(np.mean(np.square(abs1))))
            ft2_avg.append(np.log10(np.mean(np.square(abs2))))

            # scale to amplitudes of the ref map
            if ref:
                if mft1 == 0.0:
                    continue
                ft1.fullMap[fshells1] = shellvec1 * (mft2 / mft1)
            else:
                # replace with avg amplitudes for the two maps
                ft1.fullMap[fshells1] = shellvec1 * (mft2 + mft1) / (2 * mft1)
                ft2.fullMap[fshells2] = shellvec2 * (mft2 + mft1) / (2 * mft2)

            # new radial average (to check)
            mft1 = np.mean(abs(ft1.fullMap[fshells1]))
            ft1_avg_new.append(
                np.log10(
                    np.mean(
                        np.square(abs(ft1.fullMap[fshells1]))
                    )
                )
            )
            lfreq.append(highlevel)

            sampling_frq = highlevel

            cutoff_freq = min((1.0 / reso) + 0.25, maxlevel)

            # scale the rest and break after relevant frequencies
            if sampling_frq > cutoff_freq:
                fshells1 = (dist1 >= highlevel)
                shellvec1 = ft1.fullMap[fshells1]
                mft1 = np.mean(abs(shellvec1))
                fshells2 = (dist2 >= highlevel)
                shellvec2 = ft2.fullMap[fshells2]
                mft2 = np.mean(abs(shellvec2))
                if mft1 == 0.0 and mft2 == 0.0:
                    break
                ft1_avg.append(np.log10(np.mean(np.square(abs(shellvec1)))))
                ft2_avg.append(np.log10(np.mean(np.square(abs(shellvec2)))))

                if ref:
                    if mft1 == 0.0:
                        break
                    ft1.fullMap[fshells1] = shellvec1*(mft2/mft1)
                else:
                    ft1.fullMap[fshells1] = shellvec1*(mft2+mft1)/(2*mft1)
                    ft2.fullMap[fshells2] = shellvec2*(mft2+mft1)/(2*mft2)

                mft1 = np.mean(abs(ft1.fullMap[fshells1]))
                ft1_avg_new.append(
                    np.log10(
                        np.mean(
                            np.square(abs(ft1.fullMap[fshells1]))
                        )
                    )
                )
                lfreq.append((highlevel + step / 2))
                break
            x = highlevel
            highlevel = x + step
        # low pass filter after?
        # low pass filter before scaling
        if reso is not None:
            if lpfilta and not lpfiltb:
                ft1._tanh_lowpass(cutoff1, fall=0.2, ftmap=True)
                ft2._tanh_lowpass(cutoff2, fall=0.2, ftmap=True)
        try:
            if pyfftw_flag == 0:
                raise ImportError
            ifft = pyfftw.FFTW(
                inputa1,
                outputa1,
                direction='FFTW_BACKWARD',
                axes=(0, 1, 2),
                flags=['FFTW_ESTIMATE'],
            )
            inputa1[:, :, :] = ifftshift(ft1.fullMap)[:, :, :]
            ifft()
            map1_filt = Map(
                outputa1.real.astype('float'),
                map_1.origin,
                map_1.apix,
                map_1.filename,
                map_1.header[:],
            )
        except Exception:
            # use numpy ifft instead
            map1_filt = map_1.copy()
            map1_filt.fullMap = np.real(ifftn(ifftshift(ft1.fullMap)))
        try:
            if pyfftw_flag == 0:
                raise ImportError
            ifft = pyfftw.FFTW(
                inputa2,
                outputa2,
                direction='FFTW_BACKWARD',
                axes=(0, 1, 2),
                flags=['FFTW_ESTIMATE'],
            )
            inputa2[:, :, :] = ifftshift(ft2.fullMap)[:, :, :]
            ifft()
            map2_filt = Map(
                outputa2.real.astype('float'),
                map_2.origin,
                map_2.apix,
                map_2.filename,
                map_2.header[:],
            )
        except Exception:
            map2_filt = map_2.copy()
            map2_filt.fullMap = np.real(ifftn(ifftshift(ft2.fullMap)))
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from matplotlib import pylab
            try:
                plt.style.use('ggplot')
            except AttributeError:
                pass
            plt.rcParams.update({'font.size': 18})
            plt.rcParams.update({'legend.fontsize': 18})
            plt.plot(lfreq, ft1_avg, 'r--', label='map1')
            plt.plot(lfreq, ft2_avg, 'bs', label='map2')
            plt.plot(lfreq, ft1_avg_new, 'g^', label='scaled')
            leg = plt.legend(loc='upper right')
            for legobj in leg.legendHandles:
                legobj.set_linewidth(2.0)
            pylab.savefig("spectra.png")
            plt.close()
        except Exception:
            pass
        return map1_filt.fullMap, map2_filt.fullMap

    def get_clash_map(self, emmap, apix):
        template_grid = emmap._make_clash_map(apix)
        return template_grid

    def get_sm_score(
            self,
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
        overlay_maplist = self.get_overlay_comp_maplist(struct, template_grid)
        nc = range(ncomp)
        cpair = list(itertools.combinations(nc, 2))
        score = 0.0
        n_overlap_voxel = 0
        overlap_volume = 0.0
        for i in cpair:
            n_overlap_voxel = (
                    overlay_maplist[i[0]].fullMap *
                    overlay_maplist[i[1]].fullMap
            ).sum()
            overlap_volume = ((apix.prod()) * n_overlap_voxel) * 2
            clash_percent = (
                float(overlap_volume / (cvol[i[0]] + cvol[i[1]]))
            )
            score = score + clash_percent
        return -(score)

    def get_overlay_comp_maplist(self, struct, template_grid):
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
        return overlay_maplist

    def calculate_alcps(self, ref_chain, probe_chain):
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

    def get_log10_alcps(self, ref_chain, probe_chain, lowest_value=-2):
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

        alcps = self.calculate_alcps(ref_chain, probe_chain)

        if alcps == 0.0:
            return lowest_value
        else:
            return math.log10(alcps)

    def _get_max_distance_between_residues(atoms):

        max_dist = 0
        atom_list = atoms[:]
        for atom in atoms:
            atom_list.pop(atom_list.index(atom))
            for atom2 in atom_list:
                vec = np.linalg.norm([atom.x, atom.y, atom.z],
                                     [atom2.x, atom2.y, atom2.z])
                if vec > max_dist:
                    max_dist = vec
        return max_dist

    def map_model_fsc_resolution(
                                self,
                                structure,
                                target_map,
                                map_resolution,
                                mask=None,
                                sim_map=None,
                                cutoff_correlation=0.5,
                                use_highest_resolution=True):
        """Calculate the Map-model "resolution" using Fourier Shell Correlation (FSC).

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

        fsc = self.map_model_fsc(structure, target_map, map_resolution,
                                 mask=mask, sim_map=sim_map)

        max_frequency_at_cutoff = fourier.get_fsc_resolution(
                                fsc,
                                fsc_threshold=cutoff_correlation,
                                interpolate_cutoff=False,
                                use_highest_resolution=use_highest_resolution
                                )

        return max_frequency_at_cutoff

    def map_model_fsc(self, structure, target_map, map_resolution, mask=None,
                      sim_map=None):
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

    def LoQFit(
            self,
            structure,
            target_map,
            resolution_map_target,
            sim_map=None,
            max_res=18.,
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
        print(f"Calculating LoQFit score for model {structure.filename} into "
              f"map {target_map.filename}")

        # set up some stuff
        target_map.apix = np.array(target_map.apix)
        blurrer = StructureBlurrer(with_vc=True)

        if sim_map is None:
            sim_map = blurrer.gaussian_blur_real_space(
                                                    structure,
                                                    resolution_map_target,
                                                    densMap=target_map)
        fsc_threshold = 0.5
        sim_map.normalise_to_1_minus1(in_place=True)
        target_map.normalise_to_1_minus1(in_place=True)

        # approximate mask sphere diameter
        sphere_diameter_angstroms = resolution_map_target * 5
        sphere_diameter_pixels = int(sphere_diameter_angstroms /
                                     target_map.apix[0])

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
                                    sphere_diameter_pixels + (2*cos_edge),
                                    target_map.fullMap.shape)

        if mask_dims == [0, 0, 0]:
            mask = Map(np.ones(target_map.fullMap.shape), target_map.origin,
                       target_map.apix, target_map.filename)
            mask_dims = mask.fullMap.shape
        else:
            centre_of_mask_map = [mask_dims[0]/2, mask_dims[1]/2,
                                  mask_dims[2]/2]
            mask = blurrer.make_spherical_mask(sphere_diameter_pixels,
                                               mask_dims, centre_of_mask_map,
                                               cos_edge)

        # save scores for each chain and res
        dict_res_scores = OrderedDict()
        chains = structure.split_into_chains()
        number_of_residues = structure.number_of_residues()

        # set up pyfftw for very fast ffts
        input1 = pyfftw.empty_aligned(mask_dims, dtype='float64')
        fftw_object1 = fourier.get_pyfftw_object(mask_dims)
        fftw_object2 = fourier.get_pyfftw_object(mask_dims)

        # precompute these to speed up calculations
        qbins, labelled_shells = fourier.get_labelled_shells(
            input1.shape)

        warnings = []
        res_no = 0

        for chain in chains:
            for atom in chain.atomList:
                if atom.atom_name == 'CA' or atom.atom_name == "C1'":
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
                    warnings.append(f"Warning: FSC at residue {atom.res_no} in"
                                    f" chain {atom.chain} never falls below "
                                    f"0.5. LoQFit score for this residue set "
                                    f"to {freq_at_corr_cutoff}. This is NOT "
                                    f"expected and NOT an indication of a "
                                    f"good fit between map and model.")

                # If there is poor correlation in low resolution shells the
                # freq_at_cutoff can be ridiculously high (i.e. >100 angstroms)
                # which ruins the scaling when the score is plotted
                if freq_at_corr_cutoff > max_res:
                    warnings.append(f"Warning: Residue {atom.res_no} in chain "
                                    f"{atom.chain} has local resolution of "
                                    f" {freq_at_corr_cutoff}, which is set "
                                    f"to {max_res}")
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

                dict_res_scores[(atom.chain, int(atom.res_no))] = \
                    freq_at_corr_cutoff

                res_no += 1
                if verbose:
                    zfill_len = len(str(number_of_residues))
                    print(f"\rProcessed residue {str(res_no).zfill(zfill_len)}"
                          f"/{number_of_residues}", sep='', end='', flush=True)

        if verbose:
            print("")
            for warning in warnings:
                print(warning)

        return dict_res_scores

    def map_local_resolution(
                            self,
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
        print(f"Calculating Local Resolution for half map:"
              f"{half_map_1.filename} and map {half_map_2.filename}")

        # set up some stuff
        apix = np.array(half_map_1.apix)[0]
        map_res = self.map_resolution_FSC(half_map_1, half_map_2)
        blurrer = StructureBlurrer()

        # approximate mask sphere diameter
        sphere_diameter_angstroms = map_res * 7
        sphere_diameter_pixels = int(sphere_diameter_angstroms/apix)

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
            mask = Map(np.ones(half_map_1.fullMap.shape), half_map_1.origin,
                       half_map_1.apix, half_map_1.filename)
            mask_dims = mask.fullMap.shape
        else:
            centre_of_mask_map = [mask_dims[0]/2, mask_dims[1]/2,
                                  mask_dims[2]/2]
            mask = blurrer.make_spherical_mask(sphere_diameter_pixels,
                                               mask_dims, centre_of_mask_map,
                                               cos_edge)

        # save scores for each chain and res
        dict_res_scores = OrderedDict()

        # set up pyfftw for very fast ffts
        input1 = pyfftw.empty_aligned(mask_dims, dtype='float64')

        fftw_object1 = fourier.get_pyfftw_object(mask_dims)
        fftw_object2 = fourier.get_pyfftw_object(mask_dims)

        qbins, labelled_shells = fourier.get_labelled_shells(
            input1.shape)

        # get coordinates where local FSC should be calculated
        if structure is not None:
            coordinates = structure.get_CAonly().get_atom_zyx_map_indexes(
                half_map_1)
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
                warnings.append(f"Warning: FSC at coordinate {coordinate}"
                                f" never falls below 0.5. SLRS "
                                f"score for this residue set to "
                                f"{freq_at_corr_cutoff}. This is NOT "
                                f"expected and NOT an indication of a good "
                                f"fit between map and model.")

            dict_res_scores[tuple(coordinate)] = freq_at_corr_cutoff

            n += 1
            if verbose:
                zfill_len = len(str(len(coordinates)))
                print(f"\rProcessed residue {str(n).zfill(zfill_len)}"
                      f"/{len(coordinates)}", sep='', end='', flush=True)

        if verbose:
            print("")
            for warning in warnings:
                print(warning)

        return dict_res_scores

    def map_resolution_FSC(self, half_map1, half_map2, mask=None,
                           fsc_threshold=0.143, use_highest_resolution=True):
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
                                                pixel_size=half_map1.apix[0],)
        else:
            fsc = fourier.calculate_fsc(half_map1.fullMap,
                                        half_map2.fullMap,
                                        pixel_size=half_map1.apix[0],)

        resolution = fourier.get_fsc_resolution(
            fsc, fsc_threshold=fsc_threshold,
            use_highest_resolution=use_highest_resolution,
            interpolate_cutoff=False)

        return resolution


class SlidingResidueWindow:
    def __init__(self, accumulator):
        self.accumulator = accumulator

    def scores(self, residue_atoms_list, size):
        self.accumulator.zero()

        half_window = int((size - 1) / 2)

        scores = []
        for head in range(0, len(residue_atoms_list) + half_window):
            tail = head - size

            # While the head is with in the allowed range, use all the voxels
            # associated with the residues atoms.
            if head < len(residue_atoms_list):
                for atom in residue_atoms_list[head]:
                    self.accumulator.add_atom(atom)

            # Drop the tail if it within the range of residues.
            if tail >= 0:
                for atom in residue_atoms_list[tail]:
                    self.accumulator.del_atom(atom)

            # Extract the SMOC score
            if head - half_window >= 0:
                scores.append(self.accumulator.get_val())

        return scores


class _AbstractSlidingScore:
    def __init__(self, struct, accumulator):
        mapping = {}
        for a in struct.atomList:
            if mapping.get(a.chain) is None:
                mapping[a.chain] = {}
            if mapping[a.chain].get(a.res_no) is None:
                mapping[a.chain][a.res_no] = []
            mapping[a.chain][a.res_no].append(a)
        self.mapping = mapping
        self.slider = SlidingResidueWindow(accumulator)

    def _get_contigs(self, chain):
        contigs = [[]]
        for res_num in self.mapping[chain]:
            last = contigs[-1]
            if len(last) == 0:
                last.append(res_num)
            else:
                if last[-1] + 1 == res_num:
                    last.append(res_num)
                else:
                    contigs.append([res_num])
        return contigs

    def score_chain_contig(self, chain, size):
        """Generate sliding window scores where windows do not span chain breaks."

        This method computes sliding windows over each contiguous region of the chain.

        Args:
           chain (str): The chain name to generate window scores.
           size (int): The size of the window. Should be an odd number.
        Returns:
           A dictionary mapping each residue to its score.
        """

        scores = {}

        res_mapping = self.mapping[chain]
        contigs = self._get_contigs(chain)

        for contig in contigs:
            residue_atoms_list = [res_mapping[r] for r in contig]
            contig_scores = self.slider.scores(residue_atoms_list, size)
            for k, v in zip(contig, contig_scores):
                scores[k] = v

        return scores

    def score_chain_span(self, chain, size):
        """Generate sliding window scores where windows do span chain breaks.

        This method ignores any breaks in the chain, so windows may include distant residues.

        Args:
           chain (str): The chain name to generate window scores.
           size (int): The size of the window. Should be an odd number.
        Returns:
           A dictionary mapping each residue to its score.
        """
        residue_mapping = self.mapping[chain]
        residue_atoms_list = list(residue_mapping.values())
        numbers = residue_mapping.keys()
        scores = self.slider.scores(residue_atoms_list, size)

        return {k: v for k, v in zip(numbers, scores)}


class _Accumulator:
    """An accumulator computes a score over a sliding window of atoms"""

    def add_atom(self, atom):
        pass

    def del_atom(self, atom):
        pass

    def get_val(self):
        pass

    def zero(self):
        pass


class _MOCAccumulator(_Accumulator):
    """Placeholder docstring
    """

    def __init__(self, exp_map, sim_map, radius):
        from math import ceil, log, pow
        import voxcov as vc

        max_dim = max(exp_map.box_size())
        next_pow2 = int(pow(2, ceil(log(max_dim) / log(2))))
        self.radius = radius

        self.moc = vc.SMOC(
            exp_map.apix,
            exp_map.origin,
            next_pow2,
            [exp_map.x_size(), exp_map.y_size(), exp_map.z_size()],
            np.ascontiguousarray(exp_map.fullMap, dtype="float64"),
            np.ascontiguousarray(sim_map.fullMap, dtype="float64"),
        )

    def add_atom(self, atom):
        self.moc.add_sphere([atom.x, atom.y, atom.z], self.radius)

    def del_atom(self, atom):
        self.moc.del_sphere([atom.x, atom.y, atom.z], self.radius)

    def get_val(self):
        return self.moc.get_val()

    def zero(self):
        self.moc.zero()


class _MIAccumulator(_Accumulator):
    """Incremental calculation of MI score over voxels
    covered by atoms."""

    def __init__(self, exp_map, sim_map, radius, x_bins, y_bins):
        from math import ceil, log, pow
        import voxcov as vc

        max_dim = max(exp_map.box_size())
        next_pow2 = int(pow(2, ceil(log(max_dim) / log(2))))
        self.radius = 3
        self.exp_map = exp_map
        self.sim_map = sim_map

        self.mi = vc.SMI(
            exp_map.apix,
            exp_map.origin,
            next_pow2,
            [exp_map.x_size(), exp_map.y_size(), exp_map.z_size()],
            np.ascontiguousarray(sim_map.fullMap, dtype="float64"),
            np.ascontiguousarray(exp_map.fullMap, dtype="float64"),
            np.min(exp_map.fullMap),
            np.max(exp_map.fullMap),
            np.min(sim_map.fullMap),
            np.max(sim_map.fullMap),
            x_bins, y_bins
        )

    def add_atom(self, atom):
        self.mi.add_sphere(
            [atom.x, atom.y, atom.z],
            self.radius,
        )

    def del_atom(self, atom):
        self.mi.del_sphere(
            [atom.x, atom.y, atom.z],
            self.radius,
        )

    # Not strictly essential, but I should add zeroing to DiffMap in voxcov.
    def zero(self):
        self.mi.zero()

    # Return current MI value
    def get_val(self):
        return self.mi.get_val()


class LocalMI(_AbstractSlidingScore):
    """
    """
    def __init__(self, struct, exp_map, sim_map, resolution, radius, no_bins=20):
        sigma_coeff=0.225

        self.exp_map = exp_map
        self.sim_map = sim_map
        self.radius = radius
        self.no_bins = no_bins

        if sim_map is None:
            sim_map = StructureBlurrer().gaussian_blur_real_space(
                    struct,
                    resolution,
                    exp_map,
                    sigma_coeff=sigma_coeff
            )

        mi = _MIAccumulator(exp_map, sim_map, radius, no_bins, no_bins)
        super().__init__(struct, mi)


class FastSMOC(_AbstractSlidingScore):
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
        locres=None,
    ):
        radius = sigma_threshold * max(sigma_coeff * resolution, 1.0)
        if sim_map is None:
            sim_map = StructureBlurrer(locres=locres).gaussian_blur_real_space(
                    struct,
                    resolution,
                    exp_map,
                    sigma_coeff=sigma_coeff
            )

        moc = _MOCAccumulator(exp_map, sim_map, radius)
        super().__init__(struct, moc)


class FastSCCC:
    def __init__(
            self,
            structure,
            map_target,
            resolution,
            sigma_coeff=0.225,
    ):
        """Calculate local cross-correlation for a segment of a protein model.

        Args:
            structure: The entire atomic structure
            map_target: An experimental map.
            resolution: The sesolution of the experimental map.
            sigma_coeff: The sigma coefficient for blurring.
                :ref:`here<Note on real space blurring:>`
        Returns:
            A SCCC object.
        """
        self.blurrer = StructureBlurrer()
        self.scorer = ScoringFunctions()
        self.map_target = map_target
        self.resolution = resolution
        self.sigma_coeff = sigma_coeff
        self.whole_sim_map = self.blurrer.gaussian_blur_real_space(
            structure,
            resolution,
            densMap=map_target,
            sigma_coeff=sigma_coeff,
            normalise=True,
        )

    def score_segment(self, segment_structure):
        """Score a segment of the structure.

        Args:
            segment: An atomic structure which should be a component
        Returns:
            CCC score: (float)
        """
        segment_sim_map = self.blurrer.gaussian_blur_real_space(
            segment_structure,
            self.resolution,
            self.map_target,
            self.sigma_coeff,
            normalise=True,
        )
        minDens = segment_sim_map.std()
        segment_mask = segment_sim_map._get_maskArray(minDens)
        target_masked = self.map_target._get_maskMap(segment_mask)
        sim_masked = self.whole_sim_map._get_maskMap(segment_mask)
        sse, _ = self.scorer.CCC_map(target_masked, sim_masked, cmode=False)
        return sse
