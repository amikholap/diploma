#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import time


SAMPLERATE = 2048000


def main():
    parser = argparse.ArgumentParser(description='Periodically record raw I/Q samples')
    parser.add_argument('-f', type=int, required=True, help='frequency')
    parser.add_argument('-d', type=float, required=True, help='sample duration (seconds)')
    parser.add_argument('-t', type=float, required=True, help='interval between sampling (seconds)')
    parser.add_argument('-n', type=int, required=True, help='number of samples')
    parser.add_argument('-o', type=str, required=True, help='output directory')

    args = parser.parse_args()

    nsamples = args.d * SAMPLERATE

    for _ in range(args.n):
        filename = '{}-{}.bin'.format(args.f, int(time.time()))
        path = os.path.join(os.path.realpath(args.o), filename)
        cmd = ['rtl_sdr', path, '-f', str(args.f), '-n', str(nsamples), '-s', str(SAMPLERATE)]

        retcode = subprocess.call(cmd)
        if retcode != 0:
            pass
            #msg = 'rtl_sdr exited with code {}'.format(retcode)
            #print(msg, file=sys.stderr)
            #sys.exit(1)

        time.sleep(args.t)


if __name__ == '__main__':
    main()
