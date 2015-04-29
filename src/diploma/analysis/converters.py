import numpy as np

from . import transformation
from .. import conf
from .. import utils


def iq_to_stft(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    data = utils.raw_iq_to_complex(data)
    data = transformation.dstft(data, conf.DSTFT_WINDOW_SIZE, conf.DSTFT_WINDOW_STEP)
    np.save(output_file, data)
