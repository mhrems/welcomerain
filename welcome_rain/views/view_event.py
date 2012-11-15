from datetime import datetime,timedelta 
 
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from welcome_rain.common.mhrlog import * 
import welcome_rain.common.const
from welcome_rain.common.dashboardTreeMenuBuilder import *
from welcome_rain.common.models import *
from welcome_rain.common.summaryDataBuilder import *
from welcome_rain.common.util import *
from welcome_rain.common.eventManager import *

from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

#from welcome_rain.common import fabricMhr

#from fabric.api import *


@login_required
def index(request):
    template = get_template('event.html')
    
    events = EventManager()
    eventsData = events.getEvents(request)
    
    variables = RequestContext(request,{
        'title':'title',
        'events' : eventsData
    })
    
    return HttpResponse(template.render(variables))



import uuid
def get_universally_unique_identifiers():
    _generate_uuid = str(uuid.uuid4().hex)  
    return charShowWhereIsNumber(_generate_uuid,30)


def charShowWhereIsNumber(str,num):
    return str[:int(num)]
