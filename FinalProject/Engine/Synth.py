from dataclasses import dataclass, field
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import numpy as np

SAMPLE_RATE = 48000


@dataclass
class AdditiveSynth:
    wave_file_path: str = ''
    wave_type: str = ''
    wave: list[float] = field(default_factory=list)

    def generate_additive_wav(self, notes, type):
        self.wave_type = type
        if type == 'square':
            self.wave_file_path = 'out_square'
        elif type == 'sine':
            self.wave_file_path = 'out_sine'
        frequencies = notes.frequencies
        amplitudes = notes.amplitudes
        durations = notes.durations

        print('frequencies=', frequencies)
        print('amplitudes=', amplitudes)
        print('durations=', durations)

        for i in range(len(frequencies)):
            print("*** i=", i, "***")
            print('frequencies[i], durations[i], amplitudes[i]=',frequencies[i], durations[i], amplitudes[i])
            if self.wave_type == 'sine':
                self.wave.extend(self.add_sine_waves(frequencies[i], durations[i], amplitudes[i]))
                plt.plot(self.wave)
                plt.savefig('sineplot.jpg')
                plt.close()
                plt.plot(self.wave[0:1000])
                plt.savefig('sineplot_subset.jpg')
                plt.close()
            elif self.wave_type == 'square':
                self.wave.extend(self.generate_square_wave(frequencies[i], durations[i], amplitudes[i]))
                plt.plot(self.wave)
                plt.savefig('squareplot.jpg')
                plt.close()
                plt.plot(self.wave[0:1000])
                plt.savefig('squareplot_subset.jpg')
                plt.close()

        write(self.wave_file_path + ".wav", SAMPLE_RATE, np.array(self.wave))


    def get_single_phase_argument(self, frequency):
        single_cycle_length = SAMPLE_RATE / (2*float(frequency))
        omega = np.pi * 2 / single_cycle_length
        phase_array = np.arange(0, int(single_cycle_length)) * omega
        return phase_array
    
    def generate_sine_wave(self, frequency, duration, amplitude):
        num_samples = int(duration * SAMPLE_RATE/2)
        if frequency == 0:
            resized_single_cycle = np.zeros(num_samples)
        else:
            phase_array = self.get_single_phase_argument(frequency)
            single_cycle = amplitude * np.sin(phase_array)
            resized_single_cycle = np.resize(single_cycle, num_samples).astype(np.float)

        return resized_single_cycle

    def generate_square_wave(self, frequency, duration, amplitude):
        return amplitude * np.sign(self.generate_sine_wave(frequency, duration, amplitude))

    def add_sine_waves(self, frequency, duration, amplitude):
        #first harmonic (fundamental frequency)
        numHarmonics=3
        h1=frequency
        sumSines = self.generate_sine_wave(h1, duration, amplitude)
        #2nd harmonic octave above fundamental
        h2 = h1 * 2
        sumSines += self.generate_sine_wave(h2, duration, amplitude/2)
        #3rd harmonic 5th above 2nd
        h3 = h2 * 1.5
        sumSines += self.generate_sine_wave(h3, duration, amplitude/3)
        #4th harmonic 2 octaves above fundamental
        h4 = h1 * 4
        sumSines += self.generate_sine_wave(h4, duration, amplitude / 4)

        #print('harmonics=',h1,h2,h3,h4)

        #rescale to prevent clipping
        x = sumSines / (numHarmonics - 1)

        return x



@dataclass
class WavetableSynth:
    name: str

    def replace_this_function_name(self, name='Default Name'):
        self.name = name
        print('Working')
