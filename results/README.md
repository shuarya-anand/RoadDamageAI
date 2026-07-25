# 📈 Model Training Results

This folder contains the evaluation results generated during the training of the RoadDamageAI YOLOv8 model.

The images in this directory help evaluate the model's performance and determine whether it has learned effectively or started to overfit.

---

# Files

## results.png

Contains the complete training history.

It includes:

- Training Loss
- Validation Loss
- Precision
- Recall
- mAP@0.50
- mAP@0.50:0.95

This graph is used to monitor learning progress and identify signs of overfitting or underfitting.

---

## confusion_matrix.png

Shows the confusion matrix for all road damage classes.

It illustrates:

- Correct classifications
- Incorrect classifications
- Which classes are frequently confused

A stronger diagonal indicates better classification performance.

---

## confusion_matrix_normalized.png

Displays the normalized confusion matrix.

Each row is normalized to percentages, making it easier to compare performance across different classes regardless of sample count.

---

## PR_curve.png

Precision-Recall Curve for each damage class.

A curve closer to the upper-right corner represents better detection performance.

---

## F1_curve.png

Shows the F1 score across different confidence thresholds.

This graph helps determine the confidence threshold that provides the best balance between Precision and Recall.

---

## P_curve.png

Precision vs Confidence Curve.

Higher values indicate fewer false positive detections.

---

## R_curve.png

Recall vs Confidence Curve.

Shows how recall changes as the confidence threshold increases.

---

## labels.jpg

Visualization of the dataset labels.

Shows:

- Distribution of bounding boxes
- Object sizes
- Class frequency
- Dataset balance

Useful for understanding the characteristics of the training dataset.

---

# Training Summary

- **Model:** YOLOv8
- **Framework:** Ultralytics
- **Language:** Python
- **Dataset:** RDD2022 (Road Damage Detection)
- **Task:** Road Damage Detection

---

# Model Evaluation

The model was evaluated using standard object detection metrics including:

- Precision
- Recall
- F1 Score
- mAP@0.50
- mAP@0.50:0.95

These metrics provide a comprehensive assessment of detection accuracy and generalization performance.

---

# Notes

Signs of overfitting can include:

- Training loss continues to decrease while validation loss increases.
- Precision and Recall stop improving after additional epochs.
- mAP values plateau or decrease despite continued training.

If overfitting is observed, possible improvements include:

- Early stopping
- Additional training data
- Stronger data augmentation
- Hyperparameter tuning

---

Generated using the Ultralytics YOLOv8 training pipeline.
