class ResponseDataBuider:

  def __init__(self):
    pass
      
  def makeJSON(self,series_list):
    series_data = []
    for series in series_list:
        timestamps = range(series.start, series.end, series.step)
        datapoints = zip(series, timestamps)
        series_data.append( dict(target=series.name, datapoints=datapoints) )
    
    return series_data

  def makeRaw(self,series_list):
    for series in series_list:
        response.write( "%s,%d,%d,%d|" % (series.name, series.start, series.end, series.step) )
        response.write( ','.join(map(str,series)) )
        response.write('\n')
    
"""
    if format == 'raw':
      response = HttpResponse(mimetype='text/plain')
      for series in data:
        response.write( "%s,%d,%d,%d|" % (series.name, series.start, series.end, series.step) )
        response.write( ','.join(map(str,series)) )
        response.write('\n')
"""    
