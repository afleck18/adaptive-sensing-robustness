import numpy as np

def simulate_system(T, dt):
    """
    Simulates system for all time values. System dynamics
    were manually changed after t=100
    """
    x = np.zeros((T, 4))
    x[0] = [1.0, 0.5, 0.8, 0.2]

    for t in range(T - 1):
        if t < 100:
            A = np.array([
                [1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 0.98, 0],
                [0, 0, 0, 0.98],
            ])
        else:
            A = np.array([
                [1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 1.02, 0],
                [0, 0, 0, 1.02],
            ])

        x[t + 1] = A @ x[t]

    return x