# Fused Filament Fabrication (FFF) Defect Detection - Image Datasets

## Overview

This branch contains high-resolution image datasets for defect detection in fused filament fabrication (FFF). These datasets are used for training and validation of machine learning models to identify various print defects.

Thermal Imaging

Thermal imaging is incorporated to provide spatial temperature information that is not observable using a single-point infrared sensor.


The thermal image database currently contains multiple print conditions:

- Normal prints
- Over-extrusion
- Under-extrusion
- Warping
-Layer shifting

Captured using:

`FLIR A70 `
`Fluke RSE600 `

Thermal images are intended to support future computer vision and multimodal learning by enabling extraction of image-based features such as:

- Maximum surface temperature
- Temperature distribution
- Thermal gradients
- Heat concentration
- Cooling uniformity
- Hot spot localization
- Layer-wise thermal evolution

These image-derived features will ultimately be fused with sensor measurements to improve prediction accuracy and Digital Twin fidelity.

## Thermal Cameras
`FLIR A70` Used for:

- Layer-by-layer thermal monitoring
- Temperature field visualization
- Thermal feature extraction

`Fluke RSE600` Used for:

- High-resolution thermal imaging
- Dynamic heating analysis
- Thermal validation

 Approximately 1,500 thermal images per print were collected for multiple defect scenarios.
