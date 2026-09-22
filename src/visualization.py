from pathlib import Path
import matplotlib.pyplot as plt


def plot_oscillation(data, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        3, 1,
        figsize=(10, 8),
        sharex=True
    )

    # Roll angle
    axes[0].plot(data["time_s"], data["roll_deg"])
    axes[0].set_ylabel("Roll [deg]")
    axes[0].set_title("Lateral-Directional Oscillation")
    axes[0].grid(True, alpha=0.3)

    # Yaw rate
    axes[1].plot(data["time_s"], data["yaw_rate_dps"])
    axes[1].set_ylabel("Yaw rate [deg/s]")
    axes[1].grid(True, alpha=0.3)

    # Rudder
    axes[2].plot(data["time_s"], data["rudder_deg"])
    axes[2].set_ylabel("Rudder [deg]")
    axes[2].set_xlabel("Time [s]")
    axes[2].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

def plot_test_point_validation(data, violations, minimum_ias, maximum_ias, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        2, 1,
        figsize=(10, 6),
        sharex=True
    )

    # Airspeed validation
    axes[0].plot(data["time_s"], data["ias_kt"], label="IAS")
    axes[0].axhline(minimum_ias, linestyle="--", label="Lower limit")
    axes[0].axhline(maximum_ias, linestyle="--", label="Upper limit")

    if not violations.empty:
        axes[0].scatter(
            violations["time_s"],
            violations["ias_kt"],
            marker="x",
            s=80,
            label="Limit violation"
        )

    axes[0].set_ylabel("IAS [kt]")
    axes[0].set_title("Test Point Validation")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Altitude
    axes[1].plot(data["time_s"], data["altitude_ft"])
    axes[1].set_ylabel("Altitude [ft]")
    axes[1].set_xlabel("Time [s]")
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)