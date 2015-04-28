import numpy as np

from .. import conf
from ..analysis.transformation import dstft


__all__ = ['Detector']


class Detector(object):

    WINDOW_SIZE = conf.SAMPLE_RATE
    WINDOW_STEP = 0.1 * WINDOW_SIZE

    def __init__(self, provider):
        self.data = np.empty((0, 0))
        self._buffer = np.empty((0, 0))
        provider.events.on_sample_chunk += self.on_sample_chunk

    def on_sample_chunk(self, samples):
        data = np.append(self._buffer, samples)
        if data.size >= self.WINDOW_SIZE:
            ffts = dstft(data, self.WINDOW_SIZE, self.WINDOW_STEP)
            print(ffts.shape, self.data.shape)
            self.data = np.concatenate([ffts, self.data], axis=0)
            nspectrogramms = ffts.shape[0]
            leftovers_start_index = nspectrogramms * self.WINDOW_STEP + self.WINDOW_SIZE
            self._buffer = data[leftovers_start_index:]
        else:
            self._buffer = np.append(self._buffer, data)
