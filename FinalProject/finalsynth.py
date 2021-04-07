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
    parser.add_argument('-l', '--lowpass', nargs='+', action='append', help='Add a lowpass filter to the signal path.'
                                                                            'Ex: finalsynth -l 100Hz')
    parser.add_argument('-r', '--reverb', nargs='+', action='append', help='Add a reverb effect to the signal path '
                                                                           'that utilizes a provided impulse response '
                                                                           'wav file. Ex: finalsynth -r IR.wav')
    parser.add_argument('-k', '--kern', nargs='+', action='append', help='Provide the name of the input file in kern '
                                                                         'format. Ex: finalsynth -k melody1.krn')
    return parser.parse_args()


if __name__ == '__main__':

    args = define_args()
    kern_file = args.kern[0][0]
    notes = Notes()
    notes.parse_kern(kern_file=kern_file)
    print(args)
