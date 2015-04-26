import numpy as np


def stft(s, time_range, window_size, window_step):
    """Short-time Fourier transform"""

    _validate_window_parameters(window_size, window_step)

    tmin, tmax, dt = time_range
    nspectrograms = int((tmax - tmin) / window_step - (window_size / window_step))
    samples_per_window = int(np.ceil(window_size / dt))

    data = np.zeros((nspectrograms, samples_per_window), dtype=np.complex)

    for i in range(nspectrograms):
        tlow = tmin + i * window_step
        thigh = tlow + window_size
        ts = np.linspace(tlow, thigh, samples_per_window)
        signal_data = s(ts)
        data[i, :] = np.fft.fft(signal_data)

    return data


def dstft(s, window_size, window_step):
    """Discrete Short-time Fourier transform"""

    _validate_window_parameters(window_size, window_step)

    nspectrograms = int((len(s) - window_size) // window_step + 1)

    data = np.zeros((nspectrograms, window_size), dtype=np.complex)

    for i in range(nspectrograms):
        low = i * window_step
        high = low + window_size
        signal_data = s[low:high]
        data[i, :] = np.fft.fft(signal_data)

    return data


def _validate_window_parameters(window_size, window_step):
    # Window should be at least connected to its neighbours.
    if window_size < window_step:
        raise RuntimeError('Window size must be larger than window step')
