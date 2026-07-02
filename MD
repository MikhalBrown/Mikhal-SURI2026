# Quick Start - Defect Detection and Digital Twin Concept

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Convert Raw SensorTOOL Data

Use the converter script to transform raw sensorTOOL exports into a formatted Excel workbook.

```bash
python sensorTOOL_to_excel.py sample_sensordata.csv
```

This produces:
- `sample_sensordata_formatted.xlsx`

To specify a different output file:

```bash
python sensorTOOL_to_excel.py sample_sensordata.csv formatted_output.xlsx
```

## 3. Generate Digital Twin State

The digital twin script reads formatted thermal data and computes a defect risk score.

```bash
python digital_twin_implementation.py
```

By default it uses:
- input: `input_file_formatted.xlsx`
- output: `digital_twin_state_output.xlsx`

If your formatted file has a different name:

```bash
python digital_twin_implementation.py --input sample_sensordata_formatted.xlsx --output digital_twin_state_output.xlsx
```

## 4. Example End-to-End Workflow

```bash
pip install -r requirements.txt
python sensorTOOL_to_excel.py sample_sensordata.csv
cp sample_sensordata_formatted.xlsx input_file_formatted.xlsx
python digital_twin_implementation.py
```

## 5. Required Columns for Digital Twin Input

The input file must include these columns exactly:
- `Peak Temperature`
- `Mean Temperature`
- `Cooling Rate`
- `Temperature Variance`
- `Thermal Gradient`
- `Peak Frequency`
- `Spectral Energy`

## 6. Output Files

- `*_formatted.xlsx`: formatted sensor data
- `digital_twin_state_output.xlsx`: digital twin state with defect probability and defect status

## 7. Adjust Model Behavior

Open `digital_twin_implementation.py` to change:
- `INPUT_FILE`
- `OUTPUT_FILE`
- `DEFECT_THRESHOLD`
- `NORMAL_RANGES`

## 8. Troubleshooting

- If the converter fails, verify that the raw input file exists and is valid CSV/Excel/JSON.
- If the digital twin generator raises missing-column errors, open the formatted E
