import numpy as np
# from numpy.fft import fft,ifft, rfft, irfft
from dataclasses import dataclass, field
from scipy.io.wavfile import write, read
from scipy.fftpack import rfft, irfft
from scipy.signal import convolve, fftconvolve


SAMPLE_RATE = 48000


@dataclass
class Reverb:
    wave_file_path: str = 'Reverb'
    wave: list[float] = field(default_factory=list)
    ir: list[float] = field(default_factory=list)

    def apply_reverb(self, wave, ir, percent_mix=0):
        self.wave = np.float32(wave)
        self.ir = 'Effects/IR_Files/' + ir

        sr, stream = read('Effects/IR_Files/' + ir)

        self.ir = stream

        convolved_wave = fftconvolve(self.wave, self.ir)

        dry_wave = self.wave * (1.0 - percent_mix)
        wet_wave = (convolved_wave / np.abs(np.max(convolved_wave)))*percent_mix

        if len(dry_wave) < len(wet_wave):
            pad_length = np.abs(len(dry_wave) - len(wet_wave))
            dry_wave = np.pad(dry_wave, (0, pad_length), 'constant')
        elif len(wet_wave) < len(dry_wave):
            pad_length = np.abs(len(dry_wave) - len(wet_wave))
            wet_wave = np.pad(wet_wave, (0, pad_length), 'constant')

        convolved_wave = dry_wave + wet_wave

        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(convolved_wave))

        return convolved_wave
