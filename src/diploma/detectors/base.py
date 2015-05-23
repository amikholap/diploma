import events
import numpy as np
import statsmodels.tsa.arima_model

from .. import conf
from ..analysis.stft import dstft


class StftDetector(object):

    WINDOW_SIZE = 2 ** 14
    WINDOW_STEP = 0.5 * WINDOW_SIZE
    MAX_SPECTROGRAMS = int((10 * conf.SAMPLE_RATE - WINDOW_SIZE) / WINDOW_STEP) + 1  # 10s

    def __init__(self, provider):
        self.data = np.empty((0, self.WINDOW_SIZE))
        self._buffer = np.empty((0, self.WINDOW_SIZE))

        self.events = DetectorEvents()
        self.events.on_spectrum_changed += self.on_spectrum_changed

        self._provider = provider
        self._provider.events.on_sample_chunk += self.on_sample_chunk

    def on_sample_chunk(self, samples):
        data = np.append(self._buffer, samples)
        if data.size >= self.WINDOW_SIZE:
            ffts = dstft(data, self.WINDOW_SIZE, self.WINDOW_STEP)
            ffts = np.abs(ffts)

            new_len = ffts.shape[0] + self.data.shape[0]
            to_drop = new_len - self.MAX_SPECTROGRAMS
            to_drop_idx = -to_drop if to_drop > 0 else None
            self.data = np.concatenate([ffts, self.data[:to_drop_idx]], axis=0)

            nspectrogramms = ffts.shape[0]
            leftovers_start_index = nspectrogramms * self.WINDOW_STEP + self.WINDOW_SIZE
            self._buffer = data[leftovers_start_index:]
            self.events.on_spectrum_changed(self.data)
        else:
            self._buffer = np.append(self._buffer, data)

    def on_spectrum_changed(self):
        pass

    #def on_data_changed(self, data):

        #def fill_mask_gaps(mask):
            #"""
            #Set small gaps of zeroes to ones.
            #"""
            ## lame heuristics
            #threshold = 0.005 * self.WINDOW_SIZE
            #zeroes_count = 0
            #for i, value in enumerate(mask):
                #if value == 0:
                    #zeroes_count += 1
                #elif zeroes_count < threshold:
                    #mask[i-zeroes_count:i] = 1
            #return mask


        #maxs = data.max(axis=0)
        #mask = np.where(maxs > np.percentile(maxs, 99), 1, 0)
        #fill_mask_gaps(mask)

        #indices, = np.nonzero(mask)
        #possible_signals = data[:,indices]

        #arimas = np.array([statsmodels.tsa.arima_model.ARIMA(fs, (1, 1, 1)) for fs in possible_signals.T],
                          #dtype=np.object)

        #results = np.empty(arimas.size, dtype=np.object)
        #for i, arima in enumerate(arimas):
            #try:
                #results[i] = arima.fit(tol=1e-3, disp=False, warn_convergence=False)
            #except Exception:
                #results[i] = None

        #max_resids = np.empty(results.size)
        #for i, result in enumerate(results):
            #if result is None:
                #max_resids[i] = -1000
            #else:
                #max_resids[i] = np.mean(np.abs(result.resid))

        #import matplotlib.pyplot as plt
        #ys = np.zeros(maxs.size)
        #ys[indices] = max_resids
        #plt.stem(ys)
        #plt.show()


class DetectorEvents(events.Events):
    __events__ = ['on_spectrum_changed']
