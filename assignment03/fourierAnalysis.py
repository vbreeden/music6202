import numpy as np
import matplotlib.pyplot as plt


results_dir = 'results/'
question1_file = '01_sinusoidal.png'
question2_file = '02_squareWave.png'


# Question 1: Generating sinusoids in Python
def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    # x = amplitude*np.sin(2*np.pi*frequency_Hz*length_secs+phase_radians)
    samples = int(sampling_rate_Hz * length_secs)

    w = 2*np.pi*frequency_Hz
    t = np.fromiter([sample_time/sampling_rate_Hz for sample_time in range(samples)], dtype=np.float)
    x = [amplitude*np.sin(w*sample_time/sampling_rate_Hz+phase_radians) for sample_time in range(samples)]

    return t, x


# Question 2: Combine Sinusoids to generate waveforms with complex spectra (10 sinusoidals)
def generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    t = np.zeros(int(frequency_Hz*length_secs))
    sinusoids = []
    # A Square wave is a summation of odd harmonics (1, 3, 5, 7, etc)
    for i in range(10):
        interval = 2*i + 1
        harmonic = interval * frequency_Hz
        t_samples, x = generateSinusoidal(amplitude, sampling_rate_Hz, harmonic, length_secs, phase_radians)
        t = t_samples
        sinusoids.append(x)

    return t, 0


def plotWaveFunction(wave, sr, ms, title, save_file):

    # Set the tick marks to display milliseconds instead of samples.
    samples = int(sr / 1000 * ms)
    samples_per_ms = sr/1000
    x_ticks = [float(i) for i in range(int(np.ceil(samples / samples_per_ms)))]

    fig, ax = plt.subplots(1, 1)
    ax.set_title(title)
    ax.set_xlabel('Time(ms)')
    ax.set_ylabel('Amplitude')

    # There is a bug in set_xticklabels that requires an empty element at the beginning of a list to properly plot
    # custom labels.
    ax.set_xticklabels([''] + x_ticks)
    ax.plot((wave[:samples]))
    plt.savefig(save_file)
    plt.show()


if __name__ == '__main__':
    amplitude = 1
    sampling_rate_Hz = 44100
    frequency_Hz = 400
    length_secs = 0.5
    phase_radians = np.pi/2

    # Question 1: Generate a 400Hz Sine Wave
    # t, x = generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians)
    #
    # # Plot the first 5ms of x
    # title = '5ms plot of 400Hz Sine Wave'
    # save_file = results_dir + question1_file
    # plotWaveFunction(wave=x, sr=sampling_rate_Hz, ms=5, title=title, save_file=save_file)

    # Question 2: Generate a 400Hz Square Wave
    t, x = generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians)

    # Plot the first 5ms of x
    title = '5ms plot of 400Hz Square Wave'
    save_file = results_dir + question2_file
    plotWaveFunction(wave=x, sr=sampling_rate_Hz, ms=5, title=title, save_file=save_file)