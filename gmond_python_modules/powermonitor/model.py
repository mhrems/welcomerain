'''
Created on Sep 26, 2012

@author: bond
'''
import cont
import datetime

class PowerProxy:
    def __init__(self,SERIAL_PORT,PLUGIN_NAME):
        self.items = []
	self.dataBuilder = AdPowerBuilder(SERIAL_PORT,PLUGIN_NAME)

    def addPowerData(self,power):
        self.items.append(power)
    
    def clear(self):
        self.items = []
    
    def getCount(self):
        return len(self.items)
    
    def getDataByIndex(self,index):
        if index>self.getCount():
            print "Error!!! : index is out of bound!!! , index=",index
            return None
        
        return self.items[index]
    
    def addPowerDataByRawData(self,data):
        data = self.dataBuilder.createPowerObject(data)
        self.addPowerData(data)
        return data
        
    def getLastData(self):
        return self.getDataByIndex(self.getCount()-1)
    
class AdPowerBuilder():

    def __init__(self,SERIAL_PORT,PLUGIN_NAME):
	self.port = SERIAL_PORT
	self.plugin_name = PLUGIN_NAME
    
    def createPowerObject(self,data):
        if not self.checkValue(data):
            print 'Error!!! : Fail to createPowerObject'
            return False
        oData = self.createPowerData(data)
        return self.createObject(oData,data)
    
    def checkValue(self,data):   
        data = data.strip()
        if(len(data)<cont.AD_DATA_MIN_LEN):
            return False
        if(data[0]!=cont.AD_DATA_START_STR):
            return False
        if(data[len(data)-1]!=cont.AD_DATA_END_STR):
            return False
        return True
    
    def createPowerData(self,data):
        strData = data
        new_data = ''
        addseparator = True
        for min_str in strData[2:len(strData)-1]:
            if not min_str==' ':
                if not min_str.isdigit():
                    if addseparator:
                        min_str = cont.ADPOWER_KEY_VALUE_SEPARATOR+min_str
                        addseparator = False
                else:
                    addseparator = True
                new_data = new_data + min_str
        
        oData = new_data.split(':')
        return oData
    
    def createObject(self,oData,data):
        return Power(oData[1].split(cont.ADPOWER_KEY_VALUE_SEPARATOR)[0],data,self.port,self.plugin_name)
    

class PowerManager:
    def getTextTypeData(self):
        return "datetime=%s|ampere=%s|port=%s|plugin_name=%s|original=%s"%(datetime.datetime.today(),self.ampere,self.port,self.plugin_name,self.original)


class Power(PowerManager):
    def __init__(self,ampere,original,port,plugin_name):
        self.ampere = ampere
        self.original = original
        self.port = port
        self.plugin_name = plugin_name
