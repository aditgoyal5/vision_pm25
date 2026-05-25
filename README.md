
# Vision-Based PM2.5 Estimation using Arduino UNO Q
<img width="402" height="304" alt="IMG_8229" src="https://github.com/user-attachments/assets/ee7b2eed-7084-45ec-8639-502211d8a7f1" />
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/d469ef75-ae6f-4430-bd58-5ca0344f9f08" />


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

***PICTURES AND DETAILED EXPLANATION OF PROBLEMS and SOLUTIONS are listed TOWARDS THE END of this readME file.***

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
* AI-driven environmental monitoring system capable of running directly on embedded hardware.


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



# Hybrid Linux + MCU Architecture [UNO Q]

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
│       ├── sketch/
│           └── sketch.ino
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


# Machine Learning Pipeline

## Models Explored

The project experiments with multiple regression architectures:

* ConvNeXt-based regression
* MobileNet-based regression
* Hybrid regression models
* Multi-task learning models

The objective is to map image features to PM2.5 concentration values.
Although I explored multiple regression and classification models, regression worked best for this project. 
Accuracy is one of the major problems that I faced, which I'll address later. 

# ONNX Deployment

The trained models are exported to ONNX format for deployment on the UNO Q.

Why ONNX:

* lightweight deployment
* hardware portability
* optimized inference
* ARM/Linux compatibility
* edge-AI suitability

Inference is performed locally on the UNO Q without cloud dependency.


# Flask Upload Interface

The system includes a Flask-based web server that allows:

* image uploads directly from a phone
* browser-based inference
* real-time PM estimation
* deployment over local network

Workflow:

```text
Phone Upload → Flask Server → ONNX Inference → Calibration (to improve accuracy) → PM Output
```


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

Basically here what I'm doing is im manually entering the real world measurements and mapping that to the predicted value. This would ensure better predictions- more accurate ones in the future, but I do realize that this method would require exposure and multiple rounds of testings in different environments in locations all over the world to make this system accurate and scalable. This indeed is one of the major flaws of this project.


# Why This Project is Different
This project is different because I'm trying to do this in a slightly unorthodox manner. Although what I was attempting to do was being called reduandant by some, I still decided to go ahead with it. I'm attempting to map images to PM values such that we would in the future, be able to predict PM just using an image of the sky. How cool does that sound? 

Moreover, this project is also different because here accuracy is off the charts. The funny thing is that its TERRIBLE. Its around 50% when using classification with bins with defined values. However, my strategy of mapping values as discussed earlier and is apparent in some of the nano_server3 code, is something that I've looked at. Although it is a method that wouldn't be considered the best, it is something that I've thought of as a quick and comparitively easy fix. 

# Current Capabilities

* Upload image from phone
* Run local inference on UNO Q
* Predict PM2.5 concentration
* Apply calibration correction
* Log prediction history
* Operate without cloud inference


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



# Results

The project successfully demonstrates:

* real-time PM2.5 estimation from images
* edge deployment on embedded hardware
* hybrid Linux + MCU execution
* adaptive calibration workflow
* mobile-accessible inference pipeline



# Images

## System Setup

<img width="571" height="428" alt="IMG_8098" src="https://github.com/user-attachments/assets/d6e3bec2-f513-46e9-9470-7fa5489f53e2" />

This is the picure of the apparatus just exposed to smoke. 

## Flask Upload Interface

<img width="625" height="441" alt="image" src="https://github.com/user-attachments/assets/46203f53-b2f3-4d21-bbf3-b689c7df4465" />
<img width="612" height="98" alt="image" src="https://github.com/user-attachments/assets/d0bb005a-1618-44d0-8297-269dca441405" />

Now after clicking Predict, we get the predicted value as well as automatically updated calibrated mapping of the new prediction with the shown value (actual reading) entered by the user.

<img width="366" height="123" alt="image" src="https://github.com/user-attachments/assets/2f9fb778-a020-448a-88e9-3830eeb4d8c2" />

*The flask server automatically initialises along with the PMS5003 sensor, as soon as the UNO Q is powered on*


## Problems Faced
1) **High Sensitivity to Enviromental Conditions** : The model predictions were highly sensitive to environmental conditions rather than just pollution levels. Changes in lighting, cloud cover, sky brightness, and time of day significantly affected the output. In many cases, the model could confuse a cloudy or overexposed sky with high pollution conditions. To reduce this issue, calibration mechanisms were introduced where predicted PM values and actual PM values were stored together and correction logic was applied over time. Historical predictions and nonlinear calibration approaches were also explored to stabilize the outputs. However, the project could still not fully solve the fundamental issue of ensuring that the model was truly learning PM2.5 characteristics instead of indirectly learning lighting and atmospheric visual patterns.
   
2) **Dataset quality and Synchronization** : PM values collected from external sources, there were cases where timestamps did not perfectly align. This introduced noisy labels into the dataset, which directly affected model training quality. To improve this, timestamp-based logging and structured CSV files were implemented so that each image could be associated more accurately with its corresponding PM reading. Despite these improvements, the project still lacked a very large, clean, and perfectly synchronized dataset collected under controlled conditions, limiting the overall reliability of the model. Moreover, another major issue was that the dataset was filled with non-sky elements- which warrented for proper cleaning of the each of the dataset images along with preservation of actual valuable information which turned out to be difficult.

3) **Reliability (of the data points and of the calibration based approach as a whole)** : The project also encountered challenges related to validation and scientific reliability. Although prediction outputs could visually appear reasonable, it was difficult to conclusively prove that the model generalized well across different weather conditions, locations, seasons, and camera settings. The system performed best under conditions similar to the training data, but there was still uncertainty regarding how reliably it would function in completely new environments.
Another major issue faced during the project was the calibration-mapping based correction approach itself, which turned out to be fundamentally flawed as an attempt at reinforcement-style improvement. The idea was to continuously map predicted PM2.5 values against actual PM readings and use those corrections to improve future predictions over time. Initially, this appeared promising because it reduced some short-term prediction fluctuations. However, the system was not truly learning environmental features in a robust way; instead, it was gradually becoming dependent on historical correction patterns. This remained one of the largest unresolved concerns in the project.

4) Another small but notable issue was the bugs encountered while using Arduino UNO Q. Since the board is quite new, its software interfacing is quite buggy. The Arduino App Lab has limited functionality when it comes to using SSH based commands. It performs poorly and refuses to cooperate with the SSH. I initially wanted to auto-capture the actual PM value instead of asking the user to manually enter it, since it is already being displayed on the LED matrix of the UNO Q. However, this was not possible since the UNO Q's firmware refused to cooperate. Arduino App Lab refused to harmonise the python code on the app lab and on the board itself. It was as if both were clashing with each other. I tried looking for solutions but when I made my project in April 2026, no fixes for this were present. Hence I made my own fix for the time being. I'm sure that as more people use Arduino UNO Q, bugs like these would be fixed and interfacing python from multiple points (app lab as well as SSH) would be more compatible with each other. 

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


# Author

Adit Goyal

Electronics and Communication Engineering

This project was partly developed for my Ai/ML Course (January - April 2026)


