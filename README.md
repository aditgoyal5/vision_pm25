
# Vision-Based PM2.5 Estimation using Arduino UNO Q

## Overview

This project is a real-time edge-AI system designed to estimate **PM2.5 concentration directly from environmental images** using computer vision and deep learning.

Instead of relying entirely on expensive particulate sensors, this system uses:

* image-based atmospheric analysis
* deep learning regression models
* real-time edge inference
* adaptive calibration

The project runs on the **Arduino UNO Q**, leveraging its hybrid architecture:

* Linux MPU side for AI inference and server-side processing
* STM32 MCU side for embedded control and hardware interfacing

The system provides a complete edge-AI pipeline:

1. Capture or upload image
2. Run ONNX inference locally on the UNO Q
3. Predict PM2.5 concentration
4. Calibrate prediction using real-world measurements
5. Return refined PM estimate through a Flask web interface

\---

# Motivation

Conventional PM2.5 monitoring stations are:

* expensive
* sparse
* difficult to deploy at scale
* dependent on dedicated sensing hardware

This project explores whether atmospheric conditions visible in images can be used to estimate PM2.5 levels using computer vision.

The goal is to create a:

* low-cost
* scalable
* edge-deployable
* AI-driven environmental monitoring system

capable of running directly on embedded hardware.

\---

# Key Features

* Real-time PM2.5 estimation from images
* Edge AI deployment on Arduino UNO Q
* ConvNeXt and MobileNet regression pipelines
* ONNX Runtime inference
* Flask-based image upload interface
* Adaptive calibration using real-world PM values
* Linux + MCU hybrid architecture
* Embedded deployment workflow
* Calibration logging and refinement
* Mobile-accessible inference interface

\---

# Hardware Platform

## Arduino UNO Q

The project is deployed on the Arduino UNO Q platform.

The UNO Q combines:

* Qualcomm Dragonwing QRB2210 MPU (Linux side)
* STM32U585 MCU (real-time embedded side)

This architecture enables:

* AI inference on Linux
* embedded hardware control on MCU
* inter-processor communication between both systems

The Linux subsystem handles:

* Flask server
* image processing
* ONNX inference
* calibration logic

The STM32 MCU side handles:

* embedded runtime operations
* Arduino sketch execution
* low-level interfacing

\---

# System Architecture

```text
          Phone / Camera Upload
                     ↓
               Flask Server
                     ↓
            Image Preprocessing
                     ↓
           ONNX Runtime Inference
                     ↓
          Initial PM2.5 Prediction
                     ↓
          Calibration Adjustment
                     ↓
            Final PM2.5 Estimate
```

\---

# Hybrid Linux + MCU Architecture

```text
Linux MPU Side (Python)
    ├── Flask Server
    ├── ONNX Runtime
    ├── Calibration Logic
    ├── Image Processing
    └── PM Prediction

             ↕

STM32 MCU Side (Arduino Sketch)
    ├── Embedded Control
    ├── Hardware Interfacing
    └── Real-Time Operations
```

\---

# Project Structure

```text
VISION\_PM25/
│
├── deployment/
│   ├── server/
│   │   ├── nano\_server.py
│   │   ├── run\_model\_onnx.py
│   │   ├── calibration\_data.csv
│   │   └── predicted\_pm.txt
│   │
│   └── unoq\_app/
│       ├── python/
│       │   └── main.py
│       │
│       ├── sketch/
│           └── sketch.ino
│       
│       
│       
│
├── training/
│   ├── train\_convnext\_regression.py
│   ├── train\_mobilenet.py
│   ├── train\_hybrid.py
│   ├── export\_onnx.py
│   └── evaluate\_regression.py
│
├── models/
│   ├── convnext\_regression.py
│   ├── mobilenet\_regression.py
│   ├── multitask\_model.py
│   └── hybrid\_model.py
│
├── features/
│   └── physics\_features.py
│
├── evaluation/
├── pm25vision/
├── data/
├── requirements.txt
└── README.md
```

\---

# Machine Learning Pipeline

## Models Explored

The project experiments with multiple regression architectures:

* ConvNeXt-based regression
* MobileNet-based regression
* Hybrid regression models
* Multi-task learning models

The objective is to map image features to PM2.5 concentration values.

\---

# ONNX Deployment

The trained models are exported to ONNX format for deployment on the UNO Q.

Why ONNX:

* lightweight deployment
* hardware portability
* optimized inference
* ARM/Linux compatibility
* edge-AI suitability

Inference is performed locally on the UNO Q without cloud dependency.

\---

# Flask Upload Interface

The system includes a Flask-based web server that allows:

* image uploads directly from a phone
* browser-based inference
* real-time PM estimation
* deployment over local network

Workflow:

```text
Phone Upload → Flask Server → ONNX Inference → Calibration → PM Output
```

\---

# Calibration System

One of the core components of the project is the adaptive calibration pipeline.

The system stores:

* predicted PM values
* real-world PM measurements
* timestamps

inside:

```text
calibration\_data.csv
```

This allows the system to:

* refine predictions
* compensate for environmental drift
* improve real-world performance
* reduce deployment mismatch

Example:

```text
timestamp,predicted\_pm,actual\_pm
1775288723,114.58,49
1775288786,126.67,48
```

\---

# Why This Project is Different

Most ML air-quality projects stop at:

* dataset training
* offline inference
* notebook demonstrations

This project focuses heavily on:

* embedded deployment
* edge inference
* real-time operation
* calibration systems
* Linux + MCU integration
* mobile accessibility
* hardware/software co-design

The emphasis is not just on model accuracy, but on creating a deployable environmental sensing system.

\---

# Current Capabilities

* Upload image from phone
* Run local inference on UNO Q
* Predict PM2.5 concentration
* Apply calibration correction
* Log prediction history
* Operate without cloud inference

\---

# Future Improvements

## Planned Enhancements

* Real-time camera streaming
* Automatic retraining pipeline
* Sensor fusion with physical PM sensors
* Temporal sequence modeling
* Live environmental dashboard
* GPU/OpenCL acceleration
* Continuous calibration optimization
* MQTT/LoRa telemetry integration
* Mobile application interface

\---

# Technologies Used

## AI / ML

* PyTorch
* ONNX Runtime
* OpenCV
* NumPy
* scikit-learn

## Deployment

* Flask
* Python
* Linux
* Arduino App Lab

## Embedded

* Arduino UNO Q
* STM32U585
* Qualcomm Dragonwing QRB2210

\---

# Results

The project successfully demonstrates:

* real-time PM2.5 estimation from images
* edge deployment on embedded hardware
* hybrid Linux + MCU execution
* adaptive calibration workflow
* mobile-accessible inference pipeline

\---

# Images

## System Setup

*Add hardware setup images here.*

## Flask Upload Interface

*Add screenshots of the web interface here.*

## Sample Predictions

*Add inference examples and outputs here.*

## Deployment on Arduino UNO Q

*Add UNO Q runtime/setup images here.*

\---

# Repository Notes

Large model files such as:

* `.onnx`
* `.pth`
* `.pt`

are excluded from Git tracking to keep the repository lightweight.

The repository focuses on:

* architecture
* deployment pipeline
* runtime implementation
* training workflow
* reproducibility

\---

# Author

Adit Goyal

Electronics and Communication Engineering
Made for Ai/ML Course Project (January - April 2026)


