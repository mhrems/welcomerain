'''
Created on Sep 26, 2012

@author: bond
'''


from powermonitor.module import *
from powermonitor import notification


NAME_PREFIX = 'temp_'

def temp_handler(name):
    
    try:
        PLUGIN_NAME = name
        NODE_ID = name[len(NAME_PREFIX):]
        CpowerMonitor = Monitor(PLUGIN_NAME,NODE_ID)
	return float(CpowerMonitor.getTemperatureFormDb())
    except:
	#notification.EmailNotification().sendEmail('Error!!! : Fail to get temp data. that plugin name is %s'%(PLUGIN_NAME))
        return 0


def create_desc(skel, prop):
    d = skel.copy()
    for k,v in prop.iteritems():
        d[k] = v
    return d

def metric_init(params):
    global descriptors, metric_map, Desc_Skel

    descriptors = []
    
    Desc_Skel = {
          'name': 'XXX',
          'call_back': temp_handler,
          'time_max': 90,
          'value_type': 'float',
          'units': 'xxx',
          'slope': 'both',
          'format': '%.4f',
          'description': 'bond of host',
          'groups': 'temp'
    }
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "200",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "201",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "202",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "203",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "204",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "205",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "206",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "207",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "208",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "209",
    }))
    return descriptors

def metric_cleanup():
    '''Clean up the metric module.'''
    pass

#This code is for debugging and unit testing
if __name__ == '__main__':
    metric_init({})
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for %s is %u' % (d['name'],  v)
