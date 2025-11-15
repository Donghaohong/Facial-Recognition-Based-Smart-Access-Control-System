import cv2
import numpy as np
import os
import time

person_name = "Bole"
save_dir = os.path.join("dataset", person_name)
os.makedirs(save_dir, exist_ok=True)

modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
configFile = "deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

cap = cv2.VideoCapture(0)

IMAGES_PER_ACTION = 20

actions = [
    "Face the camera directly",
    "Turn your head 15 degrees to the left",
    "Turn your head 15 degrees to the right",
    "Look up",
    "Lower your head",
    "Smile"
]

def detect_face(frame):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        conf = detections[0, 0, i, 2]
        if conf > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w - 1, x2)
            y2 = min(h - 1, y2)
            return frame[y1:y2, x1:x2], (x1, y1, x2, y2)
    return None, None


count = 0

for action in actions:

    start_time = time.time()
    while time.time() - start_time < 5:
        ret, frame = cap.read()
        cv2.putText(frame, f"Please prepare: {action}",
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 0, 255), 4)
        cv2.imshow("Face Capture", frame)
        cv2.waitKey(1)

    collected = 0
    while collected < IMAGES_PER_ACTION:
        ret, frame = cap.read()
        if not ret:
            continue

        roi, bbox = detect_face(frame)
        if roi is not None and roi.size > 0:
            collected += 1
            count += 1
            cv2.imwrite(os.path.join(save_dir, f"{count}.jpg"), roi)

            (x1, y1, x2, y2) = bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"{action} - {collected}/{IMAGES_PER_ACTION}",
                        (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

        cv2.imshow("Face Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

