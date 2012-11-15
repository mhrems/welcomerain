from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import welcome_rain.common.const

from welcome_rain.common.mhrlog import * 
from welcome_rain.common.alertTreeMenuBuilder import *
from welcome_rain.common.models import vo_Chart
from welcome_rain.common.userConfig import *

@login_required
def index(request):

    template = get_template('alerts.html')
    
    treeMenu = AlertTreeMenuBuilder()
    treeMenu.init()
    html = treeMenu.getTreeMenu("abc","xml")
    
    UserConfig(request.user).getConfig()
    
    #logInfo("test")
    #logInfo(html)
    
    variables = RequestContext(request,{
        'title':'title',
        'Tree_Menu':html,
    })
    
    return HttpResponse(template.render(variables))



