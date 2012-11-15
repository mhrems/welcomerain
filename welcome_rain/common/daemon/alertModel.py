import os
from dataModel import *


class AlertDataModel:
    def __init__(self,name,condition,min,max,duration):
        self.name = name
        self.duration = duration
        self.min = min
        self.max = max
        self.condition = 1
        
        
class AlertModel:
    def __init__(self):
        self.user = -1
        self.regdate = ""
        self.updatedate = ""
        self.plugin = ""
    
        self.condition = "" 
        self.threhhold_vale = -1
        self.descriptions = ""


class Alerts:
    def __init__(self):
        self.alert = BaseDataCollection()
    
    def clear(self):
        self.data = []
    
    def addAlert(self,alert):
        self.data.append(alert)
    
    def getCount(self):
        return len(self.data)

    def getAlert(self,index):
        if index>=self.getCount():
            return None
        return self.data[index]
    
    def dump(self):
        for row in self.data:
            print row
     

