import os
import cv2
import numpy as np
import pickle

# assign a unique integer ID to each label
current_id = 0
# create a dictionary to store the mapping of label and id
# {'Donghao_Hong': 0, 'Bole_Ding': 1}
label_ids = {}
# create a list to store the region of interest of each face
# remove redundant inf to prevent interference with learning
x_train = []
# the corresponding integer id
y_labels = []

# find the absolute path of the directory where the python file is located
# __file__ returns the path of the current python script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#print(BASE_DIR)

# get the full path to the 'dataset' folder in the directory
image_dir = os.path.join(BASE_DIR, 'dataset')
#print(image_dir)

# create a local binary patterns histograms face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# load a pre-trained model to detect frontal human faces
classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

# os.walk() recursively traverse the entire folder tree
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        # get the absolute path for each image in the dataset
        path = os.path.join(root, file)
        #print(path)

        # return (height, width, channels)
        # 3 299x299 matrices which are the relevant intensity of 3 channels (Blue, Green, Red)
        image = cv2.imread(path)
        #print(image.shape)
        # convert color to grayscale so only 1 matrix left to represent the brightness of each pixel
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ensure the correctness of the datatype
        # to avoid float type during the dividing process to convert color to grayscale
        # Gray = 0.299Red + 0.587Green + 0.114Blue
        # unit8 (unsigned 8-bit integer) to represent the range of the grayscale from 0~255
        image_array = np.array(gray, 'uint8')
        #print(image_array.shape)
        label = os.path.basename(root)
        # store the face name with corresponding unique integer id into the directory
        if not label in label_ids:
            label_ids[label] = current_id
            current_id += 1
        id_ = label_ids[label]
        #print(label_ids)
        faces = classifier.detectMultiScale(image_array, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi = image_array[y:y+h, x:x+w]
            x_train.append(roi)
            y_labels.append(id_)
#print(y_labels)

with open("label_pickle", "wb") as f:
    pickle.dump(label_ids, f)

# train the recognizer using the dataset
recognizer.train(x_train, np.array(y_labels))
recognizer.save('trainer.yml')