import math
from datetime import datetime,timedelta 
 
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from welcome_rain.common.const import *
from welcome_rain.common.mhrlog import * 
from welcome_rain.common.models import *
from welcome_rain.common.summaryDataBuilder import *
from welcome_rain.common.util import *

from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


class EventManager:
    def __init__(self):
        pass
    
    def getEvents(self,request,filter=None):
        results = vo_Event.objects.all().filter(user=request.user)
        return results
    
    
    def makeDict(self,result,max):
        data = []
        for row in result:
            for index in range(-1,2):
                points = {}
                points['x'] = row.eventDateTime_unix + index
                points['color'] = const.EVENT_LINE_COLOR
                data.append( points )

        return data
    
    def getXAxisIndex(self,target_time,time_min,time_max,time_count):
        if target_time>time_max:
            return -1
            
        if target_time<time_min:
            return -1
            
        time_diff = time_max - time_min
        if time_diff==0:
            return -1
        
        time_unit = math.trunc(time_diff/time_count)
        time_index = round((target_time-time_min)/time_unit)
            
        #return time_diff,time_unit,time_index
        return time_index

    def getSeriesStatData(self,series_list):
        time_min = 0
        time_max = 0
        time_count = 0
        
        for series in series_list:
            time_min = series.start
            time_max = series.end
            time_count = series.step

        return time_min,time_max,time_count
    
    def getEventDataForChart(self,request,series):
        result = vo_Event.objects.all().filter(user=request.user)

        time_min,time_max,time_count = self.getSeriesStatData(series)

        data = []
        for row in result:
            utctime = row.eventDateTime_unix
            time_index = self.getXAxisIndex(utctime,time_min, time_max, time_count)
            
            #logInfo("getEventDataForChart : utc="+str(utctime)+" , min="+str(time_min)+" , max="+str(time_max)+" , index="+str(time_index))
            
            points = {}
            points['x_axis_index'] = time_index
            points['color'] = const.EVENT_LINE_COLOR
            data.append( points )

        return data


if __name__ == '__main__':
    
    events = EventManager()
    print events.getXAxisIndex(1348444800,1348444800,1348444800,10)
    