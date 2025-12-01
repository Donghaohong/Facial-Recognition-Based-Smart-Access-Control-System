import cv2
import numpy as np
import onnxruntime as ort

class ArcFaceEmbedder:
    def __init__(self, model_path="arcface.onnx"):
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def preprocess(self, img_bgr):
        img = cv2.resize(img_bgr, (112, 112))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32)
        img = (img - 127.5) / 128.0     # from model card
        img = np.expand_dims(img, axis=0)   # (1,112,112,3)
        return img

    def get_embedding(self, face_bgr):
        blob = self.preprocess(face_bgr)
        emb = self.session.run([self.output_name], {self.input_name: blob})[0][0]
        emb = emb.astype(np.float32)
        emb = emb / np.linalg.norm(emb)
        return emb


if __name__ == "__main__":
    embedder = ArcFaceEmbedder("arcface.onnx")
    img = cv2.imread("dataset/Donghao/1.jpg")
    if img is None:
        print("Failed to load test image.")
        exit()
    emb = embedder.get_embedding(img)
    print("Embedding shape:", emb.shape)
    print("First 10 values:", emb[:10])
    print("L2 norm:", np.linalg.norm(emb))
