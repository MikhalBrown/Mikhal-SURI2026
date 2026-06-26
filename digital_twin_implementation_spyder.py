"""
create_digital_twin_state_spyder_filepicker.py

Spyder-ready version.

Opens File Explorer so you can choose a CSV or Excel sensorTOOL data file.
Creates an Excel file with:
- Unit ID
- Original thermal feature columns
- Predictive defect probability
- Defect status

Author: Mikhal Brown
"""

import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


# -----------------------------
# USER SETTINGS
# -----------------------------

DEFECT_THRESHOLD = 0.60

NORMAL_RANGES = {
    "Peak Temperature": (190, 230),
    "Mean Temperature": (185, 220),
    "Cooling Rate": (0, 25),
    "Temperature Variance": (0, 40),
    "Thermal Gradient": (0, 15),
    "Peak Frequency": (0, 10),
    "Spectral Energy": (0, 5000)
}

FEATURE_WEIGHTS = {
    "Peak Temperature": 0.25,
    "Mean Temperature": 0.20,
    "Cooling Rate": 0.20,
    "Temperature Variance": 0.15,
    "Thermal Gradient": 0.10,
    "Peak Frequency": 0.05,
    "Spectral Energy": 0.05
}


# -----------------------------
# FILE EXPLORER INPUT SELECTION
# -----------------------------

def select_input_file():
    """Open File Explorer and let the user select a CSV or Excel file."""

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select Formatted sensorTOOL Data File",
        filetypes=[
            ("Excel Files", "*.xlsx *.xls"),
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ]
    )

    root.destroy()

    if not file_path:
        raise SystemExit("No file selected. Program terminated.")

    return Path(file_path)


# -----------------------------
# FUNCTIONS
# -----------------------------

def load_data(file_path):
    """Load CSV or Excel file."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found:\n{file_path}")

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    else:
        raise ValueError("Input file must be CSV, XLSX, or XLS.")


def calculate_feature_risk(value, normal_min, normal_max):
    """Convert feature value into a risk score between 0 and 1."""

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
    """Calculate total defect probability based on abnormal thermal behavior."""

    total_probability = 0

    for feature, weight in FEATURE_WEIGHTS.items():
        normal_min, normal_max = NORMAL_RANGES[feature]

        feature_risk = calculate_feature_risk(
            row[feature],
            normal_min,
            normal_max
        )

        total_probability += weight * feature_risk

    return round(total_probability, 4)


def assign_defect_status(probability):
    """Assign defect label based on probability threshold."""

    if probability >= DEFECT_THRESHOLD:
        return "Defective"
    else:
        return "Non-Defective"


def create_digital_twin_state(input_file, output_file):
    """Create the digital twin state Excel file."""

    print("Loading input file...")
    print(f"Input file: {input_file}")

    df = load_data(input_file)

    required_columns = list(FEATURE_WEIGHTS.keys())

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns:\n{missing_columns}\n\n"
            f"Available columns are:\n{list(df.columns)}"
        )

    output_df = df[required_columns].copy()

    output_df.insert(
        0,
        "Unit ID",
        [f"L{i + 1:03d}" for i in range(len(output_df))]
    )

    output_df["Predictive Defect Probability"] = output_df.apply(
        calculate_defect_probability,
        axis=1
    )

    output_df["Defect Status"] = output_df[
        "Predictive Defect Probability"
    ].apply(assign_defect_status)

    output_df.to_excel(output_file, index=False)

    print("\nDigital twin state file created successfully!")
    print(f"Output file: {output_file}")
    print("\nPreview:")
    print(output_df.head())

    return output_df


# -----------------------------
# RUN SCRIPT IN SPYDER
# -----------------------------

if __name__ == "__main__":

    INPUT_FILE = select_input_file()

    OUTPUT_FILE = INPUT_FILE.parent / "digital_twin_state_output.xlsx"

    digital_twin_df = create_digital_twin_state(
        INPUT_FILE,
        OUTPUT_FILE
    )

    print("\nDone!")
