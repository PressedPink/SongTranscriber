# encoding.py
import pickle
def encode(obj):
    return pickle.dumps(obj)
def decode(obj):
    return pickle.loads(obj)