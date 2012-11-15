import os
import cPickle as pickle

#from node import Node
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from const import *
from monitoringNode import * 
from metricDBBuilder import *

 
class MetaDataBuilder:
    def __init__(self): 
        self.metric = ClusterNodes()
        self.metricBuilder = FileMetricDBBuilder()
       
    def clear(self):
        self.metric = None
        self.metric = ClusterNodes()
        
    def buildMetric(self,filter):
        self.clear()
        #self.metricBuilder.buildMetricInstance(self.metric,const.RRD_PATH)
        self.metricBuilder.buildMetricInstance(self.metric,const.RRD_PATH,filter)
        
        return self.metric

    def dump(self):
        self.metric.dump()
        
   
if __name__ == "__main__":
    import pprint
    
    builder = MetaDataBuilder()
    builder.build()
    data = pickle.dumps(builder.metric)
    
    pprint.pprint(data)
    
    metric = pickle.loads(data)
    metric.dump()
    