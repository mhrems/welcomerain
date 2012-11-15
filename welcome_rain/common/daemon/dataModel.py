import os
import scipy
import math
from datetime import datetime,timedelta 



class BaseDataCollection:
    def __init__(self):
        self.items = []
        
    def clear(self):
        self.items = []
    
    def add(self,item):
        self.items.append(item)

    def getCount(self):
        return len(self.items)
    
    def find(self,name):
        for data in self.items:
            #print "find : key=",name
            if not data.name.find(name)==-1:
                return data
        return None


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
    
    def getProbabilityCount(self):
        return len(self.probability)
    
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
        if index>=self.getProbabilityCount():
            print "getProbability : Error, value=",x," has wrong index=",index
            return -1
        
        return self.probability[index]
    
    def dump(self):
        print "name=" , self.series.getFullName(), " , count=",self.count, " , binCount=",self.binCount," , binSize=",self.binSize
        print "numbers=",self.numbers
        print "bins=",self.bins
        print "probability=",self.probability


    
class StatDataModel:
    def __init__(self):
        #self.metric = None
        self.firstDate = 0
        self.lastDate = 0
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
        
    #def setMetric(self,metric):
    #    self.metric = metric
    
    def getCount(self):
        return len(self.series)
    
    def dump(self):
        print "StatData.dump : name=", self.series.getFullName() ," , count=", self.getCount() , " , avg=",self.avg, " , variance=",self.variance, " , stddev=",self.stddev
    
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
        #self.histogram.dump()
    
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

    def dump(self):
        print "StatDataModel : ", self.histogram.dump()
    


class ServerRawDataModel:
    def __init__(self):
        self.updated = 0
        self.rawData = 0
        self.probability = 0.0
    
    def dump(self):
        print "ServerRawDataModel : rawData=",self.rawData," , updated=",self.updated," , probability=",self.probability



class SummaryDataModel:
    def __init__(self):
        self.avg = 0.0
        self.min = 0.0
        self.max = 0.0
        self.rawData = 0.0
        
    def setData(self,avg,min,max,rawdata):
        self.avg = avg
        self.min = min
        self.max = max
        self.rawData = rawdata
        
        
        
class ServerDataSourceModel:
    def __init__(self,parent,name):
        self.gridName = ""
        self.clusterName = ""
        self.serverName = ""
        self.name = name
        self.normal = True
        self.unit = ""
        self.data = ServerRawDataModel()
        self.parent = parent
        self.stat = None
        
        #for summary Data
        self.summary = SummaryDataModel()
                
        self.setParentNames()
        
    def setParentNames(self):
        self.serverName = self.parent.name
        self.clusterName = self.parent.parent.name
        self.gridName = self.parent.parent.parent.name
        
    def setName(self,name):
        self.name = name
        
    def setData(self,data_source,value,unit=""):
        self.dataSource = data_source
        self.rawData = value
        self.unit = unit
    
    def calcMaxValue(self,value):
        if value>self.summary.max:
            self.summary.max = value

    def calcMinValue(self,value):
        if self.summary.min>value:
            self.summary.min = value

    def calcAvgValue(self,value):
        if self.summary.avg==0.0:
            self.summary.avg = value
            return
        
        self.summary.avg = (float(self.summary.avg)+float(value))/2
        
    def updateData(self,updated,value,unit=""):
        self.data.updated = updated
        self.data.rawData = value
        self.unit = unit 
        self.summary.rawData = value
        self.calcMinValue(value)
        self.calcMaxValue(value)
        self.calcAvgValue(value)
        
    
    def updateProbability(self,value):
        self.data.probability = value
    
    def updateStat(self,stat):
        self.stat = stat

    def isBadStatNow(self):
        probability = self.stat.getProbability(self.data.rawData)
        
        self.normal = False
        #if self.threshold>probability:
        #    self.normal = True
        #    return False
        
        return True
    
    def dump(self):
        print "> ServerDataSourceModel : name=",self.name , " , grid=",self.gridName," , cluster=", self.clusterName," , server=" , self.serverName , " , value=" , self.data.dump()
        if self.stat is None:
            print "ServerDataSourceModel : name=",self.name , " , grid=",self.gridName," , cluster=", self.clusterName," , server=" , self.serverName  
            return 
        
        print "stat : " , self.stat.dump()     
     
     
     
class ServerStatusDataModel:
    def __init__(self,name):
        self.name = name
        self.gridName = ""
        self.clusterName = ""
        self.serverName = ""
        self.running = True
        self.isStatOK = True
        self.isAlertOK = True
        
        self.cpu = SummaryDataModel()
        self.disk = SummaryDataModel()
        self.memory = SummaryDataModel()
        self.workload = SummaryDataModel()
        self.networkIn = SummaryDataModel()
        self.networkOut = SummaryDataModel()
        
        self.abnormalStat = BaseDataCollection()
        self.abnormalAlert = BaseDataCollection()
        self.abnormalStatCount = 0
        self.abnormalAlertCount = 0
        
    def clear(self):
        self.clearAbnormalStat()
        self.clearAbnormalAlert()
        
    def clearAbnormalStat(self):
        self.abnormalStat.clear()
        self.isStatOK = True
        self.abnormalStatCount = 0
        
    def addAbnormalStatDataSource(self,data_source):
        self.abnormalStat.add(data_source)
        self.isStatOK = False
        self.abnormalStatCount = self.abnormalStat.getCount()
        
    def clearAbnormalAlert(self):
        self.abnormalAlert.clear()
        self.isAlertOK = True
        self.abnormalAlertCount = 0
        
    def addAbnormalAlertDataSource(self,data_source):
        self.abnormalAlert.add(data_source)
        self.isAlertOK = False
        self.abnormalAlertCount = self.abnormalAlert.getCount()


class ServerDataModel:
    def __init__(self,parent,server_name):
        self.gridName = ""
        self.clusterName = ""
        self.parent = parent
        self.name = server_name
        self.reported = 0
        self.gmondStarted = 0
        self.lastUpdatedUTC = None
        self.lastUpdatedTime = None
        self.dataSource = BaseDataCollection()
        
        self.setNames()
        
        """
        self.dataSource = ""
        self.rawData = 0
        self.probability = 0.0
        self.normal = True
        """
    
    def setNames(self):
        self.gridName = self.parent.parent.name
        self.clusterName = self.parent.name
        
    def setName(self,server_name):
        self.name = server_name
                
    def setLastUpdatedTime(self,updated_time=None):
        if updated_time is None:
            updated_time = datetime.datetime.now()
            self.lastUpdatedTime = (updated_time.strftime("%Y:%m:%d:%H:%M:%S"))
        
        self.lastUpdatedUTC = updated_time
    
    def setReported(self,reported):
        self.reported = reported
    
    def setGmondStarted(self,started):
        self.gmondStarted = started
          
    def setProbability(self,value):
        self.probability = value
        
    def setRawData(self,data_source,data,updated=None):
        print "setRawData : data_source=",data_source, " , value=",data , " , updated=",updated
        dataSource = ServerDataSourceModel()
        dataSource.rawData = data
        dataSource.dataSource = data_source
        self.dataSources.addItem(dataSource)
        
        self.setLastUpdatedTime(updated)

    def createDataSource(self,datasource_name):
        #print "createDataSource : data=",datasource_name
        datasource = ServerDataSourceModel(self,datasource_name)
        return datasource
        
    def addDataSource(self,datasource_name):
        datasource = self.getDataSource(datasource_name)
        if datasource is None:
            datasource = self.createDataSource(datasource_name)
            self.dataSource.add(datasource)
        
        return datasource
    
    def getDataSource(self,datasource_name):
        return self.dataSource.find(datasource_name)
        
    def isRunning(self,now=0):
        if self.reported==0:
            return False
        if now==0:
            now = datetime.datetime.now()
        
        diff = now-self.reported
        if diff>const.SERVER_ALIVE_THRESHOLD:
            return False
        
        return True
    
    def getDataSourceValue(self,data_source):
        data = self.getDataSource(data_source)
        if data is None:
            return 0
        return data.rawData
    
    def dump(self):
        #print "ServerDataModel : cluster=",self.cluster," , host=",self.host," , data=",self.dataSource," , rawData=",self.rawData, " , probability=",self.probability
        print ">>> server=",self.name, "  , dataSource Count=",self.dataSource.getCount()
        for datasource in self.dataSource.items:
            datasource.dump() 
        


class ClusterDataModel:
    def __init__(self,parent,cluster_name):
        self.server = BaseDataCollection()
        self.name = cluster_name
        self.parent = parent
        self.gridName = ""
        
    def setName(self,cluster_name):
        self.name = cluster_name
    
    def createServer(self,server_name):
        server = ServerDataModel(self,server_name)
        return server
    
    def addServer(self,server_name):
        server = self.getServer(server_name)
        if server is None:
            server = self.createServer(server_name)
            self.server.add(server)
        
        return server
    
    def getServer(self,server_name):
        return self.server.find(server_name)
    
    def dump(self):
        for server in self.server.items:
            server.dump()



class GridDataModel:
    def __init__(self,grid_name):
        self.name = grid_name
        self.cluster = BaseDataCollection()
        
    def setName(self,grid_name):
        self.name = grid_name
        
    def clear(self):
        self.cluster = None
        self.cluster = BaseDataCollection()
    
    def createCluster(self,cluster_name):
        cluster = ClusterDataModel(self,cluster_name)
        return cluster
    
    def addCluster(self,cluster_name):
        cluster = self.getCluster(cluster_name)
        if cluster is None:
            cluster = self.createCluster(cluster_name)
            self.cluster.add(cluster)
        
        return cluster
    
    def getCluster(self,cluster_name):
        return self.cluster.find(cluster_name)

    def dump(self):
        for index,cluster in enumerate(self.cluster.items):
            print ">>>>> Index=",index," , Cluster=",cluster.name
            cluster.dump()



class BadStatModel(list):
    pass


class ServerDataManager(GridDataModel):
    def __init__(self,grid_name):
        GridDataModel.__init__(self, grid_name)
        #self.badStat = BaseDataCollection()
        #self.badAlert = BaseDataCollection()
        #self.goodStat = BaseDataCollection()
        self.serverSummary = BaseDataCollection() #ServerStatusDataModel()
        
    def setBadFilter(self,fields):
        self.badFilter = fields
        
    def getAbnormalStatCount(self):
        abnormal_count = 0
        for serverStatus in self.serverSummary.items:
            if not serverStatus.isStatOK:
                abnormal_count += 1    
        return abnormal_count
        
    def getAbnormalAlertCount(self):
        abnormal_count = 0
        for serverStatus in self.serverSummary.items:
            if not serverStatus.isAlertOK:
                abnormal_count += 1    
        return abnormal_count
    
    def addServerStatusData(self,serverStatus):
        #server = self.serverSummary.find(serverStatus.name)
        #if server is None:
        self.serverSummary.add(serverStatus)
        
    def addServerDateTime(self,cluster_name,server_name,reported,started):
        #print "ServerDataManager.addServerRawData : cluster=",cluster_name," , server=",server_name," , data=",datasource_name," , updated=",updated," , value=",raw_data
        cluster = self.addCluster(cluster_name)
        server = cluster.addServer(server_name)
        server.setReported(reported)
        server.setGmondStarted(started)
        
    def addServerRawData(self,cluster_name,server_name,datasource_name,updated,raw_data,unit=""):
        #print "ServerDataManager.addServerRawData : cluster=",cluster_name," , server=",server_name," , data=",datasource_name," , updated=",updated," , value=",raw_data
        cluster = self.addCluster(cluster_name)
        server = cluster.addServer(server_name)
        datasource = server.addDataSource(datasource_name)
        datasource.updateData(updated,raw_data,unit)

    def addServerStatData(self,statItem):
        #print "ServerDataManager.addServerRawData : cluster=",cluster_name," , server=",server_name," , data=",datasource_name," , updated=",updated," , value=",raw_data
        
        cluster = self.addCluster(statItem.series.cluster)
        server = cluster.addServer(statItem.series.host)
        datasource = server.addDataSource(statItem.series.dataSource)
        datasource.updateStat(statItem)
    
    def getServer(self,cluster_name,server_name):
        cluster = self.cluster.find(cluster_name)
        if cluster is None:
            print "error : cluster=",cluster_name," not found!!!"
            return None
        
        server = cluster.server.find(server_name)
        return server
    
        
"""
class ServerDataCollection:
    def __init__(self):
        self.items = []
        
    def clear(self):
        self.items = []
    
    def add(self,item):
        self.items.append(item)

    def getCount(self):
        return len(self.items)
    
    def get(self,cluster,host,data_source):
        pass
    
    def dump(self):
        for index,item in enumerate(self.items):
            print "index=", index," , cluster=",item.cluster," , host=",item.host," , data=",item.dataSource," , updatedTime=",item.lastUpdatedUTC," , value=",item.rawData

        print ">>> ServerRawDataManager.dump finished <<<"
        
class ServerDataSourceCollection:
    def __init__(self):
        self.items = []
    
    def addItem(self,item):
        self.items.append(item)
    
    def findItem(self,key):
        for data in self.items:
            if data.dataSource.lower().find(key)!=-1:
                return data
        return None
    
    def getCount(self):
        return len(self.items)
    
    def getDataSource(self,name):
        dataSource = self.findItem(name)
        return dataSource
    
    def getRawData(self,name):
        data = self.getDataSource(name)
        if data is None:
            return 0
        return data.rawData
"""
        

if __name__ == "__main__":
    print "hello"
    