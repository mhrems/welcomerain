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

"""      
class SettingTreeMenuBuilder(BaseTreeMenuBuilder):    
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
"""
     

class ConfigTreeMenuBuilder(BaseTreeMenuBuilder):
    def buildConfigNodes(self,parentNode):        
        node1 = self.addLINode(parentNode,"Database")
        self.addLinkNode(node1, "General", "#" ,id="1")        
        
        node2 = self.addLINode(parentNode,"GMetaD")
        self.addLinkNode(node2, "GMetad", "#" ,id="2")        

        node3 = self.addLINode(parentNode,"GMondConf")
        self.addLinkNode(node3, "GMond Conf", "#" ,id="3")        

    def buildMenuNodes(self):
        self.buildConfigNodes(self.rootNode)
        return True

        
class SettingTreeMenuBuilder(BaseTreeMenuBuilder):
    def __init__(self,root=None,caption=None,id=None,klass=None):
        #node = self.addLINode(root,id,klass)
        #self.addLinkNode(node, caption, "", id, klass)
        #self.rootNode = self.addULNode(node,id,klass)
        pass
    
    def init(self):
        self.prepare()
        self.rootNode = self.addRootNode("div","treeMenu",menuType="setting")
        self.parentNode = self.addULNode(self.rootNode,"menu")

    
    def buildConfigMenu(self):
        dataMenu = ConfigTreeMenuBuilder(self.parentNode,"Setting",id="setting") 
        dataMenu.buildMenuNodes()
        return dataMenu
    

    def getTreeMenu(self,userId,responseFormat):
        self.buildConfigMenu()  
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
