import os
import pickle

from dataModel import *
from dataUpdater import *
from alertManager import *
from apiHandler import *
from statManager import *
from gmetadDataCollector import *


class VDaemon:
    def __init__(self):
        self.data = ServerDataManager("None")
        self.metricBuilder = MetaDataBuilder()
        self.rrd = DataUpdater()
        self.alert = AlertManager()
        self.stat = StatManager()
        self.api = DaemonAPIHandler()
        self.gmetad = GMetadDataCollector()
        self.filter = None
        self.criticalFilter = None
        
    def setFilter(self,filter):
        self.filter = filter

    def setCriticalFilter(self,filter):
        self.criticalFilter = filter
        
    def clearFilter(self):
        self.filter = None

    def setBinCount(self,bin_count):
        self.stat.setBinCount(bin_count)
        
    def prepare(self):
        self.updateMetric()
        self.rrd.setData(self.data)
        self.stat.setDataManager(self.data)
        self.gmetad.setData(self.data)
        
        
    def start(self):
        pass
    
    def updateMetric(self):
        self.metricBuilder.buildMetric(self.filter)
        #self.metricBuilder.dump()
        self.rrd.setMetric(self.metricBuilder.metric)
        self.stat.setMetric(self.metricBuilder.metric)
        
        
    def updateData(self):
        self.rrd.fetchLastData()
        self.rrd.updateServerData()
        print "VDaeMon.updateData Finished"
        
    def updateStat(self):
        self.stat.buildStatData()
        print "VDaeMon.updateStat Finished"
    
    def isServerInstance(self,server):
        if server.cluster==const.NONE_NODE and server.host==const.NONE_NODE:
            return False
        
        if server.host==const.SUMMARY_NODE:
            return False
    
        return True
    
    def createServerStatus(self,server):
        name = server.clusterName+","+server.name
        serverStatus = ServerStatusDataModel(name)
        serverStatus.gridName = server.gridName
        serverStatus.clusterName = server.clusterName
        serverStatus.name = server.name
        return serverStatus
    
    def updateServerStatus(self,server):
        """
        self.name = name
        self.gridName = ""
        self.cluserName = ""
        self.serverName = ""
        self.running = True
        self.cpu = SummaryDataModel()
        self.disk = SummaryDataModel()
        self.memory = SummaryDataModel()
        self.workload = SummaryDataModel()

        """
        print "updateServerStatus : cluster=", server.clusterName, " , server_name=",server.name
        
        name = server.clusterName+","+server.name

        serverStatus = self.data.serverSummary.find(name)
        if serverStatus is None:  
            serverStatus = self.createServerStatus(server)
            self.data.addServerStatusData(serverStatus)
                
        serverStatus.clear()
        serverStatus.running = True
        
        for dataSource in server.dataSource.items:
            if not dataSource.name.find(const.METRIC_CPU)==-1:
                serverStatus.cpu = dataSource.summary
            if not dataSource.name.find(const.METRIC_MEMORY)==-1:
                serverStatus.memory = dataSource.summary
            if not dataSource.name.find(const.METRIC_DISK)==-1:
                serverStatus.disk = dataSource.summary
            if not dataSource.name.find(const.METRIC_NETWORK_IN)==-1:
                serverStatus.networkIn = dataSource.summary
            if not dataSource.name.find(const.METRIC_NETWORK_OUT)==-1:
                serverStatus.networkOut = dataSource.summary
            if not dataSource.name.find(const.METRIC_WORKLOAD)==-1:
                serverStatus.workload = dataSource.summary
            
        
        return serverStatus
    
    def updateGmetadData(self):
        self.gmetad.collectData()
        
    def doLoop(self):
        statCount = 0
        
        for index,cluster in enumerate(self.data.cluster.items):
            for index,server in enumerate(cluster.server.items):
                
                serverStatus = self.updateServerStatus(server)

                for index,dataSource in enumerate(server.dataSource.items):
                    #if self.alert.check(server):
                    #    alertCount += 1
                    #    print "VDaemon.doLoop : alert fired , " , server
                
                    #if not self.isServerInstance(server):
                    #    continue
                    #print dataSource
                    if dataSource.isBadStatNow():
                        serverStatus.addAbnormalStatDataSource(dataSource)
                        #print "VDaemon.doLoop : stat fired , " , dataSource.dump()
                    
                    
                    #self.data.goodStat.add(dataSource)
                    
                #server.dump()
            #print "doLoop : index=",index," , server=",server.dump()
        
        print "VDaeMon.doLoop Finished : stat_count=",self.data.getAbnormalStatCount()
    



if __name__ == "__main__":
    
    daemon = VDaemon()
    #daemon.setFilter(["cpu_system","cpu_user","load_fifteen","mem_free","bytes_in","bytes_out","proc_total","proc_run"])
    daemon.setFilter(["proc_total"])
    daemon.setBinCount(10)
    daemon.prepare()
    daemon.start()
    daemon.updateStat()
    daemon.updateData()
    daemon.updateGmetadData()
    #daemon.data.dump()
    #daemon.doLoop()
    
    