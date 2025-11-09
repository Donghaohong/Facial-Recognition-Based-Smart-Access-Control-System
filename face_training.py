import os
import cv2
import numpy as np

# find the absolute path of the directory where the python file is located
# __file__ returns the path of the current python script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#print(BASE_DIR)

# get the full path to the 'dataset' folder in the directory
image_dir = os.path.join(BASE_DIR, 'dataset')
#print(image_dir)

# os.walk() recursively traverse the entire folder tree
for root, dirs, files in os.walk(image_dir):
    for file in files:
        # get the absolute path for each image in the dataset
        path = os.path.join(root, file)
        print(path)

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