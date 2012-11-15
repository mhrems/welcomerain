'''
Created on Sep 26, 2012

@author: bond
'''
import cont
import serial
import notification

class Communication:
    def __init__(self,SERIAL_PORT,PLUGIN_NAME):
        self.serial = None
        self.serial_port = SERIAL_PORT
        self.plugin_name = PLUGIN_NAME
        self.createCommunication()
        pass
    
    def createCommunication(self):
        if not self.createSerialCommunication():
            print 'Error!!! : Fail to createCommunication'
            notification.EmailNotification().sendEmail('Error!!! : Fail to createCommunication. that plugin name is %s'%(self.plugin_name))
            return False
        return True
    
    def createSerialCommunication(self):
        self.serial = SerialCommunication(self.serial_port)
        return self.serial.connect()
    
    def readStr(self):
#	print 1
        data = self.serial.read()
#	print data
        if not data:
            print 'Error!!! : Fail to readStr'
#            notification.EmailNotification().sendEmail('Error!!! : Fail to readStr. that plugin name is %s'%(self.plugin_name))
            return False
        return data


class SerialCommunication:
    def __init__(self,serial_port):
        self.timeout = cont.SERIAL_TIMEOUT
        self.port = serial_port
        self.connection = None

    
    def connect(self):
        try:
#	    print self.port
#	    print self.timeout
            self.connection = serial.Serial(port=self.port,timeout=self.timeout)
            return True
        except:
            #connection.isOpen()
            return False
    def read(self):
        try:
            return self.connection.readline()
        except:
            return False
