import datetime
import threading

from baseCommand import *
from taskItemModel import TaskItems
from taskConst import *
from taskCommand import *
from taskCommandFedora import *
from extraFormatter import *



class TaskHandler():
    def __init__(self,tasks):
        self.tasks = tasks
            
    def postUpdataTask(self):
        http = HTTPTaskPoster(self.tasks.apiServer,self.tasks.apiPort,action=API_UPDATE_TASK)
        
        self.tasks.taskFlag = TASK_STATUS_FAIL
        if self.tasks.getCount()==self.tasks.okCount:
            self.tasks.taskFlag = TASK_STATUS_OK
            
        if not http.postUpdateTask(self.tasks):
            print "TaskHandler.postUpdataTask : Fail to update to server"
            return False
        return True
    
    
    def execute(self):
        self.tasks.okCount = 0
        task_data = self.tasks.taskData
        for taskItem in self.tasks.tasks:
            task = self.getTaskExecuteClass(taskItem)
            task.setFabircEnvironment(taskItem.serverIP,taskItem.serverUser,taskItem.serverPass)
            ret = task.run(taskItem,url=self.tasks.apiServer,port=self.tasks.apiPort,task_data=task_data)
            self.tasks.appendOutput(taskItem.taskOutput)

            if ret:
                self.tasks.okCount = self.tasks.okCount + 1

            #print "TaskHandler.execute : ", output
            
        self.postUpdataTask()
        
        #CtaskExecute.setFabircEnvironment(oTask.serverIp,oTask.serverUserId,oTask.serverUserPass)

    def getTaskExecuteClass(self,taskItem):
        if taskItem.serverType==LINUX_UBUNTU:
            return self.getTaskExecuteClassUbuntu(taskItem.taskType)
        
        if taskItem.serverType==LINUX_FEDORA:
            return self.getTaskExecuteClassFedora(taskItem.taskType)
            
            
    def getTaskExecuteClassUbuntu(self,taskType):
        nTaskType = int(taskType)
        
        if nTaskType == TASK_INSTALL_GMOND:
            return GmondInstallExecute()
        elif nTaskType == TASK_INSTALL_PLUGIN:
            return GmondPluginInstallExecute()
        elif nTaskType == TASK_INSTAll_GMETAD:
            return GmetadInstallExecute()
        elif nTaskType == TASK_SERVER_INSPECTION:
            return ServerInspectionExecute()


    def getTaskExecuteClassFedora(self,taskType):
        nTaskType = int(taskType)
        
        if nTaskType == TASK_INSTALL_GMOND:
            return GmondInstallExecuteFedora()
        elif nTaskType == TASK_INSTALL_PLUGIN:
            return GmondPluginInstallExecuteFedora()
        elif nTaskType == TASK_INSTAll_GMETAD:
            return GmetadInstallExecuteFedora()
        elif nTaskType == TASK_SERVER_INSPECTION:
            return ServerInspectionExecuteFedora()



class RemoteTaskManager(threading.Thread):
    def __init__(self,taskitems):
        threading.Thread.__init__(self)
        self.taskItems = taskitems
        print "RemoteTaskManager.init"
    
    
    def run(self):
        aHandler = TaskHandler(self.taskItems)
        aHandler.execute()
    
    



if __name__ == "__main__":
    
    import pprint
    
    arguments ={
            'serverIp' : '192.168.0.84,192.168.0.84',
            'serverId' : '1,2',
            'serverUserId' : 'root,root',
            'serverUserPass' : 'mhrinc,mhrinc',
            'userId' : '1',
            'taskType' : '1',
            'taskId' : '23',
            'plugInId' : '1,2',
            'plugInConfPath' : 'plugin/network-netstats/netstats.basic.pyconf',
            'plugInScriptPath' : 'plugin/network-netstats/netstats.py',
    }

    taskType = TASK_INSTAll_GMETAD
    taskType = TASK_INSTALL_GMOND
    taskType = TASK_INSTALL_PLUGIN
    taskType = TASK_SERVER_INSPECTION
    

    formatter = PluginExtraFormatter()
    formatter.addConfNScript("/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.pyconf","/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.py")
    formatter.addConfNScript("/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.pyconf","/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.py")

    #formatter.addExtra("pyconf",  , )
    #formatter.addExtra("pyconf", "/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.pyconf","script","/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.py")
    extra = formatter.serialize()
    
    print "format_count=",formatter.getCount()
    
    gTaskItems = TaskItems(task_id=1,task_type="1",task_data="1",url="192.168.0.29",port=8080)
    gTaskItems.addTask(server_id=3,ip="192.168.10.12",server_type=LINUX_UBUNTU,task_id=1,task_type=taskType,userID="james",password="mhrinc",progress="1,1",extra=extra)
    #gTaskItems.addTask(id=4,ip="192.168.0.112",task_id=1,task_type=taskType,task_param="",userID="root",password="mhrinc")
    #gTaskItems.addTask(id=5,ip="192.168.0.113",task_id=1,task_type=taskType,task_param="",userID="root",password="mhrinc")
    #gTaskItems.build()
    
    #pprint.pprint(gTaskItems.tasks)
     
    CremoteTask = RemoteTaskManager(gTaskItems)
    CremoteTask.start()
