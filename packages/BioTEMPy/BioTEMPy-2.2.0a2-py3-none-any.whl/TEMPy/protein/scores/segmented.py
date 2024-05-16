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

import numpy as np
import TEMPy.protein.blur as blur
import TEMPy.protein.scores.glob as global_scores


class MaskedSegmentedScore:
    """TODO"""
    def __init__(self, structure, target_map, res_or_blurrer, scorer):
        self.target_map = target_map
        if isinstance(res_or_blurrer, blur.StructureBlurrer):
            self.blurrer = res_or_blurrer
        else:
            self.blurrer = blur.GlobalBlurrer(res_or_blurrer)
        self._whole_sim_map = self._simulate_map(structure)
        self.scorer = scorer

    def _simulate_map(self, structure):
        return self.blurrer.blur_structure(structure, self.target_map)

    # Default masking function is takes voxels above 1 std-dev.
    # Implement this to override.
    def _mask(self, segment_map):
        min_dens = segment_map.std()
        return segment_map.fullMap < min_dens

    def _mask_array(self, mask, array):
        return np.ma.masked_array(array, mask=mask).compressed()

    def score_segment(self, segment):
        segment_map = self._simulate_map(segment)
        mask = self._mask(segment_map)
        return self.scorer.score_arrays(
            self._mask_array(mask, self.target_map.fullMap), self._mask_array(mask, self._whole_sim_map.fullMap)
        )


class CCC(MaskedSegmentedScore):
    """TODO"""
    def __init__(self, structure, target_map, res_or_blurrer):
        super().__init__(structure, target_map, res_or_blurrer, global_scores.CCC())

class MOC(MaskedSegmentedScore):
    """TODO"""
    def __init__(self, structure, target_map, res_or_blurrer):
        super().__init__(structure, target_map, res_or_blurrer, global_scores.MOC())

class LAP(MaskedSegmentedScore):
    """TODO"""
    def __init__(self, structure, target_map, res_or_blurrer):
        super().__init__(structure, target_map, res_or_blurrer, global_scores.LaplaceCCC())

class MI(MaskedSegmentedScore):
    """TODO"""
    def __init__(self, structure, target_map, res_or_blurrer, mi = None):
        if mi is None:
            mi = global_scores.MI(bins1=20, bins2=20)
        super().__init__(structure, target_map, res_or_blurrer, mi)

