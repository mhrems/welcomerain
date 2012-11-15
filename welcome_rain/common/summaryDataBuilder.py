from datetime import datetime,timedelta 

from const import *
from summaryModel import *
from gmetadReader import *
from rrdreader import *
from rrdDataFetcher import *

from daemon.dataModel import *


class BaseSummaryBuilder:
    def __init__(self):
        self.reader = GMetaReader()
        self.clear()
    
    def clear(self):
        self.data = {}
    
    def getData(self):
        return self.data
    
    def parseXML(self,nodes):
        for item in nodes.iter("HOSTS"):
            self.data.hostUp = item.attrib.get("UP")
            self.data.hostDown = item.attrib.get("DOWN")
        
        for item in nodes.iter("GRID"):
            self.data.name = item.attrib.get("NAME")
            datestr = datetime.datetime.fromtimestamp(int(item.attrib.get("LOCALTIME")))
            self.data.localTime = datestr.strftime("%Y-%m-%d %H:%M:%S")

    def parseHostUpDown(self,nodes):
        for item in nodes.iter("HOSTS"):
            self.data['hostUp'] = item.attrib.get("UP")
            self.data['hostDown'] = item.attrib.get("DOWN")
        
    def parseGrid(self,nodes):
        for item in nodes.iter("GRID"):
            self.data['name'] = item.attrib.get("NAME")
            datestr = datetime.fromtimestamp(int(item.attrib.get("LOCALTIME")))
            self.data['localTime'] = datestr.strftime("%Y-%m-%d %H:%M:%S")
    
    def parseMetric(self,xml,attr="SUM"):
        for metric in xml.iter("METRICS"):
            name = metric.get("NAME")
            value=metric.attrib.get(attr)
            #print "name=",name," , value=",value
            self.data[name] = float(value)
    
    def toString(self):
        for metric in self.data:
            print metric,self.data[metric]
            #self.summary[metric])
            #print ke 
            


class MetaSummaryBuilder(BaseSummaryBuilder):    
    def getFilteredSummary(self,filter):
        sum = 0.0
        for key,value in self.data.items():
            if key.find(filter)>-1:
                #print "key=",key," , value=",value
                sum += float(value) 
        
        return round(sum,0)
    
    def getPercent(self,max,value):
        percent = (float(value)/float(max))*100
        #print "getPercent : max=",max," , value=",value
        return round(percent)
    
    def getCurrentLoad(self):
        return self.data['load_fifteen']

    def getCurrentServerPower(self):
        value = self.getFilteredSummary(SERVER_POWER_RRD)
        #value2 = self.getPercent(300*100, value)
        #print "getCurrentServerPower : " , value
        return value
    
    def getCurrentRackPower(self):
        value = self.getFilteredSummary(RACK_POWER_RRD)
        #value2 = self.getPercent(1000*10, value)
        #print "getCurrentRackPower : " , value
        return value

    def getCurrentTemperature(self):
        value = self.getFilteredSummary(TEMPERATURE_RRD)
        #value2 = self.getPercent(100*10, value)
        #print "getCurrentTemperature : " , value
        return value

    def getCurrentServerPowerPercent(self):
        value = self.getPercent(250*100, self.getCurrentServerPower())
        #print "getCurrentServerPowerPercent : " , value
        return value

    def getCurrentRackPowerPercent(self):
        value = self.getPercent(1000*10, self.getCurrentRackPower())
        #print "getCurrentRackPower : " , value
        return value
    
    def getCurrentTemperaturePercent(self):
        value = self.getPercent(100*10, self.getCurrentTemperature())
        #print "getCurrentTemperaturePercent : " , value
        return value
    
    def getCurrentCPU(self):
        return int(self.data['cpu_system'])+int(self.data['cpu_user'])
    
    def getCurrentDiskUsage(self):
        used = int(self.data['disk_total']) - int(self.data['disk_free'])
        return self.getPercent(self.data['disk_total'],used)

    def getServerAvailability(self):
        total = int(self.data['hostUp']) + int(self.data['hostDown'])
        return self.getPercent(total,self.data['hostUp'])

    def getTotalCPUCount(self):
        return int(self.data['cpu_num'])
    
    def getTotalServerCount(self):
        total = int(self.data['hostUp']) + int(self.data['hostDown'])
        return total
    
    def getTotalMemory(self):
        return int(self.data['mem_total']/1024)
    
    def getTotalDisk(self):
        return int(self.data['disk_total'])
    
    def getTotalBytesIn(self):
        return self.data['bytes_in']
        
    def getTotalBytesOut(self):
        return self.data['bytes_out']

    def getCurrentMemory(self):
        mem_free = float(self.data['mem_free'])
        mem_total = float(self.data['mem_total'])
        mem = float(mem_free/mem_total)*100
        #print mem
        return round(mem,0)

    def getDashboardMetric(self):
        selected = ["bytes_out","bytes_in","load_fifteen","cpu_system"]
        result = {}
        for item in selected:
            result[item] = self.data[item]
        
        result['server_power'] = self.getCurrentServerPower()
        result['rack_power'] = round(self.getCurrentRackPower()*520/100,0)
        result['temperature'] = self.getCurrentTemperature()
        
        return result
            
    def makeData(self):
        xml,element = self.getGridSummaryData()
        #print xml
        self.parseMetric(element)
        #self.parseHostUpDown(xml)
        #self.parseGrid(xml)
        
        return self.data

    def getGridSummaryData(self):
        response,xml = self.reader.getGridSummary()
        self.parseMetric(xml)
        self.parseHostUpDown(xml)
        self.parseGrid(xml)

        return self.data
        
    def getClusterSummaryData(self,cluster):
        xml = self.reader.getClusterSummary(cluster)
        self.parseMetric(xml)
        return self.data
    




class ClusterSummaryBuilder:
    def __init__(self):
        self.data = MetaSummaryModel() 
        self.reader = GMetaReader()
    
    def parseXML(self,nodes):
        for item in nodes.iter("HOSTS"):
            self.data.hostUp = item.attrib.get("UP")
            self.data.hostDown = item.attrib.get("DOWN")
        
        for item in nodes.iter("GRID"):
            self.data.name = item.attrib.get("NAME")
            datestr = datetime.datetime.fromtimestamp(int(item.attrib.get("LOCALTIME")))
            self.data.localTime = datestr.strftime("%Y-%m-%d %H:%M:%S")
    
    
    def calcLoad(self):
        pass
    
    def makeData(self):
        xml = self.reader.getClusterSummary("mhr")
        #self.parseXML(xml)
        return self.data

    def getGridSummaryData(self):
        xml = self.reader.getGridSummary()
        self.parseXML(xml)
        return self.data
        
    def getClusterSummaryData(self,cluster):
        xml = self.reader.getClusterSummary(cluster)
        self.parseXML(xml)
        return self.data
    



class SummaryDataBuilder:
    def __init__(self):
        self.data = None
    
    def setData(self,rawdata):
        self.data = rawdata
    
    def filterBadData(self,fields):
        self.clearBad()
        
        fieldCount = len(fields)
        for index in range(fieldCount):
            self.bad[fields[index]] = []
        
        
        for server in self.data.rawData.items:
            server.normal = True
            for index in range(fieldCount):
                data_source = fields[index]
                statData = self.stat.stat.getHostStat(data_source,server.cluster,server.host)
                if not statData is None:
                    probability = statData.getProbability(server.rawData)
                    if probability>50:
                       self.bad[data_source].append(server)
                       server.normal = False
                    
            
        #for index in range(fieldCount):
        #    self.bad[fields[index]] = data[index]
        
    def buildData(self):
        statCount = 0
        self.data.clearBadStat()
        for index,cluster in enumerate(self.data.cluster.items):
            for index,server in enumerate(cluster.server.items):
                for index,dataSource in enumerate(server.dataSource.items):
                    #if self.alert.check(server):
                    #    alertCount += 1
                    #    print "VDaemon.doLoop : alert fired , " , server
                
                    #if not self.isServerInstance(server):
                    #    continue
                    #print dataSource
                    if dataSource.isBadStatNow():
                        self.data.addBadStat(server)
                        print "VDaemon.doLoop : stat fired , " , dataSource.dump()
                
                #server.dump()
            #print "doLoop : index=",index," , server=",server.dump()
        
        print "summaryDataBuilder.buildData Finished : stat_count=",self.data.getBadStatCount()

        
    def getBadCPUCount(self):
        over_threshold_count = 0
        for server in self.data.serverSummary.items:
            if server.cpu.rawData>const.CPU_THRESHOLD:
                over_threshold_count += 1        
        return over_threshold_count
    
    def getBadMemoryCount(self):
        over_threshold_count = 0
        for server in self.data.serverSummary.items:
            if server.memory.rawData>const.MEMORY_THRESHOLD:
                over_threshold_count += 1        
        return over_threshold_count

    def getBadDiskCount(self):
        over_threshold_count = 0
        for server in self.data.serverSummary.items:
            if server.disk.rawData>const.DISK_THRESHOLD:
                over_threshold_count += 1        
        return over_threshold_count

    def getBadCount(self):       
        return self.data.getAbnormalStatCount()
    
    def getServerData(self):
        return self.data.cluster.items

    def getTotalCPUCount(self):
        return 1
        
    def getServerSummaryData(self):
        return self.data.serverSummary
    
    def buildServerStatusData(self):
        result = []
        for index,cluster in enumerate(self.data.cluster.items):
            for index,server in enumerate(cluster.server.items):
                for index,dataSource in enumerate(server.dataSource.items):
                    #if self.alert.check(server):
                    #    alertCount += 1
                    #    print "VDaemon.doLoop : alert fired , " , server
                
                    #if not self.isServerInstance(server):
                    #    continue
                    #print dataSource
                    if dataSource.isBadStatNow():
                        self.data.addBadStat(server)
                        print "VDaemon.doLoop : stat fired , " , dataSource.dump()
        
        
    def buildDataForDashboard(self):
        fields = [const.METRIC_CPU,const.METRIC_DISK,const.METRIC_MEMORY]
        #self.filterBadData(fields)
    
    
    
    

if __name__ == "__main__":
    builder = MetaSummaryBuilder()
    data = builder.getGridSummaryData()
    #print data
    #builder.toString()
    #print builder.getCurrentMemory()
    
    #builder2 = ClusterSummaryBuilder()
    #data = builder2.makeData()
    #print data.toString()
    
    #builder = DashboardDataBuilder()
    #builder.fetchData("cpu")
    