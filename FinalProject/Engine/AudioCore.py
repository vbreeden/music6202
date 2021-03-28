from dataclasses import dataclass


@dataclass
class Note:
    pitch: str
    onset: str
    release: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')


@dataclass
class Buffer:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')