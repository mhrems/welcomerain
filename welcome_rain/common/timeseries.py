import os

class TimeSeries(list):
    
  def __init__(self, name, start, end, step, values, consolidate='average'):
    list.__init__(self, values)
    self.name = name
    self.start = start
    self.end = end
    self.step = step
    self.consolidationFunc = consolidate
    self.valuesPerPoint = 1
    self.options = {}
    
    self.cluster = "None"
    self.host = "None"
    self.dataSource = "None"
    self.firstDate = 0
    self.lastDate = 0
    
    self.parseName(name)

  def parseName(self,name):
      tokens = name.split(",")
      self.cluster = tokens[0].strip()
      self.host  = tokens[1].strip()
      self.dataSource = tokens[2].strip()
      
  def __iter__(self):
    if self.valuesPerPoint > 1:
      return self.__consolidatingGenerator( list.__iter__(self) )
    else:
      return list.__iter__(self)

  def getFullName(self):
      return "cluster="+self.cluster+",host="+self.host+",datasource="+self.dataSource
  
  def consolidate(self, valuesPerPoint):
    self.valuesPerPoint = int(valuesPerPoint)

  def setFirstDate(self,value):
    self.firstDate = value
  
  def setLastDate(self,value):
    self.lastDate = value
      
  def __consolidatingGenerator(self, gen):
    buf = []
    for x in gen:
      buf.append(x)
      if len(buf) == self.valuesPerPoint:
        while None in buf: buf.remove(None)
        if buf:
          yield self.__consolidate(buf)
          buf = []
        else:
          yield None
    while None in buf: buf.remove(None)
    if buf: yield self.__consolidate(buf)
    else: yield None
    raise StopIteration


  def __consolidate(self, values):
    usable = [v for v in values if v is not None]
    if not usable: return None
    if self.consolidationFunc == 'sum':
      return sum(usable)
    if self.consolidationFunc == 'average':
      return float(sum(usable)) / len(usable)
    if self.consolidationFunc == 'max':
      return max(usable)
    if self.consolidationFunc == 'min':
      return min(usable)
    raise Exception, "Invalid consolidation function!"


  def __repr__(self):
    return 'TimeSeries(name=%s, start=%s, end=%s, step=%s, firstDate=%d, lastDate=%d)' % (self.name, self.start, self.end, self.step, self.firstDate, self.lastDate)


  def getInfo(self):
    """Pickle-friendly representation of the series"""
    return {
      'name' : self.name,
      'start' : self.start,
      'end' : self.end,
      'step' : self.step,
      'values' : list(self),
    }

