import json

from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers

from welcome_rain.common.monitoringNode import * 
from welcome_rain.common.metricDBBuilder import *
from welcome_rain.common.rrdDataFetcher import *
from welcome_rain.common.mhrlog import * 
from welcome_rain.common.models import *
from welcome_rain.common.jsonResponseBuilder import *
from welcome_rain.common.const import *
from welcome_rain.common.util import *
from welcome_rain.common.objectPaginator import *
from welcome_rain.common.confFile import *
from welcome_rain.common.eventManager import *
from welcome_rain.pyExcelerator import *
from welcome_rain.common.userConfig import *
from welcome_rain.common.chartDataBuilder import *
from welcome_rain.common.eventManager import *

from django.views.decorators.csrf import csrf_exempt

#import datetime
import os



def index(request):
    return HttpResponse("index")

@csrf_exempt
def downloadxls(request):
    wb = Workbook()
    ws0 = wb.add_sheet('0')
    x = 0
    
    chartData = request.GET['data'].strip()
    chartTitle = request.GET['title'].strip()
    ws0.write(x,0,"timestemp")
    ws0.write(x,1,"value")
    
    
    for data in chartData.split('|'):
        x = x + 1
        time = data.split('=')[0]
        value = data.split('=')[1]
        ws0.write(x,0,time)
        ws0.write(x,1,value)
        #print time
        #print value
    #print data
    #for x in range(10):
    #    for y in range(10):
    #        ws0.write(x,y,"this is cell %s, %s" % (x,y))
    
    response = HttpResponse()
    response['Content-Type']='application/ms-excel; charset="utf-8"'
    response['Content-Transfer-Encodeing'] = 'Binary'
    response['Content-disposition'] = 'attachment; filename="%s.xls"'%(chartTitle)
    wb.save(response)
    return response
    #wb.save('output.xls')
    
    #return wb.save('output.xls')
    #response = HttpResponse(mmimetype="application/ms-excel"imetype="application/ms-excel")
    #response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    #wb = xlwt.Workbook()
    #wb.save(response)
    #return response

def getGridList(request):
    
    target1 = "__SummaryInfo__/pkts_out.rrd"
    target2 = "mhr/__SummaryInfo__/pkts_out.rrd"
    target3 = "mhr/dev.local/ap_closing.rrd"
    

    metric = ClusterNodes()

    builder = FileMetricDBBuilder()
    builder.buildMetricInstance(metric,const.RRD_PATH)

    metric.dump()    


def getClusterList(request):
    
    metric = ClusterNodes()

    builder = FileMetricDBBuilder()
    builder.buildMetricInstance(metric,const.RRD_PATH)

    #metric.dump()    

    dictData = metric.getNameAsDict('cluster')
    jsonResult = json.dumps(dictData,sort_keys=True,indent=4)
    
    return HttpResponse(jsonResult)


def getHostList(request):
    
    if request.method =='GET':
        return HttpResponse("ok")

    clusterName = request.POST['cluster'].strip()
    
    metric = ClusterNodes()

    builder = FileMetricDBBuilder()
    builder.buildMetricInstance(metric,const.RRD_PATH)

    hosts = metric.getHosts(clusterName)

    dictData = hosts.getNameAsDict('host')
    dictData['cluster'] = clusterName
    
    jsonResponse = json.dumps(dictData)

    return HttpResponse(jsonResponse)


def getDataSourceList(request):
    
    if request.method =='GET':
        return HttpResponse("ok")

    clusterName = request.POST['cluster'].strip()
    hostName = request.POST['host'].strip()
    
    metric = ClusterNodes()

    builder = FileMetricDBBuilder()
    builder.buildMetricInstance(metric,const.RRD_PATH)

    host = metric.getHost(clusterName,hostName)

    dictData = host.dataSources.getNameAsDict('dataSource')
    dictData['cluster'] = clusterName
    dictData['host'] = hostName
    
    jsonResponse = json.dumps(dictData)

    return HttpResponse(jsonResponse)


@csrf_exempt
def getData(request):

    def makeJSON(series_list,event_list):
        series_data = []
        for series in series_list:
            timestamps = range(series.start, series.end, series.step)
            #datapoints = zip(timestamps,series)
            datapoints = map(dict, map(lambda t:zip(('x','y'),t), zip(timestamps,series)))
            series_data.append( dict(target=series.getFullName(), events=event_list, datapoints=datapoints) )

        return series_data
    
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    
    target = str(request.POST['target'])
    startTime = str(request.POST['startTime'])
    endTime = str(request.POST['endTime'])
    respFormat = str(request.POST['format'].strip())
    
    """
    target = "mhr/dev.local/cpu_system.rrd"
    startTime = "2012:09:05:00:00"
    endTime = "2012:09:07:00:00"
    """
    
    logInfo("target="+target+",start="+startTime+",end="+endTime)
    
    metric = ClusterNodes()

    builder = RequestMetricDBBuilder()
    builder.buildMetricInstance(metric,target)
    
    rrdfetcher = RRDDataFetcher()
    seriesList = rrdfetcher.fetch(metric,startTime,endTime)

    
    events = EventManager()
    eventList = events.getEventDataForChart(request,seriesList)
    #print "eventData=",eventData
    
    jsonResult = makeJSON(seriesList,eventList)
    #jsonResult = json.dumps(dictData,sort_keys=True,indent=4)

    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData(jsonResult)
    return HttpResponse(jsonResponse.toJson())
    
    #return HttpResponse(jsonResult)


@csrf_exempt
def getAlertHourlyData(request):

    def makeJSON(series_list,event_list):
        series_data = []
        for series in series_list:
            timestamps = range(series.start, series.end, series.step)
            #datapoints = zip(timestamps,series)
            datapoints = map(dict, map(lambda t:zip(('x','y'),t), zip(timestamps,series)))
            series_data.append( dict(target=series.getFullName(), events=event_list, datapoints=datapoints) )

        return series_data
    
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    
    target = str(request.POST['target'])
    startTime = str(request.POST['startTime'])
    endTime = str(request.POST['endTime'])
    respFormat = str(request.POST['format'].strip())
    
    """
    target = "mhr/dev.local/cpu_system.rrd"
    startTime = "2012:09:05:00:00"
    endTime = "2012:09:07:00:00"
    """
    
    logInfo("target="+target+",start="+startTime+",end="+endTime)
    
        
    chartBuilder = ChartDataBuilder()
    alertSeries = chartBuilder.fetchAlertHourlyData(request.user.id,"cluster","server",startTime,endTime)
    
    events = EventManager()
    eventList = events.getEventDataForChart(request,alertSeries)
    #print "eventData=",eventData
    
    jsonResult = makeJSON(alertSeries,eventList)
    #jsonResult = json.dumps(dictData,sort_keys=True,indent=4)

    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData(jsonResult)
    return HttpResponse(jsonResponse.toJson())
    
    #return HttpResponse(jsonResult)

@csrf_exempt
def getServerDownHourlyData(request):
    def makeJSON(series_list,event_list):
        series_data = []
        for series in series_list:
            timestamps = range(series.start, series.end, series.step)
            #datapoints = zip(timestamps,series)
            datapoints = map(dict, map(lambda t:zip(('x','y'),t), zip(timestamps,series)))
            series_data.append( dict(target=series.getFullName(), events=event_list, datapoints=datapoints) )

        return series_data
    
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    
    target = str(request.POST['target'])
    startTime = str(request.POST['startTime'])
    endTime = str(request.POST['endTime'])
    respFormat = str(request.POST['format'].strip())
    
    """
    target = "mhr/dev.local/cpu_system.rrd"
    startTime = "2012:09:05:00:00"
    endTime = "2012:09:07:00:00"
    """
    
    logInfo("target="+target+",start="+startTime+",end="+endTime)
    
        
    chartBuilder = ChartDataBuilder()
    serverdownSeries = chartBuilder.fetchServerDownHourlyData(request.user.id,"cluster","server",startTime,endTime)
    
    events = EventManager()
    eventList = events.getEventDataForChart(request,serverdownSeries)
    #print "eventData=",eventData
    
    jsonResult = makeJSON(serverdownSeries,eventList)
    #jsonResult = json.dumps(dictData,sort_keys=True,indent=4)

    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData(jsonResult)
    return HttpResponse(jsonResponse.toJson())
    
    #return HttpResponse(jsonResult)


@csrf_exempt
def getAbnormalStatHourlyData(request):
    def makeJSON(series_list,event_list):
        series_data = []
        for series in series_list:
            timestamps = range(series.start, series.end, series.step)
            #datapoints = zip(timestamps,series)
            datapoints = map(dict, map(lambda t:zip(('x','y'),t), zip(timestamps,series)))
            series_data.append( dict(target=series.getFullName(), events=event_list, datapoints=datapoints) )

        return series_data
    
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    
    target = str(request.POST['target'])
    startTime = str(request.POST['startTime'])
    endTime = str(request.POST['endTime'])
    respFormat = str(request.POST['format'].strip())
    
    """
    target = "mhr/dev.local/cpu_system.rrd"
    startTime = "2012:09:05:00:00"
    endTime = "2012:09:07:00:00"
    """
    
    logInfo("target="+target+",start="+startTime+",end="+endTime)
    
        
    chartBuilder = ChartDataBuilder()
    serverdownSeries = chartBuilder.fetchAbnormalStatHourlyData(request.user.id,"cluster","server",startTime,endTime)
    
    events = EventManager()
    eventList = events.getEventDataForChart(request,serverdownSeries)
    #print "eventData=",eventData
    
    jsonResult = makeJSON(serverdownSeries,eventList)
    #jsonResult = json.dumps(dictData,sort_keys=True,indent=4)

    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData(jsonResult)
    return HttpResponse(jsonResponse.toJson())
    
    #return HttpResponse(jsonResult)


def getGridSummaryData(request):
    
    if request.method =='GET':
        return HttpResponse("ok")

    """
    target = str(request.POST['target'])
    startTime = str(request.POST['startTime'])
    endTime = str(request.POST['endTime'])
    respFormat = str(request.POST['format'].strip())
    """
    target = const.SUMMARY_NODE+"/cpu_system.rrd"
    startTime = "2012:09:05:00:00"
    endTime = "2012:09:07:00:00"

    
    logInfo("target="+target+",start="+startTime+",end="+endTime)
    
    metric = ClusterNodes()

    builder = RequestMetricDBBuilder()
    builder.buildMetricInstance(metric,target)
    
    rrdfetcher = RRDDataFetcher()
    seriesList = rrdfetcher.fetch(metric,startTime,endTime)
    jsonResult = makeJSON(seriesList)
    #jsonResult = json.dumps(dictData,sort_keys=True,indent=4)
    
    return HttpResponse(jsonResult)


def getSidebarMenu(request):
    metric = ClusterNodes()

    builder = RequestMetricDBBuilder()
    builder.buildMetricInstance(metric,target)
    
    rrdfetcher = RRDDataFetcher()
    seriesList = rrdfetcher.fetch(metric,startTime,endTime)
    jsonResult = makeJSON(seriesList)
    #jsonResult = json.dumps(dictData,sort_keys=True,indent=4)
    
    return HttpResponse(jsonResult)


def getUserFavoriteChartList(request):    
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    result = vo_Favorite.objects.filter(user=request.user)
    
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=("regdate","updatedate"))
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def registerUserFavoriteChart(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    favorite = vo_Favorite.objects.addFavoriteFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not favorite:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add favorite to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"uid":favorite.id})
    return HttpResponse(jsonResponse.toJson())


def removeUserFavoriteChart(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    ret = vo_Favorite.objects.deleteFavoriteFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not ret:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to delete favorite to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())
    


@csrf_exempt
def getAlertHistory(request):    
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    
    startTime = getDjangoStyleDateTime(request.POST['startTime'])
    endTime =  getDjangoStyleDateTime(request.POST['endTime'])
    server_id = request.POST.get('server_id', '')
        
    result = vo_AlertHistory.objects.select_related().filter(regdate__gte=startTime,regdate__lte=endTime,user=request.user)
    
    server_id = request.POST.get('server_id', '')
    if server_id:
        result = result.filter(server=server_id)
    
    page = request.POST.get('page', '1')
    CobjectPaginator = ObjectPaginator(result,ALERT_HISTORY_NUMBER_OF_PAGE)
    result = CobjectPaginator.getObjectInPage(page)
    page = CobjectPaginator.getCurrentPage()

    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=(),relations=('plugin','alert'))
    jsonResponse.addExtra("page",str(page))
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def getAlertDetail(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    result = vo_Alert.objects.select_related().filter(id=request.POST['alert_id'],user=request.user)
  
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=(),relations=('plugin',))
    return HttpResponse(jsonResponse.toJson())


def filterDashboardDataSources(data,name='values'):
    
    def getDataAsDict(data):
        results = []
        filters = ['temp','rack','power']
        
        for item in data:
            append = True
            for filter in filters:
                if item.name.find(filter)>-1:
                    append = False
            
            if append:
                result = dict()
                result['name'] = item.name
                results.append(result)
                
        return results
    
    results = dict()
    values = getDataAsDict(data)
    results[name] = values
    return results
    
@csrf_exempt
def getDashboardTargetList(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    clusterName = const.SUMMARY_NODE
    
    metric = ClusterNodes()

    builder = FileMetricDBBuilder()
    builder.buildMetricInstance(metric,const.RRD_PATH)

    clusterNode = metric.getClusterByName(clusterName)

    #filteredSources = clusterNode.dataSources.filter("rack")
    #dictData = filteredSources.getNameAsDict('dataSource')


    #clusterNode.dataSources.setFilter("rack")
    #dictData = clusterNode.dataSources.getNameAsDict('dataSource')
    dictData = filterDashboardDataSources(clusterNode.dataSources,'dataSource')
    dictData['cluster'] = const.SUMMARY_NODE
    
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData(dictData)
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def getAvailablePluginList(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    result = vo_Plugin.objects.all()
    #for item in result:
    #    logInfo("item="+item.plugin_name)
        
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=())
    return HttpResponse(jsonResponse.toJson())

    
@csrf_exempt
def getServerGroupList(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    group_type = request.POST['group_type']
    all_group = "2"
    
    if group_type==all_group:
        result = vo_Server.objects.all()
    else:
        result = vo_Server.objects.filter(gmond_install_flag=group_type)
    
    #page = request.POST.get('page', '1')
    
    page = request.POST.get('page', '1')
    CobjectPaginator = ObjectPaginator(result,ALERT_HISTORY_NUMBER_OF_PAGE)
    result = CobjectPaginator.getObjectInPage(page)
    page = CobjectPaginator.getCurrentPage()
    
    
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=())
    jsonResponse.addExtra("page",str(page))
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def getServerDetail(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    server_id = request.POST['server_id']
    
    result = vo_Server.objects.filter(id=server_id)
        
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=())
    return HttpResponse(jsonResponse.toJson())




@csrf_exempt
def editAlert(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    oAlert = vo_Alert.objects.editAlertFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not oAlert:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to alert server to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"alert_uid":oAlert.id})
    return HttpResponse(jsonResponse.toJson())




@csrf_exempt
def addServer(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    oServer = vo_Server.objects.addServerFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not oServer:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add server to data model")
        return HttpResponse(jsonResponse.toJson())

    apiName = "getServerDetail"    
    apiData = "server_id" + const.APIDATA_EQUAL + str(oServer.id)
    #print 'bond'
    #print apiName
    #print apiData
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"server_uid":oServer.id,"server_ip":oServer.ip,"server_version":oServer.server_version,"apiname": apiName,"apidata":apiData})
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def deleteServer(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    ret = vo_Server.objects.deleteServerFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not ret:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to delete server to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def editServer(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    oServer = vo_Server.objects.editServerFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not oServer:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to edit server to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())


"""
@csrf_exempt
def addServer(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    oServer = vo_Server.objects.addServerFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not oServer:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add server to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"server_uid":oServer.id,"server_ip":oServer.ip,"server_version":oServer.server_version})
    return HttpResponse(jsonResponse.toJson())
"""
@csrf_exempt
def deleteServer(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    ret = vo_Server.objects.deleteServerFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not ret:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to delete server to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def editServer(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    oServer = vo_Server.objects.editServerFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not oServer:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to edit server to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())

from django.contrib.auth.models import User
@csrf_exempt
def editUserProfile(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    oUser = User.objects.get(id=request.user.id)
    
    oProfile = oUser.get_profile()
    oProfile.grahp_realtime_interval = request.POST.get('grahp_realtime_interval',oProfile.grahp_realtime_interval);
    oProfile.save()

    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    #jsonResponse.setQuerysetData(oUser,excludeFields=())
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def updateGmetadConf(request):
    
    confFile = ConfFile()
    confFile.setPath('/etc/ganglia/gmetad.conf')
    gmetad_conf = request.POST.get('conf')
    confFile.write(gmetad_conf)
    
    
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def updateGmondConf(request):
    
    confFile = ConfFile()
    dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static/temp'))
    confFile.setPath(dataPath+'/gmond.conf')
    
    gmond_conf = request.POST.get('conf')
    confFile.write(gmond_conf)
    
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def updateUserConf(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    oUser = User.objects.get(id=request.user.id)
    
    oProfile = oUser.get_profile()
    oProfile.rrd_path = request.POST.get('rrd_path',oProfile.rrd_path);
    oProfile.api_server = request.POST.get('api_server',oProfile.api_server);
    oProfile.api_port = request.POST.get('api_port',oProfile.api_port);
    oProfile.gmetad_ip = request.POST.get('gmetad_ip',oProfile.gmetad_ip);
    oProfile.gmetad_port = request.POST.get('gmetad_port',oProfile.gmetad_port);
    oProfile.grahp_realtime_interval = request.POST.get('grahp_realtime_interval',oProfile.grahp_realtime_interval);
    oProfile.grahp_grid_outlineWidth = request.POST.get('grahp_grid_outlineWidth',oProfile.grahp_grid_outlineWidth);
    oProfile.grahp_line_fill = request.POST.get('grahp_line_fill',oProfile.grahp_line_fill);
    oProfile.grahp_line_color = request.POST.get('grahp_line_color',oProfile.grahp_line_color);
    oProfile.grahp_grid_color = request.POST.get('grahp_grid_color',oProfile.grahp_grid_color);
    
    
    oProfile.save()
    
    UserConfig(request.user).changeConfig()
    
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    #jsonResponse.setQuerysetData(oUser,excludeFields=())
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def addEvent(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
   
    oEvent = vo_Event.objects.addEventFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not oEvent:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add event to data model")
        return HttpResponse(jsonResponse.toJson())


    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"event_id":oEvent.id})
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def deleteEvent(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())

    ret = vo_Event.objects.deleteEventFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not ret:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to delete server to data model")
        return HttpResponse(jsonResponse.toJson())
    
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def addAlert(request):
    #logInfo("api.addAlert")
    
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
   
    #oAlert = vo_Alert.objects.addAlertFromRequest(request)
    oAlert = 123
    
    jsonResponse = jsonResponseBuilder()
    if not oAlert:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add alert to data model")
        return HttpResponse(jsonResponse.toJson())


    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({})
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def addAlertHistory(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
   
    oAlertHistory = vo_AlertHistory.objects.addAlertHistoryFromRequest(request)

    jsonResponse = jsonResponseBuilder()
    if not oAlertHistory:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add alert history to data model")
        return HttpResponse(jsonResponse.toJson())


    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({})
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def addServerDown(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    oServerDown = vo_ServerDown.objects.addServerDownFromRequest(request)

    #logInfo("addServerDown : year="+oServerDown.year+",month="+oServerDown.month+",day="+oServerDown.day)

    jsonResponse = jsonResponseBuilder()
    if not oServerDown:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add server down to data model")
        return HttpResponse(jsonResponse.toJson())


    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({})
    return HttpResponse(jsonResponse.toJson())

@csrf_exempt
def addAbnormalStat(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    oStat = vo_AbnormalStat.objects.addAbnormalStatFromRequest(request)

    #logInfo("addServerDown : year="+oServerDown.year+",month="+oServerDown.month+",day="+oServerDown.day)

    jsonResponse = jsonResponseBuilder()
    if not oStat:
        jsonResponse.setStatus(const.RESPONSE_CODE_ERROR,"Fail to add abnormal stat to data model")
        return HttpResponse(jsonResponse.toJson())


    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({})
    return HttpResponse(jsonResponse.toJson())





if __name__ == '__main__':
    
    """
    test = [1,2,3,4,5]
    test2 = dict()
    test2['cluster'] = test
    #print json.dumps(test2,sort_keys=True,indent=4)
    
    metric = ClusterNodes()

    builder = FileMetricDBBuilder()
    builder.buildMetricInstance(metric,const.RRD_PATH)
        
    dictData = metric.getNameAsDict('cluster')
    print json.dumps(dictData,sort_keys=True,indent=4)

    print
    print
    print 
    
    hosts = metric.getHosts("mhr")
    print "host len="+str(len(hosts))
    
    dictData2 = hosts.getNameAsDict('host')
    print json.dumps(dictData2,sort_keys=True,indent=4)

    host = metric.getHost("mhr","dev.local")
    #host = hosts.getHost('dev.local')
    
    dictData3 = host.dataSources.getNameAsDict("dataSource")
    dictData3['cluster'] = "mhr"
    dictData3['host'] = "dev.local"
    print json.dumps(dictData3,sort_keys=True,indent=4)
    """
    
    getData(None)
