from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import inwin.stock.urls
import inwin.fund.urls
import inwin.data.urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance_trading.views.home', name='home'),
    # url(r'^finance_trading/', include('finance_trading.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #fund_order accept django-form-designer post data
    #url(r'^allauth_accounts/', include('allauth.urls')),
    
       
    url(r'^stock/', include(inwin.stock.urls)),
    url(r'^fund/', include(inwin.fund.urls)),
    url(r'^data/', include(inwin.data.urls)),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns

#for local developing add these staticfile urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# ... the rest of your URLconf goes here ...
urlpatterns += staticfiles_urlpatterns()