# Quick Start Guide - SensorTOOL to Excel Converter

## 1. Installation
```bash
pip install -r requirements.txt
```

## 2. Basic Usage

### From Command Line (Easiest)
```bash
# Auto-detect columns and convert
python sensortool_to_excel.py your_sensordata.csv

# Specify output filename
python sensortool_to_excel.py thermal_data.csv results.xlsx
```

### From Python Script
```python
from sensortool_to_excel import SensorToolExporter

exporter = SensorToolExporter('sensordata.csv')
df = exporter.convert()  # Auto-detects columns
```

### With Custom Column Mapping
```python
from sensortool_to_excel import SensorToolExporter

exporter = SensorToolExporter('sensordata.csv')

mapping = {
    'Peak Temperature': 'T_max',
    'Mean Temperature': 'T_avg',
    'Cooling Rate': 'dT_dt',
    'Temperature Variance': 'T_var',
    'Thermal Gradient': 'dT_dx',
    'Peak Frequency': 'f_peak',
    'Spectral Energy': 'E_spec'
}

df = exporter.convert(auto_detect=False, column_mapping=mapping)
```

## 3. Expected Output

Your Excel file will have:
- ✓ 7 organized columns with units
- ✓ Professional formatting (blue headers, borders, centered text)
- ✓ Numbers formatted to 4 decimal places
- ✓ Auto-sized columns
- ✓ Sheet name: "Thermal Data"

## 4. Supported Input Formats
- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`)
- JSON files (`.json`)

## 5. Supported Input Column Names

The script automatically recognizes these column name patterns:

| Target Column | Recognized Names |
|---------------|------------------|
| Peak Temperature | peak temp, peak_temperature, max temp, T_peak |
| Mean Temperature | mean temp, mean_temperature, avg temp, T_mean |
| Cooling Rate | cooling rate, cooling_rate, cool_rate |
| Temperature Variance | temp variance, temperature_variance, temp_var |
| Thermal Gradient | thermal gradient, thermal_gradient, T_gradient |
| Peak Frequency | peak freq, peak_frequency, peak frequency, f_peak |
| Spectral Energy | spectral energy, spectral_energy, energy |

## 6. Example Files

- `example_usage.py` - Shows 3 usage examples
- `sample_sensordata.csv` - Sample data file (auto-generated)
- `sample_sensordata_formatted.xlsx` - Sample output (auto-generated)

Run: `python example_usage.py`

## 7. Troubleshooting

**Problem: Columns not detected**
- Solution 1: Check column names match the patterns above
- Solution 2: Use custom column mapping (see section 2)

**Problem: Number formatting issues**
- Solution: Ensure input contains numeric values, not text

**Problem: File encoding errors**
- Solution: Save CSV as UTF-8 or use Excel format (.xlsx)

## 8. Advanced: Process Multiple Files

```python
from pathlib import Path
from sensortool_to_excel import SensorToolExporter

data_files = list(Path('.').glob('*.csv'))

for file in data_files:
    exporter = SensorToolExporter(str(file))
    exporter.convert()
    print(f"✓ Converted {file.name}")
```

## 9. Output File Location

Excel file is saved in the same directory as the input file with `_formatted.xlsx` suffix:
- Input: `thermal_data.csv`
- Output: `thermal_data_formatted.xlsx`

Or specify custom output path:
```bash
python sensortool_to_excel.py input.csv custom_output.xlsx
```

---

**Need help?** Check [SENSORTOOLS_README.md](SENSORTOOLS_README.md) for detailed documentation.
