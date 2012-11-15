import os
import unittest
#from node import Node
from const import *
from monitoringNode import * 
from metricDBBuilder import *
from baseTreeMenu import *



class ServerTreeMenuBuilder(BaseTreeMenuBuilder):
    def addDataSource(self,parent,dataSources,id=None):    
        for data in dataSources:
            node = self.addLINode(parent,"_"+data.name)
            self.addLinkNode(node, data.name, "#")
            #print "buildMenu"+data.name

    def getAPIDataSource(self,target,dataSources):    
        result = ""
        for data in dataSources:
            result = result + "target" + const.APIDATA_EQUAL + target + "/"+data.name + const.APIDATA_SEPERATOR
            #print "buildMenu"+data.name
        return result
        
    def buildMenuNodes(self,metric):
        #metric = ClusterNodes()
    
        #builder = FileMetricDBBuilder()
        #builder.buildMetricInstance(metric,const.RRD_PATH)

        node1 = self.addLINode(self.rootNode,"Dashboard",apiName="getDashboardDataList",apiData="")
        dashboardNode = self.addLinkNode(node1, "Dashboard", "#")

        node2 = self.addLINode(self.rootNode,"Cluster")
        clusterNode = self.addLinkNode(node2, "Cluster", "#")

        clusterNodes = self.addULNode(node2,"cluster")

        for cluster in metric:
            #clusterNode = self.addLINode(clusterNodes, cluster.name)
            if cluster.name==const.SUMMARY_NODE:
                apidata = self.getAPIDataSource(cluster.name,cluster.dataSources)
                clusterNode = self.addLINode(clusterNodes, cluster.name,apiName="getData",apiData=apidata)
                self.addLinkNode(clusterNode, cluster.name, "#")
            else:
                clusterNode = self.addLINode(clusterNodes, cluster.name)
                self.addLinkNode(clusterNode, cluster.name, "#")
                
            #    clusterDataNode = self.addULNode(clusterNode)
            #    self.addDataSource(clusterDataNode,cluster.dataSources)
            
            for host in cluster.hosts:
                hostNodes = self.addULNode(clusterNode)
 
                target = cluster.name + "/"+host.name
                apidata = self.getAPIDataSource(target,host.dataSources)
                
                hostNode = self.addLINode(hostNodes,host.name, apiName="getData", apiData=apidata)
                self.addLinkNode(hostNode, host.name, "#")

                
                #dataNodes = self.addULNode(hostNode)
                #hostNode = self.addLINode(hostNodes, "host")
                #self.addLinkNode(hostNode, "", "#")

                #self.addDataSource(dataNodes,host.dataSources)
                
                            
        #metric.dump()
        
        return True
    
        

        
class TableTreeMenuBuilder(BaseTreeMenuBuilder):
    def __init__(self,root=None,caption=None,id=None,klass=None):
        #node = self.addLINode(root,id,klass)
        #self.addLinkNode(node, caption, "", id, klass)
        #self.rootNode = self.addULNode(node,id,klass)
        #super().__init__(root=root,caption=caption,id=id,klass=klass)
        self.metric = None
    
        #self.metricBuilder = FileMetricDBBuilder()
        #self.metricBuilder.buildMetricInstance(self.metric,const.RRD_PATH)
        
    def setMetric(self,metric):
        self.metric = metric
        
    def init(self):
        self.prepare()
        self.rootNode = self.addRootNode("div","treeMenu","tableView")
        self.parentNode = self.addULNode(self.rootNode,"menu")

        
    def buildWorkloadMenu(self):
        workloadMenu = ServerTreeMenuBuilder(self.parentNode,"Workload","Workload")
        workloadMenu.buildMenuNodes(self.metric)
        return workloadMenu
        

    def getTreeMenu(self,userId,responseFormat):
        self.buildWorkloadMenu()
        #MenuTree.dump(self.rootNode)
        #self.printxml(self.rootNode)
        return self.toHTML(self.rootNode)
