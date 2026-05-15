import numpy as np

def direct_measurement(x):
    """
        Direct sensing:
        Measurement noise remains constant simulating
        a direct measurement of system state.
    """
    return x[:2] + 0.2 * np.random.randn(2)