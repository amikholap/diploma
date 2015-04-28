import abc
import time
import threading

import numpy as np

from . import conf


class AbstractProvider(abc.ABC):

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ThreadedProvider(AbstractProvider):

    def __init__(self):
        super().__init__()
        self.__running = False
        self.__thread = None

    def start(self):
        print("STARTING")
        self.__thread = threading.Thread(target=self.__run)
        self.__running = True
        self.__thread.start()
        print("STARTED")

    def stop(self):
        print("STOPPING")
        self.__running = False
        self.__thread.join()
        print("STOPPED")

    def __run(self):
        while self.__running:
            self.provide()

    @abc.abstractmethod
    def provide(self):
        pass


class ModelProvider(ThreadedProvider):

    _DELAY = 0.5

    def __init__(self, model):
        super().__init__()
        self.model = model

    def start(self):
        self._last_invoked_at = time.time()  # reset timer
        super().start()

    def provide(self):
        time_from = self._last_invoked_at
        self._last_invoked_at = time.time()
        time_to = self._last_invoked_at

        ts = np.arange(time_from, time_to, 1 / conf.SAMPLE_RATE)
        samples = self.model(ts)

        time.sleep(self._DELAY)

        print(samples.size)
