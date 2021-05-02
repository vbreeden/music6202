from dataclasses import dataclass
from scipy import signal

@dataclass
class Lowpass:

    def low_pass(self, data, Fs_new, Fs):
        b, a =signal.butter(N=2, Wn=Fs_new/2, btype='low', analog=False, fs=Fs)
        filtered = signal.filtfilt(b, a, data)
        return filtered

@dataclass
class Bandpass:

    def band_pass(self, data, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, data)
        return filtered
