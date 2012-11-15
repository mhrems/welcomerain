from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from welcome_rain.common.mhrlog import * 
from welcome_rain.common.const import *
from welcome_rain.common.models import vo_Chart,vo_Server

from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

#from welcome_rain.common import fabricMhr

#from fabric.api import *

@login_required
def index(request):
    template = get_template('trendServer.html')
        
    oUser = User.objects.get(id=request.user.id)

    oProfile = oUser.get_profile()
    oProfile.grahp_realtime_interval = 1000

    
    cluster, host = parsePath(request)
    
    logInfo("cluster="+cluster+" , host="+host)
    
    server = None
    if not cluster=="" and not host=="":
        server = getServer(request,cluster,host)
        if not server is None:
            logInfo("found server ip="+server.ip)
        
    variables = RequestContext(request,{
        'title':'title',
        'server':server,
        'grahp_realtime_interval':request.user.get_profile().grahp_realtime_interval
    })
    
    return HttpResponse(template.render(variables))


def parsePath(request):
    tokens = request.path.split("/")
    logInfo("parsePath : path="+request.path + " , token_count="+str(len(tokens)))
    if not len(tokens)==4:
        return "",""
    
    return tokens[2],tokens[3]
    
    
def getServer(request,cluster,host):
    result = vo_Server.objects.get(ip=host,user=request.user)
    return result
    #return None


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
