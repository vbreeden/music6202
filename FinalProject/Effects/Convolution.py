import numpy as np
from numpy.fft import fft,ifft
from dataclasses import dataclass, field
from scipy.io.wavfile import write, read


SAMPLE_RATE = 48000


@dataclass
class Reverb:
    wave_file_path: str = 'Reverb'
    wave: list[float] = field(default_factory=list)
    ir: list[float] = field(default_factory=list)

    def apply_reverb(self, wave, ir):
        self.wave = wave
        self.ir = 'Effects/IR_Files/' + ir

        sr, stream = read('Effects/IR_Files/' + ir)

        # Normalize the data stream so that scipy's convolution doesn't break.
        self.ir = stream / np.abs(np.max(stream))

        sig_len = len(self.wave)
        imp_len = len(self.ir)
        conv_len = sig_len + imp_len - 1

        conv_arr = np.zeros(conv_len)

        # The provided audio files are in int16 format so they need to be expanded to 64 bit to prevent
        # RuntimeWarning: overflow encountered in short_scalars.
        # if self.wave.dtype == np.dtype(np.int16):
        #     self.wave = self.wave.astype(np.int)
        # if self.ir.dtype == np.dtype(np.int16):
        #     self.ir = self.ir.astype(np.int)

        wave_fft = fft(self.wave)
        ir_fft = fft(self.ir)
        pad_len = np.abs(len(self.wave) - len(self.ir))
        ir_fft = np.pad(ir_fft, (0, pad_len), 'constant')

        convolution = np.multiply(wave_fft, ir_fft)

        conv_arr = ifft(convolution)

        # for i in range(conv_len):
        #     prod_sum = 0.
        #     for j in range(imp_len):
        #         if j <= i and i - j < sig_len:
        #             prod_sum += self.wave[int(i) - int(j)] * self.ir[int(j)]
        #             conv_arr[i] = prod_sum

        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(conv_arr.real))

        return conv_arr
