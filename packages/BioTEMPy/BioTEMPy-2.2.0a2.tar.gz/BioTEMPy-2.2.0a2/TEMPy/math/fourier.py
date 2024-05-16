# =============================================================================
#     This file is part of TEMPy.
#
#     TEMPy is a software designed to help the user in the manipulation
#     and analyses of macromolecular assemblies using 3D electron microscopy
#     maps.
#
#     Copyright 2015 Birkbeck College University of London.
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

import pyfftw
import numpy as np
from scipy import interpolate, ndimage


def get_labelled_shells(input_shape):
    """ Get labelled shells for the REAL-FT of a 3D volume

    Arguments:
        input_shape: Shape of the input 3D volume (before
        FT calculation)

    Returns:
        Labelled shells as a 3D numpy array with shape
        (Z, Y, (X / 2) + 1) for an input with shape
        (Z, Y, X). Labels are from 0, 1 ... N for N shells
        in the real FT.
    """

    n = max(input_shape)
    if n % 2 != 0:
        n -= 1

    x_shape = input_shape[2]
    y_shape = input_shape[1]
    z_shape = input_shape[0]

    # get the fourier frequencies in each dimension as a 3d grid
    qx_ = np.fft.rfftfreq(x_shape)
    qy_ = np.fft.fftfreq(y_shape)
    qz_ = np.fft.fftfreq(z_shape)
    qx, qy, qz = np.meshgrid(qz_, qy_, qx_, indexing='ij')

    # use the radius to calculate which fourier shell a given pixel is in
    qr = np.sqrt(qx**2+qy**2+qz**2)
    qmax = np.max(qr)
    qstep = np.min(qx_[qx_ > 0])
    nbins = int(qmax / qstep)
    qbins = np.linspace(0, nbins*qstep, nbins+1)

    # label the fourier shells from 0 -> n-1, where n is the no of shells
    qbin_labels = np.searchsorted(qbins, qr, "right")
    qbin_labels -= 1

    return qbins, qbin_labels


def get_fft_optimised_box_size(particle_diameter, map_box_size):
    """Get a box size which is optimal for fast FFT calculation

    Calculating the FFT using an optimised library should be
    fastest for boxes whose size is a power of two (e.g. 128,
    512, etc..]. FFT calculation will also be very fast for
    boxes with a size (N * 2^x) when N is a small number (e.g.
    3 or 5). However, calculating FFTs on boxes whose size is
    a prime number (e.g. 89), will be comparatively slow, so
    to speed this up (and more finely sample fourier space) we
    pad these boxes to an appropriate/optimised size, which
    in this case would be 96 (3 * 2^5).

    Arguments:
        particle_diameter: Length of particle (in pixels)
            along its longest axis
        map_box_size:

    Returns: Optimised cubic box size as a python list with
        len = 3.
    """
    power_two = 2
    power_three = 3
    power_five = 5

    while True:
        if particle_diameter <= power_two:
            box_size = power_two
            break
        elif particle_diameter <= power_three:
            box_size = power_three
            break
        elif particle_diameter <= power_five:
            box_size = power_five
            break
        else:
            power_two = power_two * 2
            power_three = power_three * 2
            power_five = power_five * 2

    # check if crop_box is bigger than full map
    for dim in map_box_size:
        if dim < box_size:
            return map_box_size

    return [box_size, box_size, box_size]


def get_pyfftw_object(
                        input_shape,
                        input_dtype='float64',
                        output_dtype='complex128',
                        ):
    """Get an pyFFTw object for very fast FFTs on 3D volumes

    By default, pyFFTw does real FFTs - therefore output shape is set to
    for (Z, Y, (X / 2) + 1) for an input volume with dimensions (Z, Y, X)

    More info can be found here: https://pyfftw.readthedocs.io/en/latest/source/tutorial.html#the-workhorse-pyfftw-fftw-class  # noqa: E501

    Arguments:
        input_shape: Shape of the input 3D array (before FT calculation)
        input_dtype: dtype of the input 3D array
        output_dtype: dtype of the output 3D array

    Returns:
        A pyFFTw object for forward FTs
    """
    input = pyfftw.empty_aligned(input_shape, dtype=input_dtype)
    output_shape = [
                    input_shape[0],
                    input_shape[1],
                    int((input_shape[2] / 2) + 1)
                    ]
    output = pyfftw.empty_aligned(output_shape, dtype=output_dtype)

    fftw_object = pyfftw.FFTW(input, output, axes=(0, 1, 2))

    return fftw_object


def get_pyifftw_object(
                        input_shape,
                        input_dtype='complex128',
                        output_dtype='float64',
                        ):
    """Get an pyFFTw object for very fast inverse FFTs on 3D volumes

    By default, pyFFTw does real FFTs - therefore output shape is set to
    for (Z, Y, (X - 1) * 2) for an input (FT'ed) array with
    dimensions (Z, Y, X)

    More info can be found here: https://pyfftw.readthedocs.io/en/latest/source/tutorial.html#the-workhorse-pyfftw-fftw-class  # noqa: E501

    Arguments:
        input_shape: Shape of the input 3D array (in fourier space)
        input_dtype: dtype of the input 3D array
        output_dtype: dtype of the output 3D array

    Returns:
        A pyFFTw object for forward FTs
    """
    input = pyfftw.empty_aligned(input_shape, dtype=input_dtype)
    output_shape = [
                    input_shape[0],
                    input_shape[1],
                    int((input_shape[2] - 1) * 2)
                    ]
    output = pyfftw.empty_aligned(output_shape, dtype=output_dtype)

    ifftw_object = pyfftw.FFTW(input, output, axes=(0, 1, 2),
                               direction='FFTW_BACKWARD')

    return ifftw_object


def calculate_fsc(
            map1,
            map2,
            pixel_size=1.,
            labelled_shells=None,
            qbins=None,
            fftw_object1=None,
            fftw_object2=None,
            ):
    """Calculate the Fourier Shell Correlation between two numpy arrays.

    Arguments:
        map1: 3D np.array of density values from first map
        map2: 3D np.array of density values from second map
        pixel_size: pixel sizes of the maps
        labelled_shells: Pre-calculated labelled fourier shells, if not
            explicitly supplied will be calculated on the fly
        qbins: Pre-calculated qbins, which are the frequencies of the
            labelled fourier components
        fftw_object1: pyFFTw object for fast FFT calculation for map1,
            if None then numpy.fft library used for calculations
        fftw_object2: pyFFTw object for fast FFT calculation for map2,
            if None then numpy.fft library used for calculations

    Returns:
        Fourier shell correlation as numpy array with shape
        (2, (X / 2) + 1) for inputs with shape (Z, Y, X). Array has
        values as:
                 [[shell frequency (in angstroms),  correlation],
                                ... N repeats ...
                  [shell frequency (in angstroms),  correlation]]
    """

    if labelled_shells is None or qbins is None:
        qbins, qbin_labels = get_labelled_shells(map1.shape)
    else:
        qbin_labels = labelled_shells

    if fftw_object1 and fftw_object2:
        F1 = fftw_object1(map1)
        F2 = fftw_object2(map2)
    else:
        F1 = np.fft.rfftn(map1)
        F2 = np.fft.rfftn(map2)

    numerator = ndimage.sum(np.real(F1*np.conj(F2)), labels=qbin_labels,
                            index=np.arange(0, qbin_labels.max()+1))
    term1 = ndimage.sum(np.abs(F1)**2, labels=qbin_labels,
                        index=np.arange(0, qbin_labels.max()+1))
    term2 = ndimage.sum(np.abs(F2)**2, labels=qbin_labels,
                        index=np.arange(0, qbin_labels.max()+1))

    denominator = (term1*term2)**0.5
    FSC = numerator/denominator
    qidx = np.where(qbins <= 0.5)

    frequencies = qbins[qidx]
    frequencies[0] = 1e-6  # suppress divide by zero warning
    frequencies = np.divide(pixel_size, frequencies)
    frequencies[0] = 1000.

    return np.vstack((frequencies, FSC[qidx])).T


def calculate_fsc_with_mask(
                            map1,
                            map2,
                            mask,
                            pixel_size=1.,
                            labelled_shells=None,
                            qbins=None,
                            fftw_object1=None,
                            fftw_object2=None,
                            ):
    """Calculate the Fourier Shell Correlation between two masked numpy
    arrays.

    Arguments:
        map1: 3D np.array of density values from first map
        map2: 3D np.array of density values from second map
        mask: 3d np.array of soft edged mask
        pixel_size: pixel sizes of the maps
        labelled_shells: Pre-calculated labelled fourier shells, if not
            explicitly supplied will be calculated on the fly
        qbins: Pre-calculated qbins, which are the frequencies of the
            labelled fourier components
        fftw_object1: pyFFTw object for fast FFT calculation for map1,
            if None then numpy.fft library used for calculations
        fftw_object2: pyFFTw object for fast FFT calculation for map2,
            if None then numpy.fft library used for calculations

    Returns:
        Fourier shell correlation as numpy array with shape
        (2, (X / 2) + 1) for inputs with shape (Z, Y, X). Array has
        values as:
                 [[shell frequency (in angstroms),  correlation],
                                ... N repeats ...
                  [shell frequency (in angstroms),  correlation]]
    """
    masked_map1 = map1 * mask
    masked_map2 = map2 * mask

    return calculate_fsc(masked_map1, masked_map2,
                         pixel_size=pixel_size, qbins=qbins,
                         labelled_shells=labelled_shells,
                         fftw_object1=fftw_object1,
                         fftw_object2=fftw_object2)


def get_fsc_resolution(
                        fsc,
                        fsc_threshold=0.5,
                        interpolate_cutoff=True,
                        use_highest_resolution=True,
                        ):
    """Gets the resolution from an fsc curve at a defined threshold.

    Arguments:
        fsc: np.array of fsc values
        fsc_threshold: Correlation threshold value that defines
            where the map resolution is found.
        interpolate_cutoff: Use linear interpolation to find the
            "exact" point in fourier space where the correlation
            equals the fsc_threshold value.
        use_highest_resolution: If True, takes the highest
            resolution shell that crosses the fsc_threshold, if
            there are multiple crossovers.

    Returns:
        The FSC resolution (in angstroms).
    """

    freq_at_cutoff = 0.0
    prev_fsc = [1001, 1.]
    for i in fsc:
        if i[1] < fsc_threshold and prev_fsc[1] > fsc_threshold:
            if interpolate_cutoff:
                interp_func = interpolate.interp1d(
                                                [i[1], prev_fsc[1]],
                                                [i[0], prev_fsc[0]])
                freq_at_cutoff = interp_func(fsc_threshold)
            else:
                freq_at_cutoff = prev_fsc[0]

            if not use_highest_resolution:
                break

        prev_fsc = i

    return float(freq_at_cutoff)
