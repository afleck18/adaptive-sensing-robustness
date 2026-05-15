import numpy as np

def vision_measurement(x, t):
    """
    Ranged measurements take the true value, add noise
    as a function of position, add observation dropout
    past a set distance and return the observed value.
    """
    pos = x[:2]

    noise_std = 0.05 + 0.12 * np.linalg.norm(pos)
    y = pos + noise_std * np.random.randn(2)
    
    if np.linalg.norm(pos) > 4.0:
        dropout_prob = 0.20
    else:
        dropout_prob = 0.0

    if np.random.rand() < dropout_prob:
        return None
    

    y += np.array([0.001 * t, -0.0005 * t])

    return y