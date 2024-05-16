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
import functools
import warnings

def new_score_location(func):
    @functools.wraps(func)
    def wrapped_warn_loc(*args, **kwargs):
        warnings.warn(f"Calling {func.__name__} as a method of the "
            f"ScoringFunctions class is deprecated, and will be obsolete "
            f"in TEMPy v3. You can call {func.__name__} directly with "
            f"TEMPy.protein.scoring_functions.{func.__name__}()",
            category=DeprecationWarning, stacklevel=1)
        return func(*args, **kwargs)
    return wrapped_warn_loc
