from dataclasses import dataclass, field
import numpy as np

SAMPLE_RATE = 48000


@dataclass
class AdditiveSynth:
    wave_file_path: str = ''
    wave_type: str = ''
    wave: list[float] = field(default_factory=list)

    def generate_additive_wav(self, notes, synth_type):
        self.wave_type = synth_type
        if self.wave_type == 'square':
            self.wave_file_path = 'out_square'
        elif self.wave_type == 'sine':
            self.wave_file_path = 'out_sine'
        frequencies = notes.frequencies
        amplitudes = notes.amplitudes
        durations = notes.durations

        for i in range(len(frequencies)):
            if self.wave_type == 'sine':
                self.wave.extend(self.add_sine_waves(frequencies[i], durations[i], amplitudes[i]))
            elif self.wave_type == 'square':
                self.wave.extend(self.generate_square_wave(frequencies[i], durations[i], amplitudes[i]))

        return self.wave

    def get_single_phase_argument(self, frequency):
        single_cycle_length = SAMPLE_RATE / (float(frequency))
        omega = np.pi * 2 / single_cycle_length
        phase_array = np.arange(0, int(single_cycle_length)) * omega
        return phase_array

    def generate_sine_wave(self, frequency, duration, amplitude):
        num_samples = int(duration * SAMPLE_RATE)
        if frequency == 0:
            resized_single_cycle = np.zeros(num_samples, dtype='float32')
        else:
            phase_array = self.get_single_phase_argument(frequency)
            single_cycle = amplitude * np.sin(phase_array)
            resized_single_cycle = np.resize(single_cycle, num_samples).astype(np.float32)

        return resized_single_cycle

    def generate_square_wave(self, frequency, duration, amplitude):
        sum_sines = amplitude * np.sign(self.generate_sine_wave(frequency, duration, amplitude))

        flag = max(sum_sines) if max(sum_sines) else 1
        x = amplitude * np.divide(sum_sines, flag)
        x = x * np.iinfo(np.int32).max
        x = x.astype(np.int32)

        return x

    def add_sine_waves(self, frequency, duration, amplitude):
        # first harmonic (fundamental frequency)
        # num_harmonics = 4
        h1 = frequency
        sum_sines = self.generate_sine_wave(h1, duration, amplitude)
        # 2nd harmonic octave above fundamental
        h2 = h1 * 2
        sum_sines += self.generate_sine_wave(h2, duration, amplitude / 2)
        # 3rd harmonic 5th above 2nd
        h3 = h2 * 1.5
        sum_sines += self.generate_sine_wave(h3, duration, amplitude / 3)
        # 4th harmonic 2 octaves above fundamental
        h4 = h1 * 4
        sum_sines += self.generate_sine_wave(h4, duration, amplitude / 4)

        flag = max(sum_sines) if max(sum_sines) else 1
        x = amplitude * np.divide(sum_sines, flag)
        x = x * np.iinfo(np.int32).max
        x = x.astype(np.int32)
        return x


@dataclass
class WavetableSynth:
    wave_file_path: str = ''
    wave_type: str = ''
    wave: list[float] = field(default_factory=list)

    def get_single_phase_argument(self, frequency):
        single_cycle_length = SAMPLE_RATE / (float(frequency))
        omega = np.pi * 2 / single_cycle_length
        phase_array = np.arange(0, int(single_cycle_length)) * omega
        return phase_array

    def generate_wavetable(self,  notes, timbre, sweep, speed):
        self.wave_file_path = 'out_wavetable'
        frequencies = notes.frequencies
        amplitudes = notes.amplitudes
        durations = notes.durations

        print('frequencies=', frequencies)
        print('amplitudes=', amplitudes)
        print('durations=', durations)

        # get list of unique frequencies in the kern file
        unique_freqs = np.unique(frequencies)
        unique_freqs = unique_freqs[unique_freqs != 0]
        wavetable = []
        # first dimension of wavetable corresponds to number of unique frequencies in the krn file (excluding rests)
        for i in range(len(unique_freqs)):
            frequency = unique_freqs[i]
            wavetable_row = []
            # second dimension of wavetable corresponds to timbre from square to sine wave
            for j in range(0, 11):
                phase_array = self.get_single_phase_argument(frequency)
                single_sin = np.sin(phase_array)
                single_square = np.sign(single_sin)
                # third dimension of wavetable corresponds to length of a single cycle of the waveform
                # (values=amplitudes)
                single_cycle = j/10 * single_sin + (1-j/10) * single_square
                wavetable_row.append(single_cycle)
            wavetable.append(wavetable_row)

        for i in range(len(frequencies)):
            frequency = frequencies[i]
            duration = durations[i]
            amplitude = amplitudes[i]
            num_samples_note = int(duration * SAMPLE_RATE)
            if frequency != 0:
                # index of the frequency in 1st dimension of wavetable
                index = np.where(unique_freqs == frequency)[0][0]
                if sweep == 'static':
                    # pick correct single cycle from wavetable
                    single_cycle = amplitude * wavetable[index][timbre]
                    # extend to note length
                    x_curr = np.resize(single_cycle, num_samples_note).astype(np.float32)
                    x = self.wave.extend(x_curr)
                elif sweep == 'sweep':
                    # speed is the amount of time in secs to complete one L-R sweep across wavetable
                    tb = timbre  # initialize timbre
                    # initialize direction of sweep across the wavetable
                    if tb == 10:
                        direction = 'back'
                    else:
                        direction = 'forward'
                    # number of samples remaining to populate note length: initialize to total note length
                    num_samples_left = num_samples_note
                    # cumulative number of samples that have been populated for the note: initialize to 0
                    num_samples_pop = 0

                    while num_samples_left > 0:
                        # pick correct single cycle from wavetable
                        single_cycle = amplitude * wavetable[index][tb]
                        num_samples_single = len(single_cycle)
                        # number of samples needed for current position in sweep, not taking into account
                        # length of cycle
                        num_samples_curr = min(num_samples_left, int(speed/11 * SAMPLE_RATE))
                        # avoid pops at transitions by ensuring length is a multiple of the single cycle length
                        remainder = num_samples_curr % num_samples_single
                        num_samples_curr += (num_samples_single - remainder)
                        x_curr = np.resize(single_cycle, num_samples_curr).astype(np.float32)
                        x = self.wave.extend(x_curr)

                        # increment timbre to next position in wavetable and reverse direction at the ends
                        if direction == 'forward':
                            tb += 1
                            if tb == 10:
                                direction = 'back'
                        elif direction == 'back':
                            tb -= 1
                            if tb == 0:
                                direction = 'forward'
                        # update number of samples that have been populated, and number left to populate for the note
                        num_samples_pop += num_samples_curr
                        num_samples_left = num_samples_note - num_samples_pop

            elif frequency == 0:
                x_rest = np.zeros(num_samples_note, dtype='float32')
                x = self.wave.extend(x_rest)

        self.wave = np.asarray(self.wave, np.float64)

        # The following lines amplify the amplitudes proportionately to int32
        # Condition to cater to the divide by zero case
        flag = max(self.wave) if max(self.wave) else 1
        self.wave = 0.5 * np.divide(self.wave, flag)
        self.wave = self.wave * np.iinfo(np.int32).max
        self.wave = self.wave.astype(np.int32)

        return self.wave
