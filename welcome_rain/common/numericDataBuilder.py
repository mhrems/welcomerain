from datetime import datetime,timedelta 

from const import *
from summaryModel import *
from gmetadReader import *
from rrdreader import *
from rrdDataFetcher import *


class NumericDataBuilder:
    def __init__(self):
        self.rrdfetcher = RRDDataFetcher()
        #self.reader = RRDReader()
    
    def toString(self,items,limit):
        index = 1
        result = ""
        if limit==-1:
            limit = len(items)
            
        for value in items:      
            if index>limit:
                result += str(value)
                break
            else:
                result += str(value) + ","

            index += 1
        return result
    
    def fetchData(self,target,limit):
        now = datetime.now()
        past = now - timedelta(hours=1)
    
        startTime = (past.strftime("%Y:%m:%d:%H:%M"))
        endTime = (now.strftime("%Y:%m:%d:%H:%M"))
    
        """
        target = "mhr/dev.local/cpu_system.rrd"
        startTime = "2012:09:05:00:00"
        endTime = "2012:09:07:00:00"
        """
    
        logInfo("target="+target+",start="+startTime+",end="+endTime)
    
        results,name,rrdfile = self.rrdfetcher.fetchRawData(target,startTime,endTime)
 
        (timeInfo, values) = results
             
        #print "fetch=",values
        #for value in values:
        #    print value
        
        return self.toString(values,limit)


    def fetchTodayData(self,cluster_name,server_name,data_name):
        now = datetime.now()

        startTime = (now.strftime("%Y:%m:%d:00:00"))
        endTime = (now.strftime("%Y:%m:%d:%H:%M"))
    
        """
        target = "mhr/dev.local/cpu_system.rrd"
        startTime = "2012:09:05:00:00"
        endTime = "2012:09:07:00:00"
        """
    
        logInfo("target="+cluster_name+",start="+startTime+",end="+endTime)
    
        results,name,rrdfile = self.rrdfetcher.fetchRawData(cluster_name,server_name,data_name,startTime,endTime)
 
        (timeInfo, values) = results
             
        #print "fetch=",values
        #for value in values:
        #    print value
        
        return self.toString(values,-1)


if __name__ == "__main__":
    builder = MetaSummaryBuilder()
    data = builder.makeData()
    #print data.toString()
    builder.toString()
    #print builder.getCurrentMemory()
    
    #builder2 = ClusterSummaryBuilder()
    #data = builder2.makeData()
    #print data.toString()
    
    #builder = DashboardDataBuilder()
    #builder.fetchData("cpu")
    
    
    
    