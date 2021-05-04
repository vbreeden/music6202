from Effects.Filter import Lowpass
from math import ceil
import numpy as np
from dataclasses import dataclass, field
from music21 import converter
from scipy.interpolate import interp1d
from scipy import signal
import wavio
import os


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
        print("writing data:", data, "sampling-rate:", fs,  "at bit-rate:", bitrate, " to ", wave_file_path)
        if bitrate == 8:
            sampwidth=1  
        elif bitrate == 16:
            sampwidth = 2
        elif bitrate == 24:
            sampwidth = 3
        else: 
            sampwidth = 4

        output_dir = 'audio/'
        cwd = os.getcwd()
        output_file_path = os.path.join(cwd, output_dir, wave_file_path)

        wavio.write(output_file_path, data, fs, sampwidth=sampwidth)

    # Low pass filter (type of low pass: butter) : function to remove the frequencies above
    # the Shannon Nyquist frequency
    def low_pass(self, data, Fs_new, Fs):
        b, a =signal.butter(N=2, Wn=Fs_new/2, btype='low', analog=False, fs=Fs)
        filtered = signal.filtfilt(b, a, data)
        return filtered.astype(np.int32)

    # downsample: function to return the down-sampled function based on the down-sampling factor
    def down_sample(self, data, factor, Fs_new, Fs):
        lp = Lowpass()
        low_filtered = lp.low_pass(data, Fs_new, Fs)
        return low_filtered[::factor]

    # cubic_interpolate: function to return upsampled array with cubic interpolated values
    def cubic_interpolate(self, data, t, num_samples):
        x = np.linspace(0, t, num=len(data), endpoint=True)
        y = data
        cs = interp1d(x, y, kind='cubic')
        xNew = np.linspace(0, t, num=num_samples, endpoint=True)
        out = cs(xNew).astype(np.int32)
        return out

    # upsample: function to upsample original data to a new sampling rate
    def up_sample(self, data, Fold, Fnew, t):
        
        new_samples = int(int(len(data)/Fold) * int(Fnew))
        return self.cubic_interpolate(data, t, new_samples)

    def add_triangular_dither(self, original, original_br, new_br):
        # shape = original_br-new_br
        # calculate the noise shape based on the difference
        # between original and new bitrate.
        diff = original_br - new_br
        left = (-1)*(2**diff)
        mode = 0
        right = (2**diff) - 1
        size = original.shape
        noise = np.random.triangular(left, mode, right, size)  # generate noise with mean = 0 and standard dev = 0.01
        noise = noise.astype(np.int32)

        new_signal = original + noise  # add noise to the signal to generate signal with added dither
        return new_signal 

    # down_quantization: function to perform dithering and return the down-quantized signal
    def down_quantization(self, original, original_br, new_br):
        """
        The down quantization has the following steps:     
            1. Add dithering to the original audio
            2. Create an array of zeros that has datatype of specific bitrate
            3. Downquantize by right shifting
            4. Return the array of specific bitrate type
        """
        dithered = self.add_triangular_dither(original,original_br, new_br)                
        dithered = dithered.astype(np.int32)
        down_quantized = np.zeros(len(dithered), dtype=np.int32)
        
        for i in range(len(dithered)):
            down_quantized[i] = dithered[i] >> (original_br-new_br)
        return down_quantized
