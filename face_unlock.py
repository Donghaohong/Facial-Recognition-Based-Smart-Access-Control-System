import cv2
import numpy as np
import pickle
import time

modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
configFile = "deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

# ====== Load LBPH recognizer ======
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

with open("label_pickle", "rb") as f:
    origin_labels = pickle.load(f)
    labels = {v: k for k, v in origin_labels.items()}

# ====== BACK BUTTON area ======
back_button = (20, 20, 150, 70)  # x1, y1, x2, y2
clicked = None


def mouse_callback(event, x, y, flags, param):
    """
    Detect BACK button click
    """
    global clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        (x1, y1, x2, y2) = back_button
        if x1 <= x <= x2 and y1 <= y <= y2:
            clicked = "BACK"


def face_unlock_screen():
    """
    GUI-based face recognition unlock screen
    """
    global clicked
    clicked = None

    cap = cv2.VideoCapture(0)

    cv2.namedWindow("Face Unlock", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Face Unlock", 800, 480)
    cv2.setMouseCallback("Face Unlock", mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Back button UI
        (bx1, by1, bx2, by2) = back_button
        cv2.rectangle(frame, (bx1, by1), (bx2, by2), (255, 255, 255), 2)
        cv2.putText(frame, "BACK", (bx1 + 10, by1 + 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # ====== DNN Detection ======
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        best_conf = 0
        best_box = None

        # pick highest confidence face (避免多脸时乱跳)
        for i in range(detections.shape[2]):
            conf = detections[0, 0, i, 2]
            if conf > best_conf and conf > 0.6:
                best_conf = conf
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                best_box = box.astype("int")

        # ====== Recognize ======
        if best_box is not None:
            x1, y1, x2, y2 = best_box

            roi = gray[y1:y2, x1:x2]
            if roi.size > 0:
                id_, conf = recognizer.predict(roi)

                name = labels[id_] if conf <= 45 else "Unknown"
                print(f"{name}: {conf}")

                # draw box + label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                cv2.putText(
                    frame, f"{name}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2
                )

        cv2.imshow("Face Unlock", frame)

        # BACK
        if clicked == "BACK":
            clicked = None
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow("Face Unlock")

if __name__ == "__main__":
    face_unlock_screen()