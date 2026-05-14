import numpy as np

def moving_average(a, n=3):
    return np.convolve(a, np.ones(n), 'valid') / n

def first_crossing(signal, threshold):
    for t, val in enumerate(signal):
        if val > threshold:
            return t
    return None