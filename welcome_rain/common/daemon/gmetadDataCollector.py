import os
import math
from datetime import datetime,timedelta 

from dataModel import *

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from const import *
from metricDBBuilder import *
from monitoringNode import *
from timeseries import *
from gmetadReader import *
from util import *


class GMetadDataCollector:
    def __init__(self):
        self.gmetadReader = GMetaReader()
        self.data = None
    
    def setData(self,data):
        self.data = data

    def parseXML2(self,nodes):
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
        #<GRID NAME="unspecified" AUTHORITY="http://ems/ganglia/" LOCALTIME="1351852315">
        for item in nodes.iter("GRID"):
            grid_name = item.attrib.get("NAME")
            datestr = datetime.datetime.fromtimestamp(int(item.attrib.get("LOCALTIME")))
            local_time = datestr.strftime("%Y-%m-%d %H:%M:%S")
        
        print "parseGrid : name=",grid_name," , time=",local_time
        return grid_name,local_time
    
    def parseCluster(self,nodes):
        #<CLUSTER NAME="green" LOCALTIME="1350523475" OWNER="unspecified" LATLONG="unspecified" URL="unspecified">
        for item in nodes.iter("CLUSTER"):
            cluster_name = item.attrib.get("NAME")
            datestr = datetime.datetime.fromtimestamp(int(item.attrib.get("LOCALTIME")))
            local_time = datestr.strftime("%Y-%m-%d %H:%M:%S")

        print "parseCluster : name=",cluster_name," , time=",local_time
        return cluster_name,local_time

    def parseServer(self,grid_name,cluster_name,item):
        #<HOST NAME="192.168.0.247" IP="192.168.0.247" REPORTED="1350523473" TN="1328831" TMAX="20" DMAX="0" LOCATION="unspecified" GMOND_STARTED="1350332829">
        server_name = item.attrib.get("NAME")
        server_ip = item.attrib.get("IP")
        server_reported = item.attrib.get("REPORTED")
        datestr = datetime.datetime.fromtimestamp(int(item.attrib.get("GMOND_STARTED")))
        gmond_started = datestr.strftime("%Y-%m-%d %H:%M:%S")
            
        print "parseServer : name=",server_name," , ip=",server_ip," , reported=",server_reported
            
        self.parseMetric(grid_name,cluster_name,server_ip,server_reported,item)
    
    def parseMetric(self,grid_name,cluster_name,server_name,local_time,xml,attr="VAL"):
        for metric in xml.findall("METRIC"):
            name = metric.get("NAME")
            value = metric.attrib.get(attr)
            type = metric.get("TYPE")
            unit = metric.get("UNITS")            
            print "parseMetric : cluster=", cluster_name, " , server=" , server_name, " , datasource=",name," , value=",value, " , type=",type, " unit=",unit
            if self.isNumericValue(type):
                #print "updateServerData"
                self.updateServerDataSource(cluster_name,server_name, name+".rrd",local_time,value,unit)
    
    def parseClusterXML(self,xml):
        grid_name , grid_local_time = self.parseGrid(xml)
        cluster_name , cluster_local_time = self.parseCluster(xml)
        for server in xml.iter('HOST'):
            self.parseServer(grid_name,cluster_name,server)
   
    def isNumericValue(self,type):
        if type.strip()=="string":
            #print "isNumericValue : ",type
            return False
        return True
    
    def updateServerDateTime(self,cluster, server, reported, started):
        #print "updateServerData : data=",dataSource
        self.data.addServerDateTime(cluster, server, reported, started)      
    
    def updateServerDataSource(self,cluster, server, dataSource,updated,value,unit):
        #print "updateServerData : data=",dataSource
        self.data.addServerRawData(cluster, server, dataSource,updated,value,unit)      
        
    def collectClusterData(self,cluster_name):
        response,xml = self.gmetadReader.getClusterRawData(cluster_name)
        return response, xml
    
    def collectData(self):
        for cluster in self.data.cluster.items:
            print "GMetadDataCollector.collectData : cluster=",cluster.name
            if not cluster.name=="None":
                response,xml = self.collectClusterData(cluster.name)
                #print response
                self.parseClusterXML(xml)
                
        
if __name__ == "__main__":
    print "test-start"
    reader = GMetadDataCollector()
 
    