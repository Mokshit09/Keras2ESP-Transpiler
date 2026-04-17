# Keras2ESP-Transpiler
**An automated toolchain for deploying Keras MLPs to ESP32-S3 using hardware-accelerated DSP instructions.**

## Overview
This project bridges the gap between high-level Python ML development and low-level C implementation. It automates the extraction of weights from Keras models and generates optimized C code tailored for the `esp-dsp` library.

### Key Features
* **Automated Quantization:** Converts float32 weights to Q1.15 fixed-point format.
* **Memory Optimization:** Uses `FLASH_ALIGNED` attributes to store weights directly in Flash memory.
* **Hardware Acceleration:** Generates C code that invokes `dspm_mult_s16` for SIMD-accelerated matrix multiplication.
* **One-Command Deployment:** Creates a full ESP-IDF project structure automatically.

## Usage
1. Place your model in the directory.
2. Run the deployment script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh examples/nn_model.keras my_gesture_project

---

## 4. Final Python Logic Check
Make sure your `generate_main.py` includes the `model_data.h` header in its output so the C compiler can find the weights:

> **Important:** Ensure your generator script writes `#include "model_data.h"` at the top of the generated `main.c`.

---

## 5. Pushing to GitHub
Run these commands in your terminal:

1. **Initialize:** `git init`
2. **Add everything:** `git add .`
3. **First Commit:** `git commit -m "Initial release: Automated Keras to ESP-DSP transpiler"`
4. **Link to GitHub:** * Create a new repo on GitHub named `Keras2ESP-Transpiler`.
   * `git remote add origin https://github.com/YOUR_USERNAME/Keras2ESP-Transpiler.git`
5. **Push:** `git push -u origin main`

---

## Why this works for your Resume Tomorrow
When you add the link to your resume, don't just say "Python script." Say:
> **"Developed a Python-to-C Transpiler for Embedded AI (TinyML), automating the conversion of Keras models into hardware-accelerated C for ESP32-S3."**
