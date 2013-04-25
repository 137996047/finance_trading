"""
main url configuration file for the inwin site
"""
from django.conf.urls.defaults import patterns, include, handler404, handler500, url
from django.conf import settings

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('allauth.urls')),
    url(r'%s' % settings.INWIN_URL, include('inwin.urls')),
    #url(r'^accounts/', include('django.contrib.auth.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    
    #(r'^admin/c5filemanager/', include('c5filemanager.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #(r'^avatar/', include('avatar.urls')),
    #(r'^cache/', include('keyedcache.urls')), - broken views disable for now
    #(r'^settings/', include('askbot.deps.livesettings.urls')),
    #(r'^followit/', include('followit.urls')),
    #(r'^robots.txt$', include('robots.urls')),
    
    url( # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT.replace('\\','/')},
    ),
    url(r'^', include('cms.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                    url(r'^rosetta/', include('rosetta.urls')),
                )
                
