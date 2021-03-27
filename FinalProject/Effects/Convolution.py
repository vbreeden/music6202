from dataclasses import dataclass


@dataclass
class Reverb:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
