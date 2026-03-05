from ultralytics import YOLO
import cv2
import os

# Convert grayscale images to RGB
def convert_to_rgb(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".tif"):
                path = os.path.join(root, file)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                    cv2.imwrite(path, img_rgb)

convert_to_rgb("../data/tilda_dataset/images")

model = YOLO("weights/yolov8n.pt")

model.train(
    data="../data/tilda_dataset/data.yaml",
    epochs=40,
    imgsz=640,
    batch=4
) 