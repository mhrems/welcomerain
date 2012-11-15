import os
import sys
from monitoringNode import *
from const import *
from os.path import isdir, join




class MetricDBBuilder:
    def __init__(self):
        pass

    def makeGridInstance(self,name):
        gridInstance = GridNode(name)
        return gridInstance
    
    def makeClusterInstance(self,cluster,parent=None):
        clusterInstance = ClusterNode(cluster,parent)
        return clusterInstance

    def makeHostInstance(self,host,parent):
        HostInstance = HostNode(host,parent)
        return HostInstance

    def makeDataSourceInstance(self,datasource,parent):
        dataSourceInstance = DataSourceNode(datasource,parent)
        return dataSourceInstance
        
    def isClusterMetric(self,value):
        if value==2:
            return True
        return False

    def isHostMetric(self,value):
        if value==3:
            return True
        return False

    def isValidData(self,data):
        tokens = data.split(const.NODE_SEPERATOR);

        if not tokens[len(tokens)-1]:
            return False
        
        if not data.lower().find(const.RRDFILE_EXT):
            return False
        
        return True   
    
    def isExcludedDataSource(self,data):
        excludes = EXCLUDE_DATA_SOURCE
        for item in excludes:
            if data.find(item)>-1:
                return True
        return False
    
    def addClusterMetric(self,metric,cluster,file):
        
        if self.isExcludedDataSource(file):
            return 
        
        clusterInstance = metric.find(cluster) 
        if not clusterInstance:
            clusterInstance = self.makeClusterInstance(cluster)
            metric.add(clusterInstance)
            #print "addClusterMetric: cluster <"+cluster+"> added"
            
        dataSourceInstance = clusterInstance.dataSources.find(file)
        if not dataSourceInstance:
            dataSourceInstance = self.makeDataSourceInstance(file,clusterInstance)
            clusterInstance.dataSources.add(dataSourceInstance)
            
        
    def addHostMetric(self,metric,cluster,host,file):

        if self.isExcludedDataSource(file):
            return 

        clusterInstance = metric.find(cluster) 
        if not clusterInstance:
            clusterInstance = self.makeClusterInstance(cluster)
            metric.add(clusterInstance)
            #print "addHostMetric: cluster <"+clusterInstance.name+"> added"
        
        hostInstance = clusterInstance.hosts.find(host) 
        if not hostInstance:
            hostInstance = self.makeHostInstance(host,clusterInstance)
            clusterInstance.hosts.add(hostInstance)
            #print "addHostMetric: host <"+host+"> added , cluster="+clusterInstance.name
        
        dataSourceInstance = hostInstance.dataSources.find(file)
        if not dataSourceInstance:
            dataSourceInstance = self.makeDataSourceInstance(file,hostInstance)
            hostInstance.dataSources.add(dataSourceInstance)
        
    
class FileMetricDBBuilder(MetricDBBuilder):

    def find(self,root, files=True, dirs=False, hidden=False, relative=True, topdown=True):
        root = os.path.join(root, '')  # add slash if not there
        for parent, ldirs, lfiles in os.walk(root, topdown=topdown):
            if relative:
                parent = parent[len(root):]
            if dirs and parent:
                yield os.path.join(parent, '')
            if not hidden:
                lfiles   = [nm for nm in lfiles if not nm.startswith('.')]
                ldirs[:] = [nm for nm in ldirs  if not nm.startswith('.')]  # in place
            if files:
                lfiles.sort()
                for nm in lfiles:
                    nm = os.path.join(parent, nm)
                    yield nm

    
    def parse(self,metric,file):

        if not self.isValidData(file):
            #print "skip data because it does not contain file value : " + file
            return False
        
        tokens = file.split(const.NODE_SEPERATOR);
        token_count = len(tokens)
            
        #print file,tokens,token_count
        
                
        if self.isClusterMetric(token_count):
            #print
            #print "addClusterMetric : cluster_name="+tokens[0]+" , filename=" + tokens[1] + " , src="+file
            self.addClusterMetric(metric,cluster=tokens[0],file=tokens[1])
        elif self.isHostMetric(token_count):
            #print "cluster_name="+tokens[0]+" , host_name="+tokens[1] + " , filename="+tokens[2] + " , src="+file
            self.addHostMetric(metric,cluster=tokens[0],host=tokens[1],file=tokens[2])

    def isMetricFiltered(self,f,filters):
        for filter in filters:
            if f.find(filter)>-1:
                return True
        return False
    
    def buildMetricInstance(self,metric,root, filters=None):
                
        for f in self.find(root, dirs=True):
#            print f
            if filters is None:
                self.parse(metric,f)
            else:
                if self.isMetricFiltered(f, filters):
                    self.parse(metric,f)
                
    
class RequestMetricDBBuilder(MetricDBBuilder):

    def parse(self,metric,value):

        if not self.isValidData(value):
            print "skip data because it does not contain file value : " + value
            return False
        
        tokens = value.split(const.NODE_SEPERATOR);
        token_count = len(tokens)
            
        #print file,tokens,token_count
                
        if self.isClusterMetric(token_count):
            #print
            #print "addClusterMetric : cluster_name="+tokens[0]+" , filename=" + tokens[1]
            self.addClusterMetric(metric,cluster=tokens[0],file=tokens[1])
        elif self.isHostMetric(token_count):
            #print "cluster_name="+tokens[0]+" , host_name="+tokens[1] + " , filename="+tokens[2]
            self.addHostMetric(metric,cluster=tokens[0],host=tokens[1],file=tokens[2])


    def buildMetricInstance(self,metric,target):
        targets = target.split(const.TARGET_SEPERATOR)
        for item in targets:
            print "target=",item
            self.parse(metric,item)

    
if __name__ == '__main__':
    
    filepath = "/home/james/Workspace/Project/MHRCloud/graphite-web/rrds"    
    #print cats_and_subs(root=filepath)
    
    #d = fileRead(filepath)
    #print(d)

    metric = ClusterNodes()

    #builder = FileMetricDBBuilder()
    #builder.buildMetricInstance(metric,filepath)
    
    #metric.dump()
    
    
    target1 = "__SummaryInfo__/pkts_out.rrd"
    target2 = "mhr/__SummaryInfo__/pkts_out.rrd"
    target3 = "mhr/dev.local/ap_closing.rrd"
    targets = target1 + ";" + target2 + ";" + target3
    
    metric2 = ClusterNodes()

    builder2 = RequestMetricDBBuilder()
    #builder2.buildMetricInstance(metric2,target1)
    #builder2.buildMetricInstance(metric2,target2)
    #builder2.buildMetricInstance(metric2,target3)
    builder2.buildMetricInstance(metric2,targets)
        
    metric2.dump()    

    