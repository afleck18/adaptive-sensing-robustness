import numpy as np

def estimate_dynamics_windowed(
    x_est,
    window=10,
    reg=1e-2,
    return_stability=False
):
    """
    Estimate time-varying linear dynamics A_hat(t) using sliding window least squares.

    x_{t+1} ≈ A_hat x_t

    Args:
        x_est: (T, n) array of estimated states
        window: number of timesteps per regression window
        reg: ridge regularization strength
        return_stability: if True, also returns lambda_max over time

    Returns:
        A_list: list of (n, n) matrices
        stability (optional): list of lambda_max values
    """

    T, n = x_est.shape

    A_list = []
    stability = []

    I = np.eye(n)

    for t in range(window, T - 1):

        # Build regression data
        X_prev = x_est[t - window:t]        # (window, n)
        X_next = x_est[t - window + 1:t + 1]

        # Solve ridge regression:
        # A = (X^T X + λI)^(-1) X^T Y
        XtX = X_prev.T @ X_prev
        XtY = X_prev.T @ X_next

        A_hat = np.linalg.solve(XtX + reg * I, XtY)

        A_list.append(A_hat)

        if return_stability:
            A_sym = 0.5 * (A_hat + A_hat.T)
            eigvals = np.linalg.eigvals(A_sym).real
            lambda_max = np.max(eigvals)
            stability.append(lambda_max)

    if return_stability:
        return A_list, np.array(stability)

    return A_list

def get_A(t, dt):
    """
        Provides system stability variable 

        Args:
            t: current timestep in system simulation
            dt: time between timesteps

        Returns:
            A: system stability variable 
        """
    if t < 100:
        return np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 0.98, 0],
            [0, 0, 0, 0.98],
        ])
    else:
        return np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1.02, 0],
            [0, 0, 0, 1.02],
        ])