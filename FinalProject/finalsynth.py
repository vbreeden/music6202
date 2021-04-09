# This is the main file for Group 4's final project.
# Group Members:
# Virgil Breeden
# Laney Light
# Rhythm Jain
import sys
import argparse
from FinalProject.Engine.AudioCore import Notes
# from FinalProject.Effects.Convolution import Reverb
# from FinalProject.Effects.Filter import Bandpass, Lowpass
# from FinalProject.Effects.Modulation import Chorus, Delay, Vibrato
# from FinalProject.Engine.Synth import AdditiveSynth, WavetableSynth

# This is the parser that will parse commandline arguments.
parser = argparse.ArgumentParser()

# Custom arguments are added here. By default, argparse provides a Help argument. It can be accessed using:
# python finalsynth.py -h
def define_args():
    # Synthesizer choice
    parser.add_argument('-s', '--synth', nargs='+', action='append', help='Choose the synth engine to be used.'
                                                                          'Ex: finalsynth -s wavetable')

    # Modulation effects
    parser.add_argument('-c', '--chorus', nargs='+', action='append', help='Add a chorus effect to the signal path.'
                                                                           'Ex: finalsynth -c ChorusParam')
    parser.add_argument('-d', '--delay', nargs='+', action='append', help='Add a delay effect to the signal path.'
                                                                          'Ex: finalsynth -d DelayParam')
    parser.add_argument('-v', '--vibrato', nargs='+', action='append', help='Add a chorus vibrato to the signal path.'
                                                                            'Ex: finalsynth -v VibratoParam')

    # Filters
    parser.add_argument('-b', '--bandpass', nargs='+', action='append', help='Add a bandpass filter to the signal path.'
                                                                             'Ex: finalsynth -b 400Hz 500Hz')
    parser.add_argument('-l', '--lowpass', nargs='+', action='append', help='Add a lowpass filter to the signal path.'
                                                                            'Ex: finalsynth -l 100Hz')

    # Convolution effects
    parser.add_argument('-r', '--reverb', nargs='+', action='append', help='Add a reverb effect to the signal path '
                                                                           'that utilizes a provided impulse response '
                                                                           'wav file. Ex: finalsynth -r IR.wav')

    # Kern files
    parser.add_argument('-k', '--kern', nargs='+', action='append', help='Provide the name of the input file in kern '
                                                                         'format. Ex: finalsynth -k melody1.krn')
    return parser.parse_args()


if __name__ == '__main__':

    args = define_args()
    kern_file = args.kern[0][0]

    synth = args.synth[0][0]

    notes = Notes()
    notes.parse_kern(kern_file=kern_file)

    if synth == 'wavetable':
        # Call wavetable synth
        pass
    elif synth == 'additive':
        # Call additive synth
        pass
    else:
        print('No valid synthesizer provided.')
        exit(0)

    # This line exists as a convenient place to put a breakpoint for inspecting stored data. It will need
    # to be removed before delivery.
    print(args)

