from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

import datetime
from util import *


class vo_UserProfile(models.Model):
    
    user = models.ForeignKey(User, unique=True)
    regdate = models.DateTimeField(default=datetime.datetime.now())    
    
    rrd_path = models.CharField(max_length=100)
    api_server = models.IPAddressField(default="127.0.0.1")
    api_port = models.IntegerField(default=8080)
    gmetad_ip = models.IPAddressField(default="127.0.0.1")
    gmetad_port = models.IntegerField(default=8652)
    
    grahp_realtime_interval = models.IntegerField(default=30000)
    grahp_grid_outlineWidth = models.IntegerField(default=1)
    
    grahp_line_fill = models.IntegerField(default=0)
    grahp_grid_color = models.CharField(max_length=100,default="#d5b658")    
    grahp_line_color = models.CharField(max_length=100,default="#d5588d")    
    

    
    def __str__(self):  
        return "%s's profile" % self.user
    
def create_user_profile(sender, instance, created, **kwargs):  
    '''
        create_user_profile
        2012.01.10 by bond 
    '''
    if created:  
       profile, created = vo_UserProfile.objects.get_or_create(user=instance)    
post_save.connect(create_user_profile, sender=User)



class vo_Chart(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    updatedate = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User)

    name = models.CharField(max_length=50)    
    cluster = models.CharField(max_length=50)    
    host = models.CharField(max_length=50) 
    datasource = models.CharField(max_length=50)
    
    
class vo_Host(models.Model):  
    regdate = models.DateTimeField(default=datetime.datetime.now)
    updatedate = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User)

    ip = models.IPAddressField()
    description = models.TextField()    


class FavoriteManager(models.Manager):
    def addFavoriteFromRequest(self,request):
        gridValue = request.POST['grid']
        clusterValue = request.POST['cluster']
        hostValue = request.POST['host']
        dataSourceValue = request.POST['datasource']
        favorite = self.create(user=request.user,grid=gridValue,cluster=clusterValue,host=hostValue,datasource=dataSourceValue)
        favorite.save()
        
        return favorite

    def deleteFavoriteFromRequest(self,request):
        uid = request.POST['uid']
        favorite = self.get(id=uid)
        if not favorite:
            return False
        favorite.delete()
        return True

    
class vo_Favorite(models.Model): 
    regdate = models.DateTimeField(default=datetime.datetime.now,auto_now_add=True)
    updatedate = models.DateTimeField(default=datetime.datetime.now,auto_now_add=True)
    
    #regdate = models.BigIntegerField()
    #updatedate = models.BigIntegerField()

    user = models.ForeignKey(User)

    grid = models.CharField(max_length=50)    
    cluster = models.CharField(max_length=50)    
    host = models.CharField(max_length=50) 
    datasource = models.CharField(max_length=50)
    
    objects = FavoriteManager()

class ServerManager(models.Manager):
    def addServerFromRequest(self,request):
        server_ip = request.POST['server_ip']
        server_userid = request.POST['server_userid']
        server_password = request.POST['server_userpass']
        description = request.POST['description']
        server = self.create(user=request.user,ip=server_ip,server_userid=server_userid,server_password=server_password,description=description)
        server.save()
        
        return server
    
    def deleteServerFromRequest(self,request):
        id = request.POST['server_id']
    
        try:
            for server_id in id.split(','):
            
                oServer = self.get(id=server_id)
                
                oServer.delete()
            return True
        except:
            return False
        
    def editServerFromRequest(self,request):
        server_id = request.POST['server_id'] 
        
        oServer = self.get(id=server_id)
        
        if 'server_ip' in request.POST:
            oServer.ip = request.POST['server_ip']
        if 'server_userid' in request.POST:
            oServer.server_userid = request.POST['server_userid']
        if 'server_userpass' in request.POST:
            oServer.server_password = request.POST['server_userpass']
        if 'server_version' in request.POST:
            oServer.rserver_version = request.POST['server_version']
        if 'gmond_install_flag' in request.POST:
            oServer.gmond_install_flag = request.POST['gmond_install_flag']
        if 'gmetad_install_flag' in request.POST:
            oServer.gmetad_install_flag = request.POST['gmetad_install_flag']
        if 'plugin_list' in request.POST:
            oServer.plugin_lists = request.POST['plugin_list']
        if 'description' in request.POST:
            oServer.description = request.POST['description']

        if 'conf_path' in request.POST:
            oServer.conf_path = request.POST['conf_path']
        if 'module_path' in request.POST:
            oServer.module_path = request.POST['module_path']
            
        oServer.save()
        
        return oServer
    

class vo_Server(models.Model):  

    regdate = models.DateTimeField(default=datetime.datetime.now)
    updatedate = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User)
    ip = models.IPAddressField()
    server_version = models.CharField(max_length=200)
    server_userid = models.CharField(max_length=20,null=True)
    server_password = models.CharField(max_length=20,null=True)
    server_type = models.CharField(max_length=20,null=True,default='ubuntu')
    gmond_install_flag = models.IntegerField(default=0)        
    gmetad_install_flag = models.IntegerField(default=0)        
    plugin_lists = models.TextField(null=True,blank=True) 
    description = models.TextField(null=True,blank=True) 
    conf_path = models.CharField(max_length=200,null=True,blank=True)
    module_path = models.CharField(max_length=200,null=True,blank=True)
    
    machine_type = models.CharField(max_length=200,null=True,blank=True)
    server_kernel = models.CharField(max_length=200,null=True,blank=True)
    cpu_count = models.IntegerField(default=0)
    cpu_speed = models.CharField(max_length=50,null=True,blank=True)
    memory_total = models.IntegerField(default=0)
    disk_total = models.BigIntegerField(default=0)
    
    objects = ServerManager()
    
class vo_ServerAdmin(admin.ModelAdmin):
    pass
admin.site.register(vo_Server)

class vo_Progress(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    updatedate = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User)
    server = models.ForeignKey(vo_Server) 
    server_ip = models.CharField(max_length=50) 
    index = models.CharField(max_length=50) 
    task_id = models.CharField(max_length=50) 
    message = models.CharField(max_length=50) 


class PluginManager(models.Manager):
    def addFromHTTPRequest(self,request):
        plugin_name = request.POST['plugin_name']
        pyconf = request.POST['pyconf']
        script = request.POST['script']
        
        plugin = self.create(plugin_name=plugin_name,pyconf=pyconf,script=script)
        plugin.save()
        
        return plugin



class vo_Plugin(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    updatedate = models.DateTimeField(auto_now=True)
    plugin_name = models.CharField(max_length=50) 
    conf_path = models.FileField(upload_to='plugin/',blank=True,null=True)
    script_path = models.FileField(upload_to='plugin/',blank=True,null=True)

    pyconf = models.CharField(max_length=200,blank=True,null=True) 
    script = models.CharField(max_length=200,blank=True,null=True) 

    objects = PluginManager()

    """
    def save(self):
        for field in self._meta.fields:
            if field.name == 'conf_path':
                field.upload_to = 'plugin/%s/' %(self.plugin_name)
            elif field.name == 'script_path':
                field.upload_to = 'plugin/%s/' %(self.plugin_name)
        super(vo_Plugin, self).save()


    def save2(self):
        super(vo_Plugin, self).save()
    """

class vo_PluginAdmin(admin.ModelAdmin):
    pass
admin.site.register(vo_Plugin)

ALERT_CONDISION = (
    ('>','>'),
    ('=','='),
    ('<','<')
)

class AlertManager(models.Manager):
    def addAlertFromRequest(self,request):
        plugin_id = request.POST['plugin_uid']
        condition = request.POST['condition']
        threshold_value = request.POST['threshold_value']
        descriptions = request.POST['description']
        
        oAlert = self.create(user=request.user,plugin=plugin_uid,condition=condition,threshold_value=threshold_value,description=descriptions)
        oAlert.save()
        
        return oAlert
    
    def editAlertFromRequest(self,request):
        uid = request.POST['alert_uid']
        plugin_id = request.POST['plugin_uid']
        condition = request.POST['condition']
        threshold_value = request.POST['threshold_value']
        descriptions = request.POST['descriptions']
        
        oPlugin = vo_Plugin.objects.get(id=plugin_id)
        
        oAlert = self.get(id=uid)
        oAlert.plugin = oPlugin
        oAlert.condition = condition
        oAlert.threshold_vale = threshold_vale
        oAlert.descriptions = descriptions
        oAlert.save()
        return oAlert

class vo_Alert(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    updatedate = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User)
    plugin = models.ForeignKey(vo_Plugin)
    
    condition = models.CharField(max_length=1, choices=ALERT_CONDISION) 
    threshold_value = models.IntegerField()
    descriptions = models.CharField(max_length=200,null=True) 

    objects = AlertManager()
    
class vo_AlertAdmin(admin.ModelAdmin):
    pass
admin.site.register(vo_Alert)

class AlertHistoryManager(models.Manager):
    def getDateTimeTokens(self,regdate):
        tokens = regdate.split(":")
        return tokens
        
    def addAlertHistoryFromRequest(self,request):
        regdate = request.POST['regdate']
        user = request.POST['userID']
        server = request.POST['server_id']
        server_ip = request.POST['server_ip']
        alert = request.POST['alert_id']
        plugin = request.POST['plugin_id']
        alert_message = request.POST['alert_message']
        
        user = User.objects.get(id=user)
        server = vo_Server.objects.get(id=server)
        alert = vo_Alert.objects.get(id=alert)
        plugin = vo_Plugin.objects.get(id=plugin)
        timeToken = self.getDateTimeTokens(regdate)
        
        alertHistory = self.create(user=user,
                                   regdate=regdate,
                                   year=timeToken[0],month=timeToken[1],day=timeToken[2],
                                   hour=timeToken[3],minute=timeToken[4],second=timeToken[5],                                   
                                   server=server,server_ip=server_ip,alert=alert,
                                   plugin=plugin,alert_message=alert_message)
        alertHistory.save()
        
        return alertHistory

class vo_AlertHistory(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    updatedate = models.DateTimeField(auto_now=True)
    
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    second = models.IntegerField(default=0)

    user = models.ForeignKey(User)
    server = models.ForeignKey(vo_Server) 
    server_ip = models.IPAddressField()
    alert = models.ForeignKey(vo_Alert)
    plugin = models.ForeignKey(vo_Plugin)
    alert_message = models.CharField(max_length=50) 
    
    objects = AlertHistoryManager()
    
class vo_AlertHistoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(vo_AlertHistory)
    
    
    
    
class TaskManager(models.Manager):
    def addTaskFromRequest(self,request):
        taskType = request.POST['task_type']
        task_data = request.POST['task_data']
        server_id = request.POST['server_id']
        servers = server_id.split(",")
        serverCount = len(servers)
        
        task = self.create(user=request.user,task_type=taskType,task_data=task_data,server_ids=server_id,server_count=serverCount)
        task.save()
        
        return task

    def updateTaskFromRequest(self,request):
        task_id = request.POST['task_id']
        task = self.get(id=task_id)
        if not task:
            return False
        
        task_ok_count = request.POST['task_ok_count']
        task_flag = request.POST['task_flag']
        task_data = request.POST['task_data']

        task.task_flag = task_flag
        task.task_data = task_data
        task.task_ok_count = task_ok_count
        task.task_data = task_data
        
        task.save()
        
        return task

    def deleteTaskFromRequest(self,request):
        uid = request.POST['uid']
        favorite = self.get(id=uid)
        if not favorite:
            return False
        favorite.delete()
        return True

class vo_Task(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    #updatedate = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User)
    task_type = models.IntegerField()
    server_ids = models.TextField() 
    server_count = models.IntegerField()
    task_ok_count = models.IntegerField(default=0)
    task_flag = models.IntegerField(default=-1)
    task_data = models.TextField(blank=True) 
    description = models.TextField(blank=True) 
    
    objects = TaskManager()
    
class vo_TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(vo_Task)


class TaskStatusManager(models.Manager):
    def addTaskStatusFromRequest(self,request):
        task_id = request.POST['task_id']
        server_id = request.POST['server_id']
        server_ip = request.POST['server_ip']
        status_flag = request.POST['status_flag']
        progress = request.POST['progress']
        message = request.POST['message']
        
        taskStatus = self.create(task_id=task_id,server_id=server_id,server_ip=server_ip,status_flag=status_flag,progress=progress,message=message)
        taskStatus.save()
        
        return taskStatus

    def deleteTaskFromRequest(self,request):
        uid = request.POST['uid']
        favorite = self.get(id=uid)
        if not favorite:
            return False
        favorite.delete()
        return True


class vo_TaskStatus(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    #updatedate = models.DateTimeField(auto_now=True)
    
    #user = models.ForeignKey(User)
    server = models.ForeignKey(vo_Server) 
    server_ip = models.IPAddressField()
    task = models.ForeignKey(vo_Task)
    progress = models.CharField(max_length=100,default='')
    status_flag = models.CharField(max_length=100,null=True)
    message = models.TextField(null=True) 

    objects = TaskStatusManager()
    
class vo_TaskStatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(vo_TaskStatus)

import time
class EventManager(models.Manager):
    
    def addEventFromRequest(self,request):
        eventDateTime = request.POST['eventDateTime']
        title = request.POST['title']
        detail = request.POST.get('detail','')
        eventType = request.POST['eventType']
        server = self.create(user=request.user,eventDateTime=eventDateTime,title=title,detail=detail,eventType=eventType)
        
        
        date_data = server.eventDateTime.split(' ')[0].split('-')
        time_data = server.eventDateTime.split(' ')[1].split(':')
        date_time = datetime.datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]), int(time_data[0]), int(time_data[1]), 0)
        timestemp = time.mktime(date_time.timetuple())
        server.eventDateTime_unix = timestemp

        #print data[0]
        #print data[1]
        #time.mktime( (10, 8, 20, 10, 20, 30, 0, 0, 0) )
        #print time.mktime( (10, 8, 20, 10, 20, 30, 0, 0, 0) )
        #print int(time.mktime( (10, 8, 20, 10, 20, 0, 0, 0, 0) ))
        #then = server.eventDateTime + datetime.timedelta(days=3)
        
        #print server.eventDateTime
        #print then.strftime("%s")
        #print then.mktime(then.timetuple())
        #print then.mktime("%s")
        server.save()
        
        #print time.mktime(then.timetuple())*1e3 + then.microsecond/1e3
        
        return server
    
    def deleteEventFromRequest(self,request):
        id = request.POST['event_id']
    
        try:
            for event_id in id.split(','):
            
                oEvent = self.get(id=event_id)
                
                oEvent.delete()
            return True
        except:
            return False


        
class vo_Event(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    #updatedate = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User)
    eventDateTime = models.DateTimeField(default=datetime.datetime.now)
    eventDateTime_unix = models.IntegerField(default=0)
    title = models.CharField(max_length=100,default='')
    detail = models.TextField(null=True) 
    eventType = models.IntegerField()
    
    objects = EventManager()
    


class ServerDownManager(models.Manager):
    def addServerDownFromRequest(self,request):
        grid_name = request.POST['grid_name']
        cluster_name = request.POST['cluster_name']
        server_ip = request.POST['server_ip']
        reported = request.POST['reported']
        
        dated = convertUTCToDateTimeToken(reported)
        
        server = self.create(grid_name=grid_name,cluster_name=cluster_name,server_ip=server_ip,year=dated[0],month=dated[1],day=dated[2],hour=dated[3],minute=dated[4],second=dated[5])
        server.save()
                
        return server
    
class vo_ServerDown(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    #updatedate = models.DateTimeField(auto_now=True)
    grid_name = models.CharField(max_length=100,default='')
    cluster_name = models.CharField(max_length=100,default='')
    server_ip = models.CharField(max_length=100,default='')
    
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    
    objects = ServerDownManager()
    
class vo_ServerDownAdmin(admin.ModelAdmin):
    pass

admin.site.register(vo_ServerDown)


class AbnormalStatManager(models.Manager):
    def addAbnormalStatFromRequest(self,request):
        grid_name = request.POST['grid_name']
        cluster_name = request.POST['cluster_name']
        server_ip = request.POST['server_ip']
        data_name = request.POST['datasource_name']
        probability = request.POST['probability']
        reported = request.POST['reported']
        
        dated = convertUTCToDateTimeToken(reported)
        
        abnormal = self.create(grid_name=grid_name,cluster_name=cluster_name,server_ip=server_ip,datasource_name=data_name,probability=probability,year=dated[0],month=dated[1],day=dated[2],hour=dated[3],minute=dated[4],second=dated[5])
        abnormal.save()
                
        return abnormal
    
class vo_AbnormalStat(models.Model):
    regdate = models.DateTimeField(default=datetime.datetime.now)
    #updatedate = models.DateTimeField(auto_now=True)
    grid_name = models.CharField(max_length=100,default='')
    cluster_name = models.CharField(max_length=100,default='')
    server_ip = models.CharField(max_length=100,default='')
    datasource_name = models.CharField(max_length=100,default='')
    
    probability = models.FloatField(default=0)
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    
    objects = AbnormalStatManager()
    
class vo_AbnormalStatAdmin(admin.ModelAdmin):
    pass

admin.site.register(vo_AbnormalStat)
