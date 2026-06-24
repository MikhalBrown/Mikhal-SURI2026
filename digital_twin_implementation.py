"""
create_digital_twin_state.py

Reads processed sensorTOOL data from CSV or Excel and creates a new Excel file
with:
- Unit ID
- Original thermal feature columns
- Predictive defect probability
- Defect status

Author: Mikhal
"""

import pandas as pd
import numpy as np
from pathlib import Path


# -----------------------------
# USER SETTINGS
# -----------------------------

INPUT_FILE = "processed_temperature_data.xlsx"   # .csv, .xlsx, or .xls
OUTPUT_FILE = "digital_twin_state_output.xlsx"

DEFECT_THRESHOLD = 0.60   # probability >= 0.60 becomes Defective


# Normal FFF temperature ranges
# Adjust these for your material: PLA, ABS, PETG, Nylon, etc.
NORMAL_RANGES = {
    "Peak Temperature": (190, 230),       # °C
    "Mean Temperature": (185, 220),       # °C
    "Cooling Rate": (0, 25),              # °C/s
    "Temperature Variance": (0, 40),      # °C²
    "Thermal Gradient": (0, 15),          # °C/mm or °C/unit distance
    "Peak Frequency": (0, 10),            # Hz
    "Spectral Energy": (0, 5000)          # signal energy
}


# -----------------------------
# FUNCTIONS
# -----------------------------

def load_data(file_path):
    """Load CSV or Excel file."""
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    else:
        raise ValueError("Input file must be CSV, XLSX, or XLS.")


def calculate_feature_risk(value, normal_min, normal_max):
    """
    Converts a feature value into a risk score between 0 and 1.
    0 = normal
    1 = very abnormal
    """

    if pd.isna(value):
        return 0.5

    if normal_min <= value <= normal_max:
        return 0.0

    if value < normal_min:
        difference = normal_min - value
        scale = max(abs(normal_min), 1)
        return min(difference / scale, 1.0)

    if value > normal_max:
        difference = value - normal_max
        scale = max(abs(normal_max), 1)
        return min(difference / scale, 1.0)


def calculate_defect_probability(row):
    """
    Calculates total defect probability based on abnormal thermal behavior.
    """

    feature_weights = {
        "Peak Temperature": 0.25,
        "Mean Temperature": 0.20,
        "Cooling Rate": 0.20,
        "Temperature Variance": 0.15,
        "Thermal Gradient": 0.10,
        "Peak Frequency": 0.05,
        "Spectral Energy": 0.05
    }

    total_probability = 0

    for feature, weight in feature_weights.items():
        normal_min, normal_max = NORMAL_RANGES[feature]
        feature_risk = calculate_feature_risk(
            row[feature],
            normal_min,
            normal_max
        )

        total_probability += weight * feature_risk

    return round(total_probability, 4)


def assign_defect_status(probability, threshold):
    """Assign defect label based on probability threshold."""

    if probability >= threshold:
        return "Defective"
    else:
        return "Non-Defective"


def create_digital_twin_state(input_file, output_file):
    """Main function."""

    df = load_data(input_file)

    required_columns = [
        "Peak Temperature",
        "Mean Temperature",
        "Cooling Rate",
        "Temperature Variance",
        "Thermal Gradient",
        "Peak Frequency",
        "Spectral Energy"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    output_df = df[required_columns].copy()

    output_df.insert(
        0,
        "Unit ID",
        [f"L{i+1:03d}" for i in range(len(output_df))]
    )

    output_df["Predictive Defect Probability"] = output_df.apply(
        calculate_defect_probability,
        axis=1
    )

    output_df["Defect Status"] = output_df[
        "Predictive Defect Probability"
    ].apply(
        lambda p: assign_defect_status(p, DEFECT_THRESHOLD)
    )

    output_df.to_excel(output_file, index=False)

    print(f"Digital twin state file created: {output_file}")


# -----------------------------
# RUN SCRIPT
# -----------------------------

if __name__ == "__main__":
    create_digital_twin_state(INPUT_FILE, OUTPUT_FILE)
