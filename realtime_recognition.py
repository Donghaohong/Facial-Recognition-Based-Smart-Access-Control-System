import cv2
import numpy as np
import pickle

from arcface_embedder import ArcFaceEmbedder

EMB_PATH = "embeddings.npy"
NAME_PATH = "names.pkl"
MODEL_FILE = "res10_300x300_ssd_iter_140000.caffemodel"
CONFIG_FILE = "deploy.prototxt"
CONF_THRESHOLD = 0.7
SIM_THRESHOLD = 0.7


def load_database():
    embeddings = np.load(EMB_PATH)
    with open(NAME_PATH, "rb") as f:
        names = pickle.load(f)
    return embeddings, names


def load_detector():
    net = cv2.dnn.readNetFromCaffe(CONFIG_FILE, MODEL_FILE)
    return net


def detect_face(frame, net):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        frame, 1.0, (300, 300),
        (104.0, 177.0, 123.0),
        swapRB=False, crop=False
    )
    net.setInput(blob)
    detections = net.forward()

    best_conf = 0.0
    best_box = None

    for i in range(0, detections.shape[2]):
        conf = detections[0, 0, i, 2]
        if conf < CONF_THRESHOLD:
            continue
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        x1, y1, x2, y2 = box.astype(int)
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w - 1, x2)
        y2 = min(h - 1, y2)
        if x2 <= x1 or y2 <= y1:
            continue
        if conf > best_conf:
            best_conf = conf
            best_box = (x1, y1, x2, y2)

    if best_box is None:
        return None, None

    x1, y1, x2, y2 = best_box
    face = frame[y1:y2, x1:x2]
    return face, best_box


def recognize_face(face_bgr, embedder, db_embeddings, db_names):
    emb = embedder.get_embedding(face_bgr)

    db_norms = np.linalg.norm(db_embeddings, axis=1, keepdims=True)
    db_norms[db_norms == 0] = 1.0
    emb_norm = np.linalg.norm(emb)
    if emb_norm == 0:
        return "Unknown", 0.0

    sims = (db_embeddings @ emb) / (db_norms.flatten() * emb_norm)
    best_idx = int(np.argmax(sims))
    best_sim = float(sims[best_idx])
    best_name = db_names[best_idx]

    if best_sim >= SIM_THRESHOLD:
        return best_name, best_sim
    else:
        return "Unknown", best_sim


def main():
    db_embeddings, db_names = load_database()
    print("Database loaded:", db_embeddings.shape, "entries:", len(db_names))

    detector = load_detector()
    embedder = ArcFaceEmbedder("arcface.onnx")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        face, box = detect_face(frame, detector)
        if face is not None:
            name, score = recognize_face(face, embedder, db_embeddings, db_names)
            x1, y1, x2, y2 = box

            if name == "Unknown":
                color = (0, 0, 255)
                label = f"Unknown ({score:.2f})"
            else:
                color = (0, 255, 0)
                label = f"{name} ({score:.2f})"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

        cv2.imshow("Real-time Recognition", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
