'''
Created on Sep 26, 2012

@author: james
'''


from powermonitor.data import *
from powermonitor.module import *


PLUGIN_NAME = 'power1'
NODE_ID = 1

CpowerMonitor = Monitor(PLUGIN_NAME,NODE_ID)
print CpowerMonitor.getTemperatureFormDb()


