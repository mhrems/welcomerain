'''
Created on Sep 26, 2012

@author: bond
'''

import datetime
import os.path
import _mysql
import cont
import notification

class DataWriter:

    def __init__(self,SERIAL_PORT,PLUGIN_NAME):
        self.port = SERIAL_PORT
        self.plugin_name = PLUGIN_NAME
        self.createDatabases()

    def createDatabases(self):
        
        if not self.createMysqlDatabase():
            print "Error!!! : Fail to crate mysql"
#            notification.EmailNotification().sendEmail('Error!!! : Fail to crate mysql. that plugin name is %s'%(self.plugin_name))
            return False
        
        if not self.createTextDatabase():
            print "Error!!! : Fail to crate text file"
#            notification.EmailNotification().sendEmail('"Error!!! : Fail to crate text file". that plugin name is %s'%(self.plugin_name))
            return False
        
        return True
    
    def createMysqlDatabase(self):
        self.mysql = MysqlDatabase()
        return self.mysql.connect()

    def createTextDatabase(self):
        self.textFile= TextDatabase(self.plugin_name)
        return self.textFile.connect()
        
    def write(self,power):
        self.mysql.insertPowerData(power)
        self.textFile.insertPowerData(power)
        
class MysqlDatabase:
    
    def __init__(self):
        self.host = cont.MYSQL_HOST
        self.user = cont.MYSQL_USER
        self.password = cont.MYSQL_PASSWORD
        self.database = cont.MYSQL_DATABASE
        self.connection = None
    
    def connect(self):
        try:
            self.connection = _mysql.connect(host=self.host,user=self.user,passwd=self.password,db=self.database)
            self.checkDatabase()
            return True
        except:
            return False

    
    def checkDatabase(self):
        if not self.checkTable():
            self.createPowerTable()
        return True
    
    def checkTable(self):
        query = """
            show tables like '%s';
        """%(cont.MYSQL_RACK_POWER_TABLE)
        self.query(query)
        result = self.fetch()
        return len(result)

    def createPowerTable(self):
        query = """
            create table %s
            (
                id int auto_increment primary key,
                createdate datetime not null,
                ampere varchar(10) not null,
                port varchar(50) not null,
                plugin_name varchar(50) not null,
                original varchar(255) not null
            )
        """%(cont.MYSQL_RACK_POWER_TABLE)
        self.query(query)
        
    def query(self,sQuery):
        self.connection.query(sQuery)
            
    def fetch(self):
        result = self.connection.store_result()
        return result.fetch_row()
    
    
    def insertPowerData(self,power):
        #print self.oPower.ampere
        #print datetime.datetime.today()
        query = """
            INSERT INTO `%s` (`createdate`, `ampere`,`port`,`plugin_name`,`original`)
            VALUES
            ('%s','%s','%s','%s','%s');
        """%(cont.MYSQL_RACK_POWER_TABLE,datetime.datetime.today(),power.ampere,power.port,power.plugin_name,power.original)
        self.query(query)
        pass
    
    def close(self,connection):
        self.connection.close()
        

class TextDatabase:
    def __init__(self,plugin_name):
        self.plugin_name = plugin_name
        self.filePath = self.getFilePullPath()
        self.filePointer = None

    def getFileName(self):
        return "%s_%s"%(datetime.date.today(),self.oPower.plugin_name)
    
    def getFilePullPath(self):
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'data'))
        return "%s/%s_%s"%(dataPath,datetime.date.today(),self.plugin_name.replace('/','-'))
	#return "%s/%s_%s"%(dataPath,datetime.date.today(),self.plugin_name)
    
    def connect(self):
        self.filePointer = open(self.filePath,"a")
        if not self.filePointer:
            return False
        
        return True

   
    def insertPowerData(self,power):
        self.filePointer.write(power.getTextTypeData())
        self.filePointer.writelines('\n')
        
    def close(self,connection):
        self.filePointer.close()
