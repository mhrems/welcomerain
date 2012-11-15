import os

class MetaSummaryModel:
    def __init__(self):
        self.name = ""
        self.hostUp = 0
        self.hostDown = 0
        self.cpuTotal = 0
        self.avgLoad = 0
        self.localTime = ""
    
    def toString(self):
        str = "name="+self.name
        str = str + "hostUp="+self.hostUp
        str = str + "hostDown="+self.hostDown
        str = str + "localTime="+self.localTime
        return str

class PhysicalSummaryModel:
    def __init__(self):
        self.totalCPU = 0
        self.totalMemory = 0
        self.totalDisk = 0

class ServerSummaryModel:
    def __init__(self):
        self.avgLoad = 0
        self.avgCPU = 0
        self.lastUpdate = ""
        self.uptime = ""
        
        self.cpu = ""
        self.memory = ""
        self.localDisk = ""
        self.mostFullDisk = ""
        
        self.os = ""
        self.booted = ""
        self.swap = ""
        
    
    
    