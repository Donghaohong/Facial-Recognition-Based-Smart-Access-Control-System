import os
import cv2
import numpy as np
import pickle
from arcface_embedder import ArcFaceEmbedder

DATASET_DIR = "dataset"
EMB_PATH = "embeddings.npy"
NAME_PATH = "names.pkl"


def build_database():
    embedder = ArcFaceEmbedder("arcface.onnx")

    embeddings = []
    names = []

    for person in os.listdir(DATASET_DIR):
        person_dir = os.path.join(DATASET_DIR, person)
        if not os.path.isdir(person_dir):
            continue

        for fname in os.listdir(person_dir):
            if not (fname.lower().endswith(".jpg") or fname.lower().endswith(".png")):
                continue

            img_path = os.path.join(person_dir, fname)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Failed to read image: {img_path}")
                continue

            emb = embedder.get_embedding(img)
            embeddings.append(emb)
            names.append(person)

            print(f"Processed: {img_path}")

    if len(embeddings) == 0:
        print("No embeddings generated. Check your dataset directory.")
        return

    embeddings = np.stack(embeddings, axis=0)

    if os.path.exists(EMB_PATH):
        os.remove(EMB_PATH)
    if os.path.exists(NAME_PATH):
        os.remove(NAME_PATH)

    np.save(EMB_PATH, embeddings)
    with open(NAME_PATH, "wb") as f:
        pickle.dump(names, f)

    print("Database built.")
    print("Embeddings shape:", embeddings.shape)
    print("Number of entries:", len(names))
    print("Saved to:", EMB_PATH, "and", NAME_PATH)


if __name__ == "__main__":
    build_database()
