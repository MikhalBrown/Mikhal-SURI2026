# SensorTOOL to Excel Exporter

A Python utility to convert sensorTOOL 2.3.1.4177 data exports into organized Excel files with labeled columns for thermal and spectral analysis.

## Features

- **Automatic Column Detection**: Intelligently identifies and maps sensorTOOL columns to standard labels
- **Multiple Input Formats**: Supports CSV, Excel, and JSON exports from sensorTOOL
- **Professional Formatting**: Applies headers, borders, colors, and proper number formatting
- **Flexible Column Mapping**: Manually define custom column mappings if needed
- **Error Handling**: Gracefully handles missing columns and encoding issues

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Command Line Usage

```bash
# Basic usage (auto-detects columns)
python sensortool_to_excel.py input_data.csv

# Specify custom output filename
python sensortool_to_excel.py input_data.csv output_formatted.xlsx

# Works with Excel input too
python sensortool_to_excel.py thermal_data.xlsx output.xlsx
```

### Option 2: Python Script Usage

```python
from sensortool_to_excel import SensorToolExporter

# Create exporter instance
exporter = SensorToolExporter(
    input_file='sensordata.csv',
    output_file='sensordata_formatted.xlsx'
)

# Convert with auto-detection
df = exporter.convert(auto_detect=True)
```

### Option 3: Custom Column Mapping

If auto-detection doesn't work for your specific sensorTOOL export format, use custom mapping:

```python
from sensortool_to_excel import SensorToolExporter

exporter = SensorToolExporter(input_file='sensordata.csv')

# Define your custom mapping
custom_mapping = {
    'Peak Temperature': 'Max_Temp_C',
    'Mean Temperature': 'Avg_Temp_C',
    'Cooling Rate': 'Cool_Rate_C_per_s',
    'Temperature Variance': 'Temp_Var',
    'Thermal Gradient': 'Thermal_Grad',
    'Peak Frequency': 'Peak_Freq_Hz',
    'Spectral Energy': 'Spectral_Energy_dB'
}

# Convert with custom mapping
df = exporter.convert(auto_detect=False, column_mapping=custom_mapping)
```

## Output Columns

The Excel file will contain the following organized columns:

| Column | Unit | Description |
|--------|------|-------------|
| Peak Temperature | °C | Maximum temperature recorded |
| Mean Temperature | °C | Average temperature across measurement |
| Cooling Rate | °C/s | Rate of temperature decrease |
| Temperature Variance | °C² | Variance in temperature distribution |
| Thermal Gradient | °C/mm | Rate of temperature change per unit distance |
| Peak Frequency | Hz | Dominant frequency in spectral data |
| Spectral Energy | dB | Energy level in frequency domain |

## Input Data Format

The input file from sensorTOOL should contain columns with names similar to:

- peak temp / peak temperature / max temp / T_peak
- mean temp / mean temperature / avg temp / T_mean
- cooling rate / cool rate / cool_rate
- temperature variance / temp variance / temp_var
- thermal gradient / temp gradient / T_gradient
- peak frequency / peak freq / peak_freq
- spectral energy / energy / spectral_energy

## Testing

Run the example script to test with sample data:

```bash
python example_usage.py
```

This creates a sample CSV file and converts it to a formatted Excel file.

## Output File

The output Excel file includes:

- ✓ Properly labeled columns with units
- ✓ Header row with blue background and white text
- ✓ Centered text and numeric values
- ✓ Numbers formatted to 4 decimal places
- ✓ Auto-adjusted column widths
- ✓ Professional borders around all cells

## Supported Input Formats

- `.csv` - Comma-separated values
- `.xlsx` - Modern Excel format
- `.xls` - Legacy Excel format
- `.json` - JSON format

## Troubleshooting

### Columns not detected?
- Check that your input file column names are similar to the recognized patterns
- Use custom column mapping (see Option 3 above)
- Print the dataframe to verify column names: `df.columns`

### Encoding issues with CSV?
- The script automatically tries UTF-8 and Latin-1 encodings
- If issues persist, open the CSV in Excel and save as Excel format, then use that

### Numbers showing as 0 or errors?
- Ensure the input data contains numeric values, not text
- Check for special characters or spaces in numeric columns

## Files Included

- `sensortool_to_excel.py` - Main converter class
- `example_usage.py` - Example usage scripts
- `requirements.txt` - Python dependencies
- `SENSORTOOLS_README.md` - This file

## Advanced Usage

### Programmatic Processing

```python
from sensortool_to_excel import SensorToolExporter

# Process multiple files
input_files = ['data1.csv', 'data2.csv', 'data3.csv']

for input_file in input_files:
    exporter = SensorToolExporter(input_file)
    exporter.convert()
    print(f"Converted {input_file}")
```

### Access Processed Data

```python
from sensortool_to_excel import SensorToolExporter

exporter = SensorToolExporter(input_file='sensordata.csv')
df = exporter.convert()

# Now you can work with the DataFrame directly
print(df.describe())  # Statistical summary
print(df.head())      # First few rows
df.to_csv('processed.csv')  # Save to CSV if needed
```

## License

This utility is provided for use with sensorTOOL 2.3.1.4177 data processing.

## Support

For issues or questions about:
- **Data format**: Check the sensorTOOL documentation
- **Script usage**: Review the example_usage.py file
- **Column mapping**: Verify your input file structure with `pd.read_csv('file.csv').columns`
