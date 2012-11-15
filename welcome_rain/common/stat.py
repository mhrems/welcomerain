import matplotlib.pyplot as plt
import scipy
import math
from scipy import stats

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


class HistogramData:
    def __init__(self):
        self.bins = None
        self.numbers = None
        self.probability = None
        self.count = 0
        self.binCount = 0
        self.binSize = 0.0 
        self.lowRange = 0.0
        self.series = None
    
    def setSeries(self,series):
        self.series = series
        self.count = len(self.series)
        
    def setBinCount(self,count):
        self.binCount = count
            
    def setBins(self,bins):
        self.bins = bins
    
    def setNumbers(self,numbers):
        self.numbers = numbers
    
    def buildBins(self):
        self.bins = []
        for index in range(self.binCount):
            value = self.lowRange + self.binSize*(index+1)
            self.bins.append(value)
    
    def buildProbability(self):
        self.probability = []
        for numbers in self.numbers:
            value = round((numbers/self.count)*100)
            self.probability.append(value)
            
    def doHistogram(self):
        result = scipy.stats.histogram(self.series, self.binCount)
        self.numbers = result[0]
        self.lowRange = result[1]
        self.binSize = result[2]
        self.buildBins()
        self.buildProbability()
        #print "doHistogram:",result
    
    def getBinIndex(self,x):
        #index = math.ceil((x - self.bins[0])/self.binSize)
        index = math.ceil(x/self.binSize)
        return math.trunc(index-1)
            
    def getProbability(self,x):
        index = self.getBinIndex(x)
        return self.probability[index]
    
    def dump(self):
        print "name=" , self.series.getFullName(), " , count=",self.count, " , binCount=",self.binCount," , binSize=",self.binSize
        print "numbers=",self.numbers
        print "bins=",self.bins
        print "probability=",self.probability
        
    
class StatData:
    def __init__(self):
        self.metric = None
        self.avg = 0.0
        self.stddev = 0.0
        self.variance = 0.0
        self.mean = 0.0
        self.median = 0.0
        self.series = None
        self.data = []
        self.histogram = HistogramData()
        
    def makeJSON(series_list,event_list):
        series_data = []
        for series in series_list:
            timestamps = range(series.start, series.end, series.step)
            #datapoints = zip(timestamps,series)
            datapoints = map(dict, map(lambda t:zip(('x','y'),t), zip(timestamps,series)))
            series_data.append( dict(target=series.getFullName(), events=event_list, datapoints=datapoints) )

        return series_data
    
    def setSeries(self,series):
        self.series = series
        
    def setMetric(self,metric):
        self.metric = metric
    
    def getCount(self):
        return len(self.series)
    
    def dump(self):
        print "name:", self.series.getFullName() ," , count=", self.getCount() , " , avg=",self.avg, " , variance=",self.variance, " , stddev=",self.stddev
    
    def cleanData(self):
        self.data = []
        for index,value in enumerate(self.series):
            if value>0:
                self.data.append(value)
            #print "index=",index, " , value=",value
        
    def calcAvg(self):
        self.avg = scipy.average(self.series)
    
    def calcVariance(self):
        self.variance = scipy.var(self.series)

    def calcStandDeviation(self):
        self.stddev = scipy.std(self.series)

    def calcZ(self,value):
        z = (value-self.avg)/self.stddev
    
    def calcMean(self):
        self.mean = scipy.mean(self.series)
        
    def calcMedian(self):
        self.median = scipy.median(self.series)
    
    def calcHistogram(self,bin_count):
        #print "calcHistogram : count=",bin_count
        self.histogram.setBinCount(bin_count)
        self.histogram.setSeries(self.series)
        self.histogram.doHistogram()
        self.histogram.dump()
    
    def getProbability(self,x):
        return self.histogram.getProbability(x)
    
    def calcStat(self):
        #step1 : calc avg, variance, std deviation
        #step2 : n(0,1) standardization, z=(x-avg)/stddev
        #step3 : calc standard score , z=(x-avg)/stddev
        #step4 : lookup probability table
        
        #self.buildData()
        self.calcAvg()
        self.calcVariance()
        self.calcMean()
        self.calcMedian()
        self.calcStandDeviation()

        
        
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
                        print "found"
                        return stat
        return None
    
        
class StatBuilder:
    def __init__(self):
        self.metric = ClusterNodes()
        self.metricBuilder = FileMetricDBBuilder()
        self.rrdfetcher = RRDDataFetcher()
        self.data = StatDataList()
        self.binCount = 10
        self.filter = None
        self.series = None
        
    def clearFilter(self):
        self.filter = None
    
    def setBinCount(self,bin_count):
        self.binCount = bin_count
        
    def setFilter(self,fields):
        self.filter = fields
        
    def buildMetric(self):
        self.metricBuilder.buildMetricInstance(self.metric,const.RRD_PATH,self.filter)
        self.metric.dump()
        
    def buildData(self,startTime,endTime):
        self.series = self.rrdfetcher.fetch(self.metric,startTime,endTime)
    
    def buildStatData(self):
        for series in self.series:
            statItem = StatData()
            statItem.setSeries(series)
            statItem.calcStat()
            statItem.calcHistogram(self.binCount)
            statItem.dump()
            self.data.addStatData(statItem)
        
        print "probability=",statItem.getProbability(740)
        
        #chart = StatChart()
        #chart.drawHistrogram(statItem, 10)
        #chart.drawNormalDistrobution(statItem)
        
            
    def build(self,startTime,endTime):
        self.buildMetric()
        self.buildData(startTime,endTime)
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
        self.builder = StatBuilder()


if __name__ == '__main__':
    
    mu = 0
    sigma = 0.1
    #s = np.random.normal(mu, sigma, 1000)
    #data = range(1,10)
    #print scipy.average(data)

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
    