import os
import time
import rrdtool
from datetime import datetime,timedelta 

from mhrlog import * 


class RRDReader:
  supported = bool(rrdtool)

  def __init__(self):
    #self.datafile_name = datafile_name
    #self.datasource_name = datasource_name
    pass
    
  def get_intervals(self):
    start = time.time() - self.get_retention(self.datafile_name)
    end = max( os.stat(self.datafile_name).st_mtime, start )
    return IntervalSet( [Interval(start, end)] )


  def fetch(self,rrdfile,rrdfield,startTime, endTime):
    startString = time.strftime("%H:%M_%Y%m%d+%Ss", time.localtime(startTime))
    endString = time.strftime("%H:%M_%Y%m%d+%Ss", time.localtime(endTime))

#    if settings.FLUSHRRDCACHED:
#      rrdtool.flushcached(self.fs_path, '--daemon', settings.FLUSHRRDCACHED)
    cmdString = [rrdfile , 'AVERAGE' , '-s ' + str(startTime) , '-e ' + str(endTime)]
    
    #print cmdString

    (timeInfo, columns, rows) = rrdtool.fetch(cmdString)
#    (timeInfo, columns, rows) = rrdtool.fetch(self.datafile_name,'AVERAGE','-s ' + str(startTime),'-e ' + str(endTime))
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

  def fetchLastData(self,rrdfile,rrdfield):
    now = datetime.now()
    past = now - timedelta(minutes=10)
    startTime = (past.strftime("%Y%m%d %H:%M"))
    endTime = (now.strftime("%Y%m%d %H:%M"))

    cmdString = [rrdfile , 'AVERAGE' , '-s ' + startTime , '-e ' + endTime]
    
    (timeInfo, columns, rows) = rrdtool.fetch(cmdString)

    colIndex = list(columns).index(rrdfield)
    rows.pop() #chop off the latest value because RRD returns crazy last values sometimes
    
    #print "rrdfile=", rrdfile," , startTime=",startTime," , endTime=",endTime, " , time=", timeInfo, " , rows=", len(rows)
    
    lastTime = timeInfo[1]
    lastRow = rows.pop()
    if lastRow is None:
        lastValue = 0
    else:
        value = lastRow[colIndex]
        if value is None:
            lastValue = 0
        else:
            lastValue = value
        
    return lastTime, lastValue
    #item = rows.pop()
    #return item


  @staticmethod
  def getFirstDate(datafile_name):
    info = rrdtool.first(datafile_name)
    return info

  @staticmethod
  def getLastDate(datafile_name):
    info = rrdtool.last(datafile_name)
    return info

  @staticmethod
  def getInfo(datafile_name):
    info = rrdtool.info(datafile_name)
    return info
    
  @staticmethod
  def get_datasources(datafile_name):
    info = rrdtool.info(datafile_name)
    
    if 'ds' in info:
      #print "get_datasources"  
      return [datasource_name for datasource_name in info['ds']]
    else:
      #print "get_datasources else"
      ds_keys = [ key for key in info if key.startswith('ds[') ]
      datasources = set( key[3:].split(']')[0] for key in ds_keys )

      #pprint.pprint(ds_keys)
      #print "-------------------------------------------------------------------"

      return list(datasources)

  @staticmethod
  def get_retention(datafile_name):
    info = rrdtool.info(datafile_name)
    if 'rra' in info:
      print "rra"
      rras = info['rra']
    else:
      
      # Ugh, I like the old python-rrdtool api better..
      rra_count = max([ int(key[4]) for key in info if key.startswith('rra[') ]) + 1
      print "rra_count=",rra_count
      rras = [{}] * rra_count
      for i in range(rra_count):
        rras[i]['pdp_per_row'] = info['rra[%d].pdp_per_row' % i]
        rras[i]['rows'] = info['rra[%d].rows' % i]

    retention_points = 0
    for rra in rras:
      points = rra['pdp_per_row'] * rra['rows']
      if points > retention_points:
        retention_points = points

    return  retention_points * info['step']
