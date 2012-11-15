"""
    UserConfig(request.user).getConfig()
"""
class singleton(object):
    __single = None
    
    def __new__(classtype,*args,**kwargs):
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype,*args,**kwargs)
        return classtype.__single
    


class UserConfig(singleton):

    def __init__(self,oUser):
        self.userObject = oUser
    
    def getConfig(self):
        #print "getConfig"
        return UserConfigManage(self.userObject).getUserConfigOrSetUserConfig()
        #print userConfig.rrd_path
        #print userConfig.api_server
        #print userConfig.api_port
        #print userConfig.gmetad_ip
        #print userConfig.gmetad_port
        
        
        #rrd_path = models.CharField(max_length=100)
        #api_server = models.IPAddressField(default="127.0.0.1")
        #api_port = models.IntegerField(default=8080)
        #gmetad_ip = models.IPAddressField(default="127.0.0.1")
        #gmetad_port = models.IntegerField(default=8652)
        
    def changeConfig(self):
        #print "changeConfig"
        UserConfigManage(self.userObject).setUserConfigFormDbAndGet()
        
class UserConfigManage():
    
    userConfigKeyPrifix = '_userconfig'
    
    def __init__(self,userObject):
        self.userObject = userObject
        self.key = self.getUserConfigKey()
    
    def getUserConfigOrSetUserConfig(self):
        #print 'getUserConfig'
        userConfig = self.getUserConfigFormCache()
        if not userConfig:
            userConfig = self.setUserConfigFormDbAndGet()
        return userConfig
    
    
    def getUserConfigFormCache(self):
        return DjangoCache().getCache(self.key)
    
    def setUserConfigFormDbAndGet(self):
        userConfig = self.getConfigFormDb()
        DjangoCache().setCache(self.key,userConfig)
        return userConfig
        
    def getUserConfigKey(self):
        return str(self.userObject.id) + self.userConfigKeyPrifix
    
    
    def getConfigFormDb(self):
        return self.userObject.get_profile()
     
from django.core.cache import cache        
class DjangoCache():
    def getCache(self,key):
        return cache.get(key)
    def setCache(self,key,data):
        cache.set(key,data)
    def clearCache(self,key):
        cache.delete(key)
    
  
'''
test1 = UserConfig('bond1')

test2 = UserConfig('bond2')
test1.getConfig()
test2.getConfig()
'''