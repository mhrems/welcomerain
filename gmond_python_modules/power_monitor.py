'''
Created on Sep 26, 2012

@author: bond
'''


from powermonitor.module import *
from powermonitor import notification

NAME_PREFIX = 'power_'


def power_handler(name):
    
    try:
        PLUGIN_NAME = NAME_PREFIX + name
        NODE_ID = name[len(NAME_PREFIX):]
        CpowerMonitor = Monitor(PLUGIN_NAME,NODE_ID)
	return float(CpowerMonitor.getCurrwattFormDb())
    except:
#	notification.EmailNotification().sendEmail('Error!!! : Fail to get server data. that plugin name is %s'%(PLUGIN_NAME))
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
          'call_back': power_handler,
          'time_max': 90,
          'value_type': 'float',
          'units': 'xxx',
          'slope': 'both',
          'format': '%.4f',
          'description': 'bond of host',
          'groups': 'temp'
    }
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "100",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "101",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "102",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "103",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "104",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "105",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "106",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "107",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "108",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "109",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "110",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "111",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "112",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "113",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "114",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "115",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "116",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "117",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "118",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "119",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "155",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "121",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "122",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "123",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "124",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "151",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "152",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "127",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "128",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "129",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "130",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "131",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "132",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "133",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "134",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "135",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "136",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "137",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "138",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "139",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "140",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "141",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "142",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "143",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "144",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "145",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "146",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "147",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "148",
    }))
    descriptors.append(create_desc(Desc_Skel, {
        "name" : NAME_PREFIX + "149",
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
