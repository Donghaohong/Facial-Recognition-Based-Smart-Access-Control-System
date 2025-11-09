import pickle

with open('label_pickle', 'rb') as f:
    data = pickle.load(f)
print(data)
