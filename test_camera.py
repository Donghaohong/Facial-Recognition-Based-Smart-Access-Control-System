import cv2
import numpy as np
import os

# create an object for the camera
cap = cv2.VideoCapture(0)

# Haar cascade model (a type of machine learning based detector)
# cv2.data.haarcascades gives the path to the OpenCV's built-in pretrained XML models
# haarcascade_frontalface_alt2.xml is a detector designed for frontal faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

count = 0

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
            print(x, y, w, h)
            count += 1
            save_dir = '/Users/donghaohong/Documents/Facial_rcg/dataset/Donghao'
            os.makedirs(save_dir, exist_ok=True)

            cv2.imwrite(os.path.join(save_dir, f"{count}.jpg"), frame[y:y + h, x:x + w])
            #cv2.imwrite('/Users/donghaohong/Documents/Facial_rcg/dataset/100_dh/' + str(count) + '.jpg', frame[y:y+h, x:x+w])
            # cv2.rectangle('frame', 'top-left coordinate', 'bottom-right coordinate', 'color of the rectangle', 'line thickness')
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 5)

        #display the frame in a window called frame
        #cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
    #quit the program when pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif count == 200:
        break

# close the connection with the camera device
cap.release()
# close all windows opened by cv2.imshow()
cv2.destroyAllWindows()