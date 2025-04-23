import pickle

def save_project(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def load_project(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
