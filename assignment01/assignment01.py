import numpy as np
from scipy.io.wavfile import read
from scipy.signal import correlate, correlation_lags
import matplotlib.pyplot as plt


results_dir = 'results/'
correlation_file = '01-correlation.png'
snareLocation_txt = '02-snareLocation.txt'
snareLocationProcessed_txt = '02-snareLocationProcessed.txt'


# Return the filestream for the given filename
def loadSoundFile(filename):
    sr, stream = read(filename)
    return sr, stream[:, 0]


# Perform the correlation on the arrays provided.
def crossCorr(x, y):
    z = correlate(x, y)
    return z


# Find the position of the Snare file
def findSnarePosition(snareFilename, loopFilename):
    # These first few lines are redundant but are necessary to meet the required functionality
    loop_sr, drum_loop = loadSoundFile(loop_file)
    snare_sr, snare = loadSoundFile(snare_file)
    padded_snare, padded_loop = padArrays(snare, drum_loop)
    corr = crossCorr(padded_loop, padded_snare)
    lag = calculateLag(padded_loop, padded_snare)
    raw_savefile = results_dir + snareLocation_txt


    # We know from examining the file that there are four snare hits in the drum loop so we retrieve the location of
    # the four maximum values in the array. The returned partition is in last to first order so we reverse it once
    # it is retrieved.
    snare_locs = np.argpartition(corr, -4)[-4:]
    snare_locs = np.flip(snare_locs)

    # Write the raw snare locations to file.
    # np.savetxt(raw_savefile, snare_locs, delimiter=',', fmt='%d')
    with open(raw_savefile, 'w') as f:
        f.write(str(snare_locs))

    # Adjust for lag and write the snare locations and associated times to file.
    offset = lag[0]
    snare_locs_w_lag = snare_locs - np.abs(offset)

    # This only works if the sample rates are the same. In this case we know they are, but normally we would
    # add in code to reduce the higher SR file so that they match before doing this calculation.
    if snare_sr == loop_sr:
        timestamps = snare_locs_w_lag / snare_sr
        processed_savefile = results_dir + snareLocationProcessed_txt
        with open(processed_savefile, 'w') as f:
            f.writelines('Snare location array adjusted for lag:\n')
            f.write(str(snare_locs_w_lag))
            f.write('\n\nTimestamps (in seconds) of snare hits:\n')
            f.write(str(timestamps))

    # Save the raw snare locations to file
    print(snare_locs)
    print(corr[snare_locs])


# Calculate correlation lags. This is needed for plotting and finding the position of the snare hits.
def calculateLag(loop, snare):
    lag = correlation_lags(len(loop), len(snare))
    return lag


# Plot the lag adjusted correlation.
def plotCorr(loop, snare, corr):
    savefile = results_dir + correlation_file
    lag = calculateLag(loop, snare)
    offset = lag[0]
    fig, ax = plt.subplots(1, 1)
    ax.set_title('Cross-correlation of Snare and Loop')
    ax.set_xlabel('Lag-adjusted Sample Number')
    ax.set_ylabel('Normalized Cross-correlation Coefficient')
    ax.plot(lag, corr)
    plt.savefig(savefile)
    plt.show()


# Pad the shorter of the two arrays with zeroes so that they are the same length.
def padArrays(snare, drum_loop):
    # If the snare is shorter than the drum loop pad the snare array with zeroes to match the length of the drum loop.
    # Then use the padding function to ensure the shape of the drum loop matches the snare. This step won't normally
    # matter, but there are edge cases where not performing this step might have unpredictable results.
    # If a drum loop is provided that is shorter than the snare file perform the inverse of the padding operations.
    if len(snare) <= len(drum_loop):
        padded_snare = np.zeros(drum_loop.shape)
        padded_snare[0:len(snare)] = snare
        padded_loop = np.zeros(drum_loop.shape)
        padded_loop[0:len(drum_loop)] = drum_loop
    else:
        padded_loop = np.zeros(snare.shape)
        padded_loop[0:len(drum_loop)] = drum_loop
        padded_snare = np.zeros(snare.shape)
        padded_snare[0:len(snare)] = snare

    return padded_snare, padded_loop


# Normalize the provided array
def normalizeArray(arr):
    norm = np.linalg.norm(arr)
    arr = arr / norm
    return arr


if __name__ == '__main__':
    loop_file = 'drum_loop.wav'
    snare_file = 'snare.wav'
    loop_sr, drum_loop = loadSoundFile(loop_file)
    snare_sr, snare = loadSoundFile(snare_file)

    # Pad the shorter array to match the length of the longer array.
    padded_snare, padded_loop = padArrays(snare, drum_loop)

    # Perform the correlation. The longer file must be passed first, otherwise the graph is generated with
    # the signal peaks out of phase.
    corr = crossCorr(padded_loop, padded_snare)

    # Normalize the correlation coefficients, it makes the graph prettier.
    normalized_corr = normalizeArray(corr)

    # Plot the correlation.
    plotCorr(padded_loop, padded_snare, normalized_corr)

    # Find snare locations
    findSnarePosition(snare_file, loop_file)
