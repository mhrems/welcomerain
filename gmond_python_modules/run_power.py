'''
Created on Sep 26, 2012

@author: bond

getLastrow
return 

'''

from powermonitor.data import *
from powermonitor.module import *


PLUGIN_NAME = 'power1'
NODE_ID = 106

CpowerMonitor = Monitor(PLUGIN_NAME,NODE_ID)
print CpowerMonitor.getCurrwattFormDb()
