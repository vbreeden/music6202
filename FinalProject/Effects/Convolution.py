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

    def apply_reverb(self, wave, ir):
        self.wave = np.float32(wave)
        self.ir = 'Effects/IR_Files/' + ir

        sr, stream = read('Effects/IR_Files/' + ir)

        # Normalize the data stream so that scipy's convolution doesn't break.
        # word_size = np.dtype(stream.dtype).itemsize * 8
        # ir_2 = stream / float(1 << (word_size - 1))
        self.ir = np.float32(stream / np.abs(np.max(stream)))

        # sig_len = len(self.wave)
        # imp_len = len(self.ir)
        # conv_len = sig_len + imp_len - 1
        #
        # conv_arr = np.zeros(conv_len)

        convolved_wave = fftconvolve(self.wave, self.ir)

        # wave_fft = rfft(self.wave)
        # ir_fft = rfft(self.ir)
        # pad_len = np.abs(len(wave_fft) - len(ir_fft))
        # ir_fft = np.pad(ir_fft, (0, pad_len), 'constant')
        #
        # convolution = wave_fft * ir_fft
        #
        # conv_arr = irfft(convolution)
        # conv_arr *= .1

        convolved_wave *= .03

        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(convolved_wave))

        return convolved_wave
