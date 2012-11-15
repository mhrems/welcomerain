import json
import datetime


from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from welcome_rain.common.monitoringNode import * 
from welcome_rain.common.metricDBBuilder import *
from welcome_rain.common.rrdDataFetcher import *
from welcome_rain.common.mhrlog import * 
from welcome_rain.common.models import *
from welcome_rain.common.jsonResponseBuilder import *
from welcome_rain.common.const import *
from welcome_rain.common.util import *
from welcome_rain.common.objectPaginator import *
from welcome_rain.common.taskItemBuilder import *
from welcome_rain.common.task.remoteTaskHandler import *
from welcome_rain.common.task.taskItemModel import TaskItems


def index(request):
    return HttpResponse("index")



@csrf_exempt
def newTask(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    task = vo_Task.objects.addTaskFromRequest(request)

    task_type = request.POST['task_type']
    task_data = request.POST['task_data']
    
    print "---0"

    taskItems = TaskItems(task_id=task.id,task_type=task_type,task_data=task_data,url=API_SERVER,port=API_PORT)
    
    print "---1"
    taskItemBuilder = TaskItemBuilder(request,taskItems)
    taskItemBuilder.build()

    print "---2"
    
    taskHandler = RemoteTaskManager(taskItems)
    taskHandler.start()    
        
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"task_id":task.id})
    return HttpResponse(jsonResponse.toJson())



@csrf_exempt
def updateTask(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    task = vo_Task.objects.updateTaskFromRequest(request)
        
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"task_id":task.id})
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def getTaskList(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    result = vo_Task.objects.all()
    
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=())
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def addTaskStatus(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    taskStatus = vo_TaskStatus.objects.addTaskStatusFromRequest(request)
        
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"taskStatus_id":taskStatus.id})
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def queryTaskStatus(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    task_id = request.POST['task_id']
    status_id = request.POST['status_id']
    
    if status_id=="-1":
        result = vo_TaskStatus.objects.filter(task_id=task_id)
    else:
        result = vo_TaskStatus.objects.filter(task_id=task_id).filter(id>status_id)
        
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setQuerysetData(result,excludeFields=())
    return HttpResponse(jsonResponse.toJson())


@csrf_exempt
def addPlugin(request):
    if not validateHTTPRequest(request):
        return HttpResponse(badRequestResponse())
    
    plugin = vo_Plugin.objects.addFromHTTPRequest(request)
            
    jsonResponse = jsonResponseBuilder()
    jsonResponse.setStatus(const.RESPONSE_CODE_OK,const.RESPONSE_OK)
    jsonResponse.setData({"plugin_id":plugin.id})
    return HttpResponse(jsonResponse.toJson())
