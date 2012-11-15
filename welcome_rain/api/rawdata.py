import json

from django.http import HttpResponse

import welcome_rain.common.const
from welcome_rain.common.monitoringNode import * 
from welcome_rain.common.rrddatafetcher import *
from welcome_rain.common.metricDBBuilder import *



def index(request):
    return HttpResponse("index")


def getData(request):
    
    if request.method =='GET':
        return HttpResponse("ok")

    """
    target = request.POST['target'].strip()
    startTime = request.POST['startTime'].strip()
    endTime = request.POST['endTime'].strip()
    respFormat = request.POST['format'].strip()
    """
    
    target = "mhr/dev.local/cpu_system.rrd"
    startTime = "2012:09:05:00:00:00"
    endTime = "2012:09:07:00:00:00"
    
    metric = ClusterNodes()

    builder = RequestMetricDBBuilder()
    builder.buildMetricInstance(metric,target)
    
    rrdfetcher = RRDDataFetcher()
    rrdfetcher.fetch2(metric,startTime.split(":"),endTime.split(":"))

    dictData = metric.getNameAsDict('cluster')
    jsonResult = json.dumps(dictData,sort_keys=True,indent=4)
    
    return HttpResponse(jsonResult)



if __name__ == '__main__':

    getData(None)
