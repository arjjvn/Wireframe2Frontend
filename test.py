import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, conf=0.5)

    annotated = frame.copy()

    for result in results:
        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])
            cls = int(box.cls[0])

            label = model.names[cls]

            cv2.rectangle(annotated, (x1, y1), (x2, y2),
                          (0, 255, 0), 2)

            cv2.putText(
                annotated,
                f"{label} {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            # Crop detected paper
            crop = frame[y1:y2, x1:x2]

            if crop.size != 0:
                cv2.imshow("Detected Paper", crop)

    cv2.imshow("Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()