# ScanSense: Complete Document Scanning Guidance System

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

ScanSense is an OCR Assistive Python-based project that provides a guidance system to help users capture documents accurately for Optical Character Recognition (OCR) recognition. It utilizes the power of OpenCV and NumPy libraries to assist users in aligning and framing their documents within the camera view, ensuring complete coverage for optimal OCR results.

## Key Features

- Real-time document detection: The system analyzes the camera feed and detects the presence of a document, providing instant feedback to the user.
- Document alignment guidance: FrameFocus OCR Assist offers visual cues and overlays to guide users in aligning their documents properly within the camera frame.
- Automatic cropping and resizing: The project automatically crops and resizes the captured document image, removing unwanted elements and ensuring the document is the primary focus.
- Intelligent image enhancement: Enhancements like noise reduction are applied to optimize the document for OCR recognition.

## Prerequisites

- Python 3.8.10
- OpenCV 4.8.0.74
- NumPy 1.24.4

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/samaypashine/ScanSense.git
   ```

2. Install the dependencies
    
    ```bash
    pip install -r requirements.txt
    ```

3. Run the script

    ```bash
    python3 scansense.py
    ```

4. [OPTIONAL] Debug the code using debug mode.

    ```bash
    python3 scansense.py -debug=True
    ```
## Demonstration

   <p align="center">
      <img src="https://github.com/samaypashine/ScanSense/blob/main/outputs/1688876105.6346376.jpg" />
   </p>

## Contribution

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please submit a pull request or open an issue on this repository.

