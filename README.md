# 🛣️ RoadDamageAI

An AI-powered desktop application for automatic road damage detection using **YOLOv8**, **Python**, **PyTorch**, **OpenCV**, and **CustomTkinter**.

RoadDamageAI analyzes road images and detects different types of road damage using a custom-trained object detection model. The application displays detected damage using bounding boxes and confidence scores and allows users to save the annotated results.

This project was developed as a **school Artificial Intelligence / Computer Vision project** and demonstrates the complete process of building an AI solution, from dataset preparation and model training to evaluation, testing, and deployment as a desktop application.

---

# 📑 Table of Contents

* [📌 Project Overview](#-project-overview)
* [🎯 Objective](#-objective)
* [❓ Problem Statement](#-problem-statement)
* [💡 Proposed Solution](#-proposed-solution)
* [📸 Features](#-features)
* [🛣️ Supported Damage Types](#️-supported-damage-types)
* [🔄 AI Project Cycle](#-ai-project-cycle)
* [📂 Project Structure](#-project-structure)
* [🧠 Technologies Used](#-technologies-used)
* [📚 Dataset](#-dataset)
* [🗃️ Dataset Preparation](#️-dataset-preparation)
* [🤖 Model](#-model)
* [🏋️ Model Training](#️-model-training)
* [📊 Model Evaluation](#-model-evaluation)
* [📈 Training Results](#-training-results)
* [🖥️ Application](#️-application)
* [⚙️ Installation](#️-installation)
* [▶️ Running the Application](#️-running-the-application)
* [📖 Complete User Guide](#-complete-user-guide)
* [🔍 Detection Process](#-detection-process)
* [💾 Saving Results](#-saving-results)
* [🧪 Testing](#-testing)
* [🪟 Windows EXE](#️-windows-exe)
* [📦 Building the EXE](#-building-the-exe)
* [⚠️ Limitations](#️-limitations)
* [🚀 Future Improvements](#-future-improvements)
* [🎓 Project Learning Outcomes](#-project-learning-outcomes)
* [👨‍💻 Author](#-author)
* [📜 License](#-license)

---

# 📌 Project Overview

Road damage is a common problem that can affect road safety, vehicle movement, and transportation.

Traditional road inspection often requires people to manually inspect roads and identify defects. This can become difficult when a large number of roads or images need to be inspected.

RoadDamageAI uses **Computer Vision** and **Deep Learning** to automate the detection of visible road damage.

The system takes a road image as input and uses a trained **YOLOv8 object detection model** to identify different types of road damage.

The basic process is:

```text
                    Road Image
                         │
                         ▼
                  Image Processing
                         │
                         ▼
                    YOLOv8 Model
                         │
                         ▼
                  Object Detection
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Damage Category       Confidence Score
              │                     │
              └──────────┬──────────┘
                         ▼
                  Bounding Boxes
                         │
                         ▼
                  Annotated Image
                         │
                         ▼
                    Save Result
```

---

# 🎯 Objective

The main objective of RoadDamageAI is to design and build an AI-powered Computer Vision application capable of automatically detecting different types of road damage from images.

The project aims to:

* Identify visible road damage automatically.
* Classify detected damage into predefined categories.
* Locate damage using bounding boxes.
* Display confidence scores for predictions.
* Provide a simple desktop interface for users.
* Demonstrate the complete AI Project Cycle.
* Deploy the trained model as a usable application.

---

# ❓ Problem Statement

Manual road inspection can be:

* Time-consuming
* Labour-intensive
* Difficult to scale
* Dependent on human observation

When a large number of road images need to be inspected, manually identifying every damaged area can become inefficient.

The problem addressed by this project is:

> **Can Computer Vision be used to automatically identify and locate visible road damage in road images?**

RoadDamageAI attempts to solve this problem using a custom-trained YOLOv8 object detection model.

---

# 💡 Proposed Solution

RoadDamageAI addresses the problem by combining a trained Computer Vision model with a desktop application.

The system:

1. Takes a road image as input.
2. Processes the image using the trained YOLOv8 model.
3. Detects visible road damage.
4. Identifies the damage category.
5. Calculates a confidence score.
6. Draws a bounding box around detected damage.
7. Displays the result to the user.
8. Allows the annotated image to be saved.

---

# 📸 Features

* 🖼️ Load road images directly from the desktop application
* 🤖 Automatic road damage detection using a custom-trained YOLOv8 model
* 📦 Bounding boxes around detected damage
* 🏷️ Damage category labels
* 📊 Confidence scores
* 💾 Save annotated detection results
* 🎨 Modern desktop interface using CustomTkinter
* 🌙 Dark-themed interface
* ⚡ Local AI inference
* 🪟 Windows executable support

---

# 🛣️ Supported Damage Types

The trained model contains **7 road-damage classes**:

| Class ID | Damage Type        |
| -------- | ------------------ |
| D00      | Longitudinal Crack |
| D10      | Transverse Crack   |
| D20      | Alligator Crack    |
| D40      | Pothole            |
| D43      | Crosswalk Blur     |
| D44      | White Line Blur    |
| D50      | Utility Hole       |

### Longitudinal Crack

A crack that generally runs along the direction of the road.

### Transverse Crack

A crack that generally runs across the direction of the road.

### Alligator Crack

A network of interconnected cracks that forms a pattern resembling alligator skin.

### Pothole

A depression or cavity in the road surface.

### Crosswalk Blur

Damage or fading affecting crosswalk markings.

### White Line Blur

Damage or fading affecting white road markings.

### Utility Hole

A visible utility or manhole-type structure detected on the road.

---

# 🔄 AI Project Cycle

The project follows the major stages of the Artificial Intelligence Project Cycle.

## 1. Problem Scoping

The problem of automatically detecting road damage from images was identified.

## 2. Data Acquisition

The RDD2022 road-damage dataset was used to obtain labelled road images.

## 3. Data Exploration

The images and annotations were examined to understand:

* Damage categories
* Image contents
* Class distribution
* Bounding boxes
* Dataset structure

## 4. Data Preparation

The dataset was prepared in a YOLO-compatible format and configured using `data.yaml`.

## 5. Model Selection

YOLOv8 was selected as the object detection architecture.

## 6. Model Training

The YOLOv8 model was trained using the prepared road-damage dataset.

## 7. Model Evaluation

The trained model was evaluated using:

* Precision
* Recall
* F1 score
* Precision-Recall curves
* Confusion matrices

## 8. Testing

The trained model was tested using separate road images.

## 9. Deployment

The trained model was integrated into a CustomTkinter desktop application.

## 10. Packaging

The application can be packaged as a standalone Windows executable using PyInstaller.

---

# 📂 Project Structure

The actual project structure is:

```text
RoadDamageAI/
│
├── app.py
│   └── Main CustomTkinter desktop application
│
├── train.py
│   └── Model training script
│
├── predict.py
│   └── Image prediction / inference script
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
├── .gitignore
│   └── Git ignore configuration
│
├── RoadDamageAI.ico
│   └── Application icon
│
├── RoadDamageAI.spec
│   └── PyInstaller configuration
│
├── models/
│   └── best.pt
│       └── Trained YOLOv8 model
│
├── dataset/
│   ├── data.yaml
│   ├── README.md
│   ├── README.dataset.txt
│   └── README.roboflow.txt
│
├── test_images/
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 3.jpg
│   ├── ...
│   └── 18.jpg
│
├── results/
│   ├── BoxF1_curve.png
│   ├── BoxP_curve.png
│   ├── BoxPR_curve.png
│   ├── BoxR_curve.png
│   ├── confusion_matrix.png
│   ├── confusion_matrix_normalized.png
│   ├── labels.jpg
│   ├── results.csv
│   ├── results.png
│   └── README.md
│
├── screenshots/
│   └── Application screenshots
│
└── output/
    └── Saved detection results
```

> The training dataset itself is excluded from the Git repository using `.gitignore` because of its size.

---

# 🧠 Technologies Used

| Technology         | Purpose                      |
| ------------------ | ---------------------------- |
| Python             | Main programming language    |
| Ultralytics YOLOv8 | Object detection             |
| PyTorch            | Deep learning framework      |
| Torchvision        | Computer vision utilities    |
| OpenCV             | Image processing             |
| CustomTkinter      | Desktop GUI                  |
| Pillow             | Image handling               |
| NumPy              | Numerical operations         |
| Matplotlib         | Training visualizations      |
| PyInstaller        | Windows executable packaging |
| Git                | Version control              |
| GitHub             | Repository hosting           |

---

# 📚 Dataset

This project uses the **RDD2022 (Road Damage Detection 2022)** dataset.

RDD2022 contains road images with annotations for different types of road damage.

### Dataset

**Road Damage Detection 2022 (RDD2022)**

The dataset contains examples of road damage including cracks, potholes, road marking damage, and utility holes.

### Dataset Sources

Road Damage Detector:

https://github.com/sekilab/RoadDamageDetector

Dataset Ninja:

https://datasetninja.com/road-damage-detection

> The complete dataset is not included in this repository because of its size.

---

# 🗃️ Dataset Preparation

The dataset was prepared for YOLO object detection.

The configuration file is:

```text
dataset/data.yaml
```

The general process was:

```text
Raw Dataset
     │
     ▼
Dataset Extraction
     │
     ▼
Image + Annotation Inspection
     │
     ▼
YOLO Format
     │
     ▼
Training / Validation / Test Data
     │
     ▼
data.yaml
     │
     ▼
YOLOv8 Training
```

Each annotated object contains information about:

* Class
* Bounding-box position
* Bounding-box dimensions

The dataset labels were also visualized during the training process.

---

# 🤖 Model

The core of RoadDamageAI is a **YOLOv8 object detection model** provided through the Ultralytics framework.

YOLO stands for:

> **You Only Look Once**

Unlike simple image classification, object detection can determine both:

1. **What** is present in the image.
2. **Where** it is located.

For example:

```text
Road Image
     │
     ▼
YOLOv8
     │
     ├── Pothole → 0.91
     ├── Crack   → 0.84
     └── Crack   → 0.76
```

The trained model is stored as:

```text
models/best.pt
```

---

# 🏋️ Model Training

The model was trained using the prepared RDD2022 dataset and YOLOv8.

The training configuration was based on the dataset configuration:

```text
dataset/data.yaml
```

The training process was performed using the `train.py` script.

```bash
python train.py
```

The training process generated evaluation information including:

* Precision
* Recall
* F1 score
* Precision-Recall curves
* Confusion matrices
* Training results

The final trained model was saved as:

```text
models/best.pt
```

> Training was performed separately from the final desktop application. Users running the application do not need to retrain the model.

---

# 📊 Model Evaluation

The trained model was evaluated using standard object-detection metrics.

### Precision

Measures how many of the model's positive predictions were correct.

### Recall

Measures how many of the actual objects were successfully detected.

### F1 Score

Combines precision and recall into a single metric.

### mAP

Mean Average Precision is commonly used to evaluate object-detection performance.

The project includes visual evaluation results inside:

```text
results/
```

---

# 📈 Training Results

The training results generated by the model are included in the repository.

## Overall Training Results

![](results/results.png)

This graph contains the training and validation metrics recorded during the training process.

---

## 📊 Confusion Matrix

![](results/confusion_matrix.png)

The confusion matrix shows how predictions are distributed among the different road-damage classes.

It can help identify classes that the model may confuse with one another.

---

## 📊 Normalized Confusion Matrix

![](results/confusion_matrix_normalized.png)

The normalized confusion matrix represents the class predictions using normalized values, making comparison between classes easier.

---

## 📈 Precision-Recall Curve

![](results/BoxPR_curve.png)
The Precision-Recall curve shows the relationship between precision and recall at different confidence thresholds.

---

## 📈 F1 Score Curve

![](results/BoxF1_curve.png)

The F1 curve shows the relationship between precision and recall through the F1 score.

---

## 📈 Precision Curve

![](results/BoxP_curve.png)

This graph shows the model's precision at different confidence thresholds.

---

## 📉 Recall Curve

![](results/BoxR_curve.png)

This graph shows the model's recall at different confidence thresholds.

---

## 🏷️ Dataset Labels

![](results/labels.jpg)

This visualization shows information about the distribution and positioning of the dataset annotations.

---

## 📄 Training Metrics

Numerical training information is stored in:

```text
results/results.csv
```

This file contains the metrics recorded during model training.

---

# 🖥️ Application

The trained model was integrated into a desktop application using **CustomTkinter**.

The application provides an easy-to-use interface for performing road damage detection without requiring the user to interact directly with the Python code.

The basic workflow is:

```text
Open Application
       │
       ▼
Select Road Image
       │
       ▼
Preview Image
       │
       ▼
Run Detection
       │
       ▼
YOLOv8 Inference
       │
       ▼
Display Detections
       │
       ▼
Save Result
```

---

# 📸 Application Screenshots

Application screenshots can be stored inside:

```text
screenshots/
```

Recommended screenshots include:

```text
screenshots/
├── main-interface.png
├── image-selected.png
├── detection-result.png
└── saved-output.png
```

### Main Interface

![Main Interface](screenshots/main-interface.png)

The main application interface provides controls for selecting images, running detection, viewing results, and saving outputs.

### Selected Image

![Selected Image](screenshots/image-selected.png)

After selecting an image, the application displays it for analysis.

### Detection Result

![Detection Result](screenshots/detection-result.png)

After detection, the application displays the detected road damage with bounding boxes and confidence scores.

The final annotated image can be saved for documentation or further analysis.

> Replace these screenshot filenames with your actual filenames if they are different.

---

# ⚙️ Installation

## Requirements

You need:

* Python
* pip
* Git
* Sufficient storage for the required Python packages and model

---

## 1. Clone the Repository

```bash
git clone https://github.com/shuarya-anand/RoadDamageAI.git
```

Enter the project directory:

```bash
cd RoadDamageAI
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the required packages:

```bash
pip install -r requirements.txt
```

The main dependencies include:

```text
ultralytics
opencv-python
numpy
torch
torchvision
pillow
customtkinter
```

---

# ▶️ Running the Application

Once the dependencies are installed, start the application with:

```bash
python app.py
```

The RoadDamageAI desktop application should open.

---

# 📖 Complete User Guide

## Step 1 — Launch the Application

Run:

```bash
python app.py
```

The application window will appear.

---

## Step 2 — Open an Image

Click the:

```text
📂 Open Image
```

button.

A file-selection window will appear.

---

## Step 3 — Select a Road Image

Select an image from your computer.

You can use one of the included test images:

```text
test_images/
```

For example:

```text
test_images/1.jpg
```

---

## Step 4 — Preview the Image

After selecting the image, the application displays the selected image.

Make sure the correct image has been loaded before starting detection.

---

## Step 5 — Run Detection

Click:

```text
🚀 Run Detection
```

The selected image is passed to the trained YOLOv8 model.

The model analyzes the image and searches for the seven supported road-damage categories.

---

## Step 6 — Wait for Inference

The model performs inference locally on the computer.

The processing time depends on:

* CPU/GPU performance
* Image resolution
* Number of detected objects
* System resources

---

## Step 7 — View the Detection

Once processing is complete, the application displays the detected damage.

A detection can contain:

```text
Damage Type
Confidence Score
Bounding Box
```

For example:

```text
Pothole 0.91
```

means that the model assigned a confidence score of approximately 91% to that prediction.

---

## Step 8 — Review the Result

Check:

* Whether the correct road damage was detected.
* Whether the bounding box is around the damaged area.
* Whether the confidence score is reasonable.
* Whether multiple damaged areas were detected.

---

## Step 9 — Save the Result

Click:

```text
💾 Save Image
```

The annotated image can then be saved locally.

Saved detection results can be placed inside:

```text
output/
```

---

# 🔍 Detection Process

Internally, the application performs the following process:

```text
              Input Image
                   │
                   ▼
           Image Preprocessing
                   │
                   ▼
              YOLOv8 Model
                   │
                   ▼
             Model Inference
                   │
                   ▼
          Detection Predictions
                   │
                   ▼
          Confidence Filtering
                   │
                   ▼
        Class + Bounding Box
                   │
                   ▼
          OpenCV Annotation
                   │
                   ▼
            Display Result
                   │
                   ▼
             Save Image
```

---

# 💾 Saving Results

The application can save the annotated image after detection.

The result contains:

* Original image content
* Detection bounding boxes
* Damage labels
* Confidence scores

The `output/` folder is intended for saved detection results.

Example:

```text
output/
└── detected_road.png
```

---

# 🧪 Testing

The repository contains multiple road images for testing:

```text
test_images/
```

The current test-image collection includes:

```text
1.jpg
2.jpg
3.jpg
...
18.jpg
```

Testing the model on multiple images helps determine how it performs under different conditions.

Examples of changing conditions include:

* Different road surfaces
* Different lighting
* Different camera angles
* Different damage sizes
* Multiple damages in one image
* Images with little or no visible damage

---

## Testing Workflow

```text
Select Test Image
       │
       ▼
Run Detection
       │
       ▼
Observe Bounding Boxes
       │
       ▼
Check Class
       │
       ▼
Check Confidence
       │
       ▼
Save Result
```

---

# 🔬 Prediction Script

The repository also contains:

```text
predict.py
```

This script provides a separate way of performing inference using the trained model.

The trained weights are located at:

```text
models/best.pt
```

The desktop application uses the same trained model for its detection functionality.

---

# 📦 Model File

The trained model is stored at:

```text
models/best.pt
```

The application expects the model at this location when running from the project directory.

The application also contains resource-path handling for packaged execution.

---

# 🪟 Windows EXE

RoadDamageAI can be packaged into a standalone Windows executable using **PyInstaller**.

The executable is designed so that users do not need to install Python separately when using the packaged release.

The project also contains:

```text
RoadDamageAI.ico
```

which is used as the application icon.

---

# 🏗️ Windows Release Structure

The GitHub Actions release is prepared approximately as:

```text
RoadDamageAI-Windows/
│
├── RoadDamageAI.exe
│
├── models/
│   └── best.pt
│
├── test_images/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── ...
│
├── output/
│
└── README_RUN.txt
```

---

# 📦 Building the EXE

PyInstaller can be used to build the Windows executable.

The build command is:

```bash
pyinstaller --onefile --windowed --name RoadDamageAI --icon=RoadDamageAI.ico app.py
```

### Command explanation

```text
--onefile
```

Packages the application into a single executable.

```text
--windowed
```

Prevents an additional console window from opening with the GUI.

```text
--name RoadDamageAI
```

Sets the executable name.

```text
--icon=RoadDamageAI.ico
```

Sets the Windows application icon.

The resulting executable is generated inside:

```text
dist/
```

---

# 🤖 GitHub Actions Build

The repository contains a GitHub Actions workflow that can automatically build the Windows version.

The workflow:

```text
Push to main
      │
      ▼
GitHub Actions
      │
      ▼
Windows Runner
      │
      ▼
Install Python
      │
      ▼
Install Dependencies
      │
      ▼
Install PyInstaller
      │
      ▼
Build RoadDamageAI.exe
      │
      ▼
Copy best.pt
      │
      ▼
Copy test_images
      │
      ▼
Create Release
      │
      ▼
Upload Artifact
```

This allows a Windows build to be generated automatically from the GitHub repository.

---

# ⚠️ Limitations

RoadDamageAI is an educational Computer Vision project and has several limitations.

### Image Quality

Very blurry, dark, or low-resolution images may reduce detection performance.

### Lighting

Different lighting conditions can affect detection accuracy.

### Camera Angle

Images captured from unusual angles may be more difficult for the model.

### False Positives

The model may occasionally detect road damage where none exists.

### False Negatives

The model may fail to detect some visible damage.

### Dataset Limitations

The model's performance depends on the variety and quality of the training dataset.

### No Engineering Assessment

The application detects visible road damage but does not determine the structural integrity of a road.

### No Automatic Repair Decision

The model identifies visible damage categories but does not make a professional engineering decision about whether a road needs minor repair or complete reconstruction.

> RoadDamageAI should therefore be considered an AI-assisted visual inspection tool rather than a replacement for professional road inspection.

---

# 🚀 Future Improvements

Possible future versions of RoadDamageAI could include:

* 🎥 Real-time video road damage detection
* 📷 Live webcam detection
* 📱 Mobile application
* 🌐 Web-based version
* 📦 Batch image processing
* 📄 Automatic PDF inspection reports
* 📍 GPS location tagging
* 🗺️ Interactive road damage maps
* 📊 Detection statistics dashboard
* 🛣️ Road condition scoring
* 🔧 Damage severity estimation
* 🚧 Repair-priority estimation
* ☁️ Cloud deployment
* 🧠 Improved model accuracy using additional training data

---

# 🎓 Project Learning Outcomes

This project demonstrates several important Artificial Intelligence and Computer Vision concepts.

### Python Programming

Python was used for:

* Application development
* Model training
* Prediction
* Image processing
* File handling

### Computer Vision

Road images are processed and analysed using a deep-learning model.

### Object Detection

The model identifies:

* **What** the object is
* **Where** it is located
* **How confident** the model is

### Deep Learning

The project uses a neural-network-based object detection model trained on labelled data.

### Dataset Preparation

The project demonstrates how labelled image data can be prepared for machine learning.

### Model Training

A custom YOLOv8 model was trained specifically for road damage detection.

### Model Evaluation

The trained model was evaluated using multiple metrics and visualizations.

### GUI Development

The trained AI model was integrated into a functional desktop application.

### Deployment

The application can be packaged as a Windows executable using PyInstaller.

### Version Control

Git and GitHub were used to manage the project source code and documentation.

---

# 🔄 Complete Project Workflow

The complete RoadDamageAI workflow is:

```text
                    PROJECT IDEA
                         │
                         ▼
                  PROBLEM SCOPING
                         │
                         ▼
                  DATA ACQUISITION
                         │
                         ▼
                  DATA EXPLORATION
                         │
                         ▼
                  DATA PREPARATION
                         │
                         ▼
                  MODEL SELECTION
                         │
                         ▼
                   MODEL TRAINING
                         │
                         ▼
                  MODEL EVALUATION
                         │
                         ▼
                    BEST MODEL
                         │
                         ▼
                     best.pt
                         │
                         ▼
                  DESKTOP APPLICATION
                         │
                         ▼
                    USER IMAGE
                         │
                         ▼
                   YOLOv8 INFERENCE
                         │
                         ▼
                  DAMAGE DETECTION
                         │
                         ▼
               BOUNDING BOX + SCORE
                         │
                         ▼
                   SAVE RESULT
                         │
                         ▼
                    FINAL OUTPUT
```

---

# 🏁 Final Result

RoadDamageAI combines a trained Computer Vision model with a desktop graphical interface to create a complete AI application.

The final system can:

```text
Input Road Image
       ↓
AI Analysis
       ↓
Road Damage Detection
       ↓
Damage Classification
       ↓
Confidence Score
       ↓
Bounding Box
       ↓
Annotated Image
       ↓
Saved Result
```

The project demonstrates how a real-world problem can be converted into a working AI solution through the **Artificial Intelligence Project Cycle**.

---

# 👨‍💻 Author

## Shaurya Anand

RoadDamageAI was developed as a school **Artificial Intelligence and Computer Vision project**.

The project demonstrates the practical application of:

**Python + YOLOv8 + PyTorch + OpenCV + CustomTkinter**

for automated road damage detection.

---

# 📜 License

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project according to the terms of the license.

Third-party libraries, datasets, and frameworks used by this project are subject to their respective licenses.

---

# ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.

---

# 🛣️ RoadDamageAI

### Detect. Analyze. Understand Road Damage.

**Built with Python • YOLOv8 • PyTorch • OpenCV • CustomTkinter**
