#from powermonitor.data import *
#from powermonitor.module import *

import MySQLdb as mdb
import rrdtool

NODE_ID = 100
START_TIME = 1346744730
DATA_SOURCES = ['DS:sum:GAUGE:120:U:U']
rrdtool.create('power_bond.rrd','--start','1346744730',DATA_SOURCES,'RRA:AVERAGE:0.1:15:300','RRA:AVERAGE:0.1:24:300','RRA:AVERAGE:0.1:168:300','RRA:AVERAGE:0.1:672:300','RRA:AVERAGE:0.1:5760:300')
#PLUGIN_NAME = 'power1'

#CpowerMonitor = Monitor(PLUGIN_NAME,NODE_ID)

#results = CpowerMonitor.getWattByNodeId()
#print results


con = mdb.connect('localhost','mhr','mhrinc','esco')
cur = con.cursor()

query = """
	select * from power where nodeid='%s' order by date;
"""%(NODE_ID)

cur.execute(query)
results = cur.fetchall()
#print data

import datetime

for data in results:
	value = data[2]

	data_date = int(data[1].strftime("%s"))
	date_value = data[2]
	data = '%s:%s'%(data_date,date_value)
        rrdtool.update('power_bond.rrd', data)
	#n = datetime.datetime.now()
	
	#print data_date
	#print data_date.split(' ')	
	#date = data_date.split(' ')[0].split('-')
	#time = data_date.split(' ')[1].split(':')
	
	#django_datetime = datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2])
	#print django_datetime

	# datetime.datetime(2006, 8, 11, 23, 32, 43, 109000)
	#future = datetime.datetime.now() 
	#print int(data_date.strftime("%s"))
	#break
	#print n
	#print n.timetuple()
#	date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
