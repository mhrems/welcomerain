from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import welcome_rain.common.const

from welcome_rain.common.mhrlog import * 
from welcome_rain.common.serverTreeMenuBuilder import *
from welcome_rain.common.models import vo_Chart


@login_required
def index(request):

    template = get_template('server.html')
    
    treeMenu = ServerTreeMenuBuilder()
    treeMenu.init()
    html = treeMenu.getTreeMenu("abc","xml")
    
    #logInfo("test")
    #logInfo(html)
    
    variables = RequestContext(request,{
        'title':'title',
        'Tree_Menu':html,
    })
    
    return HttpResponse(template.render(variables))



