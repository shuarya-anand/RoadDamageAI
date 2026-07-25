from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os

# --------------------------
# Load Model
# --------------------------

model = YOLO("models/best.pt")

damage_names = {
    "D00": "Longitudinal Crack",
    "D10": "Transverse Crack",
    "D20": "Alligator Crack",
    "D40": "Pothole",
    "D43": "Crosswalk Blur",
    "D44": "White Line Blur",
    "D50": "Utility Hole"
}


def detect():
    filepath = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.webp")
        ]
    )

    if not filepath:
        return

    image = cv2.imread(filepath)

    results = model.predict(
        source=filepath,
        conf=0.35,
        iou=0.45,
        verbose=False
    )

    result = results[0]

    for box in result.boxes:

        cls = int(box.cls[0])
        conf = float(box.conf[0])

        class_id = model.names[cls]
        damage = damage_names.get(class_id, class_id)

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            2
        )

        label = f"{damage} {conf*100:.1f}%"

        cv2.putText(
            image,
            label,
            (x1, max(25,y1-10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(rgb)
    img.thumbnail((900,600))

    photo = ImageTk.PhotoImage(img)

    panel.configure(image=photo)
    panel.image = photo


root = tk.Tk()

root.title("RoadDamageAI")
root.geometry("1000x700")

btn = tk.Button(
    root,
    text="Select Image",
    command=detect,
    font=("Arial",14),
    padx=20,
    pady=10
)

btn.pack(pady=20)

panel = tk.Label(root)
panel.pack()

root.mainloop()