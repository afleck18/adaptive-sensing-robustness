import numpy as np

def direct_measurement(x):
    """
    Direct measurements take the true value, add Gaussian noise
    and return the observed measurement.
    """
    return x[:2] + 0.2 * np.random.randn(2)