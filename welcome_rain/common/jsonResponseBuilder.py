import datetime
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import simplejson
from django.utils.encoding import smart_unicode
from django.core import serializers
from django.forms.models import model_to_dict
from mhrlog import logInfo


class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            assert settings.TIME_ZONE == 'UTC'
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        return simplejson.JSONEncoder.default(self, obj)


def dumps(value):
    return JSONEncoder().encode(value)


def loads(txt):
    value = simplejson.loads(
        txt,
        parse_float=Decimal,
        encoding=settings.DEFAULT_CHARSET
    )
    return value


class JSONDict(dict):
    """
    Hack so repr() called by dumpdata will output JSON instead of
    Python formatted data.  This way fixtures will work!
    """
    def __repr__(self):
        return dumps(self)

class JSONList(list):
    """
    As above
    """
    def __repr__(self):
        return dumps(self)


class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.  Main thingy must be a dict object."""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = '{}'
        models.TextField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value is None or value == '':
            return {}
        elif isinstance(value, basestring):
            res = loads(value)
            if isinstance(res, dict):
                return JSONDict(**res)
            else:
                return JSONList(res)

        else:
            return value

    def get_db_prep_save(self, value, connection):
        """Convert our JSON object to a string before we save"""
        if not isinstance(value, (list, dict)):
            return super(JSONField, self).get_db_prep_save("", connection=connection)
        else:
            return super(JSONField, self).get_db_prep_save(dumps(value),
                                                           connection=connection)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
    
    
class jsonResponseBuilder():
    def __init__(self):
        self.isQuerySet = False
        self.data = None
        self.code = None
        self.msg = None
        self.excludeFields = None
        self.extraField = []
        self.extraValue = []
        
        
    def model_to_dict(self,obj, exclude=['AutoField', 'ForeignKey','OneToOneField']):
        '''
            serialize model object to dict with related objects
    
            author: Vadym Zakovinko <vp@zakovinko.com>
            date: January 31, 2011
            http://djangosnippets.org/snippets/2342/
        '''
        tree = {}
        for field_name in obj._meta.get_all_field_names():
            try:
                field = getattr(obj, field_name)
            except (ObjectDoesNotExist, AttributeError):
                continue
     
            if field.__class__.__name__ in ['RelatedManager', 'ManyRelatedManager']:
                if field.model.__name__ in exclude:
                    continue
     
                if field.__class__.__name__ == 'ManyRelatedManager':
                    exclude.append(obj.__class__.__name__)
                subtree = []
                for related_obj in getattr(obj, field_name).all():
                    value = model_to_dict(related_obj, \
                        exclude=exclude)
                    if value:
                        subtree.append(value)
                if subtree:
                    tree[field_name] = subtree
     
                continue
     
            field = obj._meta.get_field_by_name(field_name)[0]
            if field.__class__.__name__ in exclude:
                continue
     
            if field.__class__.__name__ == 'RelatedObject':
                exclude.append(field.model.__name__)
                tree[field_name] = model_to_dict(getattr(obj, field_name), \
                    exclude=exclude)
                continue
     
            value = getattr(obj, field_name)
            if value:
                tree[field_name] = value
     
        return tree
    
    def queryset2Dict(self,querySet):
        data = dict()
        index = 0
        for model in querySet:
            data['data'+str(index)] = self.model_to_dict(model)
            index=index+1
        return data
    
    def setStatus(self,code,msg):
        self.code = code
        self.msg = msg
    
    def addJsonString(self,str):
        return "\"" + str + "\""
    
    def addStringJosnItem(self,field,value):
        return self.addJsonString(field)+":"+self.addJsonString(value)

    def addNumericJosnItem(self,field,value):
        return self.addJsonString(field)+":"+value
    
    def addBracket(self,str):
        return "{" + str + "}"
    
    def getExtraString(self):
        extra = ""        
        extraCount = len(self.extraField)
        for index in range(extraCount):
            extra = extra + self.addStringJosnItem(self.extraField[index],self.extraValue[index]) 
            if (index != (extraCount -1)):
                extra = extra +","
        
        return extra
    
        
    def buildJsonString(self):
        status_msg = self.addStringJosnItem("message", self.msg)
        status_code = self.addNumericJosnItem("code", str(self.code))
        status = self.addNumericJosnItem("status", "{"+status_code+","+status_msg+"}")
        extra = self.addNumericJosnItem("extra", "{" + self.getExtraString() + "}")
     
        if not self.data:
            return self.addBracket(status+","+extra)
             
        data = self.addNumericJosnItem("data", serializers.serialize('json', self.data, excludes=self.excludeFields,relations=self.relationsFields))
        return self.addBracket(status+","+extra+","+data)

        
    def toJson(self):
        if not self.isQuerySet:
            #logInfo("not queryset")
            response = dict()
            response['status'] = {"code": self.code , "message":self.msg}
            if self.data:
                response['data'] = self.data
            jsonResponse = JSONEncoder().encode(response)
            return jsonResponse 

        #jsonResponse = serializers.serialize('json', self.data)
        #print "json type="+str(jsonResponse.__class__)
        jsonResponse = self.buildJsonString()
        return jsonResponse 

    def addExtra(self,name,value):
        self.extraField.append(name)
        self.extraValue.append(value) 
    
    def setData(self,dictData):
        self.data = dictData
        #self.response['data'] = dictData
    
    def setQuerysetData(self,queryset,excludeFields,relations=()):
        #logInfo("setQueryData : queryset="+str(queryset.count()))        
        self.isQuerySet = True
        self.data = queryset
        self.excludeFields = excludeFields
        self.relationsFields = relations
        #model_dict = model.in_bulk(ids)
        #serializers.serialize('json', model)
    