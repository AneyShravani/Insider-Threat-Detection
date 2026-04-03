#!/usr/bin/env python3
"""
Download Script for Insider Threat Detection Dataset
====================================================

This script provides instructions and utilities for downloading the insider threat
detection dataset for research purposes.

Author: Research Team
Date: 2024
"""

import os
import sys
import zipfile
import requests
from pathlib import Path

def create_download_instructions():
    """
    Create download instructions for the dataset.
    """
    instructions = """
# Download Instructions for Insider Threat Detection Dataset

## Dataset Overview
This dataset contains comprehensive insider threat detection data including:
- User Behavior Analytics (UEBA) data
- Network security logs
- Privileged Access Management (PAM) data
- Data Loss Prevention (DLP) events
- Labeled insider threat scenarios
- Malware and ransomware indicators

## Download Options

### Option 1: Direct Download (Recommended)
All dataset files are already available in your current directory:
- ueba_data.csv
- network_logs.csv
- pam_data.csv
- dlp_events.csv
- insider_threat_scenarios.csv
- malware_indicators.csv

### Option 2: GitHub Repository
If you need to download from a repository:
```bash
git clone https://github.com/your-repo/insider-threat-dataset.git
cd insider-threat-dataset
```

### Option 3: Cloud Storage Links
For large-scale distribution, the dataset is available on:
- Google Drive: [Link to be provided]
- AWS S3: [Link to be provided]
- Azure Blob Storage: [Link to be provided]

## Dataset Structure
```
insider-threat-dataset/
├── README.md                 # Dataset documentation
├── ueba_data.csv            # User behavior analytics data
├── network_logs.csv         # Network security logs
├── pam_data.csv            # Privileged access management data
├── dlp_events.csv          # Data loss prevention events
├── insider_threat_scenarios.csv  # Labeled threat scenarios
├── malware_indicators.csv   # Malware and ransomware indicators
├── data_loader.py          # Python data loading utilities
├── requirements.txt        # Python dependencies
└── download_dataset.py     # This download script
```

## Usage Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Load and Preprocess Data
```python
from data_loader import InsiderThreatDataLoader

# Initialize data loader
loader = InsiderThreatDataLoader()

# Load all datasets
datasets = loader.load_all_datasets()

# Create alert features for machine learning
alert_features = loader.create_alert_features()
```

### 3. Verify Dataset Integrity
```python
# Get dataset summary
summary = loader.get_dataset_summary()
print(summary)
```

## Dataset Statistics
- **UEBA Data**: 30 records, 10 unique users
- **Network Logs**: 35 records, 15 unique IPs
- **PAM Data**: 30 records, 10 unique users
- **DLP Events**: 30 records, 10 unique users
- **Threat Scenarios**: 30 labeled scenarios
- **Malware Indicators**: 40 malware samples

## Citation
If you use this dataset in your research, please cite:
```
Intelligent Prioritization and Escalation of Insider Threat Alerts Using Machine Learning and Behavioural Analytics
```

## License
This dataset is provided for academic research purposes only.

## Support
For questions or issues, please contact: research-team@example.com
"""
    
    with open('DOWNLOAD_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("Download instructions created: DOWNLOAD_INSTRUCTIONS.md")

def create_dataset_archive():
    """
    Create a zip archive of the dataset files.
    """
    dataset_files = [
        'README.md',
        'ueba_data.csv',
        'network_logs.csv',
        'pam_data.csv',
        'dlp_events.csv',
        'insider_threat_scenarios.csv',
        'malware_indicators.csv',
        'data_loader.py',
        'requirements.txt'
    ]
    
    archive_name = 'insider_threat_dataset.zip'
    
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in dataset_files:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to archive")
            else:
                print(f"Warning: {file} not found")
    
    print(f"\nDataset archive created: {archive_name}")
    print(f"Archive size: {os.path.getsize(archive_name) / 1024:.2f} KB")

def verify_dataset_files():
    """
    Verify that all dataset files are present.
    """
    required_files = [
        'ueba_data.csv',
        'network_logs.csv',
        'pam_data.csv',
        'dlp_events.csv',
        'insider_threat_scenarios.csv',
        'malware_indicators.csv'
    ]
    
    missing_files = []
    present_files = []
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            present_files.append((file, size))
        else:
            missing_files.append(file)
    
    print("Dataset File Verification")
    print("=" * 40)
    
    if present_files:
        print("\nPresent files:")
        for file, size in present_files:
            print(f"  ✓ {file} ({size} bytes)")
    
    if missing_files:
        print("\nMissing files:")
        for file in missing_files:
            print(f"  ✗ {file}")
        print("\nPlease ensure all dataset files are in the current directory.")
    else:
        print("\n✓ All dataset files are present!")
    
    return len(missing_files) == 0

def main():
    """
    Main function to handle dataset download and verification.
    """
    print("Insider Threat Detection Dataset Download Utility")
    print("=" * 55)
    
    # Verify dataset files
    print("\n1. Verifying dataset files...")
    files_ok = verify_dataset_files()
    
    # Create download instructions
    print("\n2. Creating download instructions...")
    create_download_instructions()
    
    # Create dataset archive
    print("\n3. Creating dataset archive...")
    create_dataset_archive()
    
    print("\n" + "=" * 55)
    print("Dataset download utility completed!")
    print("\nNext steps:")
    print("1. Review DOWNLOAD_INSTRUCTIONS.md for usage information")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run data loader: python data_loader.py")
    print("4. Start your research with the insider threat dataset!")

if __name__ == "__main__":
    main()
