import numpy as np

def compute_uncertainty(P,y,residual,residual_avg):
    """
        Risk is normalized relative to the predefined safe operating radius.
    """
    u_ekf = np.trace(P[:2,:2]) / np.trace(np.eye(4)[:2,:2])
        
    if y is None:
        residual_norm = residual_avg + 0.5
    else:
        residual_norm = np.linalg.norm(residual)

    residual_avg = 0.9 * residual_avg + 0.1 * residual_norm
    u_ours = residual_avg

    return u_ekf, u_ours, residual_avg
