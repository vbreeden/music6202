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
    wave_file_path: str = 'chorus.wav'

    def apply_chorus(self, wave, max_delay_samps, fmod):

        # Simple Chorus
        # x, sr = sf.read('input/sv.wav')
        x = LinearWrap(wave)
        print(type(x))
        # output = 'output/sv_simpleChorus.wav'

        fmod = 1.5
        A = int(0.002 * SAMPLE_RATE)
        M = int(0.002 * SAMPLE_RATE)
        BL = 0.3
        FF = 0.7

        if A > M:
            raise RuntimeError("Amplitude of vibrato too high for delay length")

        max_delay_samps = M + A + 2  # Probably don't need the 2 here, but being safe
        output_samps = len(x) + max_delay_samps
        y = np.zeros(output_samps)
        ring_buf = LinearRingBuffer(max_delay_samps)
        delta_phi = fmod/SAMPLE_RATE
        phi = 0

        for i in range(output_samps):
            s = x[i]
            ring_buf.pushSample(s)
            delay_samps = M + int(math.sin(2 * math.pi * phi) * A)
            y[i] = s * BL + ring_buf.delayedSample(delay_samps) * FF

            phi = phi + delta_phi
            while phi >= 1:
                phi -= 1

        write(self.wave_file_path, SAMPLE_RATE, np.array(y))

        return y


@dataclass
class Delay:
    wave_file_path: str = 'DelayLine'

    def apply_delay(self, wave, delay_samples, percent_mix=0.5):
        linear_wrap = LinearWrap(wave)

        output_samples = len(linear_wrap) + delay_samples
        delay = np.zeros(output_samples, dtype='float32')
        ring_buf = LinearRingBuffer(delay_samples)

        for i in range(output_samples):
            s = linear_wrap[i]
            ring_buf.pushSample(s)
            delay[i] = s * percent_mix + ring_buf.delayedSample(delay_samples) * (1 - percent_mix)

        self.wave_file_path = 'DelayLine'
        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(delay))
        return delay


@dataclass
class Vibrato:
    wave_file_path: str = 'Vibrato'
    wave: np.ndarray = np.zeros(0)

    def apply_vibrato(self, wave, max_delay_samps, fmod):
        x = LinearWrap(wave)

        output_samps = len(x) + max_delay_samps
        y = np.zeros(output_samps, dtype='float32')
        ring_buf = LinearRingBuffer(max_delay_samps)

        delta_phi = fmod/SAMPLE_RATE
        phi = 0

        for i in range(output_samps):
            s = x[i]
            ring_buf.pushSample(s)
            delay_samps = int((math.sin(2 * math.pi * phi) + 1.1) * max_delay_samps)
            y[i] = ring_buf.delayedSample(delay_samps)

            phi = phi + delta_phi
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
        self.wave_file_path = 'vibrato'
        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(y))
        return y
