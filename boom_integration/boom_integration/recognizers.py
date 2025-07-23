from typing import Protocol
import cv2
import numpy as np
import base64
from typing import Optional


class Recognizer(Protocol):
    def recognize(self, image: str) -> list[str]:
        pass


class YoloRecognizer(Recognizer):
    def __init__(self, model):
        self.model = model

    def recognize(self, image: str) -> list[str]:
        img = self.base64_to_numpy(image)
        results = self.model.predict(img, conf=0.25, iou=0.7)
        output = []
        obj_id = 1
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                label = self.model.model.names[class_id]
                output.append(f"{label} ID:{obj_id}")
                obj_id += 1
        return output

    @staticmethod
    def base64_to_numpy(base64_str: str) -> Optional[np.ndarray]:
        img_data = base64.b64decode(base64_str)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            print("Ошибка: изображение не декодировано!")
        return img
