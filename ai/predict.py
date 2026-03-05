from ultralytics import YOLO

model = YOLO("weights/yolov8m.pt")

model.train(
    data="../data/tilda_dataset/data.yaml",
    epochs=80,
    imgsz=1024,
    batch=8
)