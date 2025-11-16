import os
import cv2
import numpy as np
import pickle

current_id = 0
label_ids = {}
x_train = []
y_labels = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, 'dataset')

recognizer = cv2.face.LBPHFaceRecognizer_create()

modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
configFile = "deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        path = os.path.join(root, file)

        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_array = np.array(gray, 'uint8')
        label = os.path.basename(root)
        if not label in label_ids:
            label_ids[label] = current_id
            current_id += 1
        id_ = label_ids[label]

        roi = image_array
        if roi.size == 0:
            continue

        x_train.append(roi)
        y_labels.append(id_)

with open("label_pickle", "wb") as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save('trainer.yml')
