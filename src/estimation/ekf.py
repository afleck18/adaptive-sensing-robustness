import numpy as np
from src.metrics.base import get_system_stability

class EKF:
    def __init__(self, dt):
        self.dt = dt

        self.F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ])

        self.Q = 0.05 * np.eye(4)
        self.R = 0.3 * np.eye(2)

        self.x = np.zeros(4)
        self.P = np.eye(4)

    def step(self, y, t, dt):
        """
            Takes current system state and uses it to predict and 
            update the new state of the system. Residual disagreement 
            is used as an indicator of estimator inconsistency under 
            degraded sensing conditions.
        """
        x_pred = self.F @ self.x
        P_pred = self.F @ self.P @ self.F.T + self.Q

        if y is None:
            return x_pred, P_pred, None

        y_pred = self.H @ x_pred
        residual = y - y_pred

        S = self.H @ P_pred @ self.H.T + self.R
        K = P_pred @ self.H.T @ np.linalg.inv(S)

        x_est = x_pred + K @ residual
        self.x = x_est
        self.P = (np.eye(4) - K @ self.H) @ P_pred

        noise_std = 0.05 + 0.15 * np.linalg.norm(x_est[:2])
        self.R = (noise_std**2) * np.eye(2)

        A, _ = get_system_stability(t,dt)
        self.F = A

        return self.x, self.P, residual
