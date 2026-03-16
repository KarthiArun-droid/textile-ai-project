from ultralytics import YOLO

model = YOLO("app/models/yolov8_fabric.pt")

def detect_defects(image_path):

    results = model(image_path)

    return results