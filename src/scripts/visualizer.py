#!/usr/bin/env python3
import argparse
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from diploma.analysis.stft import streaming_dstft
from diploma.providers import FileProvider
from diploma.visualization import time_frequency


def main():
    parser = argparse.ArgumentParser(description='Draw time-frequency diagrams of recorded signals')
    parser.add_argument('source', type=str, help='source file or directory')
    parser.add_argument('--wsize', type=int, default=2**15, help='SFTF window size')
    parser.add_argument('--wstep', type=int, default=2**14, help='SFTF window step')
    parser.add_argument('--interactive', action='store_true', help='Show plot instead of saving it to a file')

    args = parser.parse_args()

    visualize(args.source, args.wsize, args.wstep, args.interactive)


def visualize(source, window_size, window_step, interactive):

    def walker(root):
        if os.path.isdir(root):
            for fname in os.listdir(root):
                fname = os.path.join(root, fname)
                walker(fname)
        elif os.path.splitext(root)[-1] == '.bin':
            visualize_file(root, window_size, window_step, interactive)

    source = os.path.normpath(source)
    walker(source)


def visualize_file(fname, window_size, window_step, interactive):
    provider = FileProvider(fname)
    stream = iter(provider)
    fft_generator = streaming_dstft(stream, window_size, window_step)

    ffts = []
    for fft in fft_generator:
        ffts.append(fft)
    ffts = np.array(ffts)

    time_frequency(ffts)

    if interactive:
        plt.show()
    else:
        png_name = os.path.splitext(fname)[0]
        png_name += '.png'
        plt.savefig(png_name)

    print('Done with {}'.format(fname))


if __name__ == '__main__':
    main()
