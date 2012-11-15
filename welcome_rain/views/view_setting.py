from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import welcome_rain.common.const
import os
from welcome_rain.common.confFile import *
from welcome_rain.common.mhrlog import * 
from welcome_rain.common.settingTreeMenuBuilder import *
from welcome_rain.common.models import vo_Chart


@login_required
def index(request):
    
    template = get_template('setting.html')
    
    treeMenu = SettingTreeMenuBuilder()
    treeMenu.init()
    html = treeMenu.getTreeMenu("abc","xml")
    
    confFile = ConfFile()
    confFile.setPath('/etc/ganglia/gmetad.conf')
    gmetad_conf = confFile.readConf()
    
    dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static/temp'))
    confFile.setPath(dataPath+'/gmond.conf')
    gmond_conf = confFile.readConf()
    
    print '*'*10
    print request.user
    print request.user.get_profile().api_server
    #gmond_conf
    
    '''
    gmond_conf = open('/etc/ganglia/gmetad.conf',"r")
    
    logInfo("test")
    logInfo(html)
    logInfo(gmond_conf)
    #logInfo(gmond_conf.readline())
    conf_file = []
    
    for line in gmond_conf:
        print line
        conf_file.append(line)
    
    gmond_conf = open('/etc/ganglia/gmetad.conf',"w")
    gmond_conf.write('eer')
    '''
    variables = RequestContext(request,{
        'title':'title',
        #'Tree_Menu':html,
        'gmetad_conf': gmetad_conf,
        'gmond_conf' : gmond_conf,
        'profile' : request.user.get_profile(),
        
    })
    
    return HttpResponse(template.render(variables))



