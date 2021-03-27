from dataclasses import dataclass


@dataclass
class Lowpass:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')


@dataclass
class Bandpass:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
