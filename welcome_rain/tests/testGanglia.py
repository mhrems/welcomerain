import json
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from welcome_rain.common.models import vo_Server
from welcome_rain.common.mhrlog import logInfo,logAddLine
from welcome_rain.common.const import RESPONSE_CODE_OK

# python manage.py test welcome_rain.tests.testGanglia:GmondInstallTestCase.GmondInstall


"""

class GmondInstallTestCase(TestCase):
    
    def GmondInstall(self):
        self.createBaseEnv()
        self.assertTrue(True)
        return False
    #    return True
    
    def createBaseEnv(self):
        #logInfo(self)
        TestUser().login()
    #    self.assertTrue(False)
    #    TestServer().createServer()
        return True
    
    
class TestUser():
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
        if not TestClient().login('test','mhrinc'):
            logInfo("Test Login Failed!!!")
            return False
        return True
    

class TestServer():
    
    def createServer(self):
        ubuntu_10 = ['192.168.0.200','192.168.0.201','192.168.0.202']
        ubuntu_11 = ['192.168.0.203','192.168.0.204','192.168.0.205']
        ubuntu_12 = ['192.168.0.206','192.168.0.207','192.168.0.208']
        fedora_16 = ['192.168.0.211','192.168.0.212','192.168.0.213']
        fedora_16 = ['192.168.0.214','192.168.0.215','192.168.0.216']
        
        testServer = ubuntu_11
        
        for server_ip in testServer:
            data = {
                    "server_ip" : server_ip,
                    "server_userid" : 'root',
                    "server_userpass" : 'mhrinc',
                    "description" : 'test server'
            }
            self.addServer(data)
            
    def addServer(self,data):
        print 1
        #TestUser().login()
        #response = TestClient().post('/api/addServer/',data)
        #logInfo('status_code='+str(response.status_code),"test_addServer")
        #self.assertTrue(EmsApi().checkAPIResponse(response.content))

class TestClient():
    
    def post(self,url,data):
        return self.client.post(url, data)
    
    def login(self,username,password):
        return self.client.login(username=username, password=password)
    
class EmsApi():
    
    def checkAPIResponse(self,response):
        jsonDict = json.loads(response)
        status = jsonDict["status"]
        if status["code"]==RESPONSE_CODE_OK:
            return True
        return False
"""

# python manage.py test welcome_rain.tests.testGanglia:EmsInstallTestCase.GmondInstall
# python manage.py test welcome_rain.tests.testGanglia:EmsInstallTestCase.GmetadInstall
class EmsInstallTestCase(TestCase):
    
    def checkAPIResponse(self,response):
        jsonDict = json.loads(response)
        status = jsonDict["status"]
        if status["code"]==RESPONSE_CODE_OK:
            return True
        return False
    
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
    
    def ClientPost(self,url,data):
        return self.client.post(url, data)
    
    
    def GmondInstall(self):
        #self.assertTrue(True)
        self.createBaseEnv()
        self.installGmond()
        
    def GmetadInstall(self):
        #self.assertTrue(True)
        self.createBaseEnv()
        self.installGmetad()
        
    
    
    def createBaseEnv(self):
        self.createTestServer()
        
        
    def createTestServer(self):
        ubuntu_10 = ['192.168.0.200','192.168.0.201','192.168.0.202']
        ubuntu_11 = ['192.168.0.203','192.168.0.204','192.168.0.205']
        ubuntu_12 = ['192.168.0.206','192.168.0.207','192.168.0.208']
        fedora_16 = ['192.168.0.211','192.168.0.212','192.168.0.213']
        fedora_17 = ['192.168.0.214','192.168.0.215','192.168.0.216']
        gmetad = ['192.168.0.207']
        
        testServer = gmetad
        
        for server_ip in testServer:
            data = {
                    "server_ip" : server_ip,
                    "server_userid" : 'root',
                    "server_userpass" : 'mhrinc',
                    "description" : 'test server'
            }
            self.addServer(data)
            
    def addServer(self,data):
        self.login()
        response = self.ClientPost('/api/addServer/', data)
        logInfo('status_code='+str(response.status_code),"test_addServer")
        self.assertTrue(self.checkAPIResponse(response.content))
    
    def installGmetad(self):
        oServer = vo_Server.objects.all()
        for server in oServer:
            data = {
                    "server_id" : server.id,
                    "task_type" : '3',
                    "task_data" : '',
            }
            self.newTask(data)
    
    def installGmond(self):
        oServer = vo_Server.objects.all()
        for server in oServer:
            data = {
                    "server_id" : server.id,
                    "task_type" : '0',
                    "task_data" : '',
            }
            self.newTask(data)
            
    def newTask(self,data):
        self.login()
        response = self.ClientPost('/api/newTask/', data)
        logInfo('status_code='+str(response.status_code),"test_newTask")
        self.assertTrue(self.checkAPIResponse(response.content))
        
        

"""
class GmondInstallTestCase(TestCase):
    def checkAPIResponse(self,response):
        jsonDict = json.loads(response)
        status = jsonDict["status"]
        if status["code"]==RESPONSE_CODE_OK:
            return True
        return False
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
    
    
    def addServer(self,data):
        self.login()
        response = self.client.post('/api/addServer/', data)
        logInfo('status_code='+str(response.status_code),"test_addServer")
        self.assertTrue(self.checkAPIResponse(response.content))
        
    def newTask(self,data):
        self.login()
        response = self.client.post('/api/newTask/', data)
        logInfo('status_code='+str(response.status_code),"test_newTask")
        self.assertTrue(self.checkAPIResponse(response.content))
    
    
    def createServer(self):
        ubuntu_10 = ['192.168.0.200','192.168.0.201','192.168.0.202']
        ubuntu_11 = ['192.168.0.203','192.168.0.204','192.168.0.205']
        ubuntu_12 = ['192.168.0.206','192.168.0.207','192.168.0.208']
        fedora_16 = ['192.168.0.211','192.168.0.212','192.168.0.213']
        fedora_16 = ['192.168.0.214','192.168.0.215','192.168.0.216']
        
        testServer = ubuntu_11
        
        for server_ip in testServer:
            data = {
                    "server_ip" : server_ip,
                    "server_userid" : 'root',
                    "server_userpass" : 'mhrinc',
                    "description" : 'test server'
            }
            self.addServer(data)
    
    def installGmond(self):
        oServer = vo_Server.objects.all()
        for server in oServer:
            data = {
                    "server_id" : server.id,
                    "task_type" : '0',
                    "task_data" : 'root',
            }
            self.newTask(data)
    
    def GmondInstall(self):
        self.createServer()
        self.installGmond()
        
"""




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
    
   