import datetime
import time
import math


def convertStringToDateTime(str):
    print datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    d = datetime.datetime.strptime(str+":00", "%Y:%m:%d:%H:%M:%S")
    return int(time.mktime(d.timetuple()))

def getPercent(max,value):
    percent = (float(value)/float(max))*100
    return round(percent)


def getXAxisIndex(target_time,time_min,time_max,time_count):
    if target_time>time_max:
        return -1
        
    if target_time<time_min:
        return -1
        
    time_diff = time_max - time_min
    if time_diff==0:
        return -1
    
    time_unit = math.trunc(time_diff/time_count)
    time_index = round((target_time-time_min)/time_unit)
        
    return time_diff,time_unit,time_index


startTime = "2012:10:14:16:24"
endTime = "2012:10:14:17:53"

startTime2 = convertStringToDateTime(startTime) 
endTime2   = convertStringToDateTime(endTime) 

#print "start="+str(startTime2), " , end=",endTime2


temp = 286
max = 3000

#print getPercent(3000,286)

#print getXAxisIndex(1348444800,1348444100,1348445800,10)
print "date=",datetime.datetime.fromtimestamp(1350523473)

#UTCDateTime(1240561632)
   