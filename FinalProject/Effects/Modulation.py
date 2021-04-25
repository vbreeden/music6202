from dataclasses import dataclass
import numpy as np
import math
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# code for ring buffer and modulated effects adapted from Andrew Beck's code in 19-ModulatedEffects.ipynb

SAMPLE_RATE = 48000


@dataclass
class RingBuffer(object):
    def __init__(self, maxDelay):
        self.maxDelay = maxDelay + 1
        self.buf = np.zeros(self.maxDelay)
        self.writeInd = 0

    def pushSample(self, s):
        self.buf[self.writeInd] = s
        self.writeInd = (self.writeInd + 1) % len(self.buf)

    def delayedSample(self, d):
        d = min(self.maxDelay - 1, max(0, d))
        i = ((self.writeInd + self.maxDelay) - d) % self.maxDelay
        return self.buf[i]


class LinearRingBuffer(RingBuffer):
    def __init__(self, maxDelay):
        self.maxDelay = maxDelay + 1
        self.buf = LinearWrap(np.zeros(self.maxDelay))
        self.writeInd = 0


class LinearWrap(object):
    def __init__(self, it):
        self.it = it

    def __len__(self):
        return len(self.it)

    def __setitem__(self, inI, val):
        if type(inI) != int:
            raise RuntimeError('Can only write to integer values')
        self.it[inI] = val

    def __getitem__(self, inI):
        loI = math.floor(inI)
        hiI = math.ceil(inI)
        a = inI - loI
        inRange = lambda val: val >= 0 and val < len(self.it)
        loX = self.it[loI] if inRange(loI) else 0
        hiX = self.it[hiI] if inRange(hiI) else 0
        return loX * (1 - a) + hiX * a


@dataclass
class Chorus:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')


@dataclass
class Delay:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')


@dataclass
class Vibrato:
    wave_file_path: str = 'Reverb'

    def apply_vibrato(self, wave, maxDelaySamps, fmod):
        self.wave = wave
        x = LinearWrap(wave)

        outputSamps = len(x) + maxDelaySamps
        y = np.zeros(outputSamps, dtype='float32')
        ringBuf = LinearRingBuffer(maxDelaySamps)

        deltaPhi = fmod/SAMPLE_RATE
        phi = 0

        for i in range(outputSamps):
            s = x[i]
            ringBuf.pushSample(s)
            delaySamps = int((math.sin(2 * math.pi * phi) + 1.1) * maxDelaySamps)
            y[i] = ringBuf.delayedSample(delaySamps)

            phi = phi + deltaPhi
            while phi >= 1:
                phi -= 1

        plt.plot(y)
        plt.savefig('vibratoplot.jpg')
        plt.close()
        plt.plot(y[0:1000])
        plt.savefig('vibratoplot_subset.jpg')
        plt.close()
        plt.plot(y[46000:50000])
        plt.savefig('vibratoplot_subset2.jpg')
        plt.close()
        self.wave_file_path='vibrato'
        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(y))
        return y
