from math import ceil
import numpy as np
from dataclasses import dataclass, field
from music21 import converter


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

        stream = converter.parse(self.kern_file)
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
