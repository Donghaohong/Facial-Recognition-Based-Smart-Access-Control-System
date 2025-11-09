import os

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