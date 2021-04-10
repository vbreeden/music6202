from dataclasses import dataclass, field
from scipy.io.wavfile import write
from scipy import signal

import numpy as np

SAMPLE_RATE = 48000

@dataclass
class AdditiveSynth:
    wave_file_path: str = ''
    wave_type: str = ''
    wave: list[float] = field(default_factory=list)

    def generate_additive_wav(self, notes, wave_file_path='out_square', wave_type = 'square'):
        self.wave_file_path = wave_file_path
        self.wave_type = wave_type
        frequencies = notes.frequencies
        amplitudes = notes.amplitudes
        durations = notes.durations

        for i in range(len(frequencies)):
        	print("*** i=", i, "***")
        	if(frequencies[i] != 0):
        		if (self.wave_type == 'sine'):
	        		self.wave.extend(self.generate_sine_wave(frequencies[i], durations[i], amplitudes[i]))
	        	elif (self.wave_type == 'square'):
	        		self.wave.extend(self.generate_square_wave(frequencies[i], durations[i], amplitudes[i]))
	        	
        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(self.wave))

    def get_single_phase_argument(self,frequency):
    	single_cycle_length = SAMPLE_RATE / float(frequency)
    	omega = np.pi * 2 / single_cycle_length
    	phase_array = np.arange(0, int(single_cycle_length)) * omega
    	return phase_array
    
    def generate_sine_wave(self,frequency, amplitude, duration):
    	num_samples = int(duration * SAMPLE_RATE)
    	phase_array = self.get_single_phase_argument(frequency)
    	single_cycle = amplitude * np.sin(phase_array)
    	resized_single_cycle = np.resize(single_cycle, (num_samples)).astype(np.float)
    	return resized_single_cycle

    def generate_square_wave(self, frequency, amplitude, duration):
    	return amplitude * np.sign(self.generate_sine_wave(frequency, amplitude, duration))

@dataclass
class WavetableSynth:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
