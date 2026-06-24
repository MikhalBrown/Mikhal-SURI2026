# LPBF-Defect-Fusion/Progression towards Temperature Process Monitoring of Fused Filament Fabrication AM
Introductory Progress on Machine Learning Pipeline for Detection of XCT Defects (Specifically with the use of Dataset for Metal Powder Bed Fusion Additive Manufacturing: Data Processing, Feature Extraction, Registration, and Uncertainties)

The expected outcome is a reproducible computational study that determines whether multimodal fusion improves LPBF defect detection on held-out parts in the NIST dataset, supported by real training runs, ablation results, and manual error analysis

This project organizes the NIST fully registered in-situ and ex-situ LPBF dataset into three main parts: Raw Data, Processed Data, and Split Data
Dataset Used: https://data.amerigeoss.org/dataset/a-fully-registered-in-situ-and-ex-situ-dataset-for-metal-powder-bed-fusion-additive-manufa

The findings from research will then transition into a comprehensive study on melt-pool figures as it relates to thermal process monitoring (with a switch into fused filament fabrication).

Data: prepare_lpbf_data.py

Organizes NIST LPBF ZIP archive data into:
1. Raw Data
2. Processed Data
3. Split Data

Compatible with Spyder, VS Code, GitHub, and normal Python.

The initial code for processing the data should run using this: 

```bash
python src/prepare_lpbf_data.py

https://benedicttigers-my.sharepoint.com/:x:/g/personal/mikhal_brown69_my_benedict_edu/IQCfE8TBuFILQYgAM9uwbmAGARHBeXQ2_Ds6ao6ApgFavbs?e=774duq
