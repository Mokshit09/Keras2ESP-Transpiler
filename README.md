# Keras2ESP-Transpiler
**An automated toolchain for deploying Keras MLPs to ESP32-S3 using hardware-accelerated DSP instructions.**

## Overview
This project bridges the gap between high-level Python ML development and low-level C implementation. It automates the extraction of weights from Keras models and generates optimized C code tailored for the `esp-dsp` library.

### Key Features
* **Automated Quantization:** Converts float32 weights to Q1.15 fixed-point format.
* **Memory Optimization:** Uses `FLASH_ALIGNED` attributes to store weights directly in Flash memory.
* **Hardware Acceleration:** Generates C code that invokes `dspm_mult_s16` for SIMD-accelerated matrix multiplication.
* **One-Command Deployment:** Creates a full ESP-IDF project structure automatically.

## 🛠 Requirements

### 1. Python Environment (Host Machine)
To run the transpiler and analyze the models, you need:
* **Python 3.8+**
* **TensorFlow 2.x**: For loading and parsing `.keras` or `.h5` models.
* **NumPy**: For weight quantization and matrix manipulation.

   ```bash
   pip install tensorflow numpy

### 2. Embedded Toolchain (Target Device)
To compile the generated project for the ESP32-S3:
* **ESP-IDF (v5.0 or later)**: The official development framework.
* **esp-dsp Library**: Ensure the DSP component is added to your project to use dspm_mult_s16
   ```bash
   # To add the DSP component to your generated project
   idf.py add-dependency "espressif/esp-dsp^1.4.0"


## Usage
1. Place your model in the directory.
2. Run the deployment script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh examples/nn_model.keras my_gesture_project


