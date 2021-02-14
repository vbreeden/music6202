import numpy as np
from numpy.fft import fft, fftfreq
import matplotlib.pyplot as plt


results_dir = 'results/'
question1_file = '01_sinusoidal.png'
question2_file = '02_squareWave.png'
question3_file1 = '03_sineWaveFFT.png'
question3_file2 = '03_squareWaveFFT.png'


# Question 1: Generating sinusoids in Python
def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    # x = amplitude*np.sin(2*np.pi*frequency_Hz*length_secs+phase_radians)
    samples = int(sampling_rate_Hz * length_secs)
    sample_time = 1 / sampling_rate_Hz
    w = 2 * np.pi * frequency_Hz

    t = np.arange(0, (samples * sample_time) + sample_time, sample_time)
    x = amplitude*np.sin(w*t + phase_radians)

    # t = np.fromiter([sample_time/sampling_rate_Hz for sample_time in range(samples)], dtype=np.float)
    # x = [amplitude*np.sin((w*sample_time/sampling_rate_Hz)+phase_radians) for sample_time in range(samples)]

    return t, x


# Question 2: Combine Sinusoids to generate waveforms with complex spectra (10 sinusoidals)
def generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    iterations = 10
    t = np.zeros(int(sampling_rate_Hz*length_secs) + 1)
    sinusoids = np.zeros(len(t))
    # A Square wave is a summation of odd harmonics (1, 3, 5, 7, etc)
    for i in range(iterations):
        k = i+1
        interval = 2*i + 1
        harmonic = interval * frequency_Hz
        amp = amplitude * (4/(np.pi*(2*k-1)))
        t_samples, x = generateSinusoidal(amp, sampling_rate_Hz, harmonic, length_secs, phase_radians)
        t = t_samples
        sinusoids = np.add(sinusoids, x)

    return t, sinusoids


def computeSpectrum(x, sample_rate_Hz):
    spectrum = fft(x) / x.shape[0]
    samples = spectrum.shape[-1]

    pos_samples = int(samples/2)
    time_step = 1/sample_rate_Hz

    # We're only interested in the real portion so we only return the positive values.
    f = fftfreq(samples, time_step)[:pos_samples]
    XAbs = np.abs(spectrum)[:pos_samples]
    XPhase = np.angle(spectrum)[:pos_samples]
    XRe = spectrum.real[:pos_samples]
    XIm = spectrum.imag[:pos_samples]

    return f, XAbs, XPhase, XRe, XIm


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


# Plot FFT Data for Question 3
def plotFFTData(f, XAbs, XPhase, title, xlabel, ylabels, save_file):
    fig, axes = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0})
    fig.suptitle(title)
    axes[0].plot(f, XAbs)
    axes[0].set(xlabel=xlabel)
    axes[0].set(ylabel=ylabels[0])
    axes[1].plot(f, np.unwrap(XPhase))
    # axes[1].plot(f, XPhase)
    axes[1].set(xlabel=xlabel)
    axes[1].set(ylabel=ylabels[1])

    for ax in axes:
        ax.label_outer()

    plt.savefig(save_file)
    plt.show()


if __name__ == '__main__':
    amplitude = 1
    sampling_rate_Hz = 44100
    frequency_Hz = 400
    length_secs = 0.5
    phase_radians = np.pi/2

    # --------------------------------------
    # Question 1: Generate a 400Hz Sine Wave
    t, x_sine = generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians)

    # Plot the first 5ms of x
    title = '5ms plot of 400Hz Sine Wave'
    save_file = results_dir + question1_file
    plotWaveFunction(wave=x_sine, sr=sampling_rate_Hz, ms=5, title=title, save_file=save_file)

    # --------------------------------------
    # Question 2: Generate a 400Hz Square Wave
    phase_radians = 0
    t, x_square = generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians)

    # Plot the first 5ms of x
    title = '5ms plot of 400Hz Square Wave'
    save_file = results_dir + question2_file
    plotWaveFunction(wave=x_square, sr=sampling_rate_Hz, ms=5, title=title, save_file=save_file)

    # --------------------------------------
    # Question 3: Fourier Transforms
    # Plot sine wave data
    title = 'Sine Wave Magnitude and Phase'
    xlabel = 'Frequency'
    ylabels = ['Magnitude (energy)', 'Phase (radians)']
    save_file = results_dir + question3_file1
    f, XAbs, XPhase, XRe, XIm = computeSpectrum(x_sine, sampling_rate_Hz)
    plotFFTData(f, XAbs, XPhase, title=title, xlabel=xlabel, ylabels=ylabels, save_file=save_file)

    # Plot square wave data
    title = 'Square Wave Magnitude and Phase'
    save_file = results_dir + question3_file2
    f, XAbs, XPhase, XRe, XIm = computeSpectrum(x_square, sampling_rate_Hz)
    plotFFTData(f, XAbs, XPhase, title=title, xlabel=xlabel, ylabels=ylabels, save_file=save_file)
