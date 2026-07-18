"""
component_detector.py

Detects hand-drawn wireframe components using OpenCV.

Components:
- Button
- Input Field
- Image Placeholder
- Card
- Navbar
- Sidebar
- Text Area
- Unknown
"""

import cv2
import numpy as np


class ComponentDetector:

    def __init__(self):
        self.min_area = 800

    # --------------------------------------------------
    # Image Preprocessing
    # --------------------------------------------------

    def preprocess(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )

        kernel = np.ones((3, 3), np.uint8)

        thresh = cv2.dilate(thresh, kernel, iterations=1)

        return thresh

    # --------------------------------------------------
    # Classify Component
    # --------------------------------------------------

    def classify(self, x, y, w, h, image_width, image_height):

        aspect = w / h

        # Navbar
        if w > image_width * 0.7 and h < 120:
            return "Navbar"

        # Sidebar
        if h > image_height * 0.6 and w < image_width * 0.25:
            return "Sidebar"

        # Button
        if 60 < w < 250 and 25 < h < 90:
            return "Button"

        # Input
        if aspect > 3 and h < 70:
            return "Input Field"

        # Image Placeholder
        if 0.7 < aspect < 1.3 and w > 120 and h > 120:
            return "Image"

        # Card
        if w > 180 and h > 120:
            return "Card"

        # Text Area
        if aspect > 2 and h > 100:
            return "Text Area"

        return "Unknown"

    # --------------------------------------------------
    # Detect Components
    # --------------------------------------------------

    def detect(self, image):

        output = image.copy()

        processed = self.preprocess(image)

        contours, _ = cv2.findContours(
            processed,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        height, width = image.shape[:2]

        components = []

        component_id = 1

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < self.min_area:
                continue

            perimeter = cv2.arcLength(contour, True)

            approx = cv2.approxPolyDP(
                contour,
                0.02 * perimeter,
                True
            )

            if len(approx) < 4:
                continue

            x, y, w, h = cv2.boundingRect(approx)

            component_type = self.classify(
                x,
                y,
                w,
                h,
                width,
                height
            )

            components.append({

                "id": component_id,

                "type": component_type,

                "x": int(x),

                "y": int(y),

                "width": int(w),

                "height": int(h)

            })

            component_id += 1

            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                output,
                component_type,
                (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

        components = sorted(
            components,
            key=lambda c: (c["y"], c["x"])
        )

        return output, components

    # --------------------------------------------------
    # Draw Component Numbers
    # --------------------------------------------------

    def draw_numbers(self, image, components):

        output = image.copy()

        for component in components:

            x = component["x"]
            y = component["y"]

            cv2.circle(
                output,
                (x, y),
                15,
                (0, 0, 255),
                -1
            )

            cv2.putText(
                output,
                str(component["id"]),
                (x - 6, y + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

        return output