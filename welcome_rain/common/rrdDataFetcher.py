import os
import time
import datetime
import rrdtool

"""
from welcome_rain.common.const import *
from welcome_rain.common.timeseries import *
from welcome_rain.common.monitoringNode import * 
from welcome_rain.common.mhrlog import * 
from welcome_rain.common.rrdreader import *
"""

from const import *
from timeseries import *
from monitoringNode import * 
from mhrlog import * 
from rrdreader import *


class RRDDataFetcher:
    def __init__(self):
        self.reader = RRDReader()

    def getGridSummaryRRD(self,source):
        rrd_path = const.RRD_PATH
        summary_name = const.SUMMARY_NODE
        rrd_file_path = rrd_path + "/" + summary_name + "/" + source
        return rrd_file_path

    def getClusterSummaryRRD(self,cluster,source):
        rrd_path = const.RRD_PATH
        summary_name = const.SUMMARY_NODE
        rrd_file_path = rrd_path + "/" + cluster + "/" + summary_name + "/" + source
        return rrd_file_path
    
    def getHostRRD(self,cluster,host,source):
        rrd_path = const.RRD_PATH
        rrd_file_path = rrd_path + "/" + cluster + "/" + host + "/" + source
        return rrd_file_path
    
    def getRRDFileName(self,cluster,host,source):
        rrdfile = ""
        if cluster=="None" and host=="None":
            rrdfile = self.getGridSummaryRRD(source)
        elif host==const.SUMMARY_NODE:
            rrdfile = self.getClusterSummaryRRD(cluster,source)
        else:
            rrdfile = self.getHostRRD(cluster,host,source)
            
        return rrdfile
        
        
    def getRRD(self,query):
        rrdpath = const.RRD_PATH #"/home/james/Workspace/Project/MHRCloud/graphite-web/rrds/"    
        summaryPath = const.SUMMARY_NODE #"__SummaryInfo__"
    
        #    if query.grid:
        #        filepath = filepath + query.grid
        
        if query.cluster:
            filepath = filepath + query.cluster
        else: 
            filepath = filepath + summaryPath + "/" + query.dataSource + const.RRDFILE_EXT
 
        if query.host:
            filepath = filepath + "/" + query.host + "/" + query.dataSource + const.RRDFILE_EXT
    
        return filepath
    
    
    def oldfetch(self,query):
        seriesList = []
        startTime = int( time.mktime(query.startTime) )
        endTime   = int( time.mktime(query.endTime) )
        
        rrdFile = self.getRRD(query)
        reader = RRDReader(rrdFile,"sum")
        #log("rrdinfo",reader.getInfo(rrdFile))    
        results = reader.fetch(startTime,endTime)
        pprint.pprint(results)
        print "result_count = " , len(results)

        (timeInfo, values) = results
        (start, end, step) = timeInfo

        series = TimeSeries(query.host, start, end, step, values)
        series.pathExpression = rrdFile #hack to pass expressions through to render functions
        seriesList.append(series)
        
        return seriesList

    #    matching_nodes = STORE.find(pathExpr, startTime, endTime, local=requestContext['localOnly'])
    #    fetches = [(node, node.fetch(startTime, endTime)) for node in matching_nodes if node.is_leaf]
    """
    for node, results in fetches:
        if isinstance(results, FetchInProgress):
            results = results.waitForResults()

        if not results:
            log.info("render.datalib.fetchData :: no results for %s.fetch(%s, %s)" % (node, startTime, endTime))
            continue

    (timeInfo, values) = results
    (start, end, step) = timeInfo

    series = TimeSeries(node.path, start, end, step, values)
    series.pathExpression = pathExpr #hack to pass expressions through to render functions
    seriesList.append(series)

    # Prune empty series with duplicate metric paths to avoid showing empty graph elements for old whisper data
    names = set([ series.name for series in seriesList ])
    for name in names:
        series_with_duplicate_names = [ series for series in seriesList if series.name == name ]
        empty_duplicates = [ series for series in series_with_duplicate_names if not nonempty(series) ]

        if series_with_duplicate_names == empty_duplicates and len(empty_duplicates) > 0: # if they're all empty
            empty_duplicates.pop() # make sure we leave one in seriesList

        for series in empty_duplicates:
            seriesList.remove(series)

    return seriesList
    """

   
    def fetchData(self,request):
        seriesList = []
        startTime = int( time.mktime( requestContext['startTime'].timetuple() ) )
        endTime   = int( time.mktime( requestContext['endTime'].timetuple() ) )

        matching_nodes = STORE.find(pathExpr, startTime, endTime, local=requestContext['localOnly'])
        fetches = [(node, node.fetch(startTime, endTime)) for node in matching_nodes if node.is_leaf]

        for node, results in fetches:
            if isinstance(results, FetchInProgress):
                results = results.waitForResults()

            if not results:
                log.info("render.datalib.fetchData :: no results for %s.fetch(%s, %s)" % (node, startTime, endTime))
                continue

        (timeInfo, values) = results
        (start, end, step) = timeInfo

        series = TimeSeries(node.path, start, end, step, values)
        series.pathExpression = pathExpr #hack to pass expressions through to render functions
        seriesList.append(series)

        # Prune empty series with duplicate metric paths to avoid showing empty graph elements for old whisper data
        names = set([ series.name for series in seriesList ])
        for name in names:
            series_with_duplicate_names = [ series for series in seriesList if series.name == name ]
            empty_duplicates = [ series for series in series_with_duplicate_names if not nonempty(series) ]

            if series_with_duplicate_names == empty_duplicates and len(empty_duplicates) > 0: # if they're all empty
                empty_duplicates.pop() # make sure we leave one in seriesList

            for series in empty_duplicates:
                seriesList.remove(series)

        return seriesList


    def addResultToSeriesList(self,seriesList,results,rrdfile,name):
        if not results:
            return
        
        firstDate = self.reader.getFirstDate(rrdfile)
        lastDate = self.reader.getLastDate(rrdfile)
        
        (timeInfo, values) = results
        (start, end, step) = timeInfo
        
        series = TimeSeries(name, start, end, step, values)
        series.pathExpression = rrdfile #hack to pass expressions through to render functions
        series.setFirstDate(firstDate)
        series.setLastDate(lastDate)
        
        seriesList.append(series)
        
    def convertStringToDateTime(self,str):
        #startTime = int( time.mktime( requestContext['startTime'].timetuple() ) )
        #endTime   = int( time.mktime( requestContext['endTime'].timetuple() ) )
        curtime =  datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        newstr = str+":00"
        d = datetime.strptime(newstr, "%Y:%m:%d:%H:%M:%S")
        ret = time.mktime(d.timetuple())
        #print "convertStringToDateTime : local=",curtime," , str=",newstr," , ",ret
        return ret

    def isGridSummary(self,cluster):
        if cluster.name==const.SUMMARY_NODE:
            return True
        return False

    def isHostSummary(self,host):
        if host.name==const.SUMMARY_NODE:
            return True
        return False
    
    
    def fetch(self,metric,start,end):
        seriesList = []
        startTime = int( self.convertStringToDateTime(start) )
        endTime   = int( self.convertStringToDateTime(end) )

        #print "rrdfetcher.fetch : start=",start," > " , startTime," , end=",end," > " , endTime
        #logInfo("rrddatafetcher.fetch : "+name+" , rrdfile="+rrdfile)       
        #reader = RRDReader()

        for cluster in metric:
            
            isGridSummary = False
            if self.isGridSummary(cluster):
                isGridSummary = True
  
            for data in cluster.dataSources:
                if isGridSummary:
                    results,name,rrdfile =self.fetchGridSummaryData(data,startTime,endTime)
                else:
                    results,name,rrdfile =self.fetchClusterSummaryData(cluster,data,startTime,endTime)

                self.addResultToSeriesList(seriesList,results,rrdfile,name)
                
            for host in cluster.hosts:
                for data in host.dataSources:
                    results,name,rrdfile = self.fetchHostData(cluster,host,data,startTime,endTime)
                    self.addResultToSeriesList(seriesList,results,rrdfile,name)

        return seriesList

    def fetchLastData(self,metric):
        dataList = []
        for cluster in metric:            
            isGridSummary = False
            if self.isGridSummary(cluster):
                isGridSummary = True
  
            for data in cluster.dataSources:
                if isGridSummary:
                    results,name,rrdfile =self.fetchLastRawData("None","None",data.name)
                else:
                    results,name,rrdfile =self.fetchLastRawData(cluster.name,const.SUMMARY_NODE,data.name)

                dataList.append([results,rrdfile,name])
                
            for host in cluster.hosts:
                for data in host.dataSources:
                    results,name,rrdfile = self.fetchLastRawData(cluster.name,host.name,data.name)

                    dataList.append([results,rrdfile,name])
        
        return dataList
        
    
    def fetchRawData2(self,source,startTime,endTime):

        seriesList = []
        startTime = int( self.convertStringToDateTime(startTime) )
        endTime   = int( self.convertStringToDateTime(endTime) )
        
        #reader = RRDReader()

        for cluster in metric:
            
            isGridSummary = False
            if self.isGridSummary(cluster):
                isGridSummary = True
  
            for data in cluster.dataSources:
                if isGridSummary:
                    results,name,rrdfile =self.fetchLastRawData("None","None",startTime,endTime)
                else:
                    results,name,rrdfile =self.fetchClusterSummaryData(self.reader,cluster,data,startTime,endTime)
                self.addResultToSeriesList(seriesList,results,rrdfile,name)
                
            for host in cluster.hosts:
                for data in host.dataSources:
                    results,name,rrdfile = self.fetchHostData(cluster,host,data,startTime,endTime)
                    self.addResultToSeriesList(seriesList,results,rrdfile,name)

        return seriesList


    def fetchRawData(self,cluster,server,data,startTime,endTime):
        startTime = int( self.convertStringToDateTime(startTime) )
        endTime   = int( self.convertStringToDateTime(endTime) )

        rrdfile = self.getRRDFileName(cluster,server,data)
        rrdfield = const.DEFAULT_DATA_FIELD

        logInfo("rrddatafetcher.fetchRawData : "+" , rrdfile="+rrdfile)
                
        results = self.reader.fetch(rrdfile,rrdfield,startTime,endTime)
        
        name = data        
        #rrdfield = const.DEFAULT_DATA_FIELD
        #results = self.reader.fetch(rrdfile,rrdfield,startTime,endTime)
        #results,name,rrdfile = self.fetchHostData(cluster,server,data,startTime,endTime)
        #name = "datasource="+dataSource

        return results,name,rrdfile

    def fetchSummaryRawData(self,dataSource,startTime,endTime):
        startTime = int( self.convertStringToDateTime(startTime) )
        endTime   = int( self.convertStringToDateTime(endTime) )
        
        rrdfile = self.getGridSummaryRRD(dataSource)
        rrdfield = const.DEFAULT_DATA_FIELD
        results = self.reader.fetch(rrdfile,rrdfield,startTime,endTime)
        name = "datasource="+dataSource
        #logInfo("rrddatafetcher.fetchRawData : "+name+" , rrdfile="+rrdfile)
        return results,name,rrdfile

    def fetchGridSummaryData(self,data,startTime,endTime):
        rrdfile = self.getGridSummaryRRD(data.name)                
        rrdfield = const.DEFAULT_DATA_FIELD
        results = self.reader.fetch(rrdfile,rrdfield,startTime,endTime)
        #name = "cluster=None, host=None, datasource="+data.name
        name = "None,None,"+data.name
        #logInfo("rrddatafetcher.fetchGridSummaryData : "+name+" , rrdfile="+rrdfile)
        return results,name,rrdfile
    
    def fetchClusterSummaryData(self,cluster,data,startTime,endTime):
        rrdfile = self.getClusterSummaryRRD(cluster.name,data.name)                
        rrdfield = const.DEFAULT_DATA_FIELD
        results = self.reader.fetch(rrdfile,rrdfield,startTime,endTime)
        #name = "cluster="+cluster.name+", host=None, datasource="+data.name
        name = cluster.name+",None,"+data.name
        #logInfo("rrddatafetcher.fetchClusterSummaryData : "+name+" , rrdfile="+rrdfile)
        return results,name,rrdfile
    
    def fetchHostData(self,cluster,host,data,startTime,endTime):
        rrdfile = self.getHostRRD(cluster.name,host.name,data.name)
        rrdfield = const.DEFAULT_DATA_FIELD
        results = self.reader.fetch(rrdfile,rrdfield,startTime,endTime)
        #name = "cluster="+cluster.name+" , host=" + host.name+" , datasource="+data.name
        name = cluster.name+"," + host.name+","+data.name
        #logInfo("rrddatafetcher.fetchHostData : " +name +" , rrdfile="+rrdfile)
        return results,name,rrdfile
    
    
    def fetchLastRawData(self,cluster,host,data):
        rrdfile = self.getRRDFileName(cluster,host,data)
        rrdfield = const.DEFAULT_DATA_FIELD
        results = self.reader.fetchLastData(rrdfile,rrdfield)
        #name = "cluster="+cluster.name+" , host=" + host.name+" , datasource="+data.name
        #print "fetchLastRawData : results=",results 
        name = cluster+"," + host+","+data
        #logInfo("fetchLastRawData.fetchHostData : " +name +" , rrdfile="+rrdfile)
        return results,name,rrdfile
    