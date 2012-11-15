from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'welcome_rain.views.home', name='home'),
    # url(r'^welcome_rain/', include('welcome_rain.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url('^api/', 'welcome_rain.api.views.index'),
        
    url(r'^$', 'welcome_rain.views.view_dashboard.index3'),
    url(r'^chart', 'welcome_rain.views.view_chart.index'),
    url(r'^present', 'welcome_rain.views.view_present.index'),
    url(r'^alerts', 'welcome_rain.views.view_alert.index'),
    url(r'^setting', 'welcome_rain.views.view_setting.index'),
    url(r'^event', 'welcome_rain.views.view_event.index'),
    url(r'^summary', 'welcome_rain.views.view_summary.index'),
    url(r'^dataSource', 'welcome_rain.views.view_dataSource.index'),
    url(r'^serverChartView', 'welcome_rain.views.view_serverView.chartIndex'),
    url(r'^serverTextView', 'welcome_rain.views.view_serverView.textIndex'),
    url(r'^server', 'welcome_rain.views.view_server.index'),
            
    #url(r'^trend', 'welcome_rain.views.view_trend.index'),
    url(r'^trendServer', 'welcome_rain.views.view_trendServer.index'),

    #url(r'^trend/(?P<cluster>\w+)/(?P<host>\w+)/$', 'welcome_rain.views.view_trend.index'),

    #url(r'^cli', 'welcome_rain.cli.views.cli'),
   
    url('^api/getClusterList/$', 'welcome_rain.api.views.getClusterList'),
    url('^api/getHostList/$', 'welcome_rain.api.views.getHostList'),
    url('^api/getDataSourceList/$', 'welcome_rain.api.views.getDataSourceList'),
    url('^api/getData/$', 'welcome_rain.api.views.getData'),    
    url('^api/getAlertHourlyData/$', 'welcome_rain.api.views.getAlertHourlyData'),    
    url('^api/getServerDownHourlyData/$', 'welcome_rain.api.views.getServerDownHourlyData'),    
    url('^api/getAbnormalStatHourlyData/$', 'welcome_rain.api.views.getAbnormalStatHourlyData'),  
    url('^api/getUserFavoriteChartList/$', 'welcome_rain.api.views.getUserFavoriteChartList'),    
    url('^api/registerUserFavoriteChart/$', 'welcome_rain.api.views.registerUserFavoriteChart'),    
    url('^api/removeUserFavoriteChart/$', 'welcome_rain.api.views.removeUserFavoriteChart'),   
    url('^api/getAlertHistory/$','welcome_rain.api.views.getAlertHistory'),
    url('^api/getAlertDetail/$','welcome_rain.api.views.getAlertDetail'),
    url('^api/addServer/$','welcome_rain.api.views.addServer'),
    url('^api/deleteServer/$','welcome_rain.api.views.deleteServer'),
    url('^api/editServer/$','welcome_rain.api.views.editServer'),
    #url('^api/editServer/$','welcome_rain.api.views.editServer'),
    url('^api/getDashboardTargetList/$','welcome_rain.api.views.getDashboardTargetList'),
    url('^api/getAvailablePluginList/$','welcome_rain.api.views.getAvailablePluginList'),
    url('^api/getServerGroupList/$','welcome_rain.api.views.getServerGroupList'),
    url('^api/getServerDetail/$','welcome_rain.api.views.getServerDetail'),
    
    url('^api/editUserProfile/$','welcome_rain.api.views.editUserProfile'),
    
    url('^api/updateGmetadConf/$','welcome_rain.api.views.updateGmetadConf'),
    url('^api/updateGmondConf/$','welcome_rain.api.views.updateGmondConf'),
    url('^api/updateUserConf/$','welcome_rain.api.views.updateUserConf'),
    #remote related apis
    url('^api/newTask/$','welcome_rain.api.remotes.newTask'),
    url('^api/updateTask/$','welcome_rain.api.remotes.updateTask'),
    url('^api/getTaskList/$','welcome_rain.api.remotes.getTaskList'),
    url('^api/addTaskStatus/$','welcome_rain.api.remotes.addTaskStatus'),
    url('^api/queryTaskStatus/$','welcome_rain.api.remotes.queryTaskStatus'),
    url('^api/addPlugin/$','welcome_rain.api.remotes.addPlugin'),
    
    url('^api/downloadxls/$','welcome_rain.api.views.downloadxls'),
    
    url('^api/addEvent/$','welcome_rain.api.views.addEvent'),
    url('^api/deleteEvent/$','welcome_rain.api.views.deleteEvent'),
    url('^api/addAlert/$','welcome_rain.api.views.addAlert'),
    url('^api/addAlertHistory/$','welcome_rain.api.views.addAlertHistory'),
    url('^api/addServerDown/$','welcome_rain.api.views.addServerDown'),
    url('^api/addAbnormalStat/$','welcome_rain.api.views.addAbnormalStat'),
    

    
    ('^cli/?', include('welcome_rain.cli.urls')),

)

urlpatterns += patterns('',
    url(r'^accounts/login/$','django.contrib.auth.views.login'),
    url(r'^accounts/logout$','django.contrib.auth.views.logout',{'next_page':'/'})
)

urlpatterns += patterns('',
    url('^grahpDetail/$','welcome_rain.dashboard.views.grahpdetail'),
    
    #url(r'^alerts/$','welcome_rain.dashboard.views.alerts'),
    #url(r'^addchart/$','welcome_rain.home.views.addchart'),
    #url(r'^host/add/$','welcome_rain.dashboard.views.hostadd'),
    #url(r'^host/delete/$','welcome_rain.dashboard.views.hostdelete'),
    #url(r'^host/edit/$','welcome_rain.dashboard.views.hostedit'),
    #url(r'^host/$','welcome_rain.dashboard.views.host'),
)

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns