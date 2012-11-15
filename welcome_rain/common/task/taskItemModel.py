import os
from taskConst import *



    
class BaseTaskItem:
    def __init__(self,server_id,server_ip,server_type,task_id,task_type,server_user,server_pass,progress,extra):
        self.serverID = server_id
        self.serverIP = server_ip
        self.taskType = task_type
        self.taskID = task_id
        self.serverUser = server_user
        self.serverPass = server_pass
        self.serverType = server_type
        self.taskStatus = TASK_STATUS_NONE
        self.taskOutput = None
        self.taskData = extra
        self.progress = progress

class TaskItem(BaseTaskItem):
    def setStatus(self,status):
        self.taskStatus = status

    def setOutput(self,output):
        self.taskOutput = output


class TaskItems:
    def __init__(self,task_id,task_type,task_data,url,port=80,action=""):
        self.taskID = task_id
        self.apiServer = url
        self.apiPort = port
        self.apiName = action
        self.taskType = task_type
        self.taskData = task_data
        self.output = []
        self.okCount = 0
        self.tasks = []
        self.taskFlag = TASK_STATUS_NONE
    
    def appendOutput(self,output):
        self.output.append(output) 
    
    def addTaskItem(self,taskItem):
        task = self.tasks.append(taskItem)
        return task
    
    def addTask(self,server_id,ip,server_type,task_id,task_type,userID,password,progress,extra=""):
        task = TaskItem(server_id,ip,server_type,task_id,task_type,userID,password,progress,extra)
        return self.addTaskItem(task)
        
    def popTaskItem(self):
        return self.tasks.pop()
    
    def getCount(self):
        return len(self.tasks)

