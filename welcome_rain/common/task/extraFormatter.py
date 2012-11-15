import os
from pickle import dumps, loads


class GmondPluginExtraFormatter:
    """
    This class is for serialization/deserialization of extra parameter for remote task
    Intended extra format is like following
    
    -list
    -dict
        -field=value
        -field=value
    
     
    """
    
    def __init__(self):
        self.items = []
        self.count = 0
    
    def appendData(self,data):
        self.items.append(data)

    def clear(self):
        self.items = []
    
    def addExtra(self,*args):
        data = dict()
        
        index = 0
        for arg in args:
            print "index=",index," , arg="+arg
            if index%2==0:
                field = arg
            else:
                value = arg
                data[field] = value
                self.appendData(data)
                print "append : field=",field," , value=",value
            index = index+1
            
    def getCount(self):
        return len(self.items)
    
    def serialize(self):
        output = dumps(self.items)
        return output
    
    def deserialize(self,str):
        self.items = loads(str)

    def getItem(self,index):
        return self.items[index]
    
    def getExtra(self,index,field):
        item = self.getItem(index)
        return item[field] 


    
        
class PluginExtraFormatter(GmondPluginExtraFormatter): 
    def addConfNScript(self,conf_file,script_file):
        data = dict()
        data['pyconf'] = conf_file
        data['script'] = script_file
        self.appendData(data)



    
        
if __name__ == "__main__":
    
    conf_file = "/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.pyconf"
    print "dir=",os.path.dirname(conf_file)
    print "file=",os.path.basename(conf_file)
    
    
    formatter = PluginExtraFormatter()
    formatter.addExtra("conf", conf_file , "script","/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.py")
    formatter.addExtra("conf", "/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.pyconf","script","/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.py")
    output = formatter.serialize()
    
    
    formatter.clear()
    
    formatter.deserialize(output)
    output2 = formatter.serialize()
    #print output2
    
    #print "count=",formatter.getCount(), " : field=",formatter.getExtra(0,"script")