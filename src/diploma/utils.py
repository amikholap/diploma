import logging

import numpy as np


_logger = logging.getLogger(__name__)


def raw_iq_to_complex(data):
    data = np.fromstring(data, dtype=np.int8)

    if data.size % 2 != 0:
        _logger.warning('I/Q data length is not multiple of 2')

    data = np.array([np.complex64(data[i] + data[i+1] * 1j) for i in range(0, data.size - 1, 2)])

    return data
