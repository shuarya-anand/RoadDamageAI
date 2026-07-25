from ultralytics import YOLO
from pathlib import Path

# ==============================
# CONFIGURATION
# ==============================

DATASET_PATH = "dataset/data.yaml"
MODEL = "yolov8m.pt"

EPOCHS = 100
IMAGE_SIZE = 640
BATCH_SIZE = 8

PROJECT_NAME = "runs"
RUN_NAME = "RoadDamageAI_v8m_100ep"

# ==============================
# CHECK DATASET
# ==============================

if not Path(DATASET_PATH).exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

print("Loading YOLOv8m model...\n")

model = YOLO(MODEL)

print("Model loaded successfully!\n")

print("Starting training...\n")

# ==============================
# TRAIN MODEL
# ==============================

model.train(
    data=DATASET_PATH,
    epochs=EPOCHS,
    imgsz=IMAGE_SIZE,
    batch=BATCH_SIZE,
    workers=2,
    pretrained=True,
    optimizer="auto",
    patience=30,
    cache=False,
    amp=True,
    save=True,
    plots=True,
    val=True,
    project=PROJECT_NAME,
    name=RUN_NAME,
    exist_ok=True
)

print("\nTraining completed successfully!")

print("\nValidating best model...\n")

metrics = model.val()

print(metrics)

print("\nBest model saved at:")
print(f"{PROJECT_NAME}/detect/{RUN_NAME}/weights/best.pt")