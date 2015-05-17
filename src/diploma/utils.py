import numpy as np


def raw_iq_to_complex(data):
    raw = np.fromstring(data, dtype=np.int8)

    if raw.size % 2 != 0:
        raise RuntimeError('I/Q data length is not multiple of 2')

    converted = np.empty(raw.size // 2, dtype=np.complex64)
    for i in range(0, raw.size - 1, 2):
        converted[i/2] = np.complex64(raw[i] + raw[i+1] * 1j)

    return converted
