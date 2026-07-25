# 🛣️ RoadDamageAI

An AI-powered desktop application for detecting road damage using **YOLOv8**, **Python**, and **CustomTkinter**.

RoadDamageAI analyzes road images and automatically identifies different types of road defects, helping improve road inspection efficiency.

---

## 📸 Features

- 🚀 AI-powered road damage detection
- 🧠 YOLOv8 object detection model
- 🖥 Modern desktop interface built with CustomTkinter
- 📷 Load road images from your computer
- 🎯 Detect multiple road damages in a single image
- 📊 Display confidence score for every detection
- 💾 Save annotated detection results
- 🌙 Modern dark theme interface

---

## 🛣️ Detectable Road Damage

The model can detect the following classes:

| Class | Description |
|--------|-------------|
| D00 | Longitudinal Crack |
| D10 | Transverse Crack |
| D20 | Alligator Crack |
| D40 | Pothole |
| D43 | Crosswalk Blur |
| D44 | White Line Blur |
| D50 | Utility Hole |

---

## 🖼 Application Preview

### Original Image

- Upload a road image for inspection.

### Detection Result

The application highlights detected damages using bounding boxes and displays:

- Damage type
- Confidence score
- Detection summary

---

## 🛠 Technologies Used

- Python 3.14
- Ultralytics YOLOv8
- OpenCV
- CustomTkinter
- Pillow
- NumPy

---

## 📁 Project Structure

```
RoadDamageAI/
│
├── app.py                 # Desktop application
├── train.py               # Model training script
├── predict.py             # Prediction script
├── requirements.txt
├── README.md
│
├── models/
│   └── best.pt            # Trained YOLO model
│
├── dataset/
│
├── test_images/
│
├── output/
│
└── .gitignore
```

---

## ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/shuarya-anand/RoadDamageAI.git
cd RoadDamageAI
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶ Running the Application

Start the desktop application:

```bash
python app.py
```

---

## 📖 How to Use

1. Launch the application.
2. Click **📂 Open Image**.
3. Select a road image.
4. Click **🚀 Run Detection**.
5. View detected road damages.
6. Save the annotated image using **💾 Save Image**.

---

## 🎯 Example Workflow

```
Input Image
      │
      ▼
YOLOv8 Detection
      │
      ▼
Bounding Boxes
      │
      ▼
Confidence Scores
      │
      ▼
Save Detection Result
```

---

## 📚 Future Improvements

- Video detection
- Live webcam detection
- Drag-and-drop image upload
- PDF inspection report generation
- GPS location tagging
- Detection history
- Multi-language support

---

## 👨‍💻 Author

**Shaurya Anand**

RoadDamageAI was developed as a school AI project demonstrating the application of computer vision and deep learning for automated road damage detection.

---

## 📄 License

This project is intended for educational and learning purposes.