# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from welcome_rain.common.mhrlog import * 
import welcome_rain.common.const
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from welcome_rain.common.models import vo_Host
from welcome_rain.dashboard import forms

@login_required
def grahpdetail(request):
    template = get_template('grahpdetail.html')
    
    target = request.GET.get('target', '')
    #print request.user
    #print request.user.get_profile().grahp_realtime_interval
    variables = Context({
        'STATIC_URL' : '/static/',
        'target' : target
    })
    

    return HttpResponse(template.render(variables))

@login_required
def alerts(request):
    template = get_template('alerts.html')
    
    
    variables = Context({
        'STATIC_URL' : '/static/'
    })
    

    return HttpResponse(template.render(variables))

@login_required
def host(request):
    template = get_template('base3.html')
    
    query = request.GET.get('query', '')
    
    if query:
        qset = (
            Q(ip__icontains=query) |
            Q(description__icontains=query)
        )
        host_ref = vo_Host.objects.filter(qset).distinct()
    
    else:
        host_ref = vo_Host.objects.all()
    
    variables = Context({
        'host_ref' : host_ref,
        'query' : query
    })
    

    return HttpResponse(template.render(variables))

@csrf_exempt
@login_required
def hostadd(request):
    template = get_template('addhost.html')
    if request.method == 'POST':
        form = forms.hostForms(request.POST)
        if form.is_valid():
            oHost = vo_Host(
                uid = get_universally_unique_identifiers(),
                user = request.user,
                ip = form.cleaned_data['ip'],
                description = form.cleaned_data['description'],
            )
            oHost.save()
            return redirect('/host')
        
    else:
    
        form = forms.hostForms()
    
    variables = Context({
        'form' : form
    })

    
    return HttpResponse(template.render(variables))

@login_required
def hostdelete(request):
    host_ip = request.GET.get('id', '') 
    oHost = vo_Host.objects.get(uid=host_ip)
    oHost.delete()
    return redirect('/host')

@csrf_exempt
@login_required
def hostedit(request):
    template = get_template('edithost.html')
    
    if request.method == 'POST':
        form = forms.hostForms(request.POST)
        if form.is_valid():
            host_ip = request.POST.get('host_ip', '') 
            oHost = vo_Host.objects.get(uid=host_ip)
            oHost.ip = form.cleaned_data['ip']
            oHost.description = form.cleaned_data['description']
            oHost.save()
            return redirect('/host')
            
        
    host_ip = request.GET.get('id', '') 
    oHost = vo_Host.objects.get(uid=host_ip)
    
    form = forms.hostForms({
        'ip' : oHost.ip,
        'description' : oHost.description
    })
    
    variables = Context({
        'form' : form,
        'host_ip' : host_ip
    })
    
    return HttpResponse(template.render(variables))



import uuid
def get_universally_unique_identifiers():
    _generate_uuid = str(uuid.uuid4().hex)  
    return charShowWhereIsNumber(_generate_uuid,30)


def charShowWhereIsNumber(str,num):
    return str[:int(num)]