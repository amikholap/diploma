import abc
import time
import threading

import events
import numpy as np

from . import conf
from . import utils


__all__ = ['ModelProvider']


class AbstractProvider(abc.ABC, events.Events):

    __events__ = ['on_sample_chunk']

    def __init__(self):
        super().__init__()
        self.events = ProviderEvents()

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ProviderEvents(events.Events):
    __events__ = ['on_sample_chunk']


class ThreadedProvider(AbstractProvider):

    def __init__(self):
        super().__init__()
        self.__running = False
        self.__thread = None

    def start(self):
        self.__thread = threading.Thread(target=self.__run)
        self.__running = True
        self.__thread.start()

    def stop(self):
        self.__running = False
        self.__thread.join()

    def __run(self):
        while self.__running:
            self.provide()

    @abc.abstractmethod
    def provide(self):
        pass


class FileProvider(ThreadedProvider):

    MAX_CHUNK_SIZE = 2 ** 15

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __iter__(self):
        with open(self.filename, 'rb') as f:
            while True:
                raw = np.fromstring(f.read(2), dtype=np.int8)
                if raw.size < 2:
                    break
                yield np.complex64(raw[0] + raw[1] * 1j)

    def start(self):
        self.file = open(self.filename, 'rb')
        super().start()

    def stop(self):
        super().stop()
        self.file.close()

    def provide(self):
        raw = self.file.read(2 * self.MAX_CHUNK_SIZE)
        samples = utils.raw_iq_to_complex(raw)
        self.events.on_sample_chunk(samples)


class ModelProvider(ThreadedProvider):

    def __init__(self, model):
        super().__init__()
        self.model = model
        self._last_invoked_at = None

    def start(self):
        self._last_invoked_at = time.time()  # reset timer
        super().start()

    def provide(self):
        time_from = self._last_invoked_at
        self._last_invoked_at = time.time()
        time_to = self._last_invoked_at

        ts = np.arange(time_from, time_to, 1 / conf.SAMPLE_RATE)
        samples = self.model(ts)
        self.events.on_sample_chunk(samples)
