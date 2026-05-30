import numpy as np

from src.systems.dynamics import simulate_system
from src.sensing.range import ranged_measurement
from src.robustness.risk import risk
from src.robustness.stability import get_system_stability
from src.robustness.uncertainty import compute_uncertainty
from src.estimation.system_id import estimate_dynamics_windowed
from src.estimation.ekf import EKF
from src.utils.plotting import plot_trajectory,plot_uncertainty,plot_risk,plot_stability

def run():
    """
    Runs either "direct", "ranged", or "vision"
    experiment. Outputting all results.
    """
    T = 200
    dt = 0.1
    R_safe = 5.0

    x_true = simulate_system(T, dt)
    ekf = EKF(dt)

    residual_avg = 0.0
    
    t_list = []
    x_true_list = []
    x_est_list = []
    y_list = []
    u_ekf_list = []
    u_ours_list = []
    r_ekf_list = []
    r_ours_list = []
    system_stab_list = []
    for t in range(T):
        x = x_true[t]
        y = ranged_measurement(x)

        x_est, P, residual = ekf.step(y,t,dt)

        u_ekf, u_ours, residual_avg = compute_uncertainty(P,y,residual,residual_avg)

        margin = np.clip(R_safe - np.linalg.norm(x_est[:2]), -1.0, R_safe)

        r_ekf = risk(u_ekf, margin)
        r_ours = risk(u_ours, margin)

        A, system_stability = get_system_stability(t,dt)

        t_list.append(t)
        x_true_list.append(x)
        x_est_list.append(x_est)
        y_list.append(y)
        u_ekf_list.append(u_ekf)
        u_ours_list.append(u_ours)
        r_ekf_list.append(r_ekf)
        r_ours_list.append(r_ours)
        system_stab_list.append(system_stability)

    A_list, measurement_stability = estimate_dynamics_windowed(
        np.array(x_est_list),
        window=10,
        reg=1e-2
    )

    results = {
        "t": np.array(t_list),
        "x_true": np.array(x_true_list),
        "x_est": np.array(x_est_list),
        "y": y_list,
        "u_ekf": np.array(u_ekf_list),
        "u_ours": np.array(u_ours_list),
        "r_ekf": np.array(r_ekf_list),
        "r_ours": np.array(r_ours_list),
        "system_stability": np.array(system_stab_list),
        "meas_stability": measurement_stability
    }

    return results

if __name__ == "__main__":
    np.random.seed(0)
    results = run()

    plot_trajectory(results, 'geometry_degraded', save_plot = False)
    plot_uncertainty(results, 'geometry_degraded', save_plot = False)
    plot_risk(results, 'geometry_degraded', save_plot = False)
    plot_stability(results, 'geometry_degraded', save_plot = False)
