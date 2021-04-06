from dataclasses import dataclass
from music21 import converter

#parse krn file and create list of note names, frequencies, amplitudes, durations, and start and end times in seconds
#assumes input is a monophonic melody
#accomodates rests by setting amplitude to 0
def KrnParser(krn):
    krnfile='../KernFiles/' + krn

    s = converter.parse(krnfile)
    sflat = s.flat

    #initialize lists
    noteNames = []
    freqs = []
    amps = []
    durations = []
    startTimes = []
    endTimes = []

    i = 0;
    lastStart = 0;
    lastDur = 0;

    #populate lists for every note in the krn file
    for obj in sflat.iter.notesAndRests:
        if (obj.isNote) == True:
            amps.append(obj.volume.realized)
            freqs.append(obj.pitch.frequency)
            noteNames.append(obj.nameWithOctave)
        else:
            amps.append(0)
            freqs.append("")
            noteNames.append("")
        beat = obj.beat
        duration = obj.seconds
        durations.append(duration)

        if (i == 0):
            startTime = 0
        else:
            startTime = lastStart + lastDur

        startTimes.append(startTime)
        endTime = startTime + duration
        endTimes.append(endTime)

        lastStart = startTime
        lastDur = duration

        i += 1

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