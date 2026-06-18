# LPBF-Defect-Fusion
Introductory Progress on Machine Learning Pipeline for Detection of XCT Defects (Specifically with the use of Dataset for Metal Powder Bed Fusion Additive Manufacturing: Data Processing, Feature Extraction, Registration, and Uncertainties)

The expected outcome is a reproducible computational study that determines whether multimodal fusion improves LPBF defect detection on held-out parts in the NIST dataset, supported by real training runs, ablation results, and manual error analysis

This project organizes the NIST fully registered in-situ and ex-situ LPBF dataset into three main parts: Raw Data, Processed Data, and Split Data
Dataset Used: https://data.amerigeoss.org/dataset/a-fully-registered-in-situ-and-ex-situ-dataset-for-metal-powder-bed-fusion-additive-manufa

The initial code for processing the data should run like this: 
```bash
python src/prepare_lpbf_data.py

Table showing each feature and where it comes from:
