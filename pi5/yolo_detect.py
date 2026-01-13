
# yolo_detect.py
import torch
import cv2

class YoloDetector:
    """Détection de personnes via YOLO"""
    def __init__(self, model_path='yolov8n.pt', target_classes=[0]):
        # On charge le modèle YOLO local
        self.model = torch.hub.load('ultralytics/yolov8', 'custom', path=model_path, source='local')
        self.target_classes = target_classes

    def detect(self, frame):
        """Retourne frame annotée"""
        results = self.model(frame)
        boxes = results.xyxy[0]  # xyxy format
        for *box, conf, cls in boxes.cpu().numpy():
            if int(cls) in self.target_classes:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)
                cv2.putText(frame, f'Person {conf:.2f}', (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        return frame
