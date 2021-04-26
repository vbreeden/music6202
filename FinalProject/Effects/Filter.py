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
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
