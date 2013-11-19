from django.conf.urls import patterns, include, url
from inwin.fund.views import orders
from inwin.fund.views import clean
from inwin.fund.views import marketdata

urlpatterns = patterns('',   
    url(r'^marketdata_scale_handler/$',         marketdata.marketdata_scale_handler, name='fund_marketdata_scale_handler'),
    url(r'^marketdata_scale_config/$',          marketdata.marketdata_scale_config,  name='fund_marketdata_scale_config'),
    url(r'^marketdata_addscale_handler/$',          marketdata.marketdata_addscale_handler,  name='fund_marketdata_addscale_handler'),

    url(r'^order_order_handler/$',         orders.order_order_handler, name='fund_order_order_handler'),
    url(r'^order_order_config/$',          orders.order_order_config,  name='fund_order_order_config'),
     
    url(r'^order_transaction_handler/$',    orders.order_transaction_handler, name='fund_order_transaction_handler'),
    url(r'^order_transaction_config/$',     orders.order_transaction_config,  name='fund_order_transaction_config'),
    
    url(r'^order_portfolio_handler/$',     orders.order_portfolio_handler, name='fund_order_portfolio_handler'),
    url(r'^order_portfolio_config/$',      orders.order_portfolio_config,  name='fund_order_portfolio_config'),
    
    url(r'^clean_order_handler/$',         clean.clean_order_handler, name='fund_clean_order_handler'),
    url(r'^clean_order_config/$',          clean.clean_order_config,  name='fund_clean_order_config'),
    
    url(r'^clean_transaction_handler/$',    clean.clean_transaction_handler, name='fund_clean_transaction_handler'),
    url(r'^clean_transaction_config/$',     clean.clean_transaction_config,  name='fund_clean_transaction_config'),
    
    url(r'^clean_portfolio_handler/$',     clean.clean_portfolio_handler, name='fund_clean_portfolio_handler'),
    url(r'^clean_portfolio_config/$',      clean.clean_portfolio_config,  name='fund_clean_portfolio_config'),
    
    #Api to receive form order
    url(r'^order_api/$',                  orders.fund_order_api, name='fund_order_api'),
    url(r'^marketdata_scale_create/$',          marketdata.marketdata_scale_create,  name='fund_marketdata_scale_create'),
)

