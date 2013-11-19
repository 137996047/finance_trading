from django.conf.urls import patterns, include, url

from inwin.data.views import tradingdate_view


urlpatterns = patterns('',
   
    #Api for plugins   
    url(r'^tradingdate_handler/$',              tradingdate_view.tradingdate_handler,   name='tradingdate_handler'),
    url(r'^tradingdate_config/$',               tradingdate_view.tradingdate_config,    name='tradingdate_config'),
    url(r'^tradingdate_setting/$',              tradingdate_view.tradingdate_setting,   name='tradingdate_setting'),
    url(r'^trading_match/$',                    tradingdate_view.trading_match,     name='trading_match'),
    url(r'^trading_settle/$',                   tradingdate_view.trading_settle,    name='trading_settle'),
)
