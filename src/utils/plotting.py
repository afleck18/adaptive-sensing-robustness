import matplotlib.pyplot as plt
import numpy as np

from src.utils.general import moving_average, first_crossing

def plot_trajectory(exp_results, experiments, save_plot=False):
    """
    Plots both true and EKF predicted trajectory using the data points.
    """
    if isinstance(experiments, list):
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

            if experiment == "nominal":
                desc = "nominal sensing"

            if experiment == "geometry_degraded":
                desc = "geometry-dependent sensing"
            
            if experiment == "intermittent_degraded":
                desc = "intermittently degraded sensing"
                
            axs[i].plot(x_true[:,0], x_true[:,1], 'k--', label="True",linewidth=2.5)
            axs[i].plot(x_est[:,0], x_est[:,1], 'b', label="EKF",linewidth=1.1, alpha =0.6)
            axs[i].scatter(y_plot[:,0], y_plot[:,1], s=10, alpha=0.2)
            circle = plt.Circle((0,0), 5.0, fill=False, linestyle='--',alpha=0.6,linewidth=0.8)
            axs[i].add_patch(circle)
            axs[i].set_title(f'Estimator Behavior ({desc})')
            if i == 0:
                axs[i].legend()
            axs[i].axis("equal")
    else:
        y_plot = np.full((200, 2), np.nan)

        y = exp_results["y"]
        for t_temp, measurement in enumerate(y):
            if measurement is not None:
                y_plot[t_temp] = measurement

        x_true = exp_results["x_true"]
        x_est = exp_results["x_est"]

        if experiments == "nominal":
            desc = "nominal sensing"

        if experiments == "geometry_degraded":
            desc = "geometry-dependent sensing"
        
        if experiments == "intermittent_degraded":
            desc = "intermittently degraded sensing"

        fig, ax = plt.subplots()
            
        ax.plot(x_true[:,0], x_true[:,1], 'k--', label="True",linewidth=2.5)
        ax.plot(x_est[:,0], x_est[:,1], 'b', label="EKF",linewidth=1.1, alpha =0.6)
        ax.scatter(y_plot[:,0], y_plot[:,1], s=10, alpha=0.2)
        circle = plt.Circle((0,0), 5.0, fill=False, linestyle='--',alpha=0.6,linewidth=0.8)
        ax.add_patch(circle)
        ax.set_title(f'Estimator Behavior ({desc})')
        ax.legend()
        ax.axis("equal")

    plt.tight_layout(pad=3)
    if save_plot:
        plt.savefig('results/trajectory.png')
    plt.show()

def plot_uncertainty(exp_results, experiments,save_plot=False):
    """
    Plots both covariance and residual based uncertainties.
    """

    if isinstance(experiments, list):
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

            if experiment == "nominal":
                desc = "nominal sensing"

            if experiment == "geometry_degraded":
                desc = "geometry-dependent sensing"
            
            if experiment == "intermittent_degraded":
                desc = "intermittently degraded sensing"

            axs[i].plot(u_ekf, label="EKF")
            axs[i].plot(u_ours, label="Residual disagreement")
            axs[i].axvline(100, linestyle="--", alpha=0.5)
            axs[i].set_ylim(0, max_y_value)
            axs[i].set_title(f'Uncertainty ({desc})')
            if i == 0:
                axs[i].legend(loc="upper left")
    else:
        max_y_value = 0
        for exp in experiments:
            u_ours = exp_results["u_ours"]
            u_ekf = exp_results["u_ekf"]
            
            if max(np.max(u_ours),np.max(u_ekf)) > max_y_value:
                max_y_value = max(np.max(u_ours),np.max(u_ekf)) + 0.15

        u_ekf = exp_results["u_ekf"]
        u_ekf[0] = u_ekf[1]

        u_ours = exp_results["u_ours"]

        if experiments == "nominal":
            desc = "nominal sensing"

        if experiments == "geometry_degraded":
            desc = "geometry-dependent sensing"
        
        if experiments == "intermittent_degraded":
            desc = "intermittently degraded sensing"

        fig, ax = plt.subplots()
        ax.plot(u_ekf, label="EKF")
        ax.plot(u_ours, label="Residual disagreement")
        ax.axvline(100, linestyle="--", alpha=0.5)
        ax.set_ylim(0, max_y_value)
        ax.set_title(f'Uncertainty ({desc})')
        ax.legend(loc="upper left")

    plt.tight_layout(pad=2)
    if save_plot:
        plt.savefig('results/uncertainty.png')
    plt.show()

def plot_risk(exp_results, experiments, save_plot=False):
    """
    Plots both covariance and residual based risks.
    """

    if isinstance(experiments, list):
        fig, axs = plt.subplots(1, len(experiments), figsize=(18, 4),sharey=True)

        for i in range(len(experiments)):
            experiment = experiments[i]

            t = exp_results[experiment]["results"]["t"]
            r_ekf = exp_results[experiment]["results"]["r_ekf"]
            r_ours = exp_results[experiment]["results"]["r_ours"]

            if experiment == "nominal":
                desc = "nominal sensing"

            if experiment == "geometry_degraded":
                desc = "geometry-dependent sensing"
            
            if experiment == "intermittent_degraded":
                desc = "intermittently degraded sensing"
                
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
            axs[i].set_title(f'Operational Risk Response ({desc})')
            if i == 0:
                axs[i].legend(loc="upper left")
    else:
        t = exp_results["t"]
        r_ekf = exp_results["r_ekf"]
        r_ours = exp_results["r_ours"]

        if experiments == "nominal":
            desc = "nominal sensing"

        if experiments == "geometry_degraded":
            desc = "geometry-dependent sensing"
        
        if experiments == "intermittent_degraded":
            desc = "intermittently degraded sensing"
            
        threshold = 0.6
        t_ekf = first_crossing(r_ekf, threshold)
        t_res = first_crossing(r_ours, threshold)

        r_ekf_smooth = moving_average(r_ekf, 2)
        r_ours_smooth = moving_average(r_ours, 2)

        fig, ax = plt.subplots()
        ax.plot(r_ekf_smooth, label="EKF risk")
        ax.plot(r_ours_smooth, label="Residual risk")
        ax.axhline(1.0, linestyle='--', color='red')
        ax.axvline(t_ekf, linestyle='--',alpha=0.5)
        ax.axvline(t_res, linestyle='--',alpha=0.5)
        ax.fill_between(t,0,1, where=(t>100), alpha=0.05)
        if np.abs(t_ekf-t_res) > 10:
            if t_res < t_ekf:
                earlier_risk = "Residual"
            else:
                earlier_risk = "Covariant"
            ax.annotate(
                f'{earlier_risk} risk \ncrosses threshold \nearlier',
                xy=(min(t_res,t_ekf), 0.6), 
                xytext=(min(t_res,t_ekf)-80,0.65),
                arrowprops=dict(arrowstyle="->",lw=1.5)
            )
            ax.annotate('', xy=(t_ekf, 0.1), xytext=(t_res, 0.1),
                    arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
            ax.text(max(t_ekf,t_res)+5,-0.01,'Detection \ndelay')
        else:
            ax.text(min(t_ekf,t_res)-105,0.65,'Comparable detection \ntiming')
        ax.set_title(f'Operational Risk Response ({desc})')
        ax.legend(loc="upper left")

    plt.tight_layout(pad=2)
    if save_plot:
        plt.savefig('results/risk.png')
    plt.show()

def plot_stability(exp_results, experiments, save_plot=False):
    """
    Plots both system stability and measured stability.
    """

    if isinstance(experiments, list):
        fig, axs = plt.subplots(1, len(experiments), figsize=(18, 4),sharey=True)

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

            if experiment == "nominal":
                desc = "nominal sensing"

            if experiment == "geometry_degraded":
                desc = "geometry-dependent sensing"
            
            if experiment == "intermittent_degraded":
                desc = "intermittently degraded sensing"
                
            t = np.arange(len(meas_stability)) + 10
            
            axs[i].plot(sys_stability, label="Nominal stability baseline")
            axs[i].plot(t, meas_stability, label="Spectral stability estimate")
            axs[i].axvline(100, linestyle='--', alpha=0.2)
            axs[i].axhline(0, linestyle='--')
            axs[i].axhline(1.0, linestyle='--', alpha=0.3)
            axs[i].set_ylim(0, max_y_value)
            axs[i].set_title(f'Estimated Local Stability ({desc})')
            if i == 0:
                axs[i].legend(loc="upper left")

    else:
        max_y_value = 0
        for exp in experiments:
            sys_stability = exp_results["system_stability"]
            meas_stability = exp_results["meas_stability"]

            if max(np.max(sys_stability),np.max(meas_stability)) > max_y_value:
                max_y_value = max(np.max(sys_stability),np.max(meas_stability)) + 0.15

        t = exp_results["t"]
        sys_stability = exp_results["system_stability"]
        meas_stability = exp_results["meas_stability"]

        if experiments == "nominal":
            desc = "nominal sensing"

        if experiments == "geometry_degraded":
            desc = "geometry-dependent sensing"
        
        if experiments == "intermittent_degraded":
            desc = "intermittently degraded sensing"
            
        t = np.arange(len(meas_stability)) + 10
        
        fig, ax = plt.subplots()
        ax.plot(sys_stability, label="Nominal stability baseline")
        ax.plot(t, meas_stability, label="Spectral stability estimate")
        ax.axvline(100, linestyle='--', alpha=0.2)
        ax.axhline(0, linestyle='--')
        ax.axhline(1.0, linestyle='--', alpha=0.3)
        ax.set_ylim(0, max_y_value)
        ax.set_title(f'Estimated Local Stability ({desc})')
        ax.legend(loc="upper left")

    plt.tight_layout(pad=2)
    if save_plot:
        plt.savefig('results/stability.png')
    plt.show()