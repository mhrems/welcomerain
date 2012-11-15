import cPickle
import datetime
#from django.core.cache import cache
from dataFetcher import *
from metaDataBuilder import *
from vpackager import *


class DataCacher:
    def __init__(self):
        self.lastFetchTime = None
        self.interval = 30
        self.dataFetched = False
        
        self.rrdData = None
        self.metric = None
        
        self.dataFetcher = DataFetcher()
        self.metaDataBuilder = MetaDataBuilder()
        self.packager = VPackager()
        
        
    def setInterval(self,interval):
        self.interval = interval
        
    def setLastFetchTime(self):
        self.lastFetchTime = datetime.datetime.now()
    
    def getElapsedTime(self):
        timediff = datetime.datetime.now() - self.lastFetchTime
        return timediff.total_seconds()
    
    def setFetched(self,value):
        self.dataFetched = value
        
    def isTimeToFetchNewData(self):
        if self.lastFetchTime is None:
            return True
        
        timediff = self.getElapsedTime()
        print "timediff=",timediff
        
        if timediff>self.interval:
            return True
        elif not self.dataFetched:
            return True
        
        return False
    

    def fetch(self):
        if not self.isTimeToFetchNewData():
            return False
        
        
        self.fetchMetaData()
        self.fetchRRDData()
        
        self.setFetched(True)
        self.setLastFetchTime()
        
    
    def fetchMetaData(self):
        self.metric = self.metaDataBuilder.build()
    
    def fetchRRDData(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(hours=1)
    
        startTime = (past.strftime("%Y:%m:%d:%H:%M"))
        endTime = (now.strftime("%Y:%m:%d:%H:%M"))
                
        self.rrdData = self.dataFetcher.fetch(self.metaDataBuilder.metric,startTime,endTime)
    
    def fetchSummaryData(self):
        pass
    
    def saveToCache(self):
        rrddata = self.packager.serialize(self.rrdData)
        metric = self.packager.serialize(self.metric)
        
        cache.set('rrdata', rrddata, 30)
        cache.set('metric', metric, 30)
        #cache.get('my_key')
        
    
    
    
   
if __name__ == "__main__":
    #print "adfs"
    cacher = DataCacher()
    cacher.fetch()
    
    print cacher.rrdData
    print cacher.metric
    
    