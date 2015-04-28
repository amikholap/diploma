import numpy as np

from .. import conf  # noqa


class Detector(object):

    def __init__(self, sample_chunk_event):
        self.running = False
        self.data = np.empty((0, 0))
        sample_chunk_event.connect(self.on_sample_chunk)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def on_sample_chunk(self, samples):
        if not self.running:
            return
