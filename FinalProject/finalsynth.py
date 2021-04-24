# This is the main file for Group 4's final project.
# Group Members:
# Virgil Breeden
# Laney Light
# Rhythm Jain
import sys
import argparse
import numpy as np
from Engine.AudioCore import Notes
from Engine.Synth import AdditiveSynth, WavetableSynth
# from FinalProject.Effects.Convolution import Reverb
# from FinalProject.Effects.Filter import Bandpass, Lowpass
# from FinalProject.Effects.Modulation import Chorus, Delay, Vibrato
from Effects.Modulation import Vibrato
# from FinalProject.Engine.Synth import AdditiveSynth, WavetableSynth

# This is the parser that will parse commandline arguments.
parser = argparse.ArgumentParser()


# Custom arguments are added here. By default, argparse provides a Help argument. It can be accessed using:
# python finalsynth.py -h
def define_args():
    # Synthesizer choice
    parser.add_argument('-s', '--synth', nargs='+', action='append',
                        help='Choose the synth engine to be used (wavetable or additive) and pass in the appropriate '
                             'parameters. Ex: finalsynth -s wavetable 5 sweep 0.75')
    # Type of additive synthesizer
    # parser.add_argument('-t', '--type', nargs='+', action='append',
    #                     help='Choose type of additive synthesis (square or sine). Ex: finalsynth -s additive -t sine')

    # Starting timbre of wavetable synthesizer
    # parser.add_argument('-m', '--timbre', nargs='+', action='append',
    #                     help='Choose starting timbre of wavetable synth (integer from 0=pure square to 10=pure sine).'
    #                          'Ex: finalsynth -s wavetable -m 5')
    # parser.add_argument('-w', '--sweep', nargs='+', action='append',
    # help='Choose whether to sweep wavetable modulating between sine and square (static or sweep).'
    #                          'Ex: finalsynth -s wavetable -m 5 -w sweep')
    # parser.add_argument('-p', '--speed', nargs='+', action='append',
    #                     help='Speed of sweep: amount of time in seconds to modulate between sine and square.'
    #                          'Ex: finalsynth -s wavetable -m 5 -w sweep -p .5')

    # Modulation effects
    parser.add_argument('-c', '--chorus', nargs='+', action='append', help='Add a chorus effect to the signal path.'
                                                                           'Ex: finalsynth -c ChorusParam')
    parser.add_argument('-d', '--delay', nargs='+', action='append', help='Add a delay effect to the signal path.'
                                                                          'Ex: finalsynth -d DelayParam')
    parser.add_argument('-v', '--vibrato', nargs='+', action='append', help='Add a vibrato to the signal path. Pass in max delay samples and frequency modulation.'
                                                                            'Ex: finalsynth -v 200 1')

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


# Get the list of effects chosen by the user.
def get_effects_list():
    # sys.argv contains the full command in list form that was called by the user. We can loop through it looking for
    # effects flags.
    # It's not elegant, but it works.

    arg_list = []
    for arg in sys.argv:
        if arg == '-c' or arg == '--chorus':
            arg_list.append('chorus')
        elif arg == '-d' or arg == '--delay':
            arg_list.append('delay')
        elif arg == '-v' or arg == '--vibrato':
            arg_list.append('vibrato')
        elif arg == '-b' or arg == '--bandpass':
            arg_list.append('bandpass')
        elif arg == '-l' or arg == '--lowpass':
            arg_list.append('lowpass')
        elif arg == '-r' or arg == '--reverb':
            arg_list.append('reverb')

    return arg_list


if __name__ == '__main__':
    # Retrieve the argument information
    args = define_args()
    print(args)
    effects_list = get_effects_list()

    # The kern file declaration is here to prevent the debugger from posting any undeclared-variable warnings.
    kern_file = ''
    if args.kern is not None:
        kern_file = args.kern[0][0]
    else:
        print('A kern file must be passed to the synthesizer.')
        exit(0)

    synth = ''
    if args.synth is not None:
        synth = args.synth[0][0]
    else:
        print('A synth engine must be selected.')
        exit(0)

    if synth == 'additive':
        #print('Do additive stuff here.')
        type = str(args.synth[0][1]).lower()
        if type != 'square' and type != 'sine':
            print("The only valid additive synthesizer types are 'square' and 'sine'.")
        # type = args.type[0][0]

    elif synth == 'wavetable':
        if len(args.synth[0]) >= 3:
            timbre = np.abs(int(args.synth[0][1]))
            if timbre > 10:
                timbre = 10  # Gracefully accept any number, but cap it at 10.
            sweep = str(args.synth[0][2]).lower()
            if sweep.lower() == 'sweep':
                if len(args.synth[0]) >= 4:
                    speed = np.abs(float(args.synth[0][3]))
                else:
                    print('When passing a sweeping signal, a sweep period must be provided.')
                    exit(0)
            else:
                speed = 0
        else:
            print('The timbre value and sweep/static arguments must be passed with the wavetable.')
            print("If 'sweep' is passed as a parameter, a sweep period must also be passed.")
            exit(0)
    else:
        print('Only additive and wavetable synths are supported.')
        exit(0)

    if args.vibrato is not None:
        vibrato = Vibrato()

    notes = Notes()
    notes.parse_kern(kern_file=kern_file)

    args_ordered = sys.argv

    # Use the synth engine selected by the user to digitize the melody from the kern file.
    if synth.lower() == 'wavetable':
        synthesizer = WavetableSynth()
        synthesizer.generate_wavetable(notes, timbre, sweep, speed)
        # print('We will want to return the created audio data to this point so we can pass it through the effects')
    elif synth.lower() == 'additive':
        # Call additive synth
        # print('We will want to return the created audio data to this point so we can pass it through the effects')
        synthesizer = AdditiveSynth()
        synthesizer.generate_additive_wav(notes, type)
    else:
        print('Additive and Wavetable are the only valid synthesizer options.')
        exit(0)

    chorus_count = 0
    delay_count = 0
    vibrato_count = 0
    bandpass_count = 0
    lowpass_count = 0
    reverb_count = 0

    # Loop through the effects selected by the user and apply them to the melody in order.
    # The arg_list lists will contain the list of arguments passed in by the user that are associated with that
    # instance of that argument. This is the cleanest way I could come up with to separate multiple instances of an
    # Effect. For example, if the user inserts a low pass filter more than once then args.lowpass[0] will have the
    # arguments for the first lowpass filter, and args.lowpass[1] will have the arguments for the second lowpass filter.
    for effect in effects_list:
        if effect == 'chorus':
            chorus_arg_list = args.chorus[chorus_count]
            chorus_count += 1
            print('put chorus call here.')
            print(chorus_arg_list)
        elif effect == 'delay':
            delay_arg_list = args.delay[delay_count]
            delay_count += 1
            print('put delay call here.')
            print(delay_arg_list)
        elif effect == 'vibrato':
            #print(args.vibrato)
            if args.vibrato is not None:
                vibrato_arg_list = args.vibrato[vibrato_count]
                if vibrato_arg_list is not None:
                    maxDelaySamps = int(vibrato_arg_list[0])
                    fmod = int(vibrato_arg_list[1])
                #set default max delay and frequency modulation if no input parameters are provided
                else:
                    maxDelaySamps = 50
                    fmod = 1
            #print('maxDelaySamps',maxDelaySamps)
            #print('fmod',fmod)
            vibrato.apply_vibrato(synthesizer.wave, maxDelaySamps, fmod)
            vibrato_count += 1
            #print('put vibrato call here.')
            print(vibrato_arg_list)
        elif effect == 'bandpass':
            bandpass_arg_list = args.bandpass[bandpass_count]
            bandpass_count += 1
            print('put bandpass call here.')
            print(bandpass_arg_list)
        elif effect == 'lowpass':
            lowpass_arg_list = args.lowpass[lowpass_count]
            lowpass_count += 1
            print('put lowpass call here.')
            print(lowpass_arg_list)
        elif effect == 'reverb':
            reverb_arg_list = args.reverb[reverb_count]
            reverb_count += 1
            print('put reverb call here.')
            print(reverb_arg_list)

    # Down-sample and write-to-audio function calls should be placed here.

    # This line exists as a convenient place to put a breakpoint for inspecting stored data. It will need
    # to be removed before delivery.
    print(args)


