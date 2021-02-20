import os
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt

results_dir = 'results/'
question1_file = '01_sinusoidal.png'
question2_file = '02_squareWave.png'
question3_file1 = '03_sineWaveFFT.png'
question3_file2 = '03_squareWaveFFT.png'
question4_file1 = '04_rectSpectrogram.png'
question4_file2 = '04_hannSpectrogram.png'
cwd = os.getcwd()

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


# Question 3: The FFT and its constituent parts are computed in this function.
def computeSpectrum(x, sample_rate_Hz):
    spectrum = fft(x)  # / x.shape[0]
    samples = spectrum.shape[-1]

    pos_samples = int(samples/2)

    # We're only interested in the real portion so we only return the positive values.
    f = np.asarray([i*sample_rate_Hz/samples for i in range(pos_samples)])
    XAbs = np.abs(spectrum)[:pos_samples]
    XPhase = np.angle(spectrum)[:pos_samples]
    XRe = spectrum.real[:pos_samples]
    XIm = spectrum.imag[:pos_samples]

    return f, XAbs, XPhase, XRe, XIm


# Question 4.1: Generate blocks used to create blocks for an STFT.
def generateBlocks(x, sample_rate_Hz, block_size, hop_size):

    # Find the raw number of blocks.
    blocks = (len(x) - block_size) / hop_size

    # If blocks isn't a whole number then we need to pad the original signal and recalculate the number of blocks.
    if not blocks.is_integer():
        pad_length = int(block_size + np.ceil(blocks)*hop_size - len(x))
        x = np.pad(x, (0, pad_length), 'constant')
        blocks = int((len(x) - block_size) / hop_size) + 1

    # Initialize the time slice array and signal matrix
    t = np.zeros(blocks)
    X = np.zeros(shape=(blocks, block_size))

    # Calculate timestamps for each sample in x. We will use this to find the timestamp of the start of each block.
    # There's probably a more efficient way to do this, but it's getting late and this method is easy to read.
    sample_time = 1 / sample_rate_Hz
    full_time = np.arange(0, sample_time*len(x), sample_time)

    # Populate t and X.
    start_pos = 0
    for i in range(blocks):
        t[i] = full_time[start_pos]
        X[i] = x[start_pos:start_pos+2048]
        start_pos += hop_size

    return t, X


# Question 4.2: Generate a spectrogram
def mySpecgram(x, block_size, hop_size, sampling_rate_Hz, window_type):
    hop_size = int(hop_size)

    t, X = generateBlocks(x, sampling_rate_Hz, block_size, hop_size)

    if window_type != 'hann':
        print('A hanning window was not requested so we will be defaulting to a rectangular window.')
        print('This is equivalent to not passing a window at all.')

    hann_window = np.hanning(block_size)
    magnitude_spectrogram = np.zeros(shape=(int(np.ceil(block_size/2)), X.shape[0]))

    for i in range(X.shape[0]):
        if window_type == 'hann':
            f, XAbs, XPhase, XRe, XIm = computeSpectrum(X[i]*hann_window, sampling_rate_Hz)
        else:
            f, XAbs, XPhase, XRe, XIm = computeSpectrum(X[i], sampling_rate_Hz)
        magnitude_spectrogram[:, i] = XAbs

    freq_vector = f
    time_vector = t

    magnitude_spectrogram = 10*np.log10(magnitude_spectrogram)

    plt.imshow(magnitude_spectrogram, origin='lower', interpolation='nearest',
               aspect='auto', extent=[t[0], t[-1], f[0], f[-1]])
    plt.colorbar()

    if window_type == 'hann':
        plt.title('Spectrogram with a Hanning Window')
        save_file = os.path.join(cwd, results_dir, question4_file2)
    else:
        save_file = os.path.join(cwd, results_dir, question4_file1)
        plt.title('Spectrogram with a Rectangular Window')

    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")

    plt.savefig(save_file)
    plt.show()

    return freq_vector, time_vector, magnitude_spectrogram


# Question 5: Generate a Sine Sweep
def generateSineSweep(spectrum):
    print(2)


# Waveforms are printed for questions 1 and 2.
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
    axes[1].plot(f, XPhase)
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
    save_file = os.path.join(cwd, results_dir, question1_file)
    plotWaveFunction(wave=x_sine, sr=sampling_rate_Hz, ms=5, title=title, save_file=save_file)

    # --------------------------------------
    # Question 2: Generate a 400Hz Square Wave
    phase_radians = 0
    t, x_square = generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians)

    # Plot the first 5ms of x
    title = '5ms plot of 400Hz Square Wave'
    save_file = os.path.join(cwd, results_dir, question2_file)
    plotWaveFunction(wave=x_square, sr=sampling_rate_Hz, ms=5, title=title, save_file=save_file)

    # --------------------------------------
    # Question 3: Fourier Transforms
    # Plot sine wave data
    title = 'Sine Wave Magnitude and Phase'
    xlabel = 'Frequency (Hz)'
    ylabels = ['Magnitude (energy)', 'Phase (radians)']
    save_file = os.path.join(cwd, results_dir, question3_file1)
    f, XAbs, XPhase, XRe, XIm = computeSpectrum(x_sine, sampling_rate_Hz)
    plotFFTData(f, XAbs, XPhase, title=title, xlabel=xlabel, ylabels=ylabels, save_file=save_file)

    # Plot square wave data
    title = 'Square Wave Magnitude and Phase'
    save_file = os.path.join(cwd, results_dir, question3_file2)
    f, XAbs, XPhase, XRe, XIm = computeSpectrum(x_square, sampling_rate_Hz)
    plotFFTData(f, XAbs, XPhase, title=title, xlabel=xlabel, ylabels=ylabels, save_file=save_file)

    # --------------------------------------
    # Question 4: Spectrogram
    block_size = 2048
    hop_size = 1024

    # Spectrogram of the square wave with a rectangular window applied.
    window_type = 'rect'
    freq_vector, time_vector, magnitude_spectrogram = mySpecgram(x_square, block_size, hop_size, sampling_rate_Hz, window_type)

    # Spectrogram of the square wave with a hanning window applied.
    window_type = 'hann'
    freq_vector, time_vector, magnitude_spectrogram = mySpecgram(x_square, block_size, hop_size, sampling_rate_Hz,
                                                                 window_type)

    # --------------------------------------
    # Question 4: Sine Sweep
    # Pass in the first block of spectrogram data
    generateSineSweep(magnitude_spectrogram[:, 0])
