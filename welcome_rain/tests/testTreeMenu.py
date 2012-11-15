import json
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from welcome_rain.common.mhrlog import logInfo,logAddLine
from welcome_rain.common.const import RESPONSE_CODE_OK

from welcome_rain.common.alertTreeMenuBuilder import *



#logger = logging.getLogger('wr.custom')

class TreeMenuTestCase(TestCase):
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

    def test_alertTreeMenu(self):
        alert = AlertTreeMenuBuilder()
        alert.init()
        html = alert.getTreeMenu("abc","xml")
        logInfo(html)
            
        