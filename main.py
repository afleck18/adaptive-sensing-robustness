import numpy as np

from src.simulation.dynamics import simulate_system
from src.sensing.direct import direct_measurement
from src.sensing.range import ranged_measurement
from src.sensing.vision import vision_measurement
from src.metrics.base import risk, get_stability
from src.estimation.system_id import estimate_dynamics_windowed,get_A
from src.estimation.ekf import EKF
from src.utils.plotting import plot_all

# =========================
# MAIN
# =========================

def run(experiment):
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

        if experiment == "direct":
            y = direct_measurement(x)

        if experiment == "ranged":
            y = ranged_measurement(x)

        if experiment == "vision":
            y = vision_measurement(x,t)

        x_est, P, residual = ekf.step(y,t,dt)

        # uncertainties
        u_ekf = np.trace(P[:2,:2]) / np.trace(np.eye(4)[:2,:2])
        
        if y is None:
            residual_norm = residual_avg + 0.5
        else:
            residual_norm = np.linalg.norm(residual)

        residual_avg = 0.9 * residual_avg + 0.1 * residual_norm
        u_ours = residual_avg

        # margin
        margin = np.clip(R_safe - np.linalg.norm(x_est[:2]), -1.0, R_safe)

        # risk
        r_ekf = risk(u_ekf, margin)
        r_ours = risk(u_ours, margin)

        A = get_A(t,dt)
        stability = get_stability(A)

        t_list.append(t)
        x_true_list.append(x)
        x_est_list.append(x_est)
        y_list.append(y)
        u_ekf_list.append(u_ekf)
        u_ours_list.append(u_ours)
        r_ekf_list.append(r_ekf)
        r_ours_list.append(r_ours)
        system_stab_list.append(stability)

    # stability
    A_list, stability = estimate_dynamics_windowed(
        np.array(x_est_list),
        window=10,
        reg=1e-2,
        return_stability=True
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
        "meas_stability": stability
    }

    return results

    

if __name__ == "__main__":

    experiments = ["direct","ranged", "vision"]
    if len(experiments) > 0:
        exp_results = {}
        for experiment in experiments:
            np.random.seed(0)
            results = run(experiment)
            exp_results[experiment] = {"results": results}

        plot_all(exp_results, experiments)
    else:
        print("Add experiment type: base, ranged, or vision")