import taskItemModel
import httplib
import urllib
import urllib2

from taskConst import *
from simplefabric import *


class HTTPTaskPoster:
    def __init__(self,server_url,port,action):
        self.httpParam = dict()
        self.server = server_url
        self.action = action
        self.port = port
        self.timeout = 3
        self.headers = {"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    
    def clear(self):
        self.httpParam = dict()
        
    def addParameter(self,field,value):
        self.httpParam[field] = value
    
    def getHTTPConnection(self):
        conn = httplib.HTTPConnection(self.server,self.port,self.timeout)
        conn.set_debuglevel(1)
        conn.connect()
        return conn
    
    def checkResponse(self,response):
        if response.getcode()==200:
            return True
        return False

    def post(self):
        url = "http://%s:%d%s" % (self.server,self.port,self.action) 
        data = urllib.urlencode(self.httpParam)
        
        print "HTTPTaskPoster : url=",url
        
        try:
            response = urllib2.urlopen(url, data, self.timeout)
            ret = self.checkResponse(response)
            
            return ret
            #print "post url=",url
        
        except urllib2.HTTPError, e:
            if e.getcode()==500:
                print e.read()
            return False
    
    def post2(self):
        client = self.getHTTPConnection()
        
        client.request("POST", self.action, urllib.urlencode(self.httpParam), self.headers)
        response = client.getresponse()
        ret = self.checkResponse(response)
        
        client.close()
    
        return ret
    
    
    def postTaskStatus(self,taskItem):
        self.clear()
        self.addParameter("task_id", taskItem.taskID)
        self.addParameter("server_id", taskItem.serverID)
        self.addParameter("server_ip", taskItem.serverIP)
        self.addParameter("status_flag", taskItem.taskStatus)
        self.addParameter("progress", taskItem.progress)
        self.addParameter("message", taskItem.taskOutput)
        
        print "httpParam = ",self.httpParam
        
        return self.post()
        
    
    def listToString(self,output):
        result = ""
        for line in output:
            if isinstance(line, basestring):
                result = result + line + "\n"
        return result
    
    def postUpdateTask(self,tasks):
        self.clear()
        self.addParameter("task_id", tasks.taskID)
        self.addParameter("task_ok_count", tasks.okCount)
        self.addParameter("task_flag", tasks.taskFlag)
        self.addParameter("task_data", self.listToString(tasks.output))
 
        return self.post()
        
        
class BaseCommand(SimpleFabric):
    def postTaskStatus(self,task,url,port):
        poster = HTTPTaskPoster(url,port,action=API_ADD_TASKSTATUS)
        
        if not poster.postTaskStatus(task):
            print "ServerInspectionExecute.postTaskStatus : Fail to update to server"
            return False
        
        return True
    
    def assertResult(self):
        pass
    
    def run(self,task):
        pass

    def checkTask(self):
        pass
    
    def setResult(self,task):
        taskStatus = TASK_STATUS_FAIL
        if self.checkTask():
            taskStatus = TASK_STATUS_OK
        
        task.setOutput(self.history.toString())    
        task.setStatus(taskStatus)

    def isTaskSuccessful(self,task):
        if task.taskStatus == TASK_STATUS_FAIL:
            return False
        return True
    