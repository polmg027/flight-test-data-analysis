import numpy as np


def dominant_frequency(signal, dt):
    susbtract_mean = signal - signal.mean()

    fft_values = np.fft.rfft(susbtract_mean)

    frequencies = np.fft.rfftfreq(len(susbtract_mean), d=dt)

    amplitude = np.abs(fft_values)

    dominant_index = np.argmax(amplitude[1:]) + 1

    dominant_frequency = frequencies[dominant_index]

    return dominant_frequency


def peak_to_peak(signal):
    amplitude  = signal.max() - signal.min()
    return amplitude 


def check_limits(signal, minimum, maximum):

    if signal.max() <= maximum and signal.min() >= minimum:
        return True
    else:
        return False
    