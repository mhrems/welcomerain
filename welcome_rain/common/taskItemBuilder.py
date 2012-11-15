import os

from welcome_rain.common.models import *
from welcome_rain.common.mhrlog import *
from welcome_rain.common.task.taskConst import *
from welcome_rain.common.task.taskItemModel import *
from welcome_rain.common.task.extraFormatter import *

###################################################################################################################
# TaskItemBuilder
###################################################################################################################

class TaskItemBuilder():
    def __init__(self,request,task_items):
        self.request = request
        self.taskItems = task_items
            
    def getServerInstance(self,server_id):
        server = vo_Server.objects.get(id=server_id)
        return server
    
    def getPluginInstance(self,plugin_id):
        plugin= vo_Plugin.objects.get(id=plugin_id)
        return plugin
        
    def getDataFromArguments(self,data,index):
        return self.getSplitObject(data,self.customSplitChr)[index]
    
    def getForRangeFromServerIp(self,sServerIp):
        return range(len(self.getSplitObject(sServerIp,self.customSplitChr)))
    
    def getSplitObject(self,splitStr,splitChr):
        return splitStr.split(splitChr)
    
    def addFullPath(self,oPath):
        oFullPath = []
        for path in oPath:
            oFullPath.append('/home/james/djagno_project/welcome_rain/welcom_rain/media/'+path)
        return oFullPath

        
    def buildExtraPlugin(self,task_data):
        logInfo("TaskItemBuilder.buildExtraPlugin : task_data="+task_data)
        
        formatter = PluginExtraFormatter()
        
        plugins = task_data.split(",")
        for plugin in plugins:
            plugin_instance = self.getPluginInstance(plugin)
            #logInfo("TaskItemBuilder.buildExtraPlugin : plugin="+plugin)            

            if not plugin_instance:
                logError("TaskItemBuilder.buildTaskItem : fail to get server instance with server_id="+server_id)
                continue
            
            pyconf = plugin_instance.pyconf 
            script = plugin_instance.script
            
            formatter.addConfNScript(pyconf,script)
        
        extra = formatter.serialize()
        return extra
    
    
    def buildExtra(self):
        if self.taskItems.taskType==str(TASK_INSTALL_GMOND):
            return ""
        
        if self.taskItems.taskType==str(TASK_INSTALL_PLUGIN):
            return self.buildExtraPlugin(self.taskItems.taskData)
            
        if self.taskItems.taskType==str(TASK_INSTAll_GMETAD):
            return ""
        
        if self.taskItems.taskType==str(TASK_SERVER_INSPECTION):
            return ""

        
    def buildTaskItem(self,server_id,server_count,index):
        
        server = self.getServerInstance(server_id)
        if not server:
            logError("TaskItemBuilder.buildTaskItem : fail to get server instance with server_id="+server_id)
            return


        
        extra = self.buildExtra()
        progress = str(server_count)+","+str(index)
        print "taskItemBuilder.buildTaskItem : progress="+progress

        #logInfo("taskItemBuilder.buildTaskItem : progress="+progress)
        #logInfo("taskItemBuilder.buildTaskItem : extra="+extra)
        
        self.taskItems.addTask(server_id=server_id,
                          ip=server.ip,
                          server_type=server.server_type,
                          task_id=self.taskItems.taskID,
                          task_type=self.taskItems.taskType,
                          userID=server.server_userid,
                          password=server.server_password,
                          progress=progress,
                          extra=extra)

    
    def build(self):

        logInfo("taskItemBuilder.build : type="+self.taskItems.taskType+ " , data="+self.taskItems.taskData)
                
        #taskItems = TaskItems(self.taskID,self.url,self.port)
        #gTaskItems.addTask(server_id=3,ip="192.168.0.111",task_id=1,task_type=taskType,task_param="",userID="root",password="mhrinc",extra=extra)
 
        server_id = self.request.POST['server_id']
        servers = server_id.strip().split(",")
        server_count = len(servers)
        index = 1
        for server in servers:
            logInfo("taskItemBuilder.build : server="+server)
            self.buildTaskItem(server,server_count,index)
            index = index + 1   
    
