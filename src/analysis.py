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


def time_lag(signal_1, signal_2, dt):
    signal_1 = np.asarray(signal_1)
    signal_2 = np.asarray(signal_2)

    signal_1 = (signal_1 - signal_1.mean()) / signal_1.std()
    signal_2 = (signal_2 - signal_2.mean()) / signal_2.std()

    correlation = np.correlate(signal_1, signal_2, mode="full")
    lags = np.arange(-len(signal_1) + 1, len(signal_1))

    best_lag = lags[np.argmax(correlation)]

    return best_lag * dt


def limit_violations(data, column, minimum, maximum):
    violations = data[
        (data[column] < minimum) |
        (data[column] > maximum)
    ].copy()

    return violations
    