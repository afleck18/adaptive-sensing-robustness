import numpy as np
# =========================
# METRICS
# =========================

def get_system_stability(t,dt):
    """
        Gets time-varying linear dynamics variable at given time. Calculates 
        stability for the system with a defined instability region after
        t = 100.
    """
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

    A_sym = 0.5 * (A + A.T)
    stability = np.max(np.abs(np.linalg.eigvals(A_sym).real))

    return A, stability
