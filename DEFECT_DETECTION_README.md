# Defect Detection Read Me (Introductory Digital Twin)

A small Python toolkit for processing sensorTOOL thermal data and generating a digital twin defect state summary for fused filament fabrication (FFF).

## Repository Structure

- `sensorTOOL_to_excel.py`: Convert raw sensorTOOL CSV / Excel / JSON exports into a formatted Excel file with standard thermal feature columns.
- `digital_twin_implementation.py`: Read formatted thermal data and compute a predictive defect probability plus defect status.
- `sample_sensordata.csv`: Example raw sensorTOOL-style input.
- `sample_sensordata_formatted.xlsx`: Example formatted Excel output.
- `requirements.txt`: Python dependencies.

## Requirements

- Python 3.9+
- `pandas`, `numpy`, `openpyxl`, `xlrd`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the SensorTOOL Exporter

Convert a raw sensorTOOL file to a formatted Excel workbook:

```bash
python sensorTOOL_to_excel.py sample_sensordata.csv
```

This creates a formatted Excel file named `sample_sensordata_formatted.xlsx` by default.

To specify a custom output filename:

```bash
python sensorTOOL_to_excel.py sample_sensordata.csv formatted_output.xlsx
```

## Running the Digital Twin State Generator

By default, `digital_twin_implementation.py` reads from `input_file_formatted.xlsx` and writes `digital_twin_state_output.xlsx`.

```bash
python digital_twin_implementation.py
```

To use a different input or output file:

```bash
python digital_twin_implementation.py --input sample_sensordata_formatted.xlsx --output digital_twin_state_output.xlsx
```

## Expected Input Columns for `digital_twin_implementation.py`

The formatted input workbook must contain the following columns:

- `Peak Temperature`
- `Mean Temperature`
- `Cooling Rate`
- `Temperature Variance`
- `Thermal Gradient`
- `Peak Frequency`
- `Spectral Energy`

## Output

The digital twin generator produces an Excel file with:

- `Unit ID`
- original thermal feature columns
- `Predictive Defect Probability`
- `Defect Status`

## Example Workflow

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Convert raw sensorTOOL data:
   ```bash
   python sensorTOOL_to_excel.py sample_sensordata.csv
   ```
3. Rename or copy the formatted file if needed:
   ```bash
   cp sample_sensordata_formatted.xlsx input_file_formatted.xlsx
   ```
4. Create the digital twin state workbook:
   ```bash
   python digital_twin_implementation.py
   ```

## Notes

- `DEFECT_THRESHOLD` in `digital_twin_implementation.py` is currently set to `0.60`.
- Adjust `NORMAL_RANGES` in `digital_twin_implementation.py` to suit different FFF materials.
