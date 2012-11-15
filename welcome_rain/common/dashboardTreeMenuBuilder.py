import os
import unittest
#from node import Node
from const import *
from monitoringNode import * 
from metricDBBuilder import *
from baseTreeMenu import *

        
class RackTreeMenuBuilder(BaseTreeMenuBuilder):
    def getAPIDataSource(self,target,dataSources,target_index):    
        result = ""
        index = 0
        for data in dataSources:
            if target_index==-1:
                result = result + "target" + const.APIDATA_EQUAL + target + "/"+data.name + const.APIDATA_SEPERATOR
            elif target_index==index:
                result = result + "target" + const.APIDATA_EQUAL + target + "/"+data.name + const.APIDATA_SEPERATOR
            #print "buildMenu"+data.name
            index += 1
        return result

    
    def buildMenuNodes(self,metric):
        host = metric.getHost(RACK_POWER_CLUSTER,RACK_POWER_HOST)
        if not host:
            print "error"
            return False

        target = RACK_POWER_CLUSTER + "/" + RACK_POWER_HOST
        dataSources = host.dataSources.filter(RACK_POWER_RRD)
        #print dataSources
         
        apidata = self.getAPIDataSource(target,dataSources,-1)
        dashNode = self.addLINode(self.rootNode,"Dashboard",apiName="getData", apiData=apidata)
        self.addLinkNode(dashNode, "Dashboard", "#")
        
        index = 0       
        for data in dataSources:
            dataname = data.name[:-4]
            #print "data_source=",dataname

            apidata = self.getAPIDataSource(target,dataSources,index)
            dataNode = self.addLINode(self.rootNode,RACK_POWER_HOST, apiName="getData", apiData=apidata)
            
            self.addLinkNode(dataNode, dataname, "#")
            index += 1
        
        return True
     

class PowerTreeMenuBuilder(BaseTreeMenuBuilder):
    def getAPIDataSource(self,target,dataSources,target_index):    
        result = ""
        index = 0
        for data in dataSources:
            if target_index==-1:
                result = result + "target" + const.APIDATA_EQUAL + target + "/"+data.name + const.APIDATA_SEPERATOR
            elif target_index==index:
                result = result + "target" + const.APIDATA_EQUAL + target + "/"+data.name + const.APIDATA_SEPERATOR
            #print "buildMenu"+data.name
            index += 1
        return result
    
    def buildMenuNodes(self,metric):
        host = metric.getHost(SERVER_POWER_CLUSTER,SERVER_POWER_HOST)
        if not host:
            print "error"
            return False

        target = SERVER_POWER_CLUSTER + "/" + SERVER_POWER_HOST
        dataSources = host.dataSources.filter(SERVER_POWER_RRD)
        #print dataSources
         
        apidata = self.getAPIDataSource(target,dataSources,-1)
        dashNode = self.addLINode(self.rootNode,"Dashboard",apiName="getData", apiData=apidata)
        self.addLinkNode(dashNode, "Dashboard", "#")
        
        index = 0       
        for data in dataSources:
            dataname = data.name[:-4]
            #print "data_source=",dataname

            apidata = self.getAPIDataSource(target,dataSources,index)
            dataNode = self.addLINode(self.rootNode,SERVER_POWER_HOST, apiName="getData", apiData=apidata)
            
            self.addLinkNode(dataNode, dataname, "#")
            index += 1
        
        return True
     

class TemperatureTreeMenuBuilder(BaseTreeMenuBuilder):
    def getAPIDataSource(self,target,dataSources,target_index):    
        result = ""
        index = 0
        for data in dataSources:
            if target_index==-1:
                result = result + "target" + const.APIDATA_EQUAL + target + "/"+data.name + const.APIDATA_SEPERATOR
            elif target_index==index:
                result = result + "target" + const.APIDATA_EQUAL + target + "/"+data.name + const.APIDATA_SEPERATOR
            #print "buildMenu"+data.name
            index += 1
        return result
        
    def buildMenuNodes(self,metric):
        host = metric.getHost(TEMPERATURE_CLUSTER,TEMPERATURE_HOST)
        if not host:
            print "error"
            return False

        target = TEMPERATURE_CLUSTER + "/" + TEMPERATURE_HOST
        dataSources = host.dataSources.filter(TEMPERATURE_RRD)
        #print dataSources
         
        apidata = self.getAPIDataSource(target,dataSources,-1)
        dashNode = self.addLINode(self.rootNode,"Dashboard",apiName="getData", apiData=apidata)
        self.addLinkNode(dashNode, "Dashboard", "#")
        
        index = 0       
        for data in dataSources:
            dataname = data.name[:-4]
            #print "data_source=",dataname

            apidata = self.getAPIDataSource(target,dataSources,index)
            dataNode = self.addLINode(self.rootNode,TEMPERATURE_HOST, apiName="getData", apiData=apidata)
            
            self.addLinkNode(dataNode, dataname, "#")
            index += 1
        
        return True


class WorkloadTreeMenuBuilder(BaseTreeMenuBuilder):
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
    
        
class CustomChartTreeMenuBuilder(BaseTreeMenuBuilder):
    def buildMenuNodes(self):
        node1 = self.addLINode(self.rootNode,"Custom")
        self.addLinkNode(node1, "Dashboard", "#")
        
         

        
class DashboardTreeMenuBuilder(BaseTreeMenuBuilder):
    def __init__(self,root=None,caption=None,id=None,klass=None):
        #node = self.addLINode(root,id,klass)
        #self.addLinkNode(node, caption, "", id, klass)
        #self.rootNode = self.addULNode(node,id,klass)
        #super().__init__(root=root,caption=caption,id=id,klass=klass)
        self.metric = ClusterNodes()
    
        self.metricBuilder = FileMetricDBBuilder()
        self.metricBuilder.buildMetricInstance(self.metric,const.RRD_PATH)
        
    
    def init(self):
        self.prepare()
        self.rootNode = self.addRootNode("div","treeMenu","dashboard")
        self.parentNode = self.addULNode(self.rootNode,"menu")


        
    def buildRackMenu(self):
        rackMenu = RackTreeMenuBuilder(self.parentNode,"Rack","Rack")
        rackMenu.buildMenuNodes(self.metric)
        return rackMenu
    
    def buildPowerMenu(self):
        powerMenu = PowerTreeMenuBuilder(self.parentNode,"Server","Server") 
        powerMenu.buildMenuNodes(self.metric)
        return powerMenu
    
    def buildTemeratureMenu(self):
        temperatureMenu = TemperatureTreeMenuBuilder(self.parentNode,"Temperature","Temperature")
        temperatureMenu.buildMenuNodes(self.metric)
        return temperatureMenu
    
    def buildWorkloadMenu(self):
        workloadMenu = WorkloadTreeMenuBuilder(self.parentNode,"Workload","Workload")
        workloadMenu.buildMenuNodes(self.metric)
        return workloadMenu
        
    def buildCustomChartMenu(self):
        customMenu = CustomChartTreeMenuBuilder(self.parentNode,"CustomChart","CustomChart")
        customMenu.buildMenuNodes()
        return customMenu

    def getTreeMenu(self,userId,responseFormat):
        self.buildRackMenu()  
        self.buildPowerMenu()
        self.buildTemeratureMenu()
        self.buildWorkloadMenu()
        self.buildCustomChartMenu()
        #MenuTree.dump(self.rootNode)
        #self.printxml(self.rootNode)
        return self.toHTML(self.rootNode)
    
# Test suite

class TestNode(unittest.TestCase):
    def setUp(self):
        self.node1 = Node("Test One", "ide ntifier 1 ")

    def test_initialization(self):
        self.assertEqual(self.node1.name, "Test One")
        self.assertEqual(self.node1.identifier, "identifier1")
        self.assertEqual(self.node1.expanded, True)

    def test_set_fpointer(self):
        self.node1.update_fpointer(" identi fier 2")
        self.assertEqual(self.node1.fpointer, ['identifier2'])

    def test_set_bpointer(self):
        self.node1.bpointer = " identi fier 1"
        self.assertEqual(self.node1.bpointer, 'identifier1')
        
    def test_set_data(self):
        self.node1.data = {1:'hello', "two":'world'}
        self.assertEqual(self.node1.data, {1:'hello', "two":'world'})

    def tearDown(self):
        pass
    
    
if __name__ == "__main__":
    print "adfs"
    menus = DashboardTreeMenuBuilder()
    menus.init()
    menus.getTreeMenu("abc","xml")
    #print menus.convertToHTML()
    
    #print
    #print
    #print
    
    #html = HTMLMenuGenerator()
    #html.tree.prepare()
    #html.generateHTML()
