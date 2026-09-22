from pathlib import Path
import pandas as pd

from src.analysis import (
    dominant_frequency,
    peak_to_peak,
    check_limits,
    time_lag,
    limit_violations,
)
from src.visualization import plot_oscillation, plot_test_point_validation
from src.reporting import generate_text_report

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DATA_FILE = DATA_DIR / "flight_test_simulation_02.csv"


def main():
    print("=== FLIGHT TEST DATA ANALYSIS TOOL ===")

    df = pd.read_csv(DATA_FILE)

    print(f"Dataset loaded successfully.")
    print(f"Samples: {len(df)}")
    print(f"Variables: {len(df.columns)}")

    # Select test point
    TEST_START = 90
    TEST_END = 125

    test_point = df[
        (df["time_s"] >= TEST_START) &
        (df["time_s"] <= TEST_END)
    ].copy()

    print("\n--- TEST POINT ---")
    print(f"Time window: {TEST_START}-{TEST_END} s")
    print(f"Samples: {len(test_point)}")

    # Operating conditions
    mean_altitude = test_point["altitude_ft"].mean()
    mean_ias = test_point["ias_kt"].mean()

    ias_valid = check_limits(test_point["ias_kt"], 113, 122)

    ias_violations = limit_violations(
        test_point,
        "ias_kt",
        113,
        122
    )

    print(f"Mean altitude: {mean_altitude:.1f} ft")
    print(f"Mean IAS: {mean_ias:.2f} kt")
    print(f"IAS within limits: {ias_valid}")
    print(f"IAS violations: {len(ias_violations)}")

    if not ias_violations.empty:
        print("Out-of-limit samples:")
        print(ias_violations[["time_s", "ias_kt"]].to_string(index=False))

    # Dynamic oscillation analysis
    OSC_START = 100
    OSC_END = 117

    oscillation = df[
        (df["time_s"] >= OSC_START) &
        (df["time_s"] <= OSC_END)
    ].copy()

    dt = oscillation["time_s"].iloc[1] - oscillation["time_s"].iloc[0]

    roll_frequency = dominant_frequency(oscillation["roll_deg"], dt)
    yaw_frequency = dominant_frequency(oscillation["yaw_rate_dps"], dt)
    rudder_frequency = dominant_frequency(oscillation["rudder_deg"], dt)

    roll_p2p = peak_to_peak(oscillation["roll_deg"])
    yaw_p2p = peak_to_peak(oscillation["yaw_rate_dps"])
    rudder_p2p = peak_to_peak(oscillation["rudder_deg"])

    yaw_roll_lag = time_lag(
    oscillation["roll_deg"],
    oscillation["yaw_rate_dps"],
    dt
    )
    phase_lag = 360 * roll_frequency * abs(yaw_roll_lag)

    print("\n--- DYNAMIC ANALYSIS ---")
    print(f"Oscillation window: {OSC_START}-{OSC_END} s")
    print(f"Sampling interval: {dt:.2f} s")
    print(f"Roll dominant frequency: {roll_frequency:.3f} Hz")
    print(f"Yaw-rate dominant frequency: {yaw_frequency:.3f} Hz")
    print(f"Rudder dominant frequency: {rudder_frequency:.3f} Hz")
    print(f"Roll peak-to-peak: {roll_p2p:.2f} deg")
    print(f"Yaw-rate peak-to-peak: {yaw_p2p:.2f} deg/s")
    print(f"Rudder peak-to-peak: {rudder_p2p:.2f} deg")
    print(f"Yaw-roll time lag: {yaw_roll_lag:.2f} s")
    print(f"Yaw-roll phase lag: {phase_lag:.1f} deg")

    # Generate figures
    oscillation_figure = FIGURES_DIR / "lateral_directional_oscillation.png"

    plot_oscillation(
        oscillation,
        oscillation_figure
    )

    print("\n--- OUTPUT ---")
    print(f"Figure saved: {oscillation_figure}")

    validation_figure = FIGURES_DIR / "test_point_validation.png"

    plot_test_point_validation(
        test_point,
        ias_violations,
        113,
        122,
        validation_figure
    )

    print(f"Figure saved: {validation_figure}")

    # Store analysis results
    results = {
        "test_start": TEST_START,
        "test_end": TEST_END,
        "mean_altitude": mean_altitude,
        "mean_ias": mean_ias,
        "ias_valid": ias_valid,
        "osc_start": OSC_START,
        "osc_end": OSC_END,
        "roll_frequency": roll_frequency,
        "roll_p2p": roll_p2p,
        "yaw_p2p": yaw_p2p,
        "rudder_p2p": rudder_p2p,
        "yaw_roll_lag": yaw_roll_lag,
        "phase_lag": phase_lag,
    }

    # Generate engineering report
    report_file = REPORTS_DIR / "flight_test_report.txt"

    generate_text_report(results, report_file)

    print(f"Report saved: {report_file}")


if __name__ == "__main__":
    main()

