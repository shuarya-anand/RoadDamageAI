from ultralytics import YOLO
import cv2
import os
import glob

# ===========================
# Load Model
# ===========================
MODEL_PATH = "models/best.pt"
model = YOLO(MODEL_PATH)

# ===========================
# RDD2022 Class Names
# ===========================
damage_names = {
    "D00": "Longitudinal Crack",
    "D10": "Transverse Crack",
    "D20": "Alligator Crack",
    "D40": "Pothole",
    "D43": "Crosswalk Blur",
    "D44": "White Line Blur",
    "D50": "Utility Hole"
}

# ===========================
# Find Image Automatically
# ===========================
extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp"]

image_files = []

for ext in extensions:
    image_files.extend(glob.glob(os.path.join("test_images", ext)))

if len(image_files) == 0:
    print("❌ No image found inside test_images/")
    exit()

IMAGE_PATH = image_files[0]

print(f"📷 Using Image: {IMAGE_PATH}")

# ===========================
# Run Prediction
# ===========================
results = model.predict(
    source=IMAGE_PATH,
    conf=0.35,
    iou=0.45,
    save=False,
    verbose=False
)

result = results[0]

# ===========================
# Read Original Image
# ===========================
image = cv2.imread(IMAGE_PATH)

if image is None:
    print(f"❌ Could not read image: {IMAGE_PATH}")
    exit()

print("\n========== DETECTIONS ==========")

if len(result.boxes) == 0:
    print("✅ No road damage detected.")
else:
    for box in result.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        class_id = model.names[cls]
        damage = damage_names.get(class_id, class_id)

        print(f"{damage} ({class_id}) : {conf*100:.2f}%")

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Label
        label = f"{damage} {conf*100:.1f}%"

        (w, h), _ = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            2
        )

        cv2.rectangle(
            image,
            (x1, y1 - h - 10),
            (x1 + w, y1),
            (0, 255, 0),
            -1
        )

        cv2.putText(
            image,
            label,
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2
        )

# ===========================
# Save Result
# ===========================
os.makedirs("output", exist_ok=True)

filename = os.path.basename(IMAGE_PATH)
name, ext = os.path.splitext(filename)

output_path = os.path.join(
    "output",
    f"detected_{name}.png"
)

cv2.imwrite(output_path, image)

print(f"\n💾 Saved Result : {output_path}")
print("✅ Done.")   