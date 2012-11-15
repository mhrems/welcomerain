import os
from dataModel import *
from dataUpdater import *
from alertModel import *



class AlertManager:
    def __init__(self):
        self.interval = 300
        self.data = None
        self.alerts = BaseDataCollection()

        
    def setData(self,data):
        self.data = data
    
    def isAlert(self,value):
        return False
    
    def clearAlerts(self):
        self.alerts = BaseDataCollection()
    
    def getCount(self):
        return len(self.alerts)
    
    def addAlert(self,alert):
        self.alerts.append(alert)
    
    def getAlert(self,name):
        alert = self.alerts.find(name) 
        if alert is None:
            return None
        
        return alert
    

    def check(self,data_source):
        alert = self.getAlert(data_source.name)
        if alert is None:
            return False
        
        if self.isAlert(data_source):
            alert = None
            self.addAlerts(alert)
            return True
        
        return False
    
        
if __name__ == "__main__":
    
    serverData = ServerDataManager()

    metricBuilder = MetaDataBuilder()
    metricBuilder.build()
    
    rrd = DataUpdater()
    rrd.setData(serverData)
    rrd.setMetric(metricBuilder.metric)
    
    series = rrd.fetchLastData()
    rrd.buildServerData()
    
    serverData.dump()
    
    #print series
    
    #data = rrd.makeSeries(series)
    #print data
        