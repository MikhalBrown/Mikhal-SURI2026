"""
sensorTOOL_digital_twin_print_decision.py

Program will watch a folder for new sensorTOOL CSV/Excel files and automatically create
a digital twin state Excel output with predictive defect probability and a recommended
print decision: Continue Print, Pause Print, or Cancel Print.

Designed for Ender 5 Max PLA thermal monitoring using sensorTOOL data.

Author: Mikhal Brown
Updated with print-decision logic.
"""

import time
import os
import platform
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd


# -------------------------------------------------
# USER SETTINGS
# -------------------------------------------------

# Change this to the folder where sensorTOOL saves CSV/Excel files
WATCH_FOLDER = Path(r"C:\Users\Mikhal Brown\SURI2026")

OUTPUT_FILE = WATCH_FOLDER / "digital_twin_state_output.xlsx"

CHECK_INTERVAL_SECONDS = 5

# Number of raw sensor rows grouped together for each digital twin state
WINDOW_SIZE = 100


# -------------------------------------------------
# PLA / ENDER 5 MAX THRESHOLDS
# -------------------------------------------------

# Normal operating feature ranges for PLA printing.
# These should be updated later using validated defect data from real Ender 5 Max PLA prints.
NORMAL_RANGES = {
    "Peak Temperature (°C)": (190, 230),
    "Mean Temperature (°C)": (185, 220),
    "Cooling Rate (°C/s)": (0, 25),
    "Temperature Variance (°C²)": (0, 40),
    "Thermal Gradient (°C/mm)": (0, 15),
    "Peak Frequency (Hz)": (0, 10),
    "Spectral Energy (dB)": (0, 5000),
}

# Critical safety/quality limits.
# If any feature goes outside these limits, the system recommends Cancel Print.
CRITICAL_LIMITS = {
    "Peak Temperature (°C)": (180, 245),
    "Mean Temperature (°C)": (175, 235),
    "Cooling Rate (°C/s)": (0, 35),
    "Temperature Variance (°C²)": (0, 60),
    "Thermal Gradient (°C/mm)": (0, 25),
    "Peak Frequency (Hz)": (0, 15),
    "Spectral Energy (dB)": (0, 6000),
}

# Feature importance weights used in the predictive defect probability calculation.
# The weights should add to 1.00.
FEATURE_WEIGHTS = {
    "Peak Temperature (°C)": 0.25,
    "Mean Temperature (°C)": 0.20,
    "Cooling Rate (°C/s)": 0.20,
    "Temperature Variance (°C²)": 0.15,
    "Thermal Gradient (°C/mm)": 0.10,
    "Peak Frequency (Hz)": 0.05,
    "Spectral Energy (dB)": 0.05,
}

# Defect and print-decision thresholds
DEFECT_THRESHOLD = 0.60
PAUSE_THRESHOLD = 0.35
CANCEL_THRESHOLD = 0.70


# -------------------------------------------------
# FILE HANDLING
# -------------------------------------------------

def get_sensor_files(folder):
    files = []

    for ext in ["*.csv", "*.xlsx", "*.xls"]:
        files.extend(folder.glob(ext))

    files = [
        file for file in files
        if not file.name.startswith("~$")
        and file.name != OUTPUT_FILE.name
    ]

    return files


def get_newest_file(folder):
    files = get_sensor_files(folder)

    if not files:
        return None

    return max(files, key=lambda file: file.stat().st_mtime)


def wait_until_file_is_ready(file_path, wait_time=2):
    previous_size = -1

    while True:
        current_size = file_path.stat().st_size

        if current_size == previous_size:
            return True

        previous_size = current_size
        time.sleep(wait_time)


def load_sensor_file(file_path):
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    if file_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    raise ValueError("Input file must be CSV, XLSX, or XLS.")


# -------------------------------------------------
# COLUMN DETECTION
# -------------------------------------------------

def find_column(df, possible_names):
    for col in df.columns:
        clean_col = str(col).strip().lower()

        for name in possible_names:
            if name.lower() in clean_col:
                return col

    return None


# -------------------------------------------------
# FEATURE EXTRACTION
# -------------------------------------------------

def calculate_peak_frequency_and_energy(temperature_values, time_values):
    temperature_values = np.array(temperature_values, dtype=float)
    time_values = np.array(time_values, dtype=float)

    valid_mask = ~np.isnan(temperature_values) & ~np.isnan(time_values)

    temperature_values = temperature_values[valid_mask]
    time_values = time_values[valid_mask]

    if len(temperature_values) < 3:
        return 0, 0

    dt_values = np.diff(time_values)
    dt_values = dt_values[dt_values > 0]

    if len(dt_values) == 0:
        return 0, 0

    dt = np.mean(dt_values)

    if dt <= 0:
        return 0, 0

    temp_centered = temperature_values - np.mean(temperature_values)

    fft_values = np.fft.fft(temp_centered)
    frequencies = np.fft.fftfreq(len(temp_centered), d=dt)

    positive_mask = frequencies > 0

    if not np.any(positive_mask):
        return 0, 0

    positive_freqs = frequencies[positive_mask]
    positive_magnitudes = np.abs(fft_values[positive_mask])

    peak_frequency = positive_freqs[np.argmax(positive_magnitudes)]

    spectral_energy = np.sum(positive_magnitudes ** 2)

    if spectral_energy > 0:
        spectral_energy_db = 10 * np.log10(spectral_energy)
    else:
        spectral_energy_db = 0

    return round(peak_frequency, 4), round(spectral_energy_db, 4)


def extract_features_from_raw_data(df):
    time_col = find_column(df, ["time", "timestamp", "seconds", "sec"])
    temp_col = find_column(df, ["temperature", "temp", "pyrometer"])
    position_col = find_column(df, ["position", "distance", "x", "mm"])

    if temp_col is None:
        raise ValueError(
            "No temperature column found. Your file needs a column such as "
            "'Temperature', 'Temp', or 'Pyrometer'."
        )

    if time_col is None:
        print("No time column found. Creating generated time column.")
        df["Generated Time (s)"] = np.arange(len(df))
        time_col = "Generated Time (s)"

    output_rows = []

    for start in range(0, len(df), WINDOW_SIZE):
        chunk = df.iloc[start:start + WINDOW_SIZE]

        if len(chunk) < 3:
            continue

        temps = pd.to_numeric(chunk[temp_col], errors="coerce")
        times = pd.to_numeric(chunk[time_col], errors="coerce")

        valid = temps.notna() & times.notna()

        temps = temps[valid].reset_index(drop=True)
        times = times[valid].reset_index(drop=True)

        if len(temps) < 3:
            continue

        peak_temp = temps.max()
        mean_temp = temps.mean()
        temp_variance = temps.var()

        dT = np.diff(temps)
        dt = np.diff(times)

        valid_dt = dt > 0

        if np.any(valid_dt):
            cooling_rates = -dT[valid_dt] / dt[valid_dt]
            cooling_rate = max(np.max(cooling_rates), 0)
        else:
            cooling_rate = 0

        if position_col is not None:
            positions = pd.to_numeric(chunk[position_col], errors="coerce")
            positions = positions.dropna()

            if len(positions) >= 2:
                position_range = positions.max() - positions.min()

                if position_range > 0:
                    thermal_gradient = (temps.max() - temps.min()) / position_range
                else:
                    thermal_gradient = 0
            else:
                thermal_gradient = 0
        else:
            thermal_gradient = 0

        peak_frequency, spectral_energy = calculate_peak_frequency_and_energy(
            temps.values,
            times.values,
        )

        output_rows.append({
            "Peak Temperature (°C)": round(peak_temp, 4),
            "Mean Temperature (°C)": round(mean_temp, 4),
            "Cooling Rate (°C/s)": round(cooling_rate, 4),
            "Temperature Variance (°C²)": round(temp_variance, 4),
            "Thermal Gradient (°C/mm)": round(thermal_gradient, 4),
            "Peak Frequency (Hz)": round(peak_frequency, 4),
            "Spectral Energy (dB)": round(spectral_energy, 4),
        })

    return pd.DataFrame(output_rows)


# -------------------------------------------------
# DEFECT + PRINT DECISION CALCULATION
# -------------------------------------------------

def calculate_feature_risk(value, normal_min, normal_max):
    if pd.isna(value):
        return 0.5

    if normal_min <= value <= normal_max:
        return 0.0

    if value < normal_min:
        difference = normal_min - value
        scale = max(abs(normal_min), 1)
        return min(difference / scale, 1.0)

    difference = value - normal_max
    scale = max(abs(normal_max), 1)
    return min(difference / scale, 1.0)


def calculate_defect_probability(row):
    total_probability = 0

    for feature, weight in FEATURE_WEIGHTS.items():
        normal_min, normal_max = NORMAL_RANGES[feature]
        risk = calculate_feature_risk(row[feature], normal_min, normal_max)
        total_probability += weight * risk

    return round(total_probability, 4)


def assign_defect_status(probability):
    if probability >= DEFECT_THRESHOLD:
        return "Defective"

    if probability >= PAUSE_THRESHOLD:
        return "Warning"

    return "Non-Defective"


def check_critical_failure(row):
    failed_features = []

    for feature, limits in CRITICAL_LIMITS.items():
        critical_min, critical_max = limits
        value = row[feature]

        if pd.isna(value):
            continue

        if value < critical_min or value > critical_max:
            failed_features.append(feature)

    return failed_features


def assign_print_decision(row):
    probability = row["Predictive Defect Probability"]
    failed_features = check_critical_failure(row)

    if failed_features:
        return "Cancel Print"

    if probability >= CANCEL_THRESHOLD:
        return "Cancel Print"

    if probability >= PAUSE_THRESHOLD:
        return "Pause Print"

    return "Continue Print"


def assign_decision_reason(row):
    probability = row["Predictive Defect Probability"]
    failed_features = check_critical_failure(row)

    if failed_features:
        return "Critical threshold exceeded: " + ", ".join(failed_features)

    if probability >= CANCEL_THRESHOLD:
        return "Defect probability is too high for safe printing"

    if probability >= PAUSE_THRESHOLD:
        return "Possible defect forming; pause and inspect print"

    return "Print conditions are within acceptable PLA range"


# -------------------------------------------------
# DIGITAL TWIN PROCESSING
# -------------------------------------------------

def create_digital_twin_state(input_file):
    print("\nProcessing new sensorTOOL file:")
    print(input_file)

    df = load_sensor_file(input_file)

    required_columns = list(NORMAL_RANGES.keys())

    if all(col in df.columns for col in required_columns):
        print("Detected already-processed feature file.")
        output_df = df[required_columns].copy()
    else:
        print("Detected raw sensor data file.")
        output_df = extract_features_from_raw_data(df)

    if output_df.empty:
        raise ValueError("No valid feature rows were created from the input file.")

    output_df.insert(
        0,
        "Unit ID",
        [f"T{i + 1:03d}" for i in range(len(output_df))],
    )

    output_df["Predictive Defect Probability"] = output_df.apply(
        calculate_defect_probability,
        axis=1,
    )

    output_df["Defect Status"] = output_df[
        "Predictive Defect Probability"
    ].apply(assign_defect_status)

    output_df["Print Decision"] = output_df.apply(
        assign_print_decision,
        axis=1,
    )

    output_df["Decision Reason"] = output_df.apply(
        assign_decision_reason,
        axis=1,
    )

    output_df.to_excel(OUTPUT_FILE, index=False)

    print("Digital twin state output created/updated:")
    print(OUTPUT_FILE)

    print("\nPreview:")
    print(output_df.head())

    latest_decision = output_df.iloc[-1]["Print Decision"]
    latest_reason = output_df.iloc[-1]["Decision Reason"]

    print("\nLatest Print Decision:")
    print(latest_decision)
    print(latest_reason)

    return output_df


def open_output_file():
    try:
        if platform.system() == "Windows":
            os.startfile(OUTPUT_FILE)
        elif platform.system() == "Darwin":
            subprocess.call(["open", str(OUTPUT_FILE)])
        else:
            subprocess.call(["xdg-open", str(OUTPUT_FILE)])
    except Exception:
        print("Output saved, but could not open automatically.")


# -------------------------------------------------
# WATCH FOLDER LOOP
# -------------------------------------------------

def watch_folder():
    print("Watching folder for sensorTOOL files:")
    print(WATCH_FOLDER)
    print("\nPress the red Stop button in Spyder to end the program.\n")

    WATCH_FOLDER.mkdir(parents=True, exist_ok=True)

    last_processed_file = None
    last_processed_time = None

    while True:
        newest_file = get_newest_file(WATCH_FOLDER)

        if newest_file is not None:
            newest_time = newest_file.stat().st_mtime

            if newest_file != last_processed_file or newest_time != last_processed_time:
                wait_until_file_is_ready(newest_file)

                try:
                    create_digital_twin_state(newest_file)
                    last_processed_file = newest_file
                    last_processed_time = newest_time

                except Exception as error:
                    print("\nError while processing file:")
                    print(error)

        time.sleep(CHECK_INTERVAL_SECONDS)


# -------------------------------------------------
# RUN IN SPYDER
# -------------------------------------------------

if __name__ == "__main__":
    watch_folder()

