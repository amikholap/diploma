#!/usr/bin/env python3
import argparse
import os

from ..utils import raw_iq_to_compex


SAMPLERATE = 2048000


def main():
    parser = argparse.ArgumentParser(description='Draw time-frequency diagrams of recorded signals')
    parser.add_argument('source', type=str, help='source file or directory')

    args = parser.parse_args()

    visualize(args.source)


def visualize(fname):
    print(fname)


if __name__ == '__main__':
    main()
