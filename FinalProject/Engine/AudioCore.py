from math import ceil
import numpy as np
from dataclasses import dataclass, field
from music21 import converter
import matplotlib.pyplot as plt
from soundfile import write
from subtypes import Subtype
from scipy.interpolate import interp1d
from scipy import signal


@dataclass
class Buffer:
    sr: float = 48000
    buffer: np.ndarray = np.zeros(int(sr))

    def create_buffer(self, seconds=0.0):
        self.buffer = np.zeros(int(ceil(self.sr * seconds)))


@dataclass
class Notes:
    kern_file: str = ''
    note_names: list[str] = field(default_factory=list)
    frequencies: list[float] = field(default_factory=list)
    amplitudes: list[float] = field(default_factory=list)
    durations: list[float] = field(default_factory=list)
    start_times: list[float] = field(default_factory=list)
    end_times: list[float] = field(default_factory=list)
    buffers: list[Buffer] = field(default_factory=list)

    def parse_kern(self, kern_file):
        self.kern_file = kern_file

        stream = converter.parse('KernFiles/' + self.kern_file)
        stream_flat = stream.flat

        i = 0
        last_start = 0
        last_duration = 0

        # populate lists for every note in the krn file
        for obj in stream_flat.iter.notesAndRests:
            if obj.isNote:
                self.amplitudes.append(obj.volume.realized)
                self.frequencies.append(obj.pitch.frequency)
                self.note_names.append(obj.nameWithOctave)
            else:
                self.amplitudes.append(0)
                self.frequencies.append(0)
                self.note_names.append("")
            beat = obj.beat
            duration = obj.seconds
            self.durations.append(duration)
            buf = Buffer()
            buf.create_buffer(seconds=duration)
            self.buffers.append(buf)

            if i == 0:
                start_time = 0
            else:
                start_time = last_start + last_duration

            self.start_times.append(start_time)
            end_time = start_time + duration
            self.end_times.append(end_time)

            last_start = start_time
            last_duration = duration

            i += 1


@dataclass
class Downsampler:
    output_sample_rate: int = 48000
    output_bit_rate: int = 32

    # write_wav : function to return a wav type output file based on the data and sample rate provided
    def write_wav(self, wave_file_path, data, fs = output_sample_rate, bitrate=output_bit_rate):
        subtype = Subtype().get_subtype(bitrate)
        print("writing data:", data, "sampling-rate:", fs,  "at bit-rate:", bitrate, " to ", wave_file_path)
        write(wave_file_path, data, fs, subtype)

    # Low pass filter (type of low pass: butter) : function to remove the frequencies above the Shannon Nyquist frequency
    def low_pass(self, data, Fs_new, Fs):
        b, a =signal.butter(N=2, Wn=Fs_new/2, btype='low', analog=False, fs=Fs)

        filtered = signal.filtfilt(b, a, data)
        plt.plot(filtered)
        plt.savefig('filter.jpg')
        plt.close()
        plt.plot(data)
        plt.savefig('orig_data.jpg')
        plt.close()
        return filtered

    # downsample: function to return the down-sampled function based on the down-sampling factor
    def down_sample(self, data, factor, Fs_new, Fs):
        print("before lowpass:",data)
        low_filtered = self.low_pass(data, Fs_new, Fs)
        print("after lowpass:",low_filtered)
        return low_filtered[::factor]

    # cubic_interpolate: function to return upsampled array with cubic interpolated values
    def cubic_interpolate(self, data, t, num_samples):
        x = np.linspace(0, t, num=len(data), endpoint=True)
        y = data
        cs = interp1d(x, y, kind='cubic')
     
        xNew = np.linspace(0, t, num=num_samples, endpoint=True)
        return cs(xNew)

    # upsample: function to upsample original data to a new sampling rate
    def up_sample(self, data, Fold, Fnew, t):
        
        new_samples = int(int(len(data)/Fold) * int(Fnew))
        return self.cubic_interpolate(data, t, new_samples)

    # add_dither: function to generate and add noise to the original signal and return the noise added signal
    # def add_dither(self, original):
    #     noise = np.random.normal(0, .01, original.shape)  # generate noise with mean = 0 and standard dev = 0.01
    #     new_signal = original + noise  # add noise to the signal to generate signal with added dither
    #     return new_signal

    def add_dither(self, original, original_br, new_br):
        shape = new_br - 4  # calculate the noise shape based on the difference between original and new bitrate.
        noise = np.random.normal(0, 2**shape, original.shape)  # generate noise with mean = 0 and standard dev = 0.01

        maxval = np.max(np.abs(noise))
        bitlength = np.ceil(np.log2(maxval)).astype(int)

        # add noise to the signal to generate signal with added dither)
        new_signal = original + noise
        return new_signal

    # down_quantization: function to perform dithering and return the down-quantized signal
    def down_quantization(self, original, original_br, new_br):
        # Because our signal started the downsampling chain as an int32, we can recast it as an int32 before doing
        # further processing.
        dithered = self.add_dither(original, original_br, new_br)
        dithered = dithered.astype(np.int32)

        maxval = np.max(np.abs(dithered))
        bitlength = np.ceil(np.log2(maxval)).astype(int)

        if original_br > new_br:
            bit_shift = (original_br - new_br) + 1
        else:
            bit_shift = 0

        if bit_shift - 1 == 16:
            down_quantized = (dithered >> bit_shift)
            down_quantized = down_quantized.astype(np.int16)
        elif bit_shift - 1 == 24:
            down_quantized = (dithered >> bit_shift)

            # Because of the power loss with the drop to 16 bits the amplitude needs to be doubled.
            # down_quantized *= 3

            # Because of limitations in scipy's wave writing function, we need to encode this as a 16 bit integer.
            # However, the commented code reveals that only 8 bits are needed to encode the data.
            maxval_down = np.max(np.abs(down_quantized))
            bitlength_down = np.ceil(np.log2(maxval_down)).astype(int)
            down_quantized = down_quantized.astype(np.int16)
        else:
            down_quantized = original

        return down_quantized


