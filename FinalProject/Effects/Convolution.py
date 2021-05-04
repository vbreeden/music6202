import numpy as np
from dataclasses import dataclass, field
from scipy.io.wavfile import write, read
from scipy.signal import fftconvolve


SAMPLE_RATE = 48000


@dataclass
class Reverb:
    wave: list[float] = field(default_factory=list)
    ir: list[float] = field(default_factory=list)

    def apply_reverb(self, wave, ir, percent_mix=0):
        self.wave = np.float32(wave)
        ir_loc = 'Effects/IR_Files/' + ir
        sr, stream = read(ir_loc)
        self.ir = stream

        convolved_wave = fftconvolve(self.wave, self.ir)

        dry_signal = self.wave * (1.0 - percent_mix)
        wet_signal = (convolved_wave / np.abs(np.max(convolved_wave)))

        # The wet signal needs to be re-scaled to match the order of magnitude of the dry signal
        flag = max(wet_signal) if max(wet_signal) else 1
        wet_signal = 0.5 * np.divide(wet_signal, flag)
        wet_signal = wet_signal * np.iinfo(np.int32).max
        wet_signal = wet_signal * percent_mix
        wet_signal = wet_signal.astype(np.int32)

        if len(dry_signal) < len(wet_signal):
            pad_length = np.abs(len(dry_signal) - len(wet_signal))
            dry_signal = np.pad(dry_signal, (0, pad_length), 'constant')
        elif len(wet_signal) < len(dry_signal):
            pad_length = np.abs(len(dry_signal) - len(wet_signal))
            wet_signal = np.pad(wet_signal, (0, pad_length), 'constant')

        # Rescale the wet and dry signals

        # Re-assign the convolved wave as a mixture of the wet and dry signals.
        convolved_wave = dry_signal + wet_signal

        return convolved_wave
