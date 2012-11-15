from datetime import datetime,timedelta 
 
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from welcome_rain.common.mhrlog import * 
from welcome_rain.common.const import *
from welcome_rain.common.models import *
from welcome_rain.common.summaryDataBuilder import *
from welcome_rain.common.chartDataBuilder import *
from welcome_rain.common.eventManager import *
from welcome_rain.common.util import *

from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from welcome_rain.common.daemon.vDaemon import *

#from welcome_rain.common import fabricMhr

#from fabric.api import *


@login_required
def index(request):
    template = get_template('dashboard.html')
    
    oUser = User.objects.get(id=request.user.id)
    
    #print oUser
    
    oProfile = oUser.get_profile()
    oProfile.grahp_realtime_interval = 1000
    
    oProfile.save()
    
    builder = MetaSummaryBuilder()
    builder.getGridSummaryData()
    #print data.toString()
    #builder.toString()
        
    alerts = getAlertHistory(request)
    
    graphData = getDashboardData()
    
    #logInfo(html)
    
    variables = RequestContext(request,{
        'title':'title',
        'current_temperature':str(builder.getCurrentTemperaturePercent()),
        'current_server_power':str(builder.getCurrentServerPowerPercent()),
        'current_rack_power':str(builder.getCurrentRackPowerPercent()),
        'data':builder.getData(),
        'metaData':builder.getDashboardMetric(),
        'graphData':graphData,
        'alerts':alerts,
        'grahp_realtime_interval':request.user.get_profile().grahp_realtime_interval
    })
    
    return HttpResponse(template.render(variables))


def index2(request):
    template = get_template('dashboard2.html')
    
    oUser = User.objects.get(id=request.user.id)
    
    #print oUser
    
    oProfile = oUser.get_profile()
    oProfile.grahp_realtime_interval = 1000
    
    oProfile.save()
    
    now = datetime.now()
    startTime = now.strftime("%Y:%m:%d 00:00")
    endTime = now.strftime("%Y:%m:%d %H:%M")
    
    
    builder = MetaSummaryBuilder()
    builder.getGridSummaryData()
    #print data.toString()
    #builder.toString()
        
    daemon = VDaemon()
    #daemon.setFilter(["cpu_system","cpu_user","load_fifteen","mem_free","bytes_in","bytes_out","proc_total","proc_run"])
    daemon.setFilter(["proc_total"])
    daemon.setBinCount(10)
    daemon.prepare()
    daemon.start()
    daemon.updateStat()
    daemon.updateData()
    daemon.doLoop()
    
    
    summaryData = SummaryDataBuilder()
    summaryData.setStat(daemon.stat)
    summaryData.setData(daemon.data)
    summaryData.buildDataForDashboard()
    
    
    
    #alerts = getAlertHistory(request)
    #graphData = getDashboardData()
    #logInfo(html)
    
    variables = RequestContext(request,{
        'title':'title',
        'cpu':str(summaryData.getBadCPUCount()),
        'memory':str(summaryData.getBadMemoryCount()),
        'disk':str(summaryData.getBadDiskCount()),
        'badCount':str(summaryData.getBadCount()),        
        'data':builder.getData(),
        'summaryData':summaryData.getServerSummaryData(),
        'metaData':builder.getDashboardMetric(),
        'startTime': startTime, 
        'endTime': endTime,
        'grahp_realtime_interval':request.user.get_profile().grahp_realtime_interval
    })
    
    return HttpResponse(template.render(variables))




def index3(request):
    def makeJSON(series_list,event_list):
        series_data = []
        for series in series_list:
            print "timestamps : start=" , series.start, " , end=",series.end, " , step=",series.step
            timestamps = range(series.start, series.end, series.step)
            print "timestamps : " , timestamps
            #datapoints = zip(timestamps,series)
            datapoints = map(dict, map(lambda t:zip(('x','y'),t), zip(timestamps,series)))
            series_data.append( dict(target=series.getFullName(), events=event_list, datapoints=datapoints) )

        return series_data

    template = get_template('dashboard3.html')
    
    oUser = User.objects.get(id=request.user.id)
    
    oProfile = oUser.get_profile()
    oProfile.grahp_realtime_interval = 1000
    oProfile.save()
    
    startTime, endTime = getTodayStartEndTime(type=1)
    
    
    meta = MetaSummaryBuilder()
    meta.getGridSummaryData()
    #print data.toString()
    #builder.toString()
            
    daemon = VDaemon()
    #daemon.setFilter(["cpu_system","cpu_user","load_fifteen","mem_free","bytes_in","bytes_out","proc_total","proc_run"])
    daemon.setFilter(["proc_total"])
    daemon.setBinCount(10)
    daemon.prepare()
    daemon.start()
    daemon.updateStat()
    daemon.updateData()
    daemon.doLoop()
    
    
    summaryData = SummaryDataBuilder()
    summaryData.setData(daemon.data)
    summaryData.buildDataForDashboard()
    

    
    chartBuilder = ChartDataBuilder()
    alertSeries = chartBuilder.fetchAlertHourlyData(request.user.id,"cluster","server",startTime,endTime)
    serverdownSeries = chartBuilder.fetchServerDownHourlyData(request.user.id,"cluster","server",startTime,endTime)

    #print alert_data

    events = EventManager()
    eventList = events.getEventDataForChart(request,alertSeries)
    #print "eventData=",eventData
    
    jsonResult = makeJSON(alertSeries,eventList)
    
    #print jsonResult
    
    #alerts = getAlertHistory(request)
    #graphData = getDashboardData()
    #logInfo(html)
    
    variables = RequestContext(request,{
        'title':'title',
        'total_server':str(meta.getTotalServerCount()),
        'total_cpu':str(meta.getTotalCPUCount()),
        'total_memory':str(meta.getTotalMemory()),
        'total_disk':str(meta.getTotalDisk()),
        'badCount':str(summaryData.getBadCount()),        
        'data':meta.getData(),
        'summaryData':summaryData.getServerSummaryData(),
        'metaData':meta.getDashboardMetric(),
        'startTime': startTime, 
        'endTime': endTime,
        'grahp_realtime_interval':request.user.get_profile().grahp_realtime_interval,
        'profile' : request.user.get_profile()
    })
    
    return HttpResponse(template.render(variables))


@csrf_exempt
def getAlertHistory(request):
    now = datetime.datetime.now()
    past = now - timedelta(hours=7)
    
    startTime = getDjangoStyleDateTime(now.strftime("%Y:%m:%d:%H:%M:%S"))
    endTime = getDjangoStyleDateTime(past.strftime("%Y:%m:%d:%H:%M:%S"))
    
    #print "time1=",startTime , " - time2=",endTime
            
    result = vo_AlertHistory.objects.select_related().filter(regdate__gte=startTime,regdate__lte=endTime,user=request.user)

    return result


def getDashboardData():
    now = datetime.datetime.now()
    past = now - timedelta(hours=1)
    
    startTime = (now.strftime("%Y:%m:%d:%H:%M"))
    endTime = (past.strftime("%Y:%m:%d:%H:%M"))
    
    result = {}
    builder = ChartDataBuilder()
    
    data1 = "load_fifteen"
    result[data1] = builder.fetchData(data1+".rrd",DASHBOARD_DATA_LIMIT)

    data2 = "cpu_system"
    result[data2] = builder.fetchData(data2+".rrd",DASHBOARD_DATA_LIMIT)

    data3 = "cpu_idle"
    result[data3] = builder.fetchData(data3+".rrd",DASHBOARD_DATA_LIMIT)

    data4 = "bytes_in"
    result[data4] = builder.fetchData(data4+".rrd",DASHBOARD_DATA_LIMIT)

    data5 = "bytes_out"
    result[data5] = builder.fetchData(data5+".rrd",DASHBOARD_DATA_LIMIT)

    #print "dashbaord : ",result[data1]
    
    return result


@csrf_exempt
@login_required
def addchart(request):
    template = get_template('addchart.html')
    
    variables = Context({
        'title':'title',
        
    })
    if(request.method == 'POST'):
        
        oChart = vo_Chart(
            uid = get_universally_unique_identifiers(),
            user = request.user,
            name = request.POST['name'],
            cluster = '',
            host = '',
            datasource = request.POST['datasource_sel'],
        )
        
        if(request.POST['check_cluster'] == 'true'):
            oChart.cluster = request.POST['cluster_sel']
        if(request.POST['check_host'] == 'true'):
            oChart.host = request.POST['host_sel']
        
        oChart.save()
        return redirect('/')
        
    return HttpResponse(template.render(variables))


import uuid
def get_universally_unique_identifiers():
    _generate_uuid = str(uuid.uuid4().hex)  
    return charShowWhereIsNumber(_generate_uuid,30)


def charShowWhereIsNumber(str,num):
    return str[:int(num)]
