import os
import const


class NodeBase:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.summaryNode = False
        if name==const.SUMMARY_NODE:
            self.summaryNode = True

class DataSourceNode(NodeBase):
    pass
    

class GridNode(NodeBase):
    pass

class NodesBase(list):
    """
    def __init__(self):
        list.__init__(self)
        self.filter = None
    """
        
    def setFilter(self,filter):
        self.filter = filter
    
    def setExcludeFilter(self,filter):
        self.excludeFilter = filter
        
    def add(self,node):
        item = self.find(node.name)
        if item:
            print "duplicated data!!! : "+node.name
            return item
                
        self.append(node)
        return node
    
    def find(self,name):
        for item in self:
            if item.name==name:
                return item
        return
    
    def remove(self,index):
        pass
            
    def getCount(self):
        return len(self)

    def getDataAsList(self):
        results = []
        for item in self:
            results.append(item.name)
        
        return results

    def getDataAsDict(self,name='name'):
        results = []
        for item in self:
            append = True
            #if len(self.filter)>0:
            #    if item.name.find(self.filter)==-1:
            #        append = False
            
            if append:
                result = dict()
                result[name] = item.name
                results.append(result)
                
        return results
    
    def getNameAsDict(self,name='values'):
        results = dict()
        values = self.getDataAsDict()
        results[name] = values
        return results

    def getItemByName(self,name):
        instance = self.find(name)
        if not instance:
            return
        return instance


class DataSourceNodes(NodesBase):
    def filter(self,filter):
        result = []
        for item in self:
            if item.name.lower().find(filter.lower())>-1:
                result.append(item)
        return result
    

class HostNode(NodeBase):
    def __init__(self, name, parent):
        NodeBase.__init__(self,name, parent)    
        self.dataSources = DataSourceNodes()
    
    
class HostNodes(NodesBase):
    def getHost(self,name):
        hostInstance = self.getItemByName(name)
        if not hostInstance:
            return
        return hostInstance
        

class ClusterNode(NodeBase):
    def __init__(self, name, parent):
        NodeBase.__init__(self,name, parent)
        self.hosts = HostNodes()
        self.dataSources = DataSourceNodes()

    
class ClusterNodes(NodesBase):
    
    def getClusterByName(self,clusterName):
        clusterInstance = self.find(clusterName)
        if not clusterInstance:
            return
        return clusterInstance
        
    def getHosts(self,clusterName):
        clusterInstance = self.getClusterByName(clusterName)
        if not clusterInstance:
            return
        return clusterInstance.hosts
    
    def getHost(self,clusterName,hostName):
        clusterInstance = self.getClusterByName(clusterName)
        if not clusterInstance:
            return

        host = clusterInstance.hosts.getHost(hostName)
        if not host:
            return
        
        return host
    

    def dump(self):
        for cluster in self:
            print ">>> Begin of Cluster <<<"
            print "Cluster - "+cluster.name + " "
                        
            for datasource in cluster.dataSources:
                print "--- Data Source : " + datasource.name
            
#            print "------- Cluster:"+cluster.name + " Host List"

            for host in cluster.hosts:
                print "------------ Host:"+host.name + " Data Source List"
                for datasource in host.dataSources:
                    print datasource.name
                    
            print
            print ">>> End of Cluster <<<"
            print


class GridNodes(NodesBase):
    def __init__(self, name):
        NodeBase.__init__(self,name)
        self.clusters = ClusterNodes()
        self.dataSources = DataSourceNodes()
