import contextlib
import cStringIO
import logging
import subprocess
import threading

import events
import pandas as pd

from .utils import message


_logger = logging.getLogger(__name__)


class ScannerEvents(events.Events):
    __events__ = ['on_raw_data', 'on_parsed_data', 'on_aggregated_data', 'on_analyzed_data']


class Scanner(object):

    def __init__(self):
        self.scanning = False
        self._data = pd.DataFrame()
        self._inflight_data = []
        self._scanning_thread = None

        self.events = ScannerEvents()
        self.events.on_raw_data += self._parse_raw_data
        self.events.on_parsed_data += self._aggregate_data
        self.events.on_aggregated_data += self._analyze_data

    def start(self, low, high, step):
        self.low, self.high, self.step = low, high, step
        self.scanning = True
        self._scanning_thread = threading.Thread(target=self._start_rtl_power, args=(self.low, self.high, self.step))
        self._scanning_thread.start()

    def stop(self):
        if self.scanning:
            self.scanning = False
            self._scanning_thread.join()
            self._scanning_thread = None
            self.low = self.high = self.step = None
        else:
            _logger.warning('Trying to stop an inactive scanner.')

    def _start_rtl_power(self, low, high, step):
        cmd = ('rtl_power',
               '-c', '30%',
               '-i' '3',
               '-f', '{}:{}:{}'.format(low, high, step),
               '-')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        while self.scanning:
            line = p.stdout.readline().decode('utf-8')
            if not line:
                self.scanning = False
                continue
            self.events.on_raw_data(line)

        p.terminate()

    def _parse_raw_data(self, raw_data):
        with contextlib.closing(cStringIO.StringIO(raw_data)) as sio:
            row = pd.read_csv(sio, header=None)

        row['date'] = row[0].str.cat(row[1].str.strip(), 'T')
        grouped = row.groupby('date')

        data = {}
        for date, group in grouped:
            for idx, row in group.iterrows():
                low, high = row[2:4]
                step = row[4]
                i = 0
                f = low
                while f <= high:
                    data.setdefault(f, {})[date] = row[6+i]
                    i += 1
                    f += step
        data = pd.DataFrame(data)

        self.events.on_parsed_data(data)

    def _aggregate_data(self, data):
        if self._inflight_data and self._inflight_data[-1].index[0] != data.index[0]:
            # a new row is for a new time period
            aggregated_data = pd.concat(self._inflight_data, axis=1)
            self._inflight_data = []
            self.events.on_aggregated_data(aggregated_data)
        self._inflight_data.append(data)

    def _analyze_data(self, data):
        """
        Compute rolling statistics and select frequencies with the strongest signal.
        """

        def merge(mask, row):
            to_merge = []
            idxs = []
            for i, x in enumerate(mask.iloc[1:], 1):
                if mask.iloc[i-1] and mask.iloc[i]:
                    if idxs:
                        idxs.append(row.index[i])
                    else:
                        idxs.extend([row.index[i-1], row.index[i]])
                elif idxs:
                    to_merge.append(idxs)
                    idxs = []

            for idxs in to_merge:
                idxmax = row[idxs].argmax()
                idxs.remove(idxmax)
                mask[idxs] = False

            return mask

        self._data = pd.concat([self._data, data], axis=0)
        self._data = self._data.ix[-10:]  # limit history to the last 10 scans

        freq_window = 10e6  # 10MHz
        bin_window = int(freq_window / self.step)  # number of bins equivalent to frequency window size
        bin_subwindow = bin_window / 2  # overlap windows by 1/2 of their size

        signals = {}
        for i in range(self._data.shape[1] / bin_subwindow - 1):
            window = self._data.iloc[:,i*bin_subwindow:(i+1)*bin_subwindow]
            mean = window.mean()
            mask = (mean - mean.mean()) > 1.5 * mean.std()
            for f in mean.index[mask]:
                signals[f] = data[f].iloc[0]

        signals = pd.Series(signals)

        #mask = merge(mask, mean)

        self.events.on_analyzed_data(signals)
