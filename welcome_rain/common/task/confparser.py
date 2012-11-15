import io
import re
import cStringIO
from pyparsing import *
import xml.etree.ElementTree as Tree


COLLECTION_GROUP = "collection_group"
MODULES = "modules"
MODULE = "module"
METRIC = "metric"
INCLUDE = "includes"

class BaseASTree:
    def __init__(self):
        self.rootNode =self.addRootNode("root")
        self.currentParentNode = self.rootNode
        self.groupCount = 0;
        self.collectNodeFlag = False
        self.groupNode = self.rootNode
        
    def setID(self,node,id):
        if id:
            node.set("id",id)

    def setValue(self,node,value):
        if id:
            node.set("value",value)

    def setClass(self,node,klass):
        if klass:
            node.set("class",klass)

    def addRootNode(self,rootTag):
        root = Tree.Element(rootTag)
        #self.setID(root,id)
        #self.setClass(root,klass)
        return root

    def addParentNode(self,parentNode, parentTag,id=None, klass=None):
        node = Tree.SubElement(parentNode, parentTag)
        self.setID(node, id)
        self.setClass(node,klass)
        return node

    def addChildNode(self,parentNode, childTag,id=None, value=None, klass=None):
        node = Tree.SubElement(parentNode, childTag)
        self.setID(node, id)
        self.setValue(node, value)
        self.setClass(node,klass)
        return node
    
    def findNode(self,node,str):
        return node.find(str)

    def findNodeExt(self,node,str,id):
        found = node.find(str)
        if found==None:
            return found
        if found.get("id")==id:
            return found
        return None
    
    
    def isMetricNode(self,items):
        try:
            item = items[0][0][0]
            return True
        except:
            return False
        
        
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
    
    def printhtml(self,elem):
        self.indent(elem)
        print Tree.tostring(elem)
    
    def toHTML(self,elem):
        self.indent(elem)
        html = Tree.tostring(elem)
        return html


class ConfWriter:
    def __init__(self,indent=4):
        self.indent = indent
        self.stream = cStringIO.StringIO()
        
    def getIndent(self,index):
        return " " * self.indent*index
    
    def isNumber(self,value):
        try:
            n = str(float(value))
            if n=="nan" or n=="inf" or n=="-inf": return False
        except ValueError:
            try:
                complex(value)
            except ValueError:
                return False
        return True
    
    def isBoolean(self,value):
        if value.lower()=="yes" or value.lower()=="no":
            return True
        return False
    
    def isIPAddress(self,value):
        tokens = value.split(".")
        if len(tokens)!=4:
            return False
        
        for token in tokens:
            if not self.isNumber(token):
                return False
            
            if not 0 <= int(token) <= 255:
                return False
        return True
    
    def getDataValue(self,value):
        if self.isNumber(value):
            return value
        elif self.isBoolean(value):
            return value
        elif self.isIPAddress(value):
            return value
        else:
            return "\"" + value + "\""
    
    def isMetricNode(self,elem):
        if elem.tag==METRIC:
            return True
        return False
    
    def isGroupCollectionNode(self,elem):
        if elem.tag==COLLECTION_GROUP:
            return True
        return False
    
    def isModulesNode(self,elem):
        if elem.tag==MODULES:
            return True
        return False
    
    def isIncludeNode(self,elem):
        if elem.tag==INCLUDE:
            return True
        return False

    def addString(self,str):
        self.stream.write(str+"\n")
    
    def writeGroupCollectionNode(self,elem):
        self.addString(elem.tag + " {")
        for node in elem:
            if self.isMetricNode(node):
                self.writeMetricNode(node,1)
            else:
                self.writeDataNode(node,1)
            
        self.addString("}\n")
    
    def writeDataNode(self,elem,indentIndex):
        output = self.getIndent(indentIndex) + elem.tag + " = " + self.getDataValue(elem.get("value"))
        self.addString(output)
        
    def writeMetricNode(self,elem,indentIndex):
        self.addString(self.getIndent(indentIndex) + elem.tag + " {")
        for node in elem:
            self.writeDataNode(node,indentIndex+1)
        self.addString(self.getIndent(indentIndex)+ "}")
        

    def writeModulesNode(self,elem):
        self.addString(elem.tag + " {")
        for module in elem:
            self.addString(self.getIndent(1)+"module {")
            for node in module:
                self.writeDataNode(node,2)
            self.addString(self.getIndent(1) + "}")
        self.addString("}\n")
    
    def writeIncludeNode(self,elem):
        for node in elem:
            self.addString(node.tag)
    
        self.addString("\n")
     
    def writeGeneralNode(self,elem):
        self.addString(elem.tag + " {")
        for node in elem:
            self.writeDataNode(node,1)
        self.addString("}\n")
        
    def writeFile(self,filename,text):
        
        #with io.open(filename,"wt") as file:
        print "filename="+filename
        
        file = open(filename,"wb")
        file.write(text.encode("utf-8"))
        file.close()
        
        return True
        
    def writeToFile(self,parsedTree,filename):
        
        for elem in parsedTree:
            #print "elem=",elem.tag
            if self.isGroupCollectionNode(elem):
                self.writeGroupCollectionNode(elem)            
            elif self.isIncludeNode(elem):
                self.writeIncludeNode(elem)
            elif self.isModulesNode(elem):
                self.writeModulesNode(elem)
            else:
                self.writeGeneralNode(elem)
        
        
        ret = self.writeFile(filename, self.stream.getvalue())
        
        self.stream.close()
        
        return ret


class ConfASTree(BaseASTree):
    def addCollectionGroupNode(self):
        node = self.addParentNode(self.rootNode, COLLECTION_GROUP, id=str(self.groupCount))
        self.groupCount = self.groupCount + 1;
        return node, self.groupCount-1
    
    def addCollectionGroupDataNode(self,groupNode,field,value):
        return self.addChildNode(groupNode,field,value=value)
        
    def getCollectionGroupNode(self,id):
        return self.findNodeExt(self.rootNode,COLLECTION_GROUP,id)
                
    def getCollectionGroupDataNode(self,groupNode,field):
        return self.findNode(groupnode, field)

    def addMetricNode(self,groupNode):
        return self.addParentNode(groupNode, METRIC, id=groupNode.get("id"))

    def addMetricDataNode(self,metricNode,field,value):
        return self.addChildNode(metricNode,field,value=value)

    def addModulesNode(self):
        node = self.addParentNode(self.rootNode, MODULES)
        return node

    def addIncludeNode(self):
        node = self.addParentNode(self.rootNode, INCLUDE)
        return node

    def addIncludeDataNode(self,includeNode,field,value):
        return self.addChildNode(includeNode,field,value=value)

    def getModulesNode(self):
        return self.findNode(self.rootNode,MODULES)

    def getIncludeNode(self):
        return self.findNode(self.rootNode,INCLUDE)

    def addModuleNode(self):
        parentNode = self.getModulesNode()
        node = self.addParentNode(parentNode, MODULE)
        return node
    
    def getModuleNode(self,id):
        parentNode = self.getModulesNode()
        if not parentNode:
            return None
        return self.findNodeExt(parentNode, MODULE, id)
            
    def addModuleDataNode(self,moduleNode,field,value):
        self.addChildNode(moduleNode, field, value=value)
        
    def xmltodict(self,element):
        if not isinstance(element, Tree.Element):
            raise ValueError("must pass xml.etree.ElementTree.Element object")
    
        def xmltodict_handler(parent_element):
            result = dict()
            for element in parent_element:
                if len(element):
                    obj = xmltodict_handler(element)
                else:
                    obj = element.text
    
                if result.get(element.tag):
                    if hasattr(result[element.tag], "append"):
                        result[element.tag].append(obj)
                    else:
                        result[element.tag] = [result[element.tag], obj]
                else:
                    result[element.tag] = obj
            return result
    
        return {element.tag: xmltodict_handler(element)}


    def toConf(self,element):
        if not isinstance(element, Tree.Element):
            raise ValueError("must pass xml.etree.ElementTree.Element object")
        
        def toConf_handler(parent_element):
            result = []
            for element in parent_element:
                if len(element):
                    obj = toConf_handler(element)
                else:
                    obj = element.text
    
                """
                if result.get(element.tag):
                    if hasattr(result[element.tag], "append"):
                        result[element.tag].append(obj)
                    else:
                        result[element.tag] = [result[element.tag], obj]
                else:
                    result[element.tag] = obj
                """
                result.append(element.tag)
                
            return result
    
        return toConf_handler(element)


    def writeToFile(self,element,filename):
        writer = ConfWriter()
        return writer.writeToFile(element, filename)

            
        
    
        
astree = ConfASTree()

class GMondConfParser:
    """a class which parse gmond.conf file"""
    
    def __init__(self):
        self.prepare()

    def convertNumbers(s,l,toks):
        n = toks[0]
        try:
            return int(n)
        except ValueError, ve:
            print "Fatal Error : convertNumbers , s=",n
            return float(n)
    
    def joinStrings(s,l,toks):
        """Join string split over multiple lines"""
        return ["".join(toks)]
    

    def handleValue(s,l,toks):
        print ">>>handleValue : ",toks

    def handleData(s,l,toks):
        #depth = astree.getListDepth(toks.asList())
        print "---handleData : " ,toks
        if len(toks[0])==2:
            astree.addChildNode(astree.currentParentNode,toks[0][0],value=toks[0][1])

    def handleName(s,l,toks):
        
        if toks[0]=="module":
            astree.collectNodeFlag = False
            astree.currentParentNode = astree.findNode(astree.rootNode, "modules")
            if astree.currentParentNode==None:
                astree.currentParentNode = astree.currentParentNode = astree.addParentNode(astree.rootNode,"modules")
            astree.currentParentNode = astree.addParentNode(astree.currentParentNode,toks[0])
        elif toks[0]=="collection_group":
            astree.collectNodeFlag = True
            astree.groupNode = astree.addParentNode(astree.rootNode,toks[0],id=str(astree.groupCount))  
            astree.currentParentNode = astree.groupNode           
            astree.groupCount = astree.groupCount + 1
        elif toks[0]=="metric":
            if astree.collectNodeFlag:
                astree.currentParentNode = astree.addParentNode(astree.groupNode,toks[0])
        else:
            astree.collectNodeFlag = False
            astree.currentParentNode = astree.addParentNode(astree.rootNode,toks[0])
        
        print ">>>handleName : " , toks

    def handleNested(s,l,toks):
        #depth = getListDepth(toks)
        #if depth==1:
        #    itemStack = []
        itemStack.append(toks[0])
        print ">>>handleNested : " , toks , " , stack=",itemStack,l

    def handleObject(s,l,toks):
        #depth = getListDepth(toks)
        #if depth==1:
        #    itemStack = []
        itemStack.append(toks[0])
        print ">>>handleObject : " , toks , " , stack=",itemStack,l

    def handleField(s,l,toks):
        depth = getListDepth(toks)
        #if depth==1:
        #    itemStack = []
        #itemStack.append(toks[0])
        print ">>>handleField : " , toks , " , depth=",depth, " , stack=",itemStack
    
        
    def prepare(self):
        confString = dblQuotedString.setParseAction( removeQuotes )
        
        confNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                            Optional( '.' + Word(nums) ) +
                            Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
        confNumber.setParseAction( self.convertNumbers )
        
        confIPAddress = Word("0123456789") + "." + Word("0123456789") + "." + Word("0123456789") + "." + Word("0123456789")
        
        self.confObject = Forward()
        confValue = Forward()

        confName = Word('$'+'.'+'_'+alphas+nums)
        confName.setParseAction(self.handleName)

        confAlpha = Word('$'+'.'+'_'+alphas+nums)
        #confAlpha.setParseAction(self.handleName)

        confField = Word('$'+'.'+'_'+alphas+nums)
        #confField.setParseAction(self.handleField)
 
        
        confElements = delimitedList( confValue )
        confArray = Group(Suppress('[') + Optional(confElements) + Suppress(']') )
        confValue << ( confAlpha | confNumber | confString )
        #confValue.setParseAction( self.handleValue )
        
        confNested = Group(self.confObject)
        #confNested.setParseAction( self.handleNested )
              
        #memberDef = Group( confField + Suppress("=") + confValue | Group(self.confObject) | confValue)
        memberDef = Group( confField + Suppress("=") + confValue | confNested )
        memberDef.setParseAction( self.handleData )
        
        confMembers = OneOrMore( memberDef )
        #confMembers.setParseAction(self.handleObject)
        
        commandString = Regex(r'\"(?:\\\"|\\\\|[^"])*\"', re.MULTILINE)
        commandString.setParseAction( removeQuotes )
        #confCommand = Group(CaselessKeyword("include") + restOfLine)
        
        #confCommandValue << ( confName | confNumber | confString )
        confCommand = (CaselessKeyword("include") + Optional(Suppress('(') + confString + Suppress(')')))
        
        self.confObject <<  OneOrMore( (confName + Optional(Suppress('{') + Optional(confMembers) + Suppress('}'))) ) 
        #self.confObject <<  OneOrMore( (confName + Optional(Suppress('{') + Optional(confMembers) + Suppress('}'))) | (confName + Optional(Suppress('(') + Optional(confMembers) + Suppress(')'))) ) 
        #jsonObject << Dict(Optional(jsonMembers))
        
        singleLineCommand = (CaselessKeyword("include") + restOfLine)
        self.confObject.ignore( singleLineCommand )

        confComment = cppStyleComment 
        self.confObject.ignore( confComment )


    def removeComments(self,src):
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return ""
            else:
                return s
            
        pattern = re.compile(
                            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
                            re.DOTALL | re.MULTILINE
                            )
        return re.sub(pattern, replacer, src)


    def parseInclude(self,src):
        pattern = r'^include(.*)$'
        
        parentNode = astree.addParentNode(astree.rootNode,"includes")
        for match in re.finditer(pattern, src, re.M|re.I):
            astree.addChildNode(parentNode,match.group(),value="include")

    def readFile(self,filename):
        f = file(filename)
        s = f.read()
        f.close()
        return s
    
    def parseFromFile(self,filename):
        text = self.readFile(filename)
        results = self.parse(text,True);    
    
    def parse(self,src,withInclude=True):
        
        try:
            
            cleanedSrc = self.removeComments(src)
            results = self.confObject.parseString(cleanedSrc)
            #print "pyparsing " , results.__class__
            #pprint.pprint(results.asXML())
            if withInclude:
                self.parseInclude(cleanedSrc)
            
            return results
        
        except ParseException, err:
            print err.line
            print " "*(err.column-1) + "^"
            print err
            return
    

        


if __name__ == "__main__":

    import pprint

    def readFile(filename):
        f = file(filename)
        s = f.read()
        f.close()
        return s
    
        
    try:
        
        fileName = "/home/james/Workspace/Project/WelcomeRain/gmond.conf"
        data = readFile(fileName)

        parser = GMondConfParser()
        results = parser.parseFromFile(fileName);
        
        
        node, id = astree.addCollectionGroupNode()
        astree.addCollectionGroupDataNode(node, "james", "ahn")
        astree.addCollectionGroupDataNode(node, "taehee", "kim")
        astree.addCollectionGroupDataNode(node, "nayoung", "lee")
               
        metricNode = astree.addMetricNode(node)
        astree.addMetricDataNode(metricNode, "field", "value")
        astree.addMetricDataNode(metricNode, "name", "hahaha")
        
        module = astree.addModuleNode()
        astree.addModuleDataNode(module, "module1", "value1")
        astree.addModuleDataNode(module, "module2", "value2")
        astree.addModuleDataNode(module, "module3", "value3")
        
        #astree.printhtml(astree.rootNode)
        
        stream = astree.writeToFile(astree.rootNode, "/home/james/Workspace/Project/WelcomeRain/gmondx.conf")
        #print stream.getvalue()

        
    except ParseException, err:
        print err.line
        print " "*(err.column-1) + "^"
        print err
