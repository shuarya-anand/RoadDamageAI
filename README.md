# 🚧 RoadDamageAI

An AI-powered Road Damage Detection system built using **YOLOv8** and the **RDD2022 Dataset**.

The model automatically detects different types of road damages such as potholes and cracks from road images.

---

## Features

- Detects multiple road damage types
- Uses YOLOv8 Object Detection
- Automatically loads images from the `test_images` folder
- Displays damage type and confidence
- Saves annotated output image
- Easy to use

---

## Road Damage Classes

| Class | Damage Type |
|--------|-------------|
| D00 | Longitudinal Crack |
| D10 | Transverse Crack |
| D20 | Alligator Crack |
| D40 | Pothole |
| D43 | Crosswalk Blur |
| D44 | White Line Blur |
| D50 | Utility Hole |

---

## Project Structure

```
RoadDamageAI/
│
├── models/
│   └── best.pt
│
├── test_images/
│   └── image.jpg
│
├── output/
│
├── app.py
├── predict.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/RoadDamageAI.git
```

Go inside the project

```bash
cd RoadDamageAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run Prediction

Place an image inside

```
test_images/
```

Run

```bash
python predict.py
```

The detected image will be saved inside

```
output/
```

---

## Model

Model:
- YOLOv8m

Framework:
- Ultralytics

Dataset:
- RDD2022

Training:
- Google Colab (Tesla T4 GPU)

Image Size:
- 640×640

---

## Technologies Used

- Python
- YOLOv8
- PyTorch
- OpenCV
- Ultralytics
- Google Colab

---

## Future Improvements

- Live Webcam Detection
- Video Detection
- Dashcam Integration
- Drone-based Road Inspection
- Mobile Application

---

## Author

Shaurya Anand

Class X

School AI Project