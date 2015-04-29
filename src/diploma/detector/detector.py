import events
import numpy as np

from .. import conf
from ..analysis.transformation import dstft


__all__ = ['Detector']


class Detector(object):

    WINDOW_SIZE = 2 ** 14
    WINDOW_STEP = 0.5 * WINDOW_SIZE
    MAX_SPECTROGRAMS = int((10 * conf.SAMPLE_RATE - WINDOW_SIZE) / WINDOW_STEP) + 1  # 10s

    def __init__(self, provider):
        self.data = np.empty((0, self.WINDOW_SIZE))
        self._buffer = np.empty((0, self.WINDOW_SIZE))

        self.events = DetectorEvents()

        provider.events.on_sample_chunk += self.on_sample_chunk

    def on_sample_chunk(self, samples):
        data = np.append(self._buffer, samples)
        if data.size >= self.WINDOW_SIZE:
            ffts = dstft(data, self.WINDOW_SIZE, self.WINDOW_STEP)
            ffts = np.abs(ffts)

            new_len = ffts.shape[0] + self.data.shape[0]
            to_drop = new_len - self.MAX_SPECTROGRAMS
            to_drop_idx = -to_drop if to_drop > 0 else None
            self.data = np.concatenate([ffts, self.data[:to_drop_idx]], axis=0)
            print(self.data.shape)

            nspectrogramms = ffts.shape[0]
            leftovers_start_index = nspectrogramms * self.WINDOW_STEP + self.WINDOW_SIZE
            self._buffer = data[leftovers_start_index:]
            self.events.on_new_data()
        else:
            self._buffer = np.append(self._buffer, data)


class DetectorEvents(events.Events):
    __events__ = ['on_new_data']
