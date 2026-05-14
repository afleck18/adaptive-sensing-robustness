import numpy as np

def direct_measurement(x):
    return x[:2] + 0.2 * np.random.randn(2)