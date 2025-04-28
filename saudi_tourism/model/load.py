import pickle

def load_model(filename):

    loaded_model = pickle.load(open(filename, 'rb'))

    return loaded_model
