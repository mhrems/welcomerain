import xml.etree.ElementTree as MenuTree
import const
from monitoringNode import * 


class BaseTreeMenuBuilder:
    def __init__(self,root,caption,id=None,klass=None,apiName=None,apiData=None):
        self.prepare()
        node = self.addLINode(root,id,klass,apiName=apiName,apiData=apiData)
        self.addLinkNode(node, caption, "", "a_"+id, klass)
        self.rootNode = self.addULNode(node,id,klass)

        
    def prepare(self):
        self.nodeIndex = 0
        self.NODETYPE_TEXT = "text"
        self.NODETYPE_ACTION = "action"

        self.MENUTYPE_DASHBOARD = "dashboard"
        self.MENUTYPE_SERVER = "server"
        self.MENUTYPE_ALERT = "alert"
        self.MENUTYPE_SETTING = "setting"
                    
    def setID(self,node,id):
        if id:
            node.set("id",id)
            self.setNodeID(node, id)
    
    def setNodeID(self,node,id):
        id_postfix = "node" + str(self.nodeIndex)
        node.set("node",id_postfix)
        self.nodeIndex = self.nodeIndex + 1
        
    def setClass(self,node,klass):
        if klass:
            node.set("class",klass)
            
    def setUrl(self,node,url):
        if url:
            node.set("href",url)
            
    def setText(self,node,text):
        if text:
            node.text = text
            
    def setNodeType(self,node,nodeType):
        if nodeType:
            node.set("nodeType",nodeType)
            
    def setAPI(self,node,apiName):
        if apiName:
            node.set("apiName",apiName)
    def setAPIData(self,node,apiData):
        if apiData:
            node.set("apiData",apiData)
    def setMenuType(self,node,menuType):
        if menuType:
            node.set("menuType",menuType)

    def addRootNode(self,rootTag,id,menuType):
        root = MenuTree.Element(rootTag)
        self.setID(root,id)
        self.setMenuType(root,menuType)
        return root
    
    def addULNode(self, parentNode, id=None, klass=None):
        node = MenuTree.SubElement(parentNode, const.NODE_UL)
        self.setID(node, id)
        self.setClass(node,klass)
        return node
    
    def addLINode(self, parentNode, id=None, klass=None,apiName=None, apiData=None):
        node = MenuTree.SubElement(parentNode, const.NODE_LI)
        self.setID(node, id)
        self.setClass(node,klass)
        self.setAPI(node,apiName)
        self.setAPIData(node,apiData)
        if apiName:
            self.setNodeType(node,self.NODETYPE_ACTION)
        else:
            self.setNodeType(node,self.NODETYPE_TEXT)
            
        return node

    def addLINodeWithText(self, parentNode, text,id=None, klass=None):
        node = MenuTree.SubElement(parentNode, const.NODE_LI)
        self.setID(node, id)
        self.setClass(node,klass)
        self.setText(node, text)
        self.setNodeType(node,self.NODETYPE_TEXT)
        return node

    def addLinkNode(self,parentNode, text, url=None, id=None, klass=None, apiName=None, apiData=None):
        node = MenuTree.SubElement(parentNode, const.NODE_LINK)
        self.setText(node, text)
        self.setUrl(node, url)
        self.setID(node, id)
        self.setClass(node,klass)                
        self.setAPI(node,apiName)
        self.setAPIData(node,apiData)
        #self.setNodeType(node,self.NODETYPE_ACTION)
        return node

    def findNode(self,node,nodeText):
        foundNode = node.find(nodeText)
        return foundNode
    
    def buildMenuNodes(self,rootNode):
        pass
    
    def getMenuNodes(self):
        root = self.buildMenuNodes()
        return root
    
    def indent(self,elem, level=0):
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    def printxml(self,elem):
        self.indent(elem)
        print MenuTree.tostring(elem)
    
    def toHTML(self,elem):
        self.indent(elem)
        html = MenuTree.tostring(elem)
        return html


    def convertToHTML(self):

        tree = MenuTree.XML("""
            <menuNode>
                <dataNode>
                    <menuNode>
                        <dataNode>ball</dataNode>
                        <color>red</color>
                        <size>large</size>
                    </menuNode>
                </dataNode>
            </menuNode>
        """)        

        parent = self.addULNode(self.rootNode,"Workload")
        
        node1 = self.addLINode(parent,"index")
        node2 = self.addLinkNode(node1,"index")
        
        parent2 = self.addULNode(node1,"menuNode")
        node3 = self.addLINode(parent2,"test")
        node2 = self.addLinkNode(node3,"index222","url")
        

        MAP = {
            "div":"div",
            const.NODE_UL: "ul",
            const.NODE_LI: "li",
            const.NODE_LINK: "a",
        }
 
        #for elem in self.rootNode.getiterator():
        #    elem.tag = MAP[elem.tag]
        #    if elem:
            #    elem.set("class", klass)
        
        """
        MAP = {
            "div":("div","div"),
            const.NODE_UL: ("ul", "object"),
            const.NODE_LI: ("li", "name"),
            const.NODE_LINK: ("a", "a"),
            "color": ("li", "color"),
            "size": ("li", "size"),
        }
 
        for elem in self.rootNode.getiterator():
            elem.tag, klass = MAP[elem.tag]
            if klass:
                elem.set("class", klass)
        """
        
        #print MenuTree.tostring(self.rootNode)
         