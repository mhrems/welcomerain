from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
  ('^api/$', 'api.views.index')),
  ('^api/getClusterList/$', 'api.views.getClusterList')),
)


