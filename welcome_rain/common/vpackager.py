import pickle
import datetime
import os

class VPackager:
    def __init__(self):
        pass
    
    def serialize(self,obj):
        str = pickle.dumps(obj)
        return str
    
    def deserialize(self,str):
        obj = pickle.loads(str)
        return obj
     