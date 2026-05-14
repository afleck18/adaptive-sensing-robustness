import numpy as np

def ranged_measurement(x):
    pos = x[:2]
    noise_std = 0.05 + 0.12 * np.linalg.norm(pos)
    return pos + noise_std * np.random.randn(2)