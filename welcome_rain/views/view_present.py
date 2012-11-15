from datetime import datetime,timedelta 
 
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from welcome_rain.common.mhrlog import * 
from welcome_rain.common.const import *
from welcome_rain.common.models import *
from welcome_rain.common.summaryDataBuilder import *
from welcome_rain.common.chartDataBuilder import *
from welcome_rain.common.util import *

from welcome_rain.common.daemon.vDaemon import *


#from welcome_rain.common import fabricMhr

#from fabric.api import *


@login_required
def index(request):
    template = get_template('present.html')
    
    oUser = User.objects.get(id=request.user.id)
    
    oProfile = oUser.get_profile()
    oProfile.grahp_realtime_interval = 1000
    
    oProfile.save()
    
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
    
    #alerts = getAlertHistory(request)
    #graphData = getDashboardData()
    
    #logInfo(html)
    
    variables = RequestContext(request,{
        'title':'title',
        'availability':str(builder.getServerAvailability()),
        'disk':str(builder.getCurrentDiskUsage()),
        'cpu':str(builder.getCurrentCPU()),
        'data':builder.getData(),
        'metaData':builder.getDashboardMetric(),
        'stat':daemon.data.badStat,
        'grahp_realtime_interval':request.user.get_profile().grahp_realtime_interval
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
    
    #startTime = (now.strftime("%Y:%m:%d:%H:%M"))
    #endTime = (past.strftime("%Y:%m:%d:%H:%M"))

    startTime = (now.strftime("%Y:%m:%d:00:00"))
    endTime = (now.strftime("%Y:%m:%d:%H:%M"))
    
    result = {}
    builder = ChartDataBuilder()
    
    data1 = "load_fifteen"
    result[data1] = builder.fetchTodayData(data1+".rrd")

    data2 = "cpu_system"
    result[data2] = builder.fetchTodayData(data2+".rrd")

    data3 = "cpu_idle"
    result[data3] = builder.fetchTodayData(data3+".rrd")

    data4 = "bytes_in"
    result[data4] = builder.fetchTodayData(data4+".rrd")

    data5 = "bytes_out"
    result[data5] = builder.fetchTodayData(data5+".rrd")

    print "startTime:",startTime," , endTime:",endTime
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
