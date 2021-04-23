from dataclasses import dataclass
from scipy import signal

@dataclass
class Lowpass:

    def low_pass(self, data, factor):
        b, a = signal.butter(3, 0.1)
        filtered = signal.filtfilt(b, a, data)
        return filtered


@dataclass
class Bandpass:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
