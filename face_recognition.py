import cv2
import numpy as np
import pickle

# load a pre-trained model to detect frontal human faces
classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

# create a local binary patterns histograms face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('./trainer.yml')

labels = {}

with open("label_pickle", 'rb') as f:
    origin_labels = pickle.load(f) # {'Donghao_Hong': 0, 'Bole_Ding': 1}
    labels = {v:k for k,v in origin_labels.items()}

#print(labels)

# create an object for the camera
cap = cv2.VideoCapture(0)

# Haar cascade model (a type of machine learning based detector)
# cv2.data.haarcascades gives the path to the OpenCV's built-in pretrained XML models
# haarcascade_frontalface_alt2.xml is a detector designed for frontal faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

while(True):
    # read a single frame from the carema
    # ret is a boolean result showing whether the frame is successfully read
    # frame is the frame captured
    ret, frame = cap.read()
    if ret:
        # covert the color frame into grayscale
        # The model is based on brightness (grayscale) changes instead of colors
        # Color only adds unnecessary computation
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # scan the image at different scales to find faces at different distances to the camera
        # scale factor decides how much the image size is reduced at each scale
        # minNeighbour decides the number of rectangles must be kept to be recognized as a face
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            #print(x, y, w, h)
            gray_roi = gray[y:y+h, x:x+w]
            id_, conf = recognizer.predict(gray_roi)
            #print(id_, conf)
            if conf >= 50:
                #print(labels[id_])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, str(labels[id_]), (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 2)
            cv2.imshow('Result', frame)

    #quit the program when pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cqlose the connection with the camera device
cap.release()
# close all windows opened by cv2.imshow()
cv2.destroyAllWindows()