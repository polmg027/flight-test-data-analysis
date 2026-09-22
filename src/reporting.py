from pathlib import Path


def generate_text_report(results, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("FLIGHT TEST DATA ANALYSIS REPORT\n")
        file.write("=" * 40 + "\n\n")

        file.write("TEST POINT\n")
        file.write(f"Time window: {results['test_start']}-{results['test_end']} s\n")
        file.write(f"Mean altitude: {results['mean_altitude']:.1f} ft\n")
        file.write(f"Mean IAS: {results['mean_ias']:.2f} kt\n")
        file.write(f"IAS within limits: {results['ias_valid']}\n\n")

        file.write("DYNAMIC ANALYSIS\n")
        file.write(f"Oscillation window: {results['osc_start']}-{results['osc_end']} s\n")
        file.write(f"Dominant frequency: {results['roll_frequency']:.3f} Hz\n")
        file.write(f"Roll peak-to-peak: {results['roll_p2p']:.2f} deg\n")
        file.write(f"Yaw-rate peak-to-peak: {results['yaw_p2p']:.2f} deg/s\n")
        file.write(f"Rudder peak-to-peak: {results['rudder_p2p']:.2f} deg\n")
        file.write(f"Yaw-roll time lag: {results['yaw_roll_lag']:.2f} s\n")
        file.write(f"Yaw-roll phase lag: {results['phase_lag']:.1f} deg\n")