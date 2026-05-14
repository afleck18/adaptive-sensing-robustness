import numpy as np

# =========================
# METRICS
# =========================

def get_stability(A):
    A_sym = 0.5 * (A + A.T)
    return np.max(np.abs(np.linalg.eigvals(A_sym).real))


def risk(uncertainty, margin):
    ratio = uncertainty / (abs(margin) + 1e-3)
    risk = ratio / (1 + ratio)
    return risk
