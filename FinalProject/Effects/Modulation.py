from dataclasses import dataclass


@dataclass
class Chorus:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')


@dataclass
class Delay:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')


@dataclass
class Vibrato:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
