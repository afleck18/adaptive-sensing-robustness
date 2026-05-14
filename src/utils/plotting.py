import matplotlib.pyplot as plt
import numpy as np

from src.utils.general import moving_average, first_crossing

def plot_trajectory(exp_results, experiments):
    fig, axs = plt.subplots(1, len(experiments), figsize=(15, 4))
    for i in range(len(experiments)):
        experiment = experiments[i]

        y_plot = np.full((200, 2), np.nan)

        y = exp_results[experiment]["results"]["y"]
        for t_temp, measurement in enumerate(y):
            if measurement is not None:
                y_plot[t_temp] = measurement

        x_true = exp_results[experiment]["results"]["x_true"]
        x_est = exp_results[experiment]["results"]["x_est"]

        if experiment == "direct":
            desc = "nominal sensing"

        if experiment == "ranged":
            desc = "geometry-dependent sensing"
        
        if experiment == "vision":
            desc = "perception-driven sensing"
            
        axs[i].plot(x_true[:,0], x_true[:,1], 'k--', label="True",linewidth=2.5)
        axs[i].plot(x_est[:,0], x_est[:,1], 'b', label="EKF",linewidth=1.1, alpha =0.6)
        axs[i].scatter(y_plot[:,0], y_plot[:,1], s=10, alpha=0.2)
        circle = plt.Circle((0,0), 5.0, fill=False, linestyle='--',alpha=0.6,linewidth=0.8)
        axs[i].add_patch(circle)
        axs[i].set_title(f'Trajectory ({desc})')
        if i == 0:
            axs[i].legend()
        axs[i].axis("equal")

    plt.tight_layout(pad=3)
    plt.savefig('results/trajectory.png')
    plt.show()

def plot_uncertainty(exp_results, experiments):
    fig, axs = plt.subplots(1, len(experiments), figsize=(15, 4), sharey=True)
    max_y_value = 0
    for exp in experiments:
        u_ours = exp_results[exp]["results"]["u_ours"]
        u_ekf = exp_results[exp]["results"]["u_ekf"]
        
        if max(np.max(u_ours),np.max(u_ekf)) > max_y_value:
            max_y_value = max(np.max(u_ours),np.max(u_ekf)) + 0.15

    for i in range(len(experiments)):
        experiment = experiments[i]

        u_ekf = exp_results[experiment]["results"]["u_ekf"]
        u_ekf[0] = u_ekf[1]

        u_ours = exp_results[experiment]["results"]["u_ours"]

        if experiment == "direct":
            desc = "nominal sensing"

        if experiment == "ranged":
            desc = "geometry-dependent sensing"
        
        if experiment == "vision":
            desc = "perception-driven sensing"

        axs[i].plot(u_ekf, label="EKF")
        axs[i].plot(u_ours, label="Residual disagreement")
        axs[i].axvline(100, linestyle="--", alpha=0.5)
        axs[i].set_ylim(0, max_y_value)
        axs[i].set_title(f'Uncertainty ({desc})')
        if i == 0:
            axs[i].legend(loc="upper left")

    plt.tight_layout(pad=2)
    plt.savefig('results/uncertainty.png')
    plt.show()

def plot_risk(exp_results, experiments):
    fig, axs = plt.subplots(1, len(experiments), figsize=(15, 4),sharey=True)

    for i in range(len(experiments)):
        experiment = experiments[i]

        t = exp_results[experiment]["results"]["t"]
        r_ekf = exp_results[experiment]["results"]["r_ekf"]
        r_ours = exp_results[experiment]["results"]["r_ours"]

        if experiment == "direct":
            desc = "nominal sensing"

        if experiment == "ranged":
            desc = "geometry-dependent sensing"
        
        if experiment == "vision":
            desc = "perception-driven sensing"
            
        threshold = 0.6
        t_ekf = first_crossing(r_ekf, threshold)
        t_res = first_crossing(r_ours, threshold)

        r_ekf_smooth = moving_average(r_ekf, 2)
        r_ours_smooth = moving_average(r_ours, 2)

        axs[i].plot(r_ekf_smooth, label="EKF risk")
        axs[i].plot(r_ours_smooth, label="Residual risk")
        axs[i].axhline(1.0, linestyle='--', color='red')
        axs[i].axvline(t_ekf, linestyle='--',alpha=0.5)
        axs[i].axvline(t_res, linestyle='--',alpha=0.5)
        axs[i].fill_between(t,0,1, where=(t>100), alpha=0.05)
        if np.abs(t_ekf-t_res) > 10:
            if t_res < t_ekf:
                earlier_risk = "Residual"
            else:
                earlier_risk = "Covariant"
            axs[i].annotate(
                f'{earlier_risk} risk \ncrosses threshold \nearlier',
                xy=(min(t_res,t_ekf), 0.6), 
                xytext=(min(t_res,t_ekf)-80,0.65),
                arrowprops=dict(arrowstyle="->",lw=1.5)
            )
            axs[i].annotate('', xy=(t_ekf, 0.1), xytext=(t_res, 0.1),
                    arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
            axs[i].text(max(t_ekf,t_res)+5,-0.01,'Detection \ndelay')
        else:
            axs[i].text(min(t_ekf,t_res)-105,0.65,'Comparable detection \ntiming')
        axs[i].set_title(f'Risk ({desc})')
        if i == 0:
            axs[i].legend(loc="upper left")

    plt.tight_layout(pad=2)
    plt.savefig('results/risk.png')
    plt.show()

def plot_stability(exp_results, experiments):
    fig, axs = plt.subplots(1, len(experiments), figsize=(15, 4),sharey=True)

    max_y_value = 0
    for exp in experiments:
        sys_stability = exp_results[exp]["results"]["system_stability"]
        meas_stability = exp_results[exp]["results"]["meas_stability"]

        if max(np.max(sys_stability),np.max(meas_stability)) > max_y_value:
            max_y_value = max(np.max(sys_stability),np.max(meas_stability)) + 0.15

    for i in range(len(experiments)):
        experiment = experiments[i]

        t = exp_results[experiment]["results"]["t"]
        sys_stability = exp_results[experiment]["results"]["system_stability"]
        meas_stability = exp_results[experiment]["results"]["meas_stability"]

        if experiment == "direct":
            desc = "nominal sensing"

        if experiment == "ranged":
            desc = "geometry-dependent sensing"
        
        if experiment == "vision":
            desc = "perception-driven sensing"
            
        t = np.arange(len(meas_stability)) + 10
        
        axs[i].plot(sys_stability, label="True system stability")
        axs[i].plot(t, meas_stability, label="Estimated stability (from observations)")
        axs[i].axvline(100, linestyle='--', alpha=0.2)
        axs[i].axhline(0, linestyle='--')
        axs[i].axhline(1.0, linestyle='--', alpha=0.3)
        axs[i].set_ylim(0, max_y_value)
        axs[i].set_title(f'Stability ({desc})')
        if i == 0:
            axs[i].legend(loc="upper left")

    plt.tight_layout(pad=2)
    plt.savefig('results/stability.png')
    plt.show()