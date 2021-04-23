from scipy.io.wavfile import read, write
from scipy.signal import resample, decimate
import numpy as np

filename = "McQueen_square.wav"
x = read(filename, mmap=False)
target_fs = 8000

secs = len(x[1])/44100.0
num_samp = int(secs * target_fs) + 1
sg = resample(x[1], num_samp)


# print("current sampling rate = ", x[0])
# resampled_signal = resample( x[1], 8000 )
# print(resampled_signal)

write("example.wav", 8000, sg)


def harvest_get_downsampled_signal(x, fs, target_fs):
    decimation_ratio = np.round(fs / target_fs)
    offset = np.ceil(140. / decimation_ratio) * decimation_ratio
    start_pad = x[0] * np.ones(int(offset), dtype=np.float32)
    end_pad = x[-1] * np.ones(int(offset), dtype=np.float32)
    x = np.concatenate((start_pad, x, end_pad), axis=0)

    if fs < target_fs:
        raise ValueError("CASE NOT HANDLED IN harvest_get_downsampled_signal")
    else:
        try:
            y0 = decimate(x, int(decimation_ratio), 3, zero_phase=True)
        except:
            y0 = decimate(x, int(decimation_ratio), 3)
        actual_fs = fs / decimation_ratio
        y = y0[int(offset / decimation_ratio):-int(offset / decimation_ratio)]
    y = y - np.mean(y)
    return y, actual_fs


# returned_y, returned_fs = returned = harvest_get_downsampled_signal(x[1],x[0], 8000)
# print("Before: ",x[0], x[1], len(x[1]))

# print("After: ", returned_fs, len(returned_y))

# write("example_decimate.wav", returned_fs, int(returned_y))