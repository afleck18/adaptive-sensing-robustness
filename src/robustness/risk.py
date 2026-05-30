import numpy as np

def risk(uncertainty, margin):
    """
        Risk is normalized relative to the predefined safe operating radius.
    """
    ratio = uncertainty / (abs(margin) + 1e-3)
    risk = ratio / (1 + ratio)
    return risk
