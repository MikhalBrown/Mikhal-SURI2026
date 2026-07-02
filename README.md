# Real-Time Thermal Process Monitoring Towards Digital Twin Development for Fused Filament Fabrication (FFF)

### Project Overview

This repository contains the research, software, datasets, and machine learning pipeline developed for real-time thermal process monitoring toward Digital Twin Development for Fused Filament Fabrication (FFF) additive manufacturing.

### The objective of this project is to develop a computational framework capable of:

Monitoring thermal behavior during printing
Predicting print defects before they occur
Estimating defect probability in real time
Providing autonomous printing decisions
Forming the foundation of a real-time Digital Twin capable of continuously comparing the physical printer with its virtual representation.

Unlike traditional post-print inspection methods, this project focuses on in-situ monitoring, allowing defects to be detected while the print is still being manufactured.

## Research Motivation

Many failures in FFF printing—including:

- `Over-extrusion`
- `Under-extrusion`
- `Warping`
- `Layer shifting`
- `Delamination`
- `Thermal instability`

are caused by abnormal thermal behavior. By continuously monitoring nozzle temperatures and thermal distributions, the Digital Twin can determine whether the printing process is remaining within acceptable operating conditions.

The long-term vision is a system capable of automatically deciding whether to:

Continue printing
Pause the print
Cancel the print

before catastrophic failure occurs.

### Project Objectives

This research aims to:

Develop a complete thermal monitoring pipeline
Build predictive defect probability models
Integrate thermal sensor data with thermal imaging
Validate predictions using XCT-derived defect labels
Develop autonomous decision-making algorithms
Build a scalable Digital Twin architecture

## Digital Twin Architecture
```
ThermoMETER Sensor
          │
          ▼
sensorTOOL Software
          │
          ▼
Python Data Acquisition
          │
          ▼
Excel Dataset
          │
          ▼
Feature Extraction
          │
          ▼
Predictive Defect Probability
          │
          ▼
Decision Engine
          │
          ▼
Continue │ Pause │ Cancel Print
          │
          ▼
Digital Twin Dashboard
Repository Structure
```
``` bash
Real-Time-Thermal-Digital-Twin/ 
│
├── Data/
│   ├── Raw/
│   ├── Processed/
│   ├── Thermal Imaging/
│   ├── Sensor Data/
│   ├── XCT Labels/
│   └── Master Dataset/
│
├── Python/
│   ├── Sensor Export
│   ├── Folder Monitor
│   ├── Digital Twin
│   ├── Feature Engineering
│   ├── Prediction
│   └── Decision Engine
│
├── Models/
│
├── Results/
│
├── Documentation/
│
├── Figures/
│
└── README.md
```

## Current System Workflow

The current implementation consists of the following pipeline:
```
ThermoMETER Sensor

↓

sensorTOOL Software

↓

Temperature Logging

↓

Automatic CSV Export

↓

Python Folder Watcher

↓

Excel Processing

↓

Feature Extraction

↓

Predictive Defect Probability

↓

Print Decision
```
Hardware Printer: `Creality Ender 5 Max`

Material: `PLA`

Temperature Sensor: `Micro-Epsilon thermoMETER`

Connected through: `sensorTOOL v2.3.1.4177`

## Thermal Cameras
`FLIR A70`

Used for:

Layer-by-layer thermal monitoring
Temperature field visualization
Thermal feature extraction

`Fluke RSE600`

Used for:

High-resolution thermal imaging
Dynamic heating analysis
Thermal validation

 Approximately

1,500 thermal images per print

were collected for multiple defect scenarios.

### Current Software
Python
Pandas
NumPy
Scikit-Learn
OpenPyXL
Spyder
GitHub
sensorTOOL
Excel
Data Sources

The Digital Twin combines multiple sensing modalities.

### 1. ThermoMETER Sensor

Real-time nozzle temperature measurements

Examples:
Peak Temperature
Mean Temperature

### 2. Derived Thermal Features

The prediction model currently uses engineered features including:
``` bash
Peak Temperature
Mean Temperature
Cooling Rate
Temperature Variance
Thermal Gradient
Peak Frequency
Spectral Energy
```

These features are extracted from raw sensor measurements and transformed into predictors for defect estimation.

### 3. Thermal Imaging

Thermal imaging is incorporated to provide spatial temperature information that is not observable using a single-point infrared sensor.

The thermal image database currently contains multiple print conditions:

Normal prints
Over-extrusion
Under-extrusion
Warping
Layer shifting

Captured using:

FLIR A70
Fluke RSE600

Thermal images are intended to support future computer vision and multimodal learning by enabling extraction of image-based features such as:

``` bash
Maximum surface temperature
Temperature distribution
Thermal gradients
Heat concentration
Cooling uniformity
Hot spot localization
Layer-wise thermal evolution
```

These image-derived features will ultimately be fused with sensor measurements to improve prediction accuracy and Digital Twin fidelity.

## XCT Defect Labeling (Ground Truth Development)

Before implementing the FFF Digital Twin, this project introduced an XCT-based defect-labeling workflow using the publicly available NIST LPBF dataset. The purpose was to establish a rigorous methodology for generating reliable ground-truth defect labels and validating machine learning pipelines before transferring the approach to fused filament fabrication.

The introductory workflow consisted of:

Understanding the multimodal dataset structure
Identifying process, melt-pool, optical-intensity, and XCT feature groups
Selecting an appropriate prediction unit (voxel block, patch, or segment)
Converting XCT voxel information into binary defect labels
Cleaning and preprocessing the dataset
Creating train, validation, and test splits
Training baseline models
Developing multimodal fusion strategies
Evaluating performance using precision, recall, F1-score, ROC-AUC, and confusion matrices
Performing manual error analysis and generating reproducible experiments

To create the labels, each localized block of material was assigned a defect score based on the fraction of defective XCT voxels it contained. Blocks whose defect score exceeded a validated threshold were labeled Defect, while all remaining blocks were labeled No Defect. This threshold-based approach provided an interpretable and reproducible definition of ground truth and served as the validation framework for subsequent predictive models.

As part of this work, the following supporting analyses and datasets were developed:

Defect-score distribution histograms with annotated thresholds
Publication-quality visualizations of the threshold selection
Merged datasets containing original XCT features, computed defect scores, binary defect labels, and source-layer identifiers
Justification of the selected threshold based on the observed data distribution

Although the NIST dataset represents Laser Powder Bed Fusion (LPBF) rather than FFF, the methodology established the foundation for this repository's labeling strategy. The same concepts will be adapted to FFF using thermal sensor data, thermal imaging, and future destructive or non-destructive validation methods.

## Machine Learning Pipeline
``` bash
Raw Temperature Data

↓

Cleaning

↓

Feature Engineering

↓

Normalization

↓

Defect Probability Model

↓

Threshold Evaluation

↓

Decision Logic

↓
```

## Digital Twin Output
Predictive Model

Current model predicts:

Defect Probability

` 0.00 ────────────── 1.00 `

Outputs include
```
Predicted defect probability
Defect status
Confidence score
Decision Engine
```

The Digital Twin makes autonomous decisions using validated defect thresholds.
``` bash
Probability	Action
< 0.30	          Continue Print
0.30 – 0.60	Monitor / Warning
0.60 – 0.80	Pause Print
> 0.80	          Cancel Print
```

Thresholds will continue to be refined using experimental validation on the Ender 5 Max with PLA.

## Feature Engineering

Current engineered features include

- Peak Temperature (°C)
- Mean Temperature (°C)
- Cooling Rate (°C/s)
- Thermal Gradient (°C²)
- Temperature Variance (°C²/mm)
- Peak Frequency (Hz)
- Spectral Energy (dB)

### Future additions:

Layer number
Ambient temperature
Print speed
Fan speed
Extrusion rate
Thermal image features
Vision-based defect descriptors
Automation

Current automation includes

✔ Sensor connection

✔ Automatic data logging

✔ Folder monitoring

✔ Automatic Excel updating

✔ Custom column mapping

✔ Defect prediction

## Future automation:

Automatic thermal image synchronization
Live Digital Twin dashboard
Real-time visualization
Closed-loop printer control
Autonomous corrective actions
Future Work

### Planned research directions include:

Real-time Digital Twin visualization
Deep learning for thermal image analysis
Thermal image segmentation
CNN-based defect classification
Sensor and vision data fusion
Physics-informed Digital Twin modeling
Adaptive threshold optimization
Reinforcement learning for print control
Closed-loop process optimization
Integration with OctoPrint or Klipper
Cloud-based Digital Twin deployment
Explainable AI for defect prediction
Transfer learning across materials (PLA, PETG, ABS, graphene-enhanced polymers)
