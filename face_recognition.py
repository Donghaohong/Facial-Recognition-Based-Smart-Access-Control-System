import cv2
import numpy as np
import pickle

modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
configFile = "deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

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
        # ---- DNN face detection ----
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")

                gray_roi = gray[y1:y2, x1:x2]

                if gray_roi.size == 0:
                    continue

                id_, conf = recognizer.predict(gray_roi)
                print(labels[id_], conf)

                # 总是画框
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # 判断名字或 Unknown
                name = labels[id_] if conf <= 40 else "Unknown"

                cv2.putText(frame, name, (x1, y1 - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2)

                #break

    cv2.imshow('Result', frame)

    #quit the program when pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cqlose the connection with the camera device
cap.release()
# close all windows opened by cv2.imshow()
cv2.destroyAllWindows()
