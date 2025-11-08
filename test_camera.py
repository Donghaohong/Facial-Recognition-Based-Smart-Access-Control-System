import cv2
import numpy as np

# create an object for the camera
cap = cv2.VideoCapture(0)

while(True):
    # read a single frame from the carema
    # ret is a boolean result showing whether the frame is successfully read
    # frame is the frame captured
    ret, frame = cap.read()
    if ret:
        #display the frame in a window called frame
        cv2.imshow('frame', frame)
    #quit the program when pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# close the connection with the camera device
cap.release()
# close all windows opened by cv2.imshow()
cv2.destroyAllWindows()