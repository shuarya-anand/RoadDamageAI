from ultralytics import YOLO
import cv2
import os
import glob


# ============================================================
# ROAD DAMAGE AI - PREDICTION SCRIPT
# ============================================================

# -----------------------------
# 1. Load Model
# -----------------------------

MODEL_PATH = "models/best.pt"

if not os.path.isfile(MODEL_PATH):
    print(f"❌ Model not found: {MODEL_PATH}")
    print("Make sure best.pt is inside the models/ folder.")
    exit()

print("🔄 Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("✅ Model loaded successfully!")


# -----------------------------
# 2. RDD2022 Class Names
# -----------------------------

damage_names = {
    "D00": "Longitudinal Crack",
    "D10": "Transverse Crack",
    "D20": "Alligator Crack",
    "D40": "Pothole",
    "D43": "Crosswalk Blur",
    "D44": "White Line Blur",
    "D50": "Utility Hole",
}


# -----------------------------
# 3. Find Image Automatically
# -----------------------------

IMAGE_DIR = "test_images"

extensions = [
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.webp",
    "*.bmp",
]

image_files = []

for ext in extensions:
    image_files.extend(
        glob.glob(os.path.join(IMAGE_DIR, ext))
    )

if len(image_files) == 0:
    print("❌ No image found inside test_images/")
    exit()

# Use the first image found
IMAGE_PATH = image_files[0]

print(f"📷 Using Image: {IMAGE_PATH}")


# -----------------------------
# 4. Run YOLO Prediction
# -----------------------------

print("\n🔍 Running road damage detection...")

results = model.predict(
    source=IMAGE_PATH,
    conf=0.35,
    iou=0.45,
    save=False,
    verbose=False,
)

result = results[0]


# -----------------------------
# 5. Read Original Image
# -----------------------------

print("📖 Reading original image...")

image = cv2.imread(IMAGE_PATH)

if image is None:
    print(f"❌ Could not read image: {IMAGE_PATH}")
    exit()


# -----------------------------
# 6. Display Detections
# -----------------------------

print("\n================================")
print("        DETECTIONS")
print("================================")

if len(result.boxes) == 0:

    print("✅ No road damage detected.")

else:

    print(f"🔎 Found {len(result.boxes)} detection(s)\n")

    for box in result.boxes:

        # Class ID
        cls = int(box.cls[0])

        # Confidence
        conf = float(box.conf[0])

        # Get class name from YOLO model
        class_id = model.names[cls]

        # Convert class ID to readable damage name
        damage = damage_names.get(
            class_id,
            class_id
        )

        print(
            f"• {damage} "
            f"({class_id}) : "
            f"{conf * 100:.2f}%"
        )

        # -----------------------------
        # Bounding Box Coordinates
        # -----------------------------

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

        # -----------------------------
        # Draw Bounding Box
        # -----------------------------

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # -----------------------------
        # Create Label
        # -----------------------------

        label = (
            f"{damage} "
            f"{conf * 100:.1f}%"
        )

        # Calculate label size
        (w, h), _ = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            2
        )

        # Make sure label doesn't go above image
        label_y1 = max(y1 - h - 10, 0)
        label_y2 = max(y1, h + 10)

        # -----------------------------
        # Label Background
        # -----------------------------

        cv2.rectangle(
            image,
            (x1, label_y1),
            (x1 + w, label_y2),
            (0, 255, 0),
            -1
        )

        # -----------------------------
        # Label Text
        # -----------------------------

        cv2.putText(
            image,
            label,
            (x1, max(y1 - 5, h)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2
        )


# -----------------------------
# 7. Create Output Folder
# -----------------------------

OUTPUT_DIR = "output"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# -----------------------------
# 8. Generate Output Filename
# -----------------------------

filename = os.path.basename(
    IMAGE_PATH
)

name, ext = os.path.splitext(
    filename
)

output_path = os.path.join(
    OUTPUT_DIR,
    f"detected_{name}.png"
)


# -----------------------------
# 9. Save Result
# -----------------------------

success = cv2.imwrite(
    output_path,
    image
)

if success:

    print("\n================================")
    print("          COMPLETE")
    print("================================")

    print(
        f"💾 Saved Result: {output_path}"
    )

    print("✅ Road damage analysis completed successfully!")

else:

    print("❌ Failed to save result image.")