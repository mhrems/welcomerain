import os
import unittest
import datetime
from django.db.models.query import QuerySet

#from node import Node
import const
from models import vo_Alert,vo_Plugin,vo_AlertHistory
from monitoringNode import * 
from baseTreeMenu import *
from welcome_rain.common.mhrlog import * 

        
class AlertHistoryTreeMenuBuilder(BaseTreeMenuBuilder):    
    def findServerNode(self,parentNode,name):
        return self.findNode(parentNode,name)
    
    def buildHistoryNodes(self,parentNode): 
        node0 = self.addLINode(parentNode,id="alertHistory", apiName="getAlertHistory", apiData="server_id"+const.APIDATA_EQUAL)
        self.addLinkNode(node0, "All", url="#" ,id="0")        
        
        endDate = datetime.datetime.today()
        startDate = endDate - datetime.timedelta(days=7)
        
        query = vo_AlertHistory.objects.all().query
        query.group_by = ['server_id','regdate']
        results = QuerySet(query=query,model=vo_AlertHistory)
        
        menuNode = parentNode
        
        #for item in vo_AlertHistory.objects.filter(regdate__range=[startDate,endDate]):
        for item in results:
            plugin = item.plugin
            apidata = "server_id"+const.APIDATA_EQUAL+str(item.server.id)
            #apidata = apidate+const.APIDATA_SEPERATOR+"alerthistory_id"+const.APIDATA_EQUAL+str(item.id)
            serverNode = self.findServerNode(parentNode, item.server.ip)
            if not serverNode:
                node1 = self.addLINode(parentNode,id=item.server.ip,apiName="getAlertHistory",apiData=apidata)
                self.addLinkNode(node1, item.server.ip, url="#" ,id=str(item.id))        
                
                #serverRootNode = self.addULNode(node1,id="server")
                #serverNode = self.addLINode(serverRootNode,item.server.ip)
                #self.addLinkNode(serverNode, item.server.ip, id="123")
                #menuNode = serverRootNode
        
            #node2 = self.addLINode(menuNode,"alertHistory", apiName="getAlertHistory", apiData=apidata)
            #self.addLinkNode(node2, item.regdate.strftime("%Y-%m-%d %H:%M:%S"), url="#" ,id=str(item.id))        

    def buildMenuNodes(self):
        self.buildHistoryNodes(self.rootNode)
        return True
     

class DataSourceTreeMenuBuilder(BaseTreeMenuBuilder):
    def buildDataSourceNodes(self,parentNode):
        for item in vo_Alert.objects.all():
            apidata = "alert_id"+const.APIDATA_EQUAL+str(item.id)            
            node1 = self.addLINode(parentNode,"DataSource",apiName="getAlertDetail",apiData=apidata)
            self.addLinkNode(node1, item.plugin.plugin_name, "#" ,id=str(item.id))        
        
    def buildMenuNodes(self):
        self.buildDataSourceNodes(self.rootNode)
        return True

        
class AlertTreeMenuBuilder(BaseTreeMenuBuilder):
    def __init__(self,root=None,caption=None,id=None,klass=None):
        #node = self.addLINode(root,id,klass)
        #self.addLinkNode(node, caption, "", id, klass)
        #self.rootNode = self.addULNode(node,id,klass)
        pass
    
    def init(self):
        self.prepare()
        self.rootNode = self.addRootNode("div","treeMenu",menuType="alert")
        self.parentNode = self.addULNode(self.rootNode,"menu")

 
    def buildHistoryMenu(self):
        historyMenu = AlertHistoryTreeMenuBuilder(self.parentNode,"History",id="History")
        historyMenu.buildMenuNodes()
        return historyMenu
    
    def buildDataSourceMenu(self):
        dataMenu = DataSourceTreeMenuBuilder(self.parentNode,"DataSource",id="DataSource") 
        dataMenu.buildMenuNodes()
        return dataMenu
    

    def getTreeMenu(self,userId,responseFormat):
        self.buildHistoryMenu()  
        self.buildDataSourceMenu()
        #MenuTree.dump(self.rootNode)
        #self.printxml(self.rootNode)
        return self.toHTML(self.rootNode)
    
# Test suite

class TestAlertTreeMenu(unittest.TestCase):
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
    
    pass

    #print
    #print
    #print
    
    #html = HTMLMenuGenerator()
    #html.tree.prepare()
    #html.generateHTML()
