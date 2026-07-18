"""
camera.py

Handles:
1. Webcam capture
2. YOLO paper detection
3. Automatic crop
4. Perspective correction
5. Return processed document
"""

import os
from datetime import datetime

import cv2
import numpy as np
from ultralytics import YOLO


class CameraCapture:

    def __init__(
        self,
        model_path="best.pt",
        save_folder="captures",
        confidence=0.5
    ):

        self.model = YOLO(model_path)
        self.confidence = confidence
        self.save_folder = save_folder

        os.makedirs(save_folder, exist_ok=True)

    # =====================================================
    # Order Corner Points
    # =====================================================

    def order_points(self, pts):

        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    # =====================================================
    # Perspective Transform
    # =====================================================

    def four_point_transform(self, image, pts):

        rect = self.order_points(pts)

        (tl, tr, br, bl) = rect

        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)

        maxWidth = max(int(widthA), int(widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)

        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype="float32")

        matrix = cv2.getPerspectiveTransform(rect, dst)

        return cv2.warpPerspective(image, matrix, (maxWidth, maxHeight))

    # =====================================================
    # Perspective Correction
    # =====================================================

    def perspective_from_crop(self, crop):

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        gray = cv2.equalizeHist(gray)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 30, 120)

        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) == 0:
            return crop

        largest = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest) < 1000:
            return crop

        peri = cv2.arcLength(largest, True)

        approx = cv2.approxPolyDP(
            largest,
            0.02 * peri,
            True
        )

        debug = crop.copy()

        cv2.drawContours(debug, [largest], -1, (0, 255, 0), 3)

        cv2.imshow("Largest Contour", debug)
        cv2.waitKey(1)

        if len(approx) == 4:
            return self.four_point_transform(
                crop,
                approx.reshape(4, 2)
            )

        return crop

    # =====================================================
    # Save Image
    # =====================================================

    def save(self, image):

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"

        path = os.path.join(
            self.save_folder,
            filename
        )

        cv2.imwrite(path, image)

        return path

    # =====================================================
    # Camera Capture
    # =====================================================

    def capture(self):

        cap = cv2.VideoCapture(0)

        captured = None

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            display = frame.copy()

            paper_box = None

            results = self.model(
                frame,
                conf=self.confidence
            )

            for result in results:

                if len(result.boxes) == 0:
                    continue

                best = max(
                    result.boxes,
                    key=lambda b: float(b.conf[0])
                )

                x1, y1, x2, y2 = map(
                    int,
                    best.xyxy[0]
                )

                paper_box = (x1, y1, x2, y2)

                confidence = float(best.conf[0])

                cv2.rectangle(
                    display,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    display,
                    f"Paper {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                display,
                "Press S to Capture | Q to Quit",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            cv2.imshow(
                "VisionCraft Camera",
                display
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord("s") and paper_box is not None:

                x1, y1, x2, y2 = paper_box

                padding = int(max(x2 - x1, y2 - y1) * 0.05)

                x1 = max(0, x1 - padding)
                y1 = max(0, y1 - padding)
                x2 = min(frame.shape[1], x2 + padding)
                y2 = min(frame.shape[0], y2 + padding)

                crop = frame[y1:y2, x1:x2]

                cv2.imshow("YOLO Crop", crop)
                cv2.waitKey(500)

                captured = self.perspective_from_crop(crop)

                break

        cap.release()
        cv2.destroyAllWindows()

        if captured is None:
            return None

        file_path = self.save(captured)

        return {
            "image": captured,
            "file_path": file_path
        }