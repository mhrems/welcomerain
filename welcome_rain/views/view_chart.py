from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from welcome_rain.common.mhrlog import * 
import welcome_rain.common.const
from welcome_rain.common.dashboardTreeMenuBuilder import *

from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from welcome_rain.common.models import vo_Chart
from django.contrib.auth.models import User

#from welcome_rain.common import fabricMhr

#from fabric.api import *

@login_required
def index(request):
    template = get_template('chart.html')
    
    #bond = Fabric()
    #run('ls')
    
    #oUser = User.objects.get(id=request.user.id)
    
    #print oUser
    
    #oProfile = oUser.get_profile()
    #oProfile.grahp_realtime_interval = 1000
    
    #oProfile.save()
    
    treeMenu = DashboardTreeMenuBuilder()
    treeMenu.init()
    html = treeMenu.getTreeMenu("abc","xml")
    
    
    #logInfo(html)
    
    variables = RequestContext(request,{
        'title':'title',
        'Tree_Menu':html,
        'grahp_realtime_interval':request.user.get_profile().grahp_realtime_interval,
        'profile' : request.user.get_profile(),
    })
    
    return HttpResponse(template.render(variables))





@csrf_exempt
@login_required
def addchart(request):
    template = get_template('addchart.html')
    
    variables = Context({
        'title':'title',
        
    })
    if(request.method == 'POST'):
        
        oChart = vo_Chart(
            uid = get_universally_unique_identifiers(),
            user = request.user,
            name = request.POST['name'],
            cluster = '',
            host = '',
            datasource = request.POST['datasource_sel'],
        )
        
        if(request.POST['check_cluster'] == 'true'):
            oChart.cluster = request.POST['cluster_sel']
        if(request.POST['check_host'] == 'true'):
            oChart.host = request.POST['host_sel']
        
        oChart.save()
        return redirect('/')
        
    return HttpResponse(template.render(variables))


import uuid
def get_universally_unique_identifiers():
    _generate_uuid = str(uuid.uuid4().hex)  
    return charShowWhereIsNumber(_generate_uuid,30)


def charShowWhereIsNumber(str,num):
    return str[:int(num)]
