'''
Created on Sep 26, 2012

@author: bond


base environment

apt-get update

apt-get install mysql-server
apt-get install python-mysqldb

apt-get install minicom
apt-get install vsftpd

apt-get install ganglia-monitor
apt-get install gmetad

'''

from powermonitor.communication import *
from powermonitor.model import *
from powermonitor.data import *
from powermonitor.notification import *
import sys

#global SERIAL_PORT
#global PLUGIN_NAME



SERIAL_PORT = '/dev/ttyUSB0'
PLUGIN_NAME = 'rack1'

Ccomunication = Communication(SERIAL_PORT,PLUGIN_NAME)
CpowerProxy = PowerProxy(SERIAL_PORT,PLUGIN_NAME)
CdataWriter = DataWriter(SERIAL_PORT,PLUGIN_NAME)


data = Ccomunication.readStr()

if not data:
    sys.exit(0)

CpowerProxy.addPowerDataByRawData(data)
CdataWriter.write(CpowerProxy.getLastData())

print CpowerProxy.getLastData().plugin_name
print CpowerProxy.getLastData().ampere


