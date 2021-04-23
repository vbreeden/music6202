from math import ceil
import numpy as np
from dataclasses import dataclass, field
from music21 import converter

import soundfile as sf
from soundfile import SoundFile, write
from subtypes import Subtype
import scipy
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
        write(wave_file_path, data, fs, subtype)

    # Low pass filter (type of low pass: butter) to remove the frequencies above the Shannon Nyquist threshold
    def low_pass(self, data, factor):
        # b, a = signal.butter(3, 11025, 'lowpass', analog=True)
        # print(b, a)
        print(type(factor))
        b, a = signal.butter(3, 0.05, 'low')
        filtered = signal.filtfilt(b, a, data)
        print("filtered:", filtered)
        return filtered

    # downsample: function to return the down-sampled function based on the down-sampling factor
    def down_sample(self, data, factor):
        low_filtered = self.low_pass(data, factor)
        return low_filtered[::factor]

    # cubic_interpolate: function to return upsampled array with cubic interpolated values
    def cubic_interpolate(self, data, t, num_samples):
        x = np.linspace(0, t, num=len(data), endpoint=True)
        y = data
        cs = interp1d(x, y, kind='cubic')
     
        xNew = np.linspace(0, t, num=num_samples, endpoint=True)
        return cs(xNew)

    # upsample: function 
    def up_sample(self, data, Fold, Fnew, t):
        
        new_samples = int(int(len(data)/Fold) * int(Fnew))
        return self.cubic_interpolate(data, t, new_samples)

    # add_dither: function to generate and add noise to the original signal and return the noise added signal
    def add_dither(self, original):
        noise = np.random.normal(0, .01, original.shape) #generate noise with mean = 0 and standard dev = 0.01
        new_signal = original + noise #add noise to the signal to generate signal with added dither
        return new_signal 

    # down_quantization: function to perform dithering and return the down-quantized signal
    def down_quantization(self, original, original_br, new_br, dither=1):
        if (dither):
            dithered = self.add_dither(original)
        else:
            dithered = original
        down_quantized =  ((dithered /2**original_br)* 2**new_br).astype(np.float32)
        return down_quantized


