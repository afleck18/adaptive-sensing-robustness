import numpy as np

def ranged_measurement(x):
    """
        Geometry-dependent sensing:
        Measurement noise increases with distance from the origin,
        simulating degradation in sensing quality as the target
        moves farther from the observer.
    """
    pos = x[:2]
    noise_std = 0.05 + 0.12 * np.linalg.norm(pos)
    return pos + noise_std * np.random.randn(2)