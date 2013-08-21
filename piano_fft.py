#!/usr/bin/python

from sys import argv
import aifc
import numpy as np
from numpy.fft import rfft, fftfreq
import csv
import os

BLOCKSIZE = 2**13
OUTDIR = 'data'
ENDTIME = 5

if __name__ == '__main__':
    filename = argv[1]
    os.mkdir(OUTDIR)
    data = np.zeros(2 * BLOCKSIZE)
    axis = np.zeros(BLOCKSIZE)
    mergeddata = np.zeros(BLOCKSIZE)
    fftdata = np.zeros(BLOCKSIZE)
    with open(filename, 'rb') as f:
        audio = aifc.open(f)
        freq = audio.getframerate()
        endframe = ENDTIME*freq
        if endframe > audio.getnframes():
            endframe = audio.getnframes()

        axis = fftfreq(BLOCKSIZE, d=1.0/freq)
        # pure real - toss negative freqs
        while endframe - audio.tell() > BLOCKSIZE:
            output = '{0}.{1:.2f}.csv'.format(filename, audio.tell()/freq)
            output = os.path.join(os.getcwd(), OUTDIR, output)
            # Read BLOCKSIZE frames - these files are big endian
            data = np.fromstring(audio.readframes(BLOCKSIZE), dtype='>i2')
            mergeddata = data[0::2] + data[1::2]
            fftdata = rfft(mergeddata, n=BLOCKSIZE)

            with open(output, 'w', newline='') as of:
                writer = csv.writer(of)
                writer.writerows(zip(np.absolute(axis), np.absolute(fftdata)))

