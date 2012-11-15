from os.path import basename
import taskItemModel
from baseCommand import *
from taskConst import *
from confparser import *
from extraFormatter import *


# resource how to install ganglia on fedora
#http://www.krazyworks.com/installing-ganglia-on-rhel/

class GmondInstallExecuteFedora(BaseCommand):
    
    def checkTask(self):        
        """
        [192.168.0.111] out: Starting Ganglia Monitor Daemon: gmond.
        [192.168.0.111] out: Processing triggers for libc-bin ...
        [192.168.0.111] out: ldconfig deferred processing now taking place
        """
        
        """
        ganglia-monitor is already the newest version.
        The following packages were automatically installed and are no longer required:
        linux-headers-3.2.0-23-generic linux-headers-3.2.0-23 linux-headers-3.2.0-27
        linux-headers-3.2.0-27-generic
        Use 'apt-get autoremove' to remove them.
        0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
        """
        
        keyword_ok = "Starting Ganglia Monitor Daemon"
        keyword_installed = "ganglia-monitor is already the newest version"
        
        
        if self.history.searchText(keyword_ok)>-1:
            return True
        elif self.history.searchText(keyword_installed)>-1:
            return True
        
        return False
    

    def postResult(self,task,url,port,task_data):
        print "url=",url," port=",port," output=",task.taskOutput
    
        installFlag = "0"
        if task.taskStatus == TASK_STATUS_OK:
            installFlag = "1"
            
        poster = HTTPTaskPoster(url,port,action=API_UPDATE_SERVER)
        poster.addParameter("server_id", task.serverID)
        poster.addParameter("gmond_install_flag", installFlag)
        poster.addParameter("conf_path", DIRECTORY_GMOND_CONF)
        poster.addParameter("module_path", DIRECTORY_GMOND_CONF)
        
        print poster.httpParam
        
        if not poster.post():
            print "ServerInspectionExecute.postResult : Fail to update to server"
            return False
        
        return True

    def makeConfDirectory(self):
        output = self.commandMkdir(DIRECTORY_GMOND_CONF)
        
        return output

    def makeModuleDirectory(self):
        return self.commandMkdir(DIRECTORY_GMOND_MODULE)

        #if not self.commandMkdir(DIRECTORY_GMOND_MODULE):
        #    return self.commandMkdir(DIRECTORY_GMOND_MODULE64)   
        #return True
    
    def run(self,task,url="",port=80,task_data=""):
        env = self.getFabricEnvironment()
        command = 'yum -y install ganglia-gmond'
        result = self.commandSudo(command)
        self.setResult(task)
        self.postResult(task, url, port)
        
        self.makeConfDirectory()
        self.makeModuleDirectory()
        
        self.postTaskStatus(task, url, port)
        
        return self.isTaskSuccessful(task)




class GmetadInstallExecuteFedora(BaseCommand):
    def checkTask(self):        

        """
        [192.168.0.111] out: Setting up librrd4 (1.4.7-1) ...
        [192.168.0.111] out: Setting up gmetad (3.1.7-2ubuntu1) ...
        [192.168.0.111] out: Starting Ganglia Monitor Meta-Daemon: gmetad.
        [192.168.0.111] out: Setting up ttf-dejavu-extra (2.33-2ubuntu1) ...
        [192.168.0.111] out: Setting up ttf-dejavu (2.33-2ubuntu1) ...
        [192.168.0.111] out: Processing triggers for libc-bin ...
        [192.168.0.111] out: ldconfig deferred processing now taking place
        """
        
        """
        [192.168.0.111] out: gmetad is already the newest version.
        [192.168.0.111] out: The following packages were automatically installed and are no longer required:
        [192.168.0.111] out:   linux-headers-3.2.0-23-generic linux-headers-3.2.0-23 linux-headers-3.2.0-27
        [192.168.0.111] out:   linux-headers-3.2.0-27-generic
        [192.168.0.111] out: Use 'apt-get autoremove' to remove them.
        [192.168.0.111] out: 0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
        """
        
        keyword_ok = "Starting Ganglia Monitor Meta-Daemon"
        keyword_installed = "gmetad is already the newest version"
        
        
        if self.history.searchText(keyword_ok)>-1:
            return True
        elif self.history.searchText(keyword_installed)>-1:
            return True
        
        return False
    

    def postResult(self,task,url,port):
        print "url=",url," port=",port," output=",task.taskOutput
    
        installFlag = "0"
        if task.taskStatus == TASK_STATUS_OK:
            installFlag = "1"
            
        poster = HTTPTaskPoster(url,port,action=API_UPDATE_SERVER)
        poster.addParameter("server_id", task.serverID)
        poster.addParameter("server_ip", "")
        poster.addParameter("server_userid", "")
        poster.addParameter("server_userpass", "")                
        poster.addParameter("server_version", "")
        poster.addParameter("gmond_install_flag", "")
        poster.addParameter("gmetad_install_flag", installFlag)
        poster.addParameter("plugin_list", "")
        poster.addParameter("description", "")
        
        print poster.httpParam
        
        if not poster.post():
            print "ServerInspectionExecute.postResult : Fail to update to server"
            return False
        
        return True

    
    def run(self,task,url="",port=80,task_data=""):
        env = self.getFabricEnvironment()
        
        command = 'yum -y install ganglia-gmetad'
        result = self.commandSudo(command)
        self.setResult(task)
        self.postResult(task, url, port)
        self.postTaskStatus(task, url, port)
        
        return self.isTaskSuccessful(task)






    


###################################################################################################
# gmond plugin remote task    
###################################################################################################

class GmondPluginInstallExecuteFedora(BaseCommand):
    def checkTask(self):        

        """
        [192.168.0.111] out: Setting up librrd4 (1.4.7-1) ...
        [192.168.0.111] out: Setting up gmetad (3.1.7-2ubuntu1) ...
        [192.168.0.111] out: Starting Ganglia Monitor Meta-Daemon: gmetad.
        [192.168.0.111] out: Setting up ttf-dejavu-extra (2.33-2ubuntu1) ...
        [192.168.0.111] out: Setting up ttf-dejavu (2.33-2ubuntu1) ...
        [192.168.0.111] out: Processing triggers for libc-bin ...
        [192.168.0.111] out: ldconfig deferred processing now taking place
        """
        
        """
        [192.168.0.111] out: gmetad is already the newest version.
        [192.168.0.111] out: The following packages were automatically installed and are no longer required:
        [192.168.0.111] out:   linux-headers-3.2.0-23-generic linux-headers-3.2.0-23 linux-headers-3.2.0-27
        [192.168.0.111] out:   linux-headers-3.2.0-27-generic
        [192.168.0.111] out: Use 'apt-get autoremove' to remove them.
        [192.168.0.111] out: 0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
        """
        
        keyword_ok = "Starting Ganglia Monitor Meta-Daemon"
        keyword_installed = "gmetad is already the newest version"
        
        
        if self.history.searchText(keyword_ok)>-1:
            return True
        elif self.history.searchText(keyword_installed)>-1:
            return True
        
        return False
    
    def setResult(self,task):
        output = self.history.getLastOutput()
        
        if not output:
            task.setOutput("")    
            task.setStatus(TASK_STATUS_FAIL)
            return
        
        tokens = output.output.split(" ")
        taskStatus = TASK_STATUS_FAIL
        
        if tokens[0].lower()=="linux":
            taskStatus = TASK_STATUS_OK
        
        task.setOutput(output.output)    
        task.setStatus(taskStatus)


    def postResult(self,task,url,port,task_data):
        print "url=",url," port=",port," output=",task.taskOutput
    
        installFlag = "0"
        if task.taskStatus == TASK_STATUS_OK:
            installFlag = "1"
            
        poster = HTTPTaskPoster(url,port,action=API_UPDATE_SERVER)
        poster.addParameter("server_id", task.serverID)
        #poster.addParameter("server_ip", "")
        #poster.addParameter("server_userid", "")
        #poster.addParameter("server_userpass", "")                
        #poster.addParameter("server_version", "")
        poster.addParameter("gmond_install_flag", "1")
        #poster.addParameter("gmetad_install_flag", installFlag)
        poster.addParameter("plugin_list", task_data)
        #poster.addParameter("description", "")
        
        print poster.httpParam
        
        if not poster.post():
            print "ServerInspectionExecute.postResult : Fail to update to server"
            return False
        
        return True
    
    def insertIncludePyconf(self):
        pass
    
    def getConfFileFromHost(self,local_file):
        return self.commandGet(FILE_GMOND_CONF,local_file)
    
    def configureConfFile(self,local_file):
        parser = GMondConfParser()
        results = parser.parseFromFile(local_file);
        astree.printhtml(astree.rootNode)

        #<include ('/etc/ganglia/conf.d/*.conf')  value="include" />
        include_node = astree.getIncludeNode()
        if not include_node==None:
            #insert include value
            print "add include node"
            include_node = astree.addIncludeNode()
            tag = "include ('/etc/ganglia/conf.d/*.conf')"
            astree.addIncludeDataNode(include_node,field=tag,value="include")
            
            stream = astree.writeToFile(astree.rootNode, local_file)
            tarfile = FILE_GMOND_CONF + ".new"
            
            self.commandPut(local_file,tarfile)


        keyword = "/etc/ganglia/conf.d/*.conf"        
        for elem in include_node:
            if keyword in elem.tag:
                print "tag=",elem.tag
                return True
        
        return False
    
    def copyScriptToServer(self,file_path,file_name):
        print "copyScriptToServer : path="+file_path + " , file=" + file_name

        srcFile = file_path + file_name
        targetFile = DIRECTORY_GMOND_MODULE + file_name
        return self.commandPut(srcFile,targetFile)

    def copyPyconfToServer(self,file_path,file_name):
        print "copyPyconfToServer : path="+file_path + " , file=" + file_name
        
        srcFile = file_path + file_name
        targetFile = DIRECTORY_GMOND_CONF + file_name
        return self.commandPut(srcFile,targetFile)
    
    def installPlugin(self,pyconf_data,script_data):
        print "pyconf=",pyconf_data
        
        pyconf_dir = self.extractPath(pyconf_data)
        pyconf_file = self.extractFileName(pyconf_data)
            
        script_dir = self.extractPath(script_data)
        script_file = self.extractFileName(script_data)
        
        self.copyPyconfToServer(pyconf_dir+"/",pyconf_file)
        self.copyScriptToServer(script_dir+"/",script_file)
        
        
    def restartGmond(self):
        command = "service ganglia-monitor restart"
        output = self.commandSudo(command)
        return output
    
    def extractPath(self,file_name):
        return os.path.dirname(file_name)
    
    def extractFileName(self,file_name):
        return os.path.basename(file_name)
    
            
    def run(self,task,url="",port=80,task_data=""):
        env = self.getFabricEnvironment()

        local_file = "gmond.conf"

        #self.getConfFileFromHost(MEDIA_PATH+local_file)
        #self.configureConfFile(MEDIA_PATH+local_file)
        
        formatter = PluginExtraFormatter()
        formatter.deserialize(task.taskData)
        print "count=",formatter.getCount()
        for index in range(formatter.getCount()):
            pyconf_data = formatter.getExtra(index,"pyconf")
            script_data = formatter.getExtra(index,"script")
            
            #logInfo("taskCommand : pyconf="+pyconf_data)
            #logInfo("taskCommand : script="+script_dat,.  ,.a),.    
            
            self.installPlugin(pyconf_data,script_data)
        
        #self.restartGmond()
        
        self.postTaskStatus(task, url, port)
        self.postResult(task,url,port,task_data)        
        
        """
        for pluginConfPath in oTask.pluginConfPath:
            oConfPath = pluginConfPath.split('/')
            confName = oConfPath[len(oConfPath)-1]
            #print pluginConfPath.split('/')
            self.commandPut(pluginConfPath,'/etc/ganglia/%s'%(confName))
            self.commandSudo('chmood 777 /etc/ganglia/%s'%(confName))
        
        for pluginScriptPath in oTask.pluginScriptPath:
            oScriptPath = pluginScriptPath.split('/')
            scriptName = oScriptPath[len(oScriptPath)-1]
            
            self.commandSudo('mkdir /usr/lib/ganglia/python_modules')
            self.commandSudo('chmood 777 /usr/lib/ganglia/python_modules')
            
            self.commandPut(pluginScriptPath,'/usr/lib/ganglia/python_modules/%s'%(scriptName))
            self.commandSudo('chmood 777 /usr/lib/ganglia/python_modules/%s'%(scriptName))
                
        self.commandSudo('service ganglia-monitor restart')
        result = self.commandSudo('pwd')
        
        return result
        """
        