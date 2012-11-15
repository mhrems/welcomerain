from fabric.api import *
from taskConst import *


class CommandHistory:
    def __init__(self,cmd,output, errCode=0):
        self.command = cmd
        self.output = output
        self.errorCode = errCode
        
        
class CommandHistoryManager:
    def __init__(self):
        self.history = []
    
    def clear(self):
        self.history = []
        
    def appendCommand(self,data):
        self.history.append(data)
        
    def addCommand(self,cmd,output):
        command = CommandHistory(cmd,output,TASK_HISTORY_OK)
        self.appendCommand(command)
    
    def addError(self,cmd,errMsg):
        command = CommandHistory(cmd,errMsg,TASK_HISTORY_ERROR)
        self.appendCommand(command)
        
    def popCommandHistory(self):
        return self.history.pop()
        
    def getCount(self):
        return len(self.history)
    
    def getCommandByIndex(self,index):
        if index>=self.getCount():
            return None
        return self.history[index]

    def getLastOutput(self):
        historyCount = self.getCount()
        if historyCount==0:
            return None
        
        return self.history[historyCount-1]

    def searchText(self,str):
        output = self.toString()
        return output.find(str)
        
    def toString(self):
        output = ""
        for command in self.history:
            line = command.output.strip()
            if not line=="":
                output = output + line + "\n"
            #print "simplefabric.outputToString : output=", line
            
        return output
    
    
    
    
class SimpleFabric():
    def __init__(self):
        self.oEnv = None
        self.taskStatus = -1
        self.history = CommandHistoryManager()
        self.isError = False
        
        
    def setFabircEnvironment(self,serverIp,serverUserId,serverUserPass):
        oEnv = env
        oEnv.user = serverUserId
        oEnv.password = serverUserPass
        oEnv.host_string = serverIp
        self.oEnv = oEnv

    def getFabricEnvironment(self):
        return self.oEnv
    
    def commandSudo(self,command):
        try:
            with settings(warn_only=True):
                output = sudo(command)
    
            if output.failed:
                self.history.addError(command,env.last_result.stdout)            
            else:
                self.history.addCommand(command,output)
    
            #print "commandSudo : ", output
            #self.appendOutput(output)    
            return output
        
        except Exception as e:
            self.history.addError(command,output)
            return output
        
        
    def commandPut(self,source,target):
        try:
            
            with settings(warn_only=True):
                output = put(source,target)
            
            if output.failed:
                self.history.addError("put",env.last_result.stdout)
            else:
                self.history.addCommand("put",output)
                
            return output

        except Exception as e:
            #errMsg = env.last_result.stdout
            errMsg = e
            self.history.addError("put",errMsg)
            return errMsg


    def commandGet(self,remote,local):
        try:
            
            with settings(warn_only=True):
                output = get(remote,local)
            
            if output.failed:
                self.history.addError("get",env.last_result.stdout)
            else:
                self.history.addCommand("get",output)
                
            return output

        except Exception as e:
            errMsg = env.last_result.stdout
            self.history.addError("get",errMsg)
            return errMsg

    def commandRun(self,command):
        try:
            with settings(warn_only=True):
                output = run(command)
    
            if output.failed:
                self.history.addError(command,env.last_result.stdout)            
            else:
                self.history.addCommand(command,output)
    
            #print "commandSudo : ", output
            #self.appendOutput(output)    
            return output
        
        except Exception as e:
            errMsg = env.last_result.stdout
            self.history.addError(command,errMsg)
            return errMsg
    
    
    def commandMkdir(self,dir):    
        output = self.commandSudo("mkdir "+dir)
        
        keyword = "cannot create directory"
        if output.find(keyword)>-1:
            return True
    
        return False
    
                