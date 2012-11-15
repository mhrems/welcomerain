"""Copyright 2008 Orbitz WorldWide

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import imp
from os.path import splitext, basename
import socket
import errno
import time
import datetime
import pytz

from django.core.exceptions import ObjectDoesNotExist


#from django.contrib.auth.models import User
#from graphite.account.models import Profile
#from graphite.logger import log


# There are a couple different json modules floating around out there with
# different APIs. Hide the ugliness here.
try:
    import json
except ImportError:
    import simplejson as json

if hasattr(json, 'read') and not hasattr(json, 'loads'):
    json.loads = json.read
    json.dumps = json.write
    json.load = lambda file: json.read( file.read() )
    json.dump = lambda obj, file: file.write( json.write(obj) )


def getProfile(request,allowDefault=True):
    return None
    """
      if request.user.is_authenticated():
        try:
          return request.user.profile
        except ObjectDoesNotExist:
          profile = Profile(user=request.user)
          profile.save()
          return profile
      elif allowDefault:
        return defaultProfile
    s"""
  
def getProfileByUsername(username):
    try:
        user = User.objects.get(username=username)
        return Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        return None


def is_local_interface(host):
    if ':' in host:
        host = host.split(':',1)[0]

        for port in xrange(1025, 65535):
            try:
                sock = socket.socket()
                sock.bind( (host,port) )
                sock.close()

            except socket.error, e:
                if e.args[0] == errno.EADDRNOTAVAIL:
                    return False
                else:
                    continue
    else:
        return True

    raise Exception("Failed all attempts at binding to interface %s, last exception was %s" % (host, e))


def is_pattern(s):
    return '*' in s or '?' in s or '[' in s or '{' in s

def is_escaped_pattern(s):
    for symbol in '*?[{':
        i = s.find(symbol)
        if i > 0:
            if s[i-1] == '\\':
                return True
            return False

def find_escaped_pattern_fields(pattern_string):
    pattern_parts = pattern_string.split('.')
    for index,part in enumerate(pattern_parts):
        if is_escaped_pattern(part):
            yield index


def getTodayStartEndTime(type=0):
    now = datetime.datetime.now()
    if type==0:
        startTime = now.strftime("%Y:%m:%d 00:00")
        endTime = now.strftime("%Y:%m:%d %H:%M")
    else:
        startTime = now.strftime("%Y:%m:%d:00:00:00")
        endTime = now.strftime("%Y:%m:%d:%H:%M:%S")
    
    return startTime,endTime

def getTodayDateTimeToken():
    now = datetime.datetime.now()
    today = now.strftime("%Y:%m:%d:%H:%M:%S")
    return today.split(":")


def isNumeric(value):
    try:
        result = value + 1
        return True
    except ValueError:
        return False
    except TypeError:
        return False

    return True


def convertUTCToDateTimeToken(utc):
    dated = datetime.datetime.fromtimestamp(float(utc))
    #dated = time.gmtime(utc)
    datedString = dated.strftime("%Y:%m:%d:%H:%M:%S")
    return datedString.split(":")

"""
try:
  defaultUser = User.objects.get(username='default')
except User.DoesNotExist:
  log.info("Default user does not exist, creating it...")
  randomPassword = User.objects.make_random_password(length=16)
  defaultUser = User.objects.create_user('default','default@localhost.localdomain',randomPassword)
  defaultUser.save()

try:
  defaultProfile = Profile.objects.get(user=defaultUser)
except Profile.DoesNotExist:
  log.info("Default profile does not exist, creating it...")
  defaultProfile = Profile(user=defaultUser)
  defaultProfile.save()
"""

def getDjangoStyleDateTime(javaDateTime):
    oDateTimeList = javaDateTime.split(':')
    return datetime.datetime(int(oDateTimeList[0]), int(oDateTimeList[1]), int(oDateTimeList[2]),int(oDateTimeList[3]),int(oDateTimeList[4]),0,0)

def load_module(module_path, member=None):
    module_name = splitext(basename(module_path))[0]
    module_file = open(module_path, 'U')
    description = ('.py', 'U', imp.PY_SOURCE)
    module = imp.load_module(module_name, module_file, module_path, description)
    if member:
        return getattr(module, member)
    else:
        return module

def timestamp(datetime):
    "Convert a datetime object into epoch time"
    return time.mktime( datetime.timetuple() )
  
def validateHTTPRequest(request):
    if request.method =='GET':
        return False
    return True

def badRequestResponse():
    return "ok"


if __name__ == "__main__":
    utc= 1350523473
    print convertUTCToDateTimeToken(utc)
    