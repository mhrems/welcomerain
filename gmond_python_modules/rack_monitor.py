'''
Created on Sep 26, 2012

@author: bond
'''
from powermonitor.communication import *
from powermonitor.model import *
from powermonitor.data import *
from powermonitor.notification import *
import sys


NAME_PREFIX = 'rack_'


def rack_handler(name):
    #	import serial
    #	import time

    #ser = serial.Serial(port='/dev/ttyUSB0',timeout=1)
    #print ser.readline()
    try:
    	SERIAL_PORT = name[len(NAME_PREFIX):].replace('-','/')
    	PLUGIN_NAME = name
#	SERIAL_PORT = '/dev/ttyUSB0'
#	ser = serial.Serial(port='/dev/ttyUSB0',timeout=1)
#	data = ser.readline()
#	print data
        #print SERIAL_PORT
	#print PLUGIN_NAME
    	Ccomunication = Communication(SERIAL_PORT,PLUGIN_NAME)
    	CpowerProxy = PowerProxy(SERIAL_PORT,PLUGIN_NAME)
	print 1
    	CdataWriter = DataWriter(SERIAL_PORT,PLUGIN_NAME)
	print 2
    	CpowerProxy.addPowerDataByRawData(Ccomunication.readStr())
    	print 3
	CdataWriter.write(CpowerProxy.getLastData())
#	return 800.8
	print CpowerProxy.getLastData().ampere
#	print name
#	return 2
  	return float(CpowerProxy.getLastData().ampere)
    except:
	print 4
#	notification.EmailNotification().sendEmail('Error!!! : Fail to get rack data. that plugin name is %s'%(PLUGIN_NAME))
	return 0


def create_desc(skel, prop):
    d = skel.copy()
    for k,v in prop.iteritems():
        d[k] = v
    return d

def metric_init(params):
    global descriptors, metric_map, Desc_Skel

    descriptors = []
    
    Desc_Skel = {
          'name': 'XXX',
          'call_back': rack_handler,
          'time_max': 90,
          'value_type': 'float',
          'units': 'xxx',
          'slope': 'both',
          'format': '%.4f',
          'description': 'bond of host',
          'groups': 'rack'
    }
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB0",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB1",
    }))   
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB2",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB3",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB4",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB5",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB6",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB7",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB8",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "-dev-ttyUSB9",
    }))
    return descriptors

def metric_cleanup():
    '''Clean up the metric module.'''
    pass

#This code is for debugging and unit testing
if __name__ == '__main__':
    metric_init({})
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for %s is %u' % (d['name'],  v)
