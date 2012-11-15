'''
Created on Sep 26, 2012

@author: james
'''

from powermonitor.data import *

class Monitor:
    def __init__(self,PLUGIN_NAME,NODE_ID):
        self.plugin_name = PLUGIN_NAME
        self.node_id = NODE_ID
        self.mysql = None
        self.createMysqlDatabase()
    
    def createMysqlDatabase(self):
        self.mysql = MysqlDatabase()
        return self.mysql.connect()
    
    def getTemperatureFormDb(self):
        data_id = self.getLastDataId('hygrothermal')
        temperature = self.getTemperatureFormLastData(data_id)
        return self.toCelsius(temperature)

    
    def toCelsius(self,temperature):
        return float(int(temperature)/100.0)
   
    def getWattByNodeId(self):
	query = """
		select * from power where nodeid='%s';
	"""%(self.node_id)
	#c = self.mysql.cursor()
	#c.execute(query)
	#return c.fetchall()
	self.mysql.query(query)
	result = self.mysql.fetch_row()
        #result = self.mysql.fetch()
	return result
    def getCurrwattFormDb(self):
        data_id = self.getLastDataId('power')
        return self.getCurrwattFormLastData(data_id)

    def getLastDataId(self,table_name):
        query = """
            select MAX(no) FROM %s WHERE nodeid = '%s';
        """%(table_name,self.node_id)
	self.mysql.query(query)
        result = self.mysql.fetch()
	return result[0][0]
    
    def getTemperatureFormLastData(self,data_id):
        query = """
            select temperature FROM hygrothermal where no = '%s';
        """%(data_id)
        
        self.mysql.query(query)
        result = self.mysql.fetch()
	return result[0][0]
    
    def getCurrwattFormLastData(self,data_id):
        query = """
            select currwatt FROM power where no = '%s';
        """%(data_id)
        
        self.mysql.query(query)
        
        result = self.mysql.fetch()
        return  result[0][0]
