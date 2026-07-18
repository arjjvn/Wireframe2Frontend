
import os
from datetime import datetime
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image


class ImageProcessor:

    def __init__(
        self,
        upload_folder="uploads",
        max_width=1400,
        model_path="best.pt"
    ):

        self.upload_folder = upload_folder
        self.max_width = max_width

        os.makedirs(upload_folder, exist_ok=True)

        # Load YOLO model
        self.model = YOLO(model_path)


    # =====================================================
    # Detect Paper
    # =====================================================

    def detect_paper(self, image):

        results = self.model(image, conf=0.5)

        boxes = results[0].boxes

        if len(boxes) == 0:
            return image

        best = max(boxes, key=lambda b: float(b.conf[0]))

        x1, y1, x2, y2 = map(int, best.xyxy[0])

        paper = image[y1:y2, x1:x2]

        return paper

    # =====================================================
    # Draw Detected Paper
    # =====================================================

    def draw_paper_boundary(self, image):

        output = image.copy()

        results = self.model(output, conf=0.5)

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            cls = int(box.cls[0])

            label = self.model.names[cls]

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )

            cv2.putText(
                output,
                f"{label} {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        return output



    # =====================================================
    # Main Processing Pipeline
    # =====================================================

    def process_camera(self, camera_result):

        cv_image = camera_result["image"]

        pil_image = Image.fromarray(
            cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        )

        filepath = camera_result["file_path"]

        # Camera image is already cropped and perspective corrected
        paper = cv_image.copy()

        paper_boundary = cv_image.copy()

        return {
            "pil_image": pil_image,
            "cv_image": cv_image,
            "paper": paper,
            "paper_boundary": paper_boundary,
            "file_path": filepath
        }

    def process(self, uploaded_file):

        # Load image
        pil_image = Image.open(uploaded_file).convert("RGB")

        # Save uploaded image
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        filepath = os.path.join(self.upload_folder, filename)
        pil_image.save(filepath)

        # Convert to OpenCV
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Resize if needed
        h, w = cv_image.shape[:2]
        if w > self.max_width:
            ratio = self.max_width / w
            cv_image = cv2.resize(
                cv_image,
                (self.max_width, int(h * ratio))
            )

        # Draw YOLO detections
        paper_boundary = self.draw_paper_boundary(cv_image)

        # Crop detected paper
        paper = self.detect_paper(cv_image)

        return {
            "pil_image": pil_image,
            "cv_image": cv_image,
            "paper": paper,
            "paper_boundary": paper_boundary,
            "file_path": filepath
        }

