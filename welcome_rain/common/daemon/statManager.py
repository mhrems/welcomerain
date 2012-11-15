import os
import matplotlib.pyplot as plt
import scipy
import math

from scipy import stats
from datetime import datetime,timedelta 

from dataModel import *


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from const import *
from rrdDataFetcher import *
from metricDBBuilder import *
from monitoringNode import *
from rrdDataFetcher import *
from timeseries import *


class StatChart:
    def __init__(self):
        self.data = []

    def cleanData(self,series):
        self.data = []
        for index,value in enumerate(series):
            if value>0:
                self.data.append(value)
            #print "index=",index, " , value=",value
    
    def drawHistrogram(self,statData,bin_count):
        series = statData.series
        self.cleanData(series)
        
        n, bins, patches = plt.hist(self.data, bin_count)
        print "drawHistrogram : count=",len(self.data)
        print "drawHistrogram : n=",n
        print "drawHistrogram : bins=",bins
        print "drawHistrogram : patches=",patches
        
        l = plt.plot(n)
        
        plt.grid(True)
        plt.show()

    def drawNormalDistrobution(self,statData):
        statData.dump()
        series = statData.series
        plt.plot(series,scipy.stats.norm.pdf(series,statData.mean,statData.stddev))
        plt.grid(True)
        plt.show()


        
        
class StatDataList:
    def __init__(self):
        self.data = []
    
    def getCount(self):
        return len(self.data)
    
    def addStatData(self,stat):
        self.data.append(stat)

    def getStatData(self,data_source,cluster="None",host="None"):
        for stat in self.data:
            if stat.series.cluster.find(cluster)>-1:
                if stat.series.host.find(host)>-1:
                    if stat.series.dataSource.find(data_source)>-1:
                        #print "StatDataList.getStatData : found"
                        return stat
        return None
    
        
        
class StatBuilder:
    def __init__(self):
        self.metric = None 
        self.rrdfetcher = RRDDataFetcher()
        self.data = StatDataList()
        self.binCount = 10
        self.series = None
        self.dataManager = None
        self.filter = []
    
    def setDataManager(self,data_manager):
        self.dataManager = data_manager
        
    def setBinCount(self,bin_count):
        self.binCount = bin_count
        
    def setMetric(self,metric):
        self.metric = metric

    def setFilter(self,filter):
        self.filter = filter
                    
    def buildSeriesData(self,startTime,endTime):
        self.series = self.rrdfetcher.fetch(self.metric,startTime,endTime)

    def buildStatData_old(self):
        for series in self.series:
            statItem = StatData()
            statItem.setSeries(series)
            statItem.calcStat()
            statItem.calcHistogram(self.binCount)
            #statItem.dump()
            self.data.addStatData(statItem)
            self.updateServerData(series, statItem)
        #print "probability=",statItem.getProbability(740)
        
        #chart = StatChart()
        #chart.drawHistrogram(statItem, 10)
        #chart.drawNormalDistrobution(statItem)
    
    def buildStatData(self):
        for series in self.series:
            statItem = StatDataModel()
            statItem.setSeries(series)
            statItem.calcStat()
            statItem.calcHistogram(self.binCount)
            #statItem.dump()
            #self.data.addStatData(statItem)
            self.updateServerData(statItem)
        #print "probability=",statItem.getProbability(740)
        
        #chart = StatChart()
        #chart.drawHistrogram(statItem, 10)
        #chart.drawNormalDistrobution(statItem)
        
    def updateServerData(self,statItem):
        self.dataManager.addServerStatData(statItem)
        
    
    def build(self,startTime,endTime):
        self.buildSeriesData(startTime,endTime)
        self.buildStatData()
        
        #self.dumpSeries()

    def getGridStat(self,data_source):
        return self.data.getStatData(data_source, "None", "None")
    
    def getClusterStat(self,data_source,cluster):
        return self.data.getStatData(data_source, cluster, const.SUMMARY_NODE)
    
    def getHostStat(self,data_source,cluster,host):
        return self.data.getStatData(data_source, cluster, host)
    
    def getUnusualData(self):
        for statItem in self.data:
            pass
    
    def getProbability(self,data_source):
        #if server.rawData==0:
        #    return const.RET_FAIL
        """
        stat = None
        if server.cluster=="None" and server.host=="None":
            stat = self.getGridStat(server.dataSource)
        elif server.host==const.SUMMARY_NODE:
            stat = self.getClusterStat(server.dataSource, server.cluster)
        else:
            stat = self.getHostStat(server.dataSource, server.cluster, server.host)
        
        if stat==None:
            print "StatBuilder.getProbability : Fail to find stat data using server",server
            return const.RET_FAIL
        """
        
        value = stat.getProbability(server.dataSources.getRawData())

        return value
    
            
    def dumpSeries(self):
        for series in self.series:
            print "name:",series.getFullName()
            
            for index,value in enumerate(series):
                print value
                #print "index=",index, " , value=",value
            print "avg=",scipy.average(series)," , variance=",scipy.var(series), " , stddev=",scipy.std(series)

            #return

    
class StatManager:
    def __init__(self):
        self.stat = StatBuilder()
        self.metric = None
        self.binCount = 10
        self.threshold = 10
        self.dataManager = None
                
    def setMetric(self,metric):
        self.metric = metric
        self.stat.setMetric(self.metric)

    def setThreshold(self,value):
        self.threshold = value

    def setBinCount(self,bin_count):
        self.binCount = bin_count
    
    def setDataManager(self,data_manager):
        self.dataManager = data_manager
        
    def buildStatData(self):
        now = datetime.now()
        past = now - timedelta(days=1)
    
        startTime = (past.strftime("%Y:%m:%d:%H:%M"))
        endTime = (now.strftime("%Y:%m:%d:%H:%M"))
        
        self.stat.setDataManager(self.dataManager)
        self.stat.build(startTime, endTime)

    def check(self,data_source):
        probability = self.stat.getProbability(data_source)
        server.setProbability(probability)
        
        if probability==const.RET_FAIL:
            return False
        
        #if self.threshold>probability:
        #    return False
        
        return True
    
        
        

if __name__ == '__main__':
    
    mu = 0
    sigma = 0.1
    #s = np.random.normal(mu, sigma, 1000)
    #data = range(1,10)
    #print scipy.average(data)

    serverData = ServerDataManager("None")

    startTime = "2012:10:12:00:00"
    endTime = "2012:10:15:00:00"
    
    builder = StatBuilder()
    builder.setFilter(["cpu_system","cpu_user","load_fifteen","mem_free","bytes_in","bytes_out","proc_total","proc_run"])
    builder.setFilter(["proc_total"])
    builder.setBinCount(10)
    builder.build(startTime,endTime)
    
    stat = builder.getGridStat("proc_total")
    stat = builder.getClusterStat("proc_total","unspecified")
    stat = builder.getHostStat("proc_total","unspecified","192.168.0.62")
    
    print "getGridStat"
    stat.dump()
    