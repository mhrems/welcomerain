import socket
import xml.etree.ElementTree as ET
from const import *


class GSocket:
    def __init__(self):
        self.socket = None
    
    def createSocket(self):
        self.socket = None
        
        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            return True
        
        except socket.error:
            print "failed to create socket"
            return False
            
    def open(self,addr,port):
        if not self.createSocket():
            return
        
        self.addr = addr
        self.port = port
        
        try:
            self.socket.connect((self.addr,self.port))
            return True
        
        except socket.error:
            print "failed to connect to server"
            self.close()
            return False
    
    def close(self):
        self.socket.close()

    def send(self,str):
        self.socket.send(str)
        
    def recv(self):
        str = ""
        while True:
            bytes = self.socket.recv(4096)
            if len(bytes)==0:
                break
            str += bytes
        
        return str
    
    
class GMetaReader:
    """
    
    """
    
    def __init__(self):
        self.socket = GSocket()
    
    def getGmetaData(self,request):        
        print "gmetaReader : request=",request
        self.socket.open(GMETAD_IP, GMETAD_PORT)
        self.socket.send(request)
        recv = self.socket.recv()
        self.socket.close()
        
        #print "received XML from gmetad : ",recv
        return recv
    
    def getXMLData(self,request):
        xml = self.getGmetaData(request)
        element = ET.fromstring(xml)
        return xml,element
        
    def getGridSummary(self):
        request = "/?filter=summary\n"
        return self.getXMLData(request)
    
    def getClusterSummary(self,cluster):
        request = "/" + cluster + "?filter=summary\n"
        return self.getXMLData(request)
        
    def getClusterRawData(self,cluster):
        request = "/" + cluster + "\n"
        return self.getXMLData(request)

    def getHostRawData(self,cluster,host):
        request = "/" + cluster + "/" + host + "\n"
        return self.getXMLData(request)


if __name__ == "__main__":
    print "test-start"
    reader = GMetaReader()
    #xml = reader.getGridSummary()
    #xml,element = reader.getClusterSummary("green")
    xml,element = reader.getClusterRawData("green")
    #xml,element = reader.getHostRawData("unspecified","192.168.0.4")

    print xml
    
    #hosts = xml.findall("HOSTS")
                     