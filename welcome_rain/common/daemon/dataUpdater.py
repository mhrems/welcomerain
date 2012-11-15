import pickle
import datetime
import os

from metaDataBuilder import *
from dataModel import *


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from const import *
from monitoringNode import * 
from metricDBBuilder import *
from rrdDataFetcher import *


class DataUpdater:
    def __init__(self):
        self.rrdfetcher = RRDDataFetcher()
        self.metric = None
        self.data = None
        self.rawData = None
    
    def setMetric(self,metric):
        self.metric = metric
        
    def setData(self,item):
        self.data = item

    def clearRawData(self):
        self.rawData = []
                
    def makeSeries(self,series_list):
        series_data = []
        for series in series_list:
            timestamps = range(series.start, series.end, series.step)
            #datapoints = zip(timestamps,series)
            datapoints = map(dict, map(lambda t:zip(('x','y'),t), zip(timestamps,series)))
            series_data.append( dict(target=series.name, datapoints=datapoints) )

        return series_data
    
    def parseDataSource(self,value):
        tokens = value.split(",")        
        cluster = tokens[0]        
        host = tokens[1]        
        data = tokens[2]        
        
        return cluster,host,data
    
    """
    def makeServerDataModel(self,row):        
        server = ServerDataModel()
        server.cluster, server.host, server.dataSource = self.parseDataSource(row[2])
        server.setRawData(server.dataSource,row[0][1],row[0][0])
    
        return server
    """
        
    def updateRawData(self,row):        
        #server = ServerDataModel()
        cluster, server, dataSource = self.parseDataSource(row[2])
        updated = row[0][0]
        value = row[0][1]
        
        self.data.addServerRawData(cluster, server, dataSource,updated,value)

    
    def fetchLastData(self):
        self.clearRawData()
        self.rawData = self.rrdfetcher.fetchLastData(self.metric)
        return self.rawData
    
    def updateServerData(self):
        #self.data.clear()
        for index,row in enumerate(self.rawData):
            #print "fetchLastData : index=",index, " , data=",row
            self.updateRawData(row)
            #self.data.add(server)
        
    def fetch(self,metric,start,end):
        startTime = start
        endTime = end
        
        """
        target = "mhr/dev.local/cpu_system.rrd"
        startTime = "2012:09:05:00:00"
        endTime = "2012:09:07:00:00"
        """
        
        seriesList = self.rrdfetcher.fetch(metric,startTime,endTime)
        
        return self.makeSeries(seriesList)
         


if __name__ == "__main__":

    startTime = "2012:09:05:00:00"
    endTime = "2012:09:07:00:00"
    
    serverData = ServerDataManager("None")

    metricBuilder = MetaDataBuilder()
    metricBuilder.buildMetric(None)
    
    rrd = DataUpdater()
    rrd.setData(serverData)
    rrd.setMetric(metricBuilder.metric)
    
    series = rrd.fetchLastData()
    rrd.updateServerData()
    
    serverData.dump()
    
    print "finish"
    
    #serverData.dump()
    
    #print series
    
    #data = rrd.makeSeries(series)
    #print data
    