from datetime import datetime,timedelta 

from const import *
from summaryModel import *
from gmetadReader import *
from rrdreader import *
from rrdDataFetcher import *
from models import *
from timeseries import *



class ChartDataBuilder:
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


    def makeTimeSeriesData(self,cluster,server,items):
        """
        results = reader.fetch(startTime,endTime)
        pprint.pprint(results)
        print "result_count = " , len(results)

        (timeInfo, values) = results
        (start, end, step) = timeInfo

        series = TimeSeries(query.host, start, end, step, values)
        series.pathExpression = rrdFile #hack to pass expressions through to render functions
        seriesList.append(series)

        (timeInfo, columns, rows) = rrdtool.fetch(cmdString)
        #(timeInfo, columns, rows) = rrdtool.fetch(self.datafile_name,'AVERAGE','-s ' + str(startTime),'-e ' + str(endTime))
        colIndex = list(columns).index(rrdfield)
        rows.pop() #chop off the latest value because RRD returns crazy last values sometimes
        
        #values = (str(row[colIndex]) for row in rows)
    
        values = []
        for row in rows:
            value = row[colIndex]
            if value is None:
                values.append(0)
            else:
                values.append(value)
    
        #print "rows_count=",len(rows) 
    
        #print timeInfo
        #print columns
        #log("rows", rows)
        #log("values",values)
    
        #results = rrdtool.fetch(rrdfile,'AVERAGE','-s ' + str(startTime),'-e ' + str(endTime))
        
        return (timeInfo, values)

        """
        start = 0
        end = len(items)
        step = 1
        values = []
        for key,value in items.iteritems():
            values.append(value)
            
        name = cluster+","+server+",alert"
        series = TimeSeries(name, start, end, step, values)
        #for key,value in items:
        return series
        

    def fetchServerDownHourlyData(self,user_id,cluster,server,startTime,endTime):
        startTimeToken = startTime.split(":")
        endTimeToken = endTime.split(":")
            
        sql = "select id,hour,count(id) as total from common_vo_serverdown"
        #sql += " where user_id="+str(user_id)
        sql += " where year="+startTimeToken[0]+" and month=" + startTimeToken[1] + " and day="+startTimeToken[2]
        sql += " group by hour"
    
        max_hour = int(endTimeToken[3])+1
        items = {}
        for hour in range(max_hour):
            print "hour=",hour
            items[hour] = 0
            
        result = vo_ServerDown.objects.raw(sql)
        for item in result:
            print "hour=",item.hour," , count=",item.total
            items[item.hour] = item.total
        
        #result = vo_AlertHistory.objects.select_related().filter(user=request.user,year=startTimeToken[0],month=startTimeToken[1],day=startTimeToken[2])
    
        print items
        
        series = self.makeTimeSeriesData(cluster,server,items)
        seriesList = []
        seriesList.append(series)
        
        #print series
        
        return seriesList
    
    
    def fetchAbnormalStatHourlyData(self,user_id,cluster,server,startTime,endTime):
        startTimeToken = startTime.split(":")
        endTimeToken = endTime.split(":")
            
        sql = "select id,hour,count(id) as total from common_vo_abnormalstat"
        #sql += " where user_id="+str(user_id)
        sql += " where year="+startTimeToken[0]+" and month=" + startTimeToken[1] + " and day="+startTimeToken[2]
        sql += " group by hour"
    
        max_hour = int(endTimeToken[3])+1
        items = {}
        for hour in range(max_hour):
            print "hour=",hour
            items[hour] = 0
            
        result = vo_ServerDown.objects.raw(sql)
        for item in result:
            print "hour=",item.hour," , count=",item.total
            items[item.hour] = item.total
        
        #result = vo_AlertHistory.objects.select_related().filter(user=request.user,year=startTimeToken[0],month=startTimeToken[1],day=startTimeToken[2])
    
        print items
        
        series = self.makeTimeSeriesData(cluster,server,items)
        seriesList = []
        seriesList.append(series)
        
        #print series
        
        return seriesList

    def fetchAlertHourlyData(self,user_id,cluster,server,startTime,endTime):
        startTimeToken = startTime.split(":")
        endTimeToken = endTime.split(":")
            
        sql = "select id,hour,count(alert_id) as total from common_vo_alerthistory"
        sql += " where user_id="+str(user_id)
        sql += " and year="+startTimeToken[0]+" and month=" + startTimeToken[1] + " and day="+startTimeToken[2]
        sql += " group by hour"
    
        max_hour = int(endTimeToken[3])+1
        items = {}
        for hour in range(max_hour):
            print "hour=",hour
            items[hour] = 0
            
        result = vo_AlertHistory.objects.raw(sql)
        for item in result:
            print "hour=",item.hour," , count=",item.total
            items[item.hour] = item.total
        
        #result = vo_AlertHistory.objects.select_related().filter(user=request.user,year=startTimeToken[0],month=startTimeToken[1],day=startTimeToken[2])
    
        print items
        
        series = self.makeTimeSeriesData(cluster,server,items)
        seriesList = []
        seriesList.append(series)
        
        #print series
        
        return seriesList
    
    
    def fetchTodayData(self,target):
        now = datetime.now()

        startTime = (now.strftime("%Y:%m:%d:00:00"))
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
    
    
    
    