import numpy as np

from .base import StftDetector
from .. import analysis
from .. import conf


class WfmDetector(StftDetector):

    # Assume WFM is limited to [100kHz, 200kHz].
    MIN_BANDWIDTH = 100000
    MAX_BANDWIDTH = 200000

    # Assume everything below 30% of average is noise.
    NOISE_PERCENTILE = 30

    DETECTION_WINDOW_SIZE = MAX_BANDWIDTH
    DETECTION_WINDOW_STEP = int(0.5 * MIN_BANDWIDTH)

    def on_spectrum_changed(self):
        super().on_spectrum_changed()

        averages = self.data.mean(axis=0)
        noise_level = np.percentile(averages, self.NOISE_PERCENTILE)

        frequency_scale = analysis.stft.freqs(averages.size, 1 / conf.SAMPLE_RATE)
        frequency_step = np.abs(frequency_scale[1] - frequency_scale[0])

        # Convert from Hz to indices.
        wsize = np.ceil(self.DETECTION_WINDOW_SIZE / frequency_step)
        wstep = np.ceil(self.DETECTION_WINDOW_STEP / frequency_step)

        for i in range(0, self.data.shape[0] - wsize + 1, wstep):
            window_slice = slice(i, i + wsize)
            window_averages = averages[window_slice]
            noise_mask = np.where(window_averages > noise_level, 1, 0)
            if not self.check_noise(noise_mask):
                continue

    def check_noise(self, noise_mask):
        # Noise may occupy a limited part of a window.
        if noise_mask.sum() / noise_mask > self.MIN_BANDWIDTH / self.DETECTION_WINDOW_SIZE:
            return False
        return True

    def check_gaps(self, noise_mask):
        # There shouldn't be any big gaps in between signals.
        pass
