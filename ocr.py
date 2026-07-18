"""
ocr.py

OCR module using EasyOCR.

Features:
- Extract text
- Draw OCR boxes
- Match OCR text with detected components
- Return structured JSON
"""

import cv2
import easyocr
import numpy as np


class OCRProcessor:

    def __init__(self, languages=None):

        if languages is None:
            languages = ["en"]

        self.reader = easyocr.Reader(
            languages,
            gpu=False
        )

    # ---------------------------------------------------
    # Extract OCR
    # ---------------------------------------------------

    def extract_text(self, image):

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        results = self.reader.readtext(rgb)

        return results

    # ---------------------------------------------------
    # Draw OCR Boxes
    # ---------------------------------------------------

    def draw_boxes(self, image, results):

        output = image.copy()

        for result in results:

            box = np.array(result[0]).astype(int)

            text = result[1]

            confidence = result[2]

            cv2.polylines(
                output,
                [box],
                True,
                (0, 0, 255),
                2
            )

            cv2.putText(
                output,
                text,
                (box[0][0], box[0][1] - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

        return output

    # ---------------------------------------------------
    # Convert OCR to JSON
    # ---------------------------------------------------

    def to_json(self, results):

        data = []

        for result in results:

            box = result[0]
            text = result[1]
            confidence = float(result[2])

            x = int(min(p[0] for p in box))
            y = int(min(p[1] for p in box))

            w = int(max(p[0] for p in box) - x)
            h = int(max(p[1] for p in box) - y)

            data.append({

                "text": text,

                "confidence": round(confidence, 3),

                "x": x,

                "y": y,

                "width": w,

                "height": h

            })

        return data

    # ---------------------------------------------------
    # Match OCR to Components
    # ---------------------------------------------------

    def match_components(self, components, ocr_json):

        matched = []

        for component in components:

            cx = component["x"] + component["width"] // 2
            cy = component["y"] + component["height"] // 2

            nearest_text = ""

            best_distance = 1e9

            for item in ocr_json:

                tx = item["x"] + item["width"] // 2
                ty = item["y"] + item["height"] // 2

                distance = ((cx - tx) ** 2 + (cy - ty) ** 2) ** 0.5

                if distance < best_distance:

                    best_distance = distance
                    nearest_text = item["text"]

            matched.append({

                "id": component["id"],

                "type": component["type"],

                "text": nearest_text,

                "x": component["x"],

                "y": component["y"],

                "width": component["width"],

                "height": component["height"]

            })

        return matched

    # ---------------------------------------------------
    # Complete OCR Pipeline
    # ---------------------------------------------------

    def process(self, image, components):

        results = self.extract_text(image)

        boxed_image = self.draw_boxes(
            image,
            results
        )

        ocr_json = self.to_json(results)

        matched = self.match_components(
            components,
            ocr_json
        )

        return {

            "ocr_image": boxed_image,

            "ocr_json": ocr_json,

            "components": matched

        }