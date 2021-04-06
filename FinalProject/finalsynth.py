# This is the main file for Group 4's final project.
# Group Members:
# Virgil Breeden
# Laney Light
# Rhythm Jain
import sys
import argparse
from .Engine.AudioCore import KrnParser
#from FinalProject.Effects.Convolution import Reverb
#from FinalProject.Effects.Filter import Bandpass, Lowpass
#from FinalProject.Effects.Modulation import Chorus, Delay, Vibrato
#from FinalProject.Engine.Synth import AdditiveSynth, WavetableSynth

# This is the parser that will parse commandline arguments.
parser = argparse.ArgumentParser()


# Custom arguments are added here. By default, argparse provides a Help argument. It can be accessed using:
# python finalsynth.py -h
def define_args():
    parser.add_argument('-r', help='Add a reverb effect to the signal path that utilizes a provided impulse response '
                                   'wav file. Ex: finalsynth -r IR.wav')
    parser.add_argument('-rx', type=int, help='Provide the blend percentage for the reverb effect. '
                                              'Ex: finalsynth -r IR.wav -rx 50')
    parser.add_argument('-krn', help='Provide the name of the input file in kern format'
                                   '. Ex: finalsynth -krn melody1.krn')
    return parser.parse_args()


if __name__ == '__main__':
    args = define_args()
    print(args)

    KrnParser(args.krn)
    print('noteNames=', noteNames)
    print('freqs=', freqs)
    print('amps=', amps)
    print('startTimes=', startTimes)
    print('durations=', durations)
    print('endTimes=', endTimes)
