from django.conf.urls import patterns, include, url

from inwin.data.views import tradingdate_view


urlpatterns = patterns('',
   
    #Api for plugins   
    url(r'^tradingdate_handler/$',              tradingdate_view.tradingdate_handler, name='tradingdate_handler'),
    url(r'^tradingdate_config/$',               tradingdate_view.tradingdate_config,  name='tradingdate_config'),
)
