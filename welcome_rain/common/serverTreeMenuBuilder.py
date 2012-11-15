import os
import unittest

#from node import Node
import const
from models import vo_Server
from monitoringNode import * 
from baseTreeMenu import *
from welcome_rain.common.mhrlog import * 

        
class ServerWithGmondTreeMenuBuilder(BaseTreeMenuBuilder):
    def buildServerNodes(self,parentNode):
        for item in vo_Server.objects.filter(gmond_install_flag=1):
            apidata = "server_id" + const.APIDATA_EQUAL + str(item.id)
            node1 = self.addLINode(parentNode,"serverwithgmond",apiName="getServerDetail",apiData=apidata)
            self.addLinkNode(node1, item.ip, "#" ,id=str(item.id))        

    def buildMenuNodes(self):
        self.buildServerNodes(self.rootNode)
        return True
     

class ServerWithoutGmondTreeMenuBuilder(BaseTreeMenuBuilder):
    def buildServerNodes(self,parentNode):
        for item in vo_Server.objects.filter(gmond_install_flag=0):
            apidata = "server_id" + const.APIDATA_EQUAL + str(item.id)
            node1 = self.addLINode(parentNode,"serverwithoutgmond",apiName="getServerDetail",apiData=apidata)
            self.addLinkNode(node1, item.ip, "#" ,id=str(item.id))        
        
    def buildMenuNodes(self):
        self.buildServerNodes(self.rootNode)
        return True

        
class ServerTreeMenuBuilder(BaseTreeMenuBuilder):
    def __init__(self,root=None,caption=None,id=None,klass=None):
        #node = self.addLINode(root,id,klass)
        #self.addLinkNode(node, caption, "", id, klass)
        #self.rootNode = self.addULNode(node,id,klass)
        pass
    
    def init(self):
        self.prepare()
        self.rootNode = self.addRootNode("div","treeMenu",menuType="server")
        self.parentNode = self.addULNode(self.rootNode,"menu")

 
    def buildHistoryMenu(self):
        apidata = "group_type" + const.APIDATA_EQUAL + "1" 
        historyMenu = ServerWithGmondTreeMenuBuilder(self.parentNode,"Installed",id="main_Installed",apiName="getServerGroupList",apiData=apidata)
        historyMenu.buildMenuNodes()
        return historyMenu
    
    def buildDataSourceMenu(self):
        apidata = "group_type" + const.APIDATA_EQUAL + "0" 
        dataMenu = ServerWithoutGmondTreeMenuBuilder(self.parentNode,"Not Installed",id="main_NotInstalled",apiName="getServerGroupList",apiData=apidata) 
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
