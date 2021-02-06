import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import convolve
from timeit import default_timer as timer


results_dir = 'results/'
convolution_file = '01_convolution.png'
convstats_file = '02_convolution_stats.txt'


# Parameters:
# x: Signal
# h: Impulse
# Question 1 Answer: Given a signal with 200 samples and an impulse with 100 samples, the resulting convolution
# will contain 299 samples.
def myTimeConv(x, h):
    sig_len = len(x)
    imp_len = len(h)
    conv_len = sig_len + imp_len - 1

    conv_arr = np.zeros(conv_len)

    # The provided audio files are in int16 format so they need to be expanded to 64 bit to prevent
    # RuntimeWarning: overflow encountered in short_scalars.
    if x.dtype == np.dtype(np.int16):
        x = x.astype(np.int)
    if h.dtype == np.dtype(np.int16):
        h = h.astype(np.int)

    for i in range(conv_len):
        prod_sum = 0.
        for j in range(imp_len):
            if j <= i and i - j < sig_len:
                prod_sum += x[int(i) - int(j)] * h[int(j)]
                conv_arr[i] = prod_sum
    return conv_arr


def CompareConv(x, h):
    time = np.zeros(2)

    # Time my convlution function
    start = timer()
    y_time_myconv = myTimeConv(x, h)
    end = timer()
    time[0] = end - start

    # Time scipy's convolution function
    start = timer()
    y_time_scipy = convolve(x, h)
    end = timer()
    time[1] = end - start

    diff = y_time_myconv - y_time_scipy
    m = np.sum(diff)/(y_time_myconv.size*y_time_scipy.size)
    mabs = np.abs(m)
    stdev = np.std(diff)

    return m, mabs, stdev, time


# Parameters:
# samples: Number of samples in the triangle wave. (i.e. it's length)
# peak_amp: Peak Amplitude
# Returns: Triangle Wave
def triangle_wave(samples, peak_amp):
    theta = np.arctan(peak_amp/(samples/2))
    wave = np.zeros(samples)

    # Construct a triangle wave that ensures first and last samples are zero.
    # If an array of odd sample length is requested ensure that the midpoint equals the peak amplitude.
    for i in range(int(samples/2)):
        wave[i] = i*np.tan(theta)
        wave[samples - 1 - i] = i*np.tan(theta)
    if samples % 2 != 0:
        wave[int(np.floor(samples/2))] = peak_amp

    return wave


# Return the filestream for the given filename
def loadSoundFile(filename):
    sr, stream = read(filename)

    # Normalize the data stream so that scipy's convolution doesn't break.
    normalized_stream = stream / np.abs(np.max(stream))
    return sr, normalized_stream


if __name__ == '__main__':
    impulse_file = 'impulse-response.wav'
    piano_file = 'piano.wav'
    impulse_sr, impulse = loadSoundFile(impulse_file)
    piano_sr, piano = loadSoundFile(piano_file)

    x = np.ones(200)
    h = triangle_wave(51, 1)

    y_time = myTimeConv(x, h)

    savefile = results_dir + convolution_file
    fig, ax = plt.subplots(1, 1)
    ax.set_title('Convolution of a triangle wave with a DC signal')
    ax.set_xlabel('Sample Number')
    ax.set_ylabel('Convolution Coefficient')
    ax.plot(y_time)
    plt.savefig(savefile)
    plt.show()

    m, mabs, stdev, time = CompareConv(piano, impulse)

    savefile = results_dir + convstats_file

    with open(savefile, 'w') as f:
        f.write('m: %.2E\n' % m)
        f.write('mabs: %.2E\n' % mabs)
        f.write('stdev: %.2E\n' % stdev)
        f.write('time: %s\n' % str(time))
