# Fused Filament Fabrication (FFF) Defect Detection - Image Datasets

## Overview

This directory contains high-resolution image datasets for defect detection in fused filament fabrication (FFF). These datasets are used for training and validation of machine learning models to identify various print defects.

## Dataset Structure

The images folder contains five defect categories with the following file sizes:

| Defect Type | Folder Size |
|-------------|------------|
| **Warping** | 1.4 MB |
| **Layer Shifting** | 4.5 MB |
| **Under Extrusion** | 6.88 MB |
| **Over Extrusion** | 18.6 MB |
| **Normal Print** | 254 MB |
| **Total** | ~285 MB |

## Defect Categories

### Warping (1.4 MB)
Images of prints with warping defects, where material shrinks or curves during cooling.

### Layer Shifting (4.5 MB)
Images showing layer misalignment or shifting errors during the printing process.

### Under Extrusion (6.88 MB)
Images of prints with insufficient material extrusion, resulting in weak or incomplete layers.

### Over Extrusion (18.6 MB)
Images of prints with excess material extrusion, causing dimensional inaccuracies and blobs.

### Normal Print (254 MB)
Images of successful, defect-free prints used as reference and baseline data.

## Accessing the Image Data

The image datasets are stored in the **`data`** branch of this repository.

To clone the repository and access the image datasets:

```bash
# Clone the repository
git clone https://github.com/MikhalBrown/Mikhal-SURI2026.git
cd Mikhal-SURI2026

# Switch to the data branch
git checkout data
```

## Prerequisites: Installing Git LFS

These image datasets utilize **Git Large File Storage (LFS)** for efficient version control of large binary files. You must install Git LFS before cloning if you want to download the actual image files (otherwise you'll only get pointers).

### Installation Instructions

**macOS (using Homebrew):**
```bash
brew install git-lfs
git lfs install
```

**Windows (using Chocolatey):**
```bash
choco install git-lfs
git lfs install
```

**Windows (manual installation):**
- Download from https://git-lfs.com
- Run the installer
- Run `git lfs install` in your terminal

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install git-lfs
git lfs install
```

**Linux (Fedora/CentOS):**
```bash
sudo yum install git-lfs
git lfs install
```

### Verify Installation

```bash
git lfs version
```

## Adding Images to the Data Branch

To add new images to the data branch:

```bash
# Clone and navigate to the repository
git clone https://github.com/MikhalBrown/Mikhal-SURI2026.git
cd Mikhal-SURI2026

# Switch to the data branch
git checkout data

# Configure Git LFS to track image files
git lfs track "*.jpg" "*.png" "*.gif" "*.tiff" "*.bmp"

# Commit the LFS configuration (if first time)
git add .gitattributes
git commit -m "Setup Git LFS for image files"

# Create or navigate to your images folder
mkdir -p images/Warping
mkdir -p images/Layer_Shifting
mkdir -p images/Under_Extrusion
mkdir -p images/Over_Extrusion
mkdir -p images/Normal_Print

# Copy your images into these folders
cp -r /path/to/your/Warping/* images/Warping/
cp -r /path/to/your/Layer_Shifting/* images/Layer_Shifting/
cp -r /path/to/your/Under_Extrusion/* images/Under_Extrusion/
cp -r /path/to/your/Over_Extrusion/* images/Over_Extrusion/
cp -r /path/to/your/Normal_Print/* images/Normal_Print/

# Stage, commit, and push
git add images/
git commit -m "Add defect detection image datasets (Warping, Layer Shifting, Under Extrusion, Over Extrusion, Normal Print)"
git push origin data
```

## Using Git LFS

With Git LFS installed, large files are automatically handled:
- You get 1 GB of free LFS storage per month on GitHub
- Clones and pulls are faster since pointers are used instead of full files
- Only download the files you actually need

## Why Git LFS?

The image datasets total ~285 MB, with the Normal Print folder alone being 254 MB. Git LFS:
- Prevents bloating the repository with large binary files
- Enables efficient storage and transfer
- Maintains repository performance
- Allows for easy scaling as datasets grow

For more information on Git LFS, visit: https://git-lfs.com

## Data Branch Link

Access the image datasets here: [https://github.com/MikhalBrown/Mikhal-SURI2026/tree/data](https://github.com/MikhalBrown/Mikhal-SURI2026/tree/data)
