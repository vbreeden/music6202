import numpy as np
from scipy.io.wavfile import read
from scipy.signal import correlate, correlation_lags
import matplotlib.pyplot as plt


# Parameters:
# filename: Name of file to be loaded
# Return values:
# stream: numpy array (float)
def loadSoundFile(filename):
    sr, stream = read(filename)
    return stream[:, 0]


# Parameters:
# x: numpy array (float)
# y: numpy array (float)
# Return values:
# z: numpy array (float)
def crossCorr(x, y):
    z = correlate(x, y)
    return z


def plotCorr(loop, snare, corr):
    lag = correlation_lags(len(loop), len(snare))
    offset = lag[0]
    fig, ax_corr = plt.subplots(1, 1)
    ax_corr.plot(lag, corr)
    plt.show()

    ind = np.argpartition(corr, -4)[-4:]
    print(ind)
    print(corr[ind])


if __name__ == '__main__':
    loop_file = 'drum_loop.wav'
    snare_file = 'snare.wav'
    drum_loop = loadSoundFile(loop_file)
    snare = loadSoundFile(snare_file)

    padded_snare = np.zeros(drum_loop.shape)
    padded_snare[0:len(snare)] = snare

    padded_loop = np.zeros(drum_loop.shape)
    padded_loop[0:len(drum_loop)] = drum_loop

    corr = crossCorr(padded_loop, padded_snare)

    plotCorr(padded_loop, padded_snare, corr)
    length = len(corr)


