"""
Module with the `Filter` class.

:class:`Filter`: Object pointing to map data and holds
                 a set of methods for filtering MRC format maps.
"""
import copy
import os
import math

import numpy as np
from scipy.ndimage import measurements, gaussian_filter

from TEMPy.map_process.process import MapEdit

# For CCP-EM mac install.
try:
    from TEMPy.graphics.show_plot import Plot
except RuntimeError:
    Plot = None

try:
    import pyfftw

    pyfftw_flag = True
except ImportError:
    print(
        """pyFFTw package not found, using np.fft functions instead. To
install pyFFTw run; pip install pyFFTw"""
    )
    pyfftw_flag = False


class Filter(MapEdit):
    def __init__(self, MapInst, datacopy=True):
        if type(MapInst) is MapEdit or type(MapInst) is Filter:
            if not datacopy:
                self.__dict__ = MapInst.__dict__.copy()
            else:
                self.__dict__ = copy.deepcopy(MapInst.__dict__.copy())
        else:
            super(Filter, self).__init__(MapInst)

        # Allows testing numpy vs pyFFTw methods
        if pyfftw_flag:
            self.pyfftw_flag = True
        else:
            self.pyfftw_flag = False

    def copy(self, deep=True):
        """
        Copy contents to a new object
        """
        # create MapEdit object
        copymap = self.__class__(self.mrc)
        copymap.origin = copy.deepcopy(self.origin)
        if deep:
            copymap.fullMap = self.fullMap.copy()
        else:
            copymap.fullMap = self.fullMap
        copymap.apix = copy.deepcopy(self.apix)
        copymap.dim = copy.deepcopy(self.dim)
        return copymap

    def label_patches(self, contour, prob=0.1, inplace=False):
        """
        Remove small isolated densities
        Arguments:
            *contour*
                map threshold
            *prob*
                fraction of a size (+-) among all sizes
        """
        fp = self.grid_footprint()
        binmap = self.fullMap > float(contour)
        label_array, labels = measurements.label(
            self.fullMap * binmap,
            structure=fp,
        )
        sizes = measurements.sum(binmap, label_array, range(labels + 1))

        if labels <= 10:
            m_array = sizes < 0.05 * sizes.max()
            ct_remove = np.sum(m_array)
            remove_points = m_array[label_array]
            label_array[remove_points] = 0
            if inplace:
                self.fullMap[:] = (label_array > 0) * (self.fullMap * binmap)
            else:
                newmap = self.copy()
                newmap.fullMap[:] = (label_array > 0) * (self.fullMap * binmap)
                return newmap, labels - ct_remove
            return labels - ct_remove + 1

        means = measurements.mean(
            self.fullMap * binmap,
            label_array,
            range(labels + 1),
        )
        freq, bins = np.histogram(sizes[1:], 20)

        m_array = np.zeros(len(sizes))
        ct_remove = 0
        for i in range(len(freq)):
            fr = freq[i]
            s2 = bins[i + 1]
            s1 = bins[i]
            p_size = float(fr) / float(np.sum(freq))
            if p_size > prob:
                m_array = m_array + (
                    (sizes >= s1)
                    & (sizes < s2)
                    & (
                        means
                        < (
                            float(contour)
                            + 0.35 * (np.amax(self.fullMap) - float(contour))
                        )
                    )
                )
                ct_remove += 1
        m_array = m_array > 0
        remove_points = m_array[label_array]

        label_array[remove_points] = 0
        if inplace:
            self.fullMap[:] = (label_array > 0) * (self.fullMap * binmap)
        else:
            newmap = self.copy()
            newmap.fullMap[:] = (label_array > 0) * (self.fullMap * binmap)
            return newmap, labels - ct_remove
        return labels - ct_remove

    def make_fourier_shell(
        self, map_shape, keep_shape=False, normalise=True, fftshift=True
    ):
        """
        For a given grid, make a grid with sampling
        frequencies in the range (0:0.5)
        Return:
            grid with sampling frequencies
        """
        z, y, x = map_shape
        # numpy fftfreq : odd-> 0 to (n-1)/2 & -1 to -(n-1)/2 and
        # even-> 0 to n/2-1 & -1 to -n/2 to check with eman
        # set frequencies in the range -0.5 to 0.5
        if keep_shape:
            rad_z, rad_y, rad_x = np.mgrid[
                -np.floor(z / 2.0) : np.ceil(z / 2.0),
                -np.floor(y / 2.0) : np.ceil(y / 2.0),
                -np.floor(x / 2.0) : np.ceil(x / 2.0),
            ]
            if not fftshift:
                rad_x = np.fft.ifftshift(rad_x)
        # r2c arrays from fftw/numpy rfft
        else:
            rad_z, rad_y, rad_x = np.mgrid[
                -np.floor(z / 2.0) : np.ceil(z / 2.0),
                -np.floor(y / 2.0) : np.ceil(y / 2.0),
                0 : np.floor(x / 2.0) + 1,
            ]
        if not fftshift:
            rad_z = np.fft.ifftshift(rad_z)
            rad_y = np.fft.ifftshift(rad_y)
        if normalise:
            rad_z = rad_z / float(np.floor(z))
            rad_y = rad_y / float(np.floor(y))
            rad_x = rad_x / float(np.floor(x))
        rad_x = rad_x ** 2
        rad_y = rad_y ** 2
        rad_z = rad_z ** 2
        dist = np.sqrt(rad_z + rad_y + rad_x)
        return dist

    def fourier_transform(self, keep_shape=False, new_inparray=False):
        """
        pythonic FFTs for maps
        """
        ftarray = self.calculate_fft(
            self.fullMap, keep_shape=keep_shape, new_inparray=new_inparray
        )
        ftmap = self.copy(deep=False)
        ftmap.fullMap = ftarray
        # TODO: header not set
        # ftmap.set_dim_apix(ftmap.apix)
        # ftmap.update_header()
        return ftmap

    def calculate_fft(self, arr, keep_shape=False, new_inparray=False):

        if self.pyfftw_flag:
            fft, fftoutput, inputarray = self.plan_fft(
                arr, keep_shape=keep_shape, new_inparray=new_inparray
            )
            inputarray[:, :, :] = arr
            fft()
        else:
            print("pyFFTw not found, using numpyFT")
            # TODO: warning raises error in tasks
            # warnings.warn("PyFFTw not found!, using numpy fft")
            if not keep_shape:
                fftoutput = np.fft.rfftn(arr)
            else:
                fftoutput = np.fft.fftn(arr)
        return fftoutput

    def plan_fft(self, arr, keep_shape=False, new_inparray=False):

        input_dtype = str(arr.dtype)
        if not keep_shape:
            output_dtype = "complex64"
            if input_dtype not in ["float32", "float64", "longdouble"]:
                input_dtype = "float32"
            elif input_dtype == "float64":
                output_dtype = "complex128"
            elif input_dtype == "longdouble":
                output_dtype = "clongdouble"
            # for r2c transforms:
            output_array_shape = arr.shape[: len(arr.shape) - 1] + (
                arr.shape[-1] // 2 + 1,
            )
        else:
            output_dtype = "complex64"
            output_array_shape = arr.shape

        fftoutput = pyfftw.n_byte_align_empty(
            output_array_shape, n=16, dtype=output_dtype
        )
        # check if array is byte aligned
        # TODO: can we read the map file as byte aligned?
        if new_inparray or not pyfftw.is_byte_aligned(arr):
            inputarray = pyfftw.empty_aligned(
                arr.shape,
                n=16,
                dtype=input_dtype,
            )
            fft = pyfftw.FFTW(
                inputarray,
                fftoutput,
                direction="FFTW_FORWARD",
                axes=(0, 1, 2),
                flags=["FFTW_ESTIMATE"],
            )
        elif pyfftw.is_byte_aligned(arr):
            fft = pyfftw.FFTW(
                arr,
                fftoutput,
                direction="FFTW_FORWARD",
                axes=(0, 1, 2),
                flags=["FFTW_ESTIMATE"],
            )
            inputarray = arr

        return fft, fftoutput, inputarray

    def inv_fourier_transform(
        self,
        ftmap,
        output_dtype=None,
        output_shape=None,
    ):
        """
        Calculate inverse fourier transform
        """
        invftarray = self.calculate_ifft(
            ftmap.fullMap,
            output_shape=output_shape,
            inplace=False,
            new_inparray=False,
        )
        invftmap = self.copy(deep=False)
        invftmap.fullMap = invftarray
        return invftmap

    def calculate_ifft(
        self,
        arr,
        output_shape=None,
        inplace=False,
        new_inparray=False,
    ):
        """
        Calculate inverse fourier transform
        """
        if self.pyfftw_flag:
            ifft, output_array, inputarray = self.plan_ifft(
                arr, output_shape=output_shape, new_inparray=new_inparray
            )
            # r2c fft
            ifft()
        else:
            # TODO: warnings raises error in tasks
            # warnings.warn("PyFFTw not found!, using numpy fft")
            if output_shape is None or output_shape[-1] // 2 + 1 == arr.shape[-1]:
                output_array = np.fft.irfftn(arr, s=output_shape)
            else:
                output_array = np.real(np.fft.ifftn(arr))
        del arr
        return output_array.real.astype(np.float32, copy=False)

    def plan_ifft(
        self,
        arr,
        output_shape=None,
        output_array_dtype=None,
        new_inparray=False,
    ):
        input_dtype = str(arr.dtype)
        #         #for c2r transforms:
        #             if output_shape is None: output_shape = \
        #                                     arr.shape[:len(arr.shape)-1]+\
        #                                     ((arr.shape[-1] - 1)*2,)
        if output_array_dtype is None:
            output_array_dtype = "float32"
        if output_shape is None:
            output_shape = arr.shape[: len(arr.shape) - 1] + ((arr.shape[-1] - 1) * 2,)
            if input_dtype not in ["complex64", "complex128", "clongdouble"]:
                input_dtype = "complex64"
            elif input_dtype == "complex128":
                output_array_dtype = "float64"
            elif input_dtype == "clongdouble":
                output_array_dtype = "longdouble"
        elif output_shape[-1] // 2 + 1 == arr.shape[-1]:
            if input_dtype not in ["complex64", "complex128", "clongdouble"]:
                input_dtype = "complex64"
            elif input_dtype == "complex128":
                output_array_dtype = "float64"
            elif input_dtype == "clongdouble":
                output_array_dtype = "longdouble"
        else:
            output_shape = arr.shape
            output_array_dtype = "complex64"

        output_array = pyfftw.empty_aligned(
            output_shape, n=16, dtype=output_array_dtype
        )
        # check if array is byte aligned
        if new_inparray or not pyfftw.is_byte_aligned(arr):
            inputarray = pyfftw.n_byte_align_empty(
                arr.shape,
                n=16,
                dtype=input_dtype,
            )
            ifft = pyfftw.FFTW(
                inputarray,
                output_array,
                direction="FFTW_BACKWARD",
                axes=(0, 1, 2),
                flags=["FFTW_ESTIMATE"],
            )
            inputarray[:, :, :] = arr
        else:
            ifft = pyfftw.FFTW(
                arr,
                output_array,
                direction="FFTW_BACKWARD",
                axes=(0, 1, 2),
                flags=["FFTW_ESTIMATE"],
            )
            inputarray = arr

        return ifft, output_array, inputarray

    def fourier_filter(
        self,
        ftfilter,
        inplace=False,
        plot=False,
        plotfile="plot",
        keep_shape=False,
    ):
        """
        Apply lowpass/highpass/bandpass filters in fourier space

        ftfilter: filter applied on the fourier grid
        """

        ftmap = self.fourier_transform(keep_shape=keep_shape)
        # shift zero frequency to the center
        if not keep_shape:
            # shift zero frequency to the center and apply the filter
            ftmap.fullMap[:] = np.fft.fftshift(ftmap.fullMap, axes=(0, 1))
        else:
            ftmap.fullMap[:] = np.fft.fftshift(ftmap.fullMap)

        if plot:
            dict_plot = {}
            lfreq, shell_avg = self.get_raps(ftmap.fullMap)
            dict_plot["map"] = [lfreq[:], shell_avg[:]]

        # apply the filter
        ftmap.fullMap[:] = ftmap.fullMap * ftfilter
        if plot:
            lfreq, shell_avg = self.get_raps(ftmap.fullMap)
            dict_plot["filtered"] = [lfreq, shell_avg]
            self.plot_raps(dict_plot, plotfile=plotfile)
        if not keep_shape:
            # shift zero frequency to the center and apply the filter
            ftmap.fullMap[:] = np.fft.ifftshift(ftmap.fullMap, axes=(0, 1))
        else:
            ftmap.fullMap[:] = np.fft.ifftshift(ftmap.fullMap)
        invftmap = self.inv_fourier_transform(
            ftmap,
            output_shape=self.fullMap.shape,
        )
        if inplace:
            self.fullMap = invftmap.fullMap
        else:
            newmap = self.copy(deep=False)
            newmap.fullMap = invftmap.fullMap
            return newmap

    @staticmethod
    def apply_filter(ftmap, ftfilter, inplace=False):
        # fftshifted ftmap
        if inplace:
            ftmap.fullMap[:] = ftmap.fullMap * ftfilter
            return ftmap
        else:
            filteredmap = ftmap.copy()
            filteredmap.fullMap[:] = ftmap.fullMap * ftfilter
            return filteredmap

    def softmask_edges(self, window=3, inplace=False):
        newarray = self.softmask_gaussian(self.fullMap, sigma=1)
        if inplace:
            self.fullMap[:] = newarray
        else:
            newmap = self.copy()
            newmap.fullMap = newarray
            return newmap

    def softmask_gaussian(arr, sigma=1):
        newarray = np.copy(arr)
        bin_arr = arr > 0.0
        newarray[:] = gaussian_filter(
            newarray,
            sigma=sigma,
            mode="constant",
            cval=0.0,
        )
        newarray[bin_arr] = arr[bin_arr]
        return newarray

    def get_raps(self, ftmap, step=0.02):
        """
        Get rotationally averaged power spectra from fourier (filtered) map

        ftmap : fourier map (e.g. with any filter appied)
        step : frequency shell width [0:0.5]
        """
        dist = self.make_fourier_shell(ftmap.shape, keep_shape=True) / max(self.apix)

        maxlevel = 0.5 / max(self.apix)
        step = step / max(self.apix)
        x = 0.0
        nc = 0
        shell_avg = []
        lfreq = []
        highlevel = x + step
        while x <= maxlevel - step:
            fshells = (dist < min(maxlevel, highlevel)) & (dist >= x)
            try:
                shellvec = np.take(ftmap.ravel(), np.where(fshells.ravel()))
            except:  # noqa:E722
                shellvec = ftmap[fshells]

            shellabs = abs(shellvec)
            nshellzero = len(np.flatnonzero(shellabs))

            if nshellzero < 5:
                if highlevel == maxlevel:
                    break
                nc += 1
                highlevel = min(maxlevel, x + (nc + 1) * step)
                continue
            else:
                nc = 0
            shell_avg.append(np.log10(np.mean(np.square(shellabs))))
            lfreq.append((x + (highlevel - x) / 2.0))
            x = highlevel
            highlevel = x + step
        del fshells, shellvec, shellabs
        return lfreq, shell_avg

    @staticmethod
    def plot_raps(dict_plot, plotfile="plot"):
        if Plot is not None:
            plt = Plot()
            plt.lineplot(dict_plot, plotfile)

    def tanh_lowpass(self, map_shape, cutoff, fall=0.3, keep_shape=False):
        """
        Lowpass filter with a hyperbolic tangent function

        cutoff: high frequency cutoff [0:0.5]
        fall: smoothness of falloff [0-> tophat,1.0-> gaussian]
        Return:
            tanh lowpass filter to apply on fourier map
        """

        # e.g cutoff = apix/reso is the stop band
        if fall == 0.0:
            fall = 0.01
        drop = math.pi / (2 * float(cutoff) * float(fall))
        cutoff = min(float(cutoff), 0.5)
        # fall determines smoothness of falloff, 0-> tophat, 1.0-> gaussian
        # make frequency shells
        dist = self.make_fourier_shell(
            map_shape,
            keep_shape=keep_shape,
            fftshift=True,
        )
        # dist_ini = dist.copy()
        # filter
        dist1 = dist + cutoff
        dist1[:] = drop * dist1
        dist1[:] = np.tanh(dist1)
        dist[:] = dist - cutoff
        dist[:] = drop * dist
        dist[:] = np.tanh(dist)
        dist[:] = dist1 - dist
        dist = 0.5 * dist
        del dist1
        return dist

    def tanh_bandpass(
        self,
        map_shape,
        low_cutoff=0.0,
        high_cutoff=0.5,
        low_fall=0.1,
        high_fall=0.1,
        keep_shape=False,
    ):
        """
        Bandpass filter with a hyperbolic tangent function
        low_cutoff: low frequency cutoff [0:0.5]
        high-cutoff : high frequency cutoff [0:0.5]
        fall: determines smoothness of falloff [0-> tophat,1.0-> gaussian]
        Return:
            tanh lowpass filter to apply on fourier map
        """
        low_drop = math.pi / (2 * float(high_cutoff - low_cutoff) * float(low_fall))
        high_drop = math.pi / (2 * float(high_cutoff - low_cutoff) * float(high_fall))

        dist = self.make_fourier_shell(
            map_shape,
            keep_shape=keep_shape,
            fftshift=True,
        )
        return 0.5 * (
            np.tanh(high_drop * (dist + high_cutoff))
            - np.tanh(high_drop * (dist - high_cutoff))
            - np.tanh(low_drop * (dist + low_cutoff))
            + np.tanh(low_drop * (dist - low_cutoff))
        )

    def butterworth_lowpass(self, map_shape, pass_freq, keep_shape=False):
        """
        Lowpass filter with a gaussian function
        pass_freq : low-pass cutoff frequency [0:0.5]
        """
        eps = 0.882
        a = 10.624
        # stop band frequency (used to determine the fall off)
        high_cutoff = 0.15 * math.log10(1.0 / pass_freq) + pass_freq

        fall = 2.0 * (
            math.log10(eps / math.sqrt(a ** 2 - 1))
            / math.log10(pass_freq / float(high_cutoff))
        )

        cutoff_freq = float(pass_freq) / math.pow(eps, 2 / fall)

        dist = self.make_fourier_shell(
            map_shape,
            keep_shape=keep_shape,
            fftshift=True,
        )
        # filter
        dist = dist / cutoff_freq
        return np.sqrt(1.0 / (1.0 + np.power(dist, fall)))

    def gauss_bandpass(self, map_shape, sigma, center=0.0, keep_shape=False):
        """
        Bandpass filter with a gaussian function
        sigma : cutoff frequency [0:0.5]
        """
        dist = self.make_fourier_shell(
            map_shape,
            keep_shape=keep_shape,
            fftshift=True,
        )
        # filter
        return np.exp(-((dist - center) ** 2) / (2 * sigma * sigma))

    def gauss_lowpass(self, map_shape, sigma, keep_shape=False):
        """
        Bandpass filter with a gaussian function
        sigma : cutoff frequency [0:0.5]
        """
        dist = self.make_fourier_shell(
            map_shape,
            keep_shape=keep_shape,
            fftshift=True,
        )
        # filter
        return np.exp(-(dist ** 2) / (2 * sigma * sigma))

    # added by Scott(SWH)
    def bfact_sharpen_blur(
        self,
        bfactor,
        map_shape,
        keep_shape=False,
        resocut=2.0,
    ):
        """
        Filter to sharpen/blur map with a global B-factor value
        Arguments:
            bfactor : global B-factor value to apply to sharpen/blur map;
                      negative value to sharpen, positive value to blur
            map_shape : density map box size, grid shape
            keep_shape : boolean to keep grid shape, default=False
            resocut : resolution cutoff, high resolution cutoff to avoid
                      getting artifacts when applying sharpening to high
                      resolution parts
        Return:
            Filter to sharpen/blur map
        """
        dist = self.make_fourier_shell(
            map_shape,
            keep_shape=keep_shape,
            fftshift=True,
        )
        bfactor = float(bfactor)
        if bfactor < 0.0:
            # high resolution resolution cutoff
            # to avoid getting artifacts when applying sharpening
            # to high resolution parts
            cutoff = min(1.0 / float(resocut), 0.5)
            dist = np.where(dist < cutoff, dist, 0.0)
        dist2 = dist ** 2
        return np.exp(-1.0 * (bfactor * 0.25 * dist2))


if __name__ == "__main__":
    import mrcfile

    mapfile = "/Users/agnel/data/map_model/gs/emd_3061.map"
    mrcobj = mrcfile.open(mapfile, mode="r+")
    mrcfilt = Filter(mrcobj)
    ftfilter = mrcfilt.tanh_lowpass(0.2, fall=0.5)
    mrcfilt.fourier_filter(ftfilter, plot=True, plotfile="tanh0_2f0_5")
    map_name = os.path.basename(os.path.splitext(mapfile)[0])
    map_dir = os.path.dirname(os.path.abspath(mapfile))
    newmap = mrcfile.new(
        os.path.join(map_dir, map_name + "_modified.mrc"), overwrite=True
    )
    mrcfilt.set_newmap_data_header(newmap)
    newmap.close()
