import numpy as np
from src.estimation.system_id import get_A

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
        update the new state of the system.

        Args:
            y: (2,) array of estimated system state
            t: current timestep in system simulation
            dt: time between timesteps

        Returns:
            x: predicted state of the system
            P: covariance of EKF
            residual: innovation residual of EKF
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
        self.F = get_A(t,dt)

        return self.x, self.P, residual
