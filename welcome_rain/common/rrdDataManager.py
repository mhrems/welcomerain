import pickle
import datetime
from django.core.cache import cache


class RRDDB:
    def __init__(self):
        self.lastFetchTime = None
        self.interval = 30
        self.dataFetched = False
        
    def setInterval(self,interval):
        self.interval = interval
        
    def setLastFetchTime(self):
        self.lastFetchTime = datetime.datetime.now()
    
    def getElapsedTime(self):
        timediff = datetime.datetime.now() - self.lastFetchTime
        return timediff.total_seconds()
    
    def setToFetch(self):
        self.dataFetched = False
        
    def isTimeToFetchNewData(self):
        if self.lastFetchTime is None:
            return True
        
        timediff = self.getElapsedTime()
        if timediff>self.interval:
            return True
        elif not self.dataFetched:
            return True
        
        return False
    

    def fetch(self):
        if not self.isTimeToFetchNewData():
            return False
        
        self.setToFetch()
    
    def saveToCache(self):
        cache.set('my_key', 'hello, world!', 30)
        cache.get('my_key')
    
    
   
if __name__ == "__main__":
    print "adfs"
    