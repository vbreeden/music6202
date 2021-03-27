from dataclasses import dataclass


@dataclass
class AdditiveSynth:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')


@dataclass
class WavetableSynth:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
