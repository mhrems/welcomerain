import json
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User

from welcome_rain.common.mhrlog import logInfo,logAddLine
from welcome_rain.common.const import RESPONSE_CODE_OK


#logger = logging.getLogger('wr.custom')

class APITestCase(TestCase):
    def createUser(self):
        try:
            user = User.objects.get(username="test")
            return True
        except:
            User.objects.create_user('test', 'fake@pukkared.com', 'mhrinc')
            return True
        
        return False
    
    def login(self):
        self.createUser()
        if not self.client.login(username='test', password='mhrinc'):
            logInfo("Test Login Failed!!!")
            return False
        
        return True
    
    def checkAPIResponse(self,response):
        jsonDict = json.loads(response)
        status = jsonDict["status"]
        if status["code"]==RESPONSE_CODE_OK:
            return True
        return False
        
    def test_GetClusterList(self):
        response = self.client.get('/api/getClusterList/')
        logInfo('status_code='+str(response.status_code),"test_getClusterList")
        logInfo(response.content)
        logAddLine()
        
    def test_GetHostList(self):
        response = self.client.post('/api/getHostList/', {'cluster': 'mhr'})
        logInfo('status_code='+str(response.status_code),"test_getHostList")
        logInfo(response.content)
        logAddLine()

    def test_GetDataSourceList(self):
        response = self.client.post('/api/getDataSourceList/', {'cluster': 'mhr','host':'dev.local'})
        logInfo('status_code='+str(response.status_code),"test_getDataSourceList")
        logInfo(response.content)
        logAddLine()


    def test_AddEvent(self):
        """
        eventDateTime = request.POST['eventDateTime']
        eventDateTime_unix = '12323'
        title = request.POST['title']
        detail = request.POST.get('detail','')
        eventType = request.POST['eventType']
        """
        
        data = dict()
        data['eventDateTime'] = "2012-10-24 19:23"
        data['title'] = "mhr"
        data['detail'] = "test event"
        data['eventType'] = "1"
        
        self.login()

        response = self.client.post('/api/addEvent/', data)
        logInfo('status_code='+str(response.status_code),"test_AddEvent")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    
        
    def test_GetData(self):
        data = dict()
        data['user'] = ""
        
        self.test_AddEvent()

        self.login() 
        
        #data['target'] = "mhr/dev.local/cpu_system.rrd"
        data['target'] = "__SummaryInfo__/cpu_system.rrd;unspecified/192.168.0.5/cpu_system.rrd"
        data['startTime'] = "2012:09:05:00:00"
        data['endTime'] = "2012:10:24:00:00"
        data['format'] = "json"
        
        response = self.client.post('/api/getData/', data)
        logInfo('status_code='+str(response.status_code),"test_getData")
        logInfo(response.content)
        logAddLine()

    def test_GetAlertHourlyData(self):
        data = dict()
        data['user'] = ""

        self.login() 
        
        #data['target'] = "mhr/dev.local/cpu_system.rrd"
        data['target'] = "__SummaryInfo__/cpu_system.rrd;unspecified/192.168.0.5/cpu_system.rrd"
        data['startTime'] = "2012:09:05:00:00"
        data['endTime'] = "2012:10:24:00:00"
        data['format'] = "json"
        
        response = self.client.post('/api/getAlertHourlyData/', data)
        logInfo('status_code='+str(response.status_code),"test_GetAlertHourlyData")
        logInfo(response.content)
        logAddLine()

    def test_addServerDown(self):
        self.login() 
        
        #data['target'] = "mhr/dev.local/cpu_system.rrd"
        data = dict()
        data['grid_name'] = "None"
        data['cluster_name'] = "unspecified"
        data['server_ip'] = "192.168.0.2"
        data['reported'] = 1350523473
        #print "date=",datetime.datetime.fromtimestamp(1350523473)
        
        response = self.client.post('/api/addServerDown/', data)
        logInfo('status_code='+str(response.status_code),"test_addServerDown")
        logInfo(response.content)
        logAddLine()

    def test_addAbnormalStat(self):
        self.login() 
        
        #data['target'] = "mhr/dev.local/cpu_system.rrd"
        data = dict()
        data['grid_name'] = "None"
        data['cluster_name'] = "unspecified"
        data['server_ip'] = "192.168.0.2"
        data['datasource_name'] = "proc_total.rrd"
        data['probability'] = 1.4
        data['reported'] = 1350523473
        #print "date=",datetime.datetime.fromtimestamp(1350523473)
        
        response = self.client.post('/api/addAbnormalStat/', data)
        logInfo('status_code='+str(response.status_code),"test_addAbnormalStat")
        logInfo(response.content)
        logAddLine()

    def test_getUserFavoriteChartList(self):        
        data = dict()
        data['user'] = ""
        
        self.login()
        
        response = self.client.post('/api/getUserFavoriteChartList/', data)
        logInfo('status_code='+str(response.status_code),"test_getUserFavoriteChartList")
        logInfo(response.content)
        logAddLine()
        self.assertTrue(self.checkAPIResponse(response.content))

    def test_registerUserFavoriteChart(self):        
        data = dict()
        data['grid'] = ""
        data['cluster'] = "mhr"
        data['host'] = "192.168.0.228"
        data['datasource'] = "bytes_in.rrd"
        
        self.login()

        response = self.client.post('/api/registerUserFavoriteChart/', data)
        logInfo('status_code='+str(response.status_code),"test_registerUserFavoriteChart")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    def test_removeUserFavoriteChart(self):        
        data = dict()
        data['uid'] = 1
        
        self.login()

        response = self.client.post('/api/removeUserFavoriteChart/', data)
        logInfo('status_code='+str(response.status_code),"test_removeUserFavoriteChart")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))


    def test_favorite(self):
        
        self.test_registerUserFavoriteChart()
        self.test_registerUserFavoriteChart()
        self.test_registerUserFavoriteChart()
        self.test_getUserFavoriteChartList()
        self.test_removeUserFavoriteChart()
    
    
    def test_getDashboardTargetList(self):
        data = dict()        
        self.login()

        response = self.client.post('/api/getDashboardTargetList/', data)
        logInfo('status_code='+str(response.status_code),"test_getDashboardTargetList")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    
    def test_getAvailablePluginList(self):
        data = dict()        
        self.login()

        response = self.client.post('/api/getAvailablePluginList/', data)
        logInfo('status_code='+str(response.status_code),"test_getAvailablePluginList")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
    
    def test_getAlertHistory(self):
        data = dict()       
        data['page'] = 1 
        data['server_id'] = 1
        data['startTime'] = "2012:09:05:00:00"
        data['endTime'] = "2012:09:07:00:00"

        self.login()

        response = self.client.post('/api/getAlertHistory/', data)
        logInfo('status_code='+str(response.status_code),"test_getAlertHistory")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    def test_addAlert(self):
        
        data = dict()       
        #data['userID'] = 1
        data['plugin_uid'] = 1 
        data['condition'] = 1
        data['threshold_value'] = 10
        data['description'] = "description"

        self.login()

        response = self.client.post('/api/addAlert/', data)
        logInfo('status_code='+str(response.status_code),"test_addAlert")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    def test_addAlertHistory(self):
        
        self.test_addServer()
        self.test_addAlert()
        
        data = dict()       
        data['userID'] = 1
        data['regdate'] = "2012:10:05:02:30:12" 
        data['server_id'] = 1
        data['server_ip'] = "192.168.0.69"
        data['alert_id'] = 1
        data['plugin_id'] = 1
        data['alert_message'] = "data is over threshold"

        self.login()

        response = self.client.post('/api/addAlertHistory/', data)
        logInfo('status_code='+str(response.status_code),"test_addAlertHistory")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    def test_getServerGroupList(self):
        data = dict()       
        data['page'] = 1 
        data['group_type'] = 2

        self.login()

        response = self.client.post('/api/getServerGroupList/', data)
        logInfo('status_code='+str(response.status_code),"test_getServerGroupList")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
        
    def test_getServerDetail(self):
        data = dict()       
        data['server_id'] = 1 

        self.login()

        response = self.client.post('/api/getServerDetail/', data)
        logInfo('status_code='+str(response.status_code),"test_getServerDetail")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
        

    def test_newTask(self):
        data = dict()       
        data['server_id'] = "1"
        data['task_type'] = 1 
        data['task_data'] = "1" 

        self.login()

        response = self.client.post('/api/newTask/', data)
        logInfo('status_code='+str(response.status_code),"test_newTask")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    def test_updateTask(self):
        data = dict()       
        data['task_id'] = 1
        data['task_flag'] = 1
        data['task_ok_count'] = 10         
        data['task_data'] = "params" 

        self.login()

        response = self.client.post('/api/updateTask/', data)
        logInfo('status_code='+str(response.status_code),"test_updateTask")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
        
    def test_getTaskList(self):
        data = dict()       
        data['server_id'] = 1 

        self.login()

        response = self.client.post('/api/getTaskList/', data)
        logInfo('status_code='+str(response.status_code),"test_getTaskList")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
        
    def test_Task(self):
        self.test_newTask()
        self.test_newTask()
        self.test_newTask()

        self.test_updateTask()
        self.test_getTaskList()
        


    def test_addServer(self):
        data = dict()       
        data['server_ip'] = "192.168.0.2"
        data['server_userid'] = "root" 
        data['server_userpass'] = "mhrinc"
        data['description'] = "ok"

        self.login()

        response = self.client.post('/api/addServer/', data)
        logInfo('status_code='+str(response.status_code),"test_addServer")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))

    def test_editServer(self):
        data = dict()       
        data['server_id'] = 1
        data['server_ip'] = "192.168.0.2"
        data['server_userid'] = "root" 
        data['server_userpass'] = "mhrinc"
        data['server_version'] = "linux"
        data['gmond_install_flag'] = 1
        data['plugin_list'] = "1"
        data['description'] = "description !!!!"

        self.login()

        response = self.client.post('/api/editServer/', data)
        logInfo('status_code='+str(response.status_code),"test_editServer")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))


    def test_Server(self):
        self.test_addServer()
        self.test_editServer()
        self.test_getServerGroupList()
        

    def test_addTaskStatus(self):
        data = dict()       
        data['task_id'] = 1 
        data['server_id'] = 1 
        data['server_ip'] = "192.168.0.2"
        data['status_flag'] = 1
        data['progress'] = "1,1"
        data['message'] = "ok"

        self.login()

        response = self.client.post('/api/addTaskStatus/', data)
        logInfo('status_code='+str(response.status_code),"test_addTaskStatus")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
    
    def test_queryTaskStatus(self):
        data = dict()       
        data['task_id'] = 1 
        data['status_id'] = -1 

        self.login()

        response = self.client.post('/api/queryTaskStatus/', data)
        logInfo('status_code='+str(response.status_code),"test_queryTaskStatus")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
    
    def test_Query(self):
        self.test_addServer()
        self.test_addPlugin()
        self.test_newTask()
        
        self.test_addTaskStatus()
        self.test_addTaskStatus()
        self.test_addTaskStatus()
    
        self.test_queryTaskStatus()


    def test_addPlugin(self):
        #addConfNScript("/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.pyconf","/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.py")
        #addConfNScript("/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.pyconf","/home/james/Workspace/Project/WelcomeRain/python_modules/disk/diskfree.py")
        
        data = dict()       
        data['plugin_name'] = "vm_stat" 
        data['pyconf'] = "/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.pyconf"
        data['script'] = "/home/james/Workspace/Project/WelcomeRain/python_modules/vm_stats/vm_stats.py"

        self.login()

        response = self.client.post('/api/addPlugin/', data)
        logInfo('status_code='+str(response.status_code),"test_addPlugin")
        logInfo(response.content)
        logAddLine()
        
        self.assertTrue(self.checkAPIResponse(response.content))
    
    
    def test_RemoteTask(self):
        self.test_addServer()
        self.test_addPlugin()
        self.test_newTask()
        
        self.test_addTaskStatus()
        self.test_addTaskStatus()
        self.test_addTaskStatus()
    
        self.test_queryTaskStatus()
        