from django.conf.urls import patterns, include, url
from inwin.stock.views import orders
from inwin.stock.views import clean


urlpatterns = patterns('',
   
    url(r'^order_order_handler/$',        orders.order_order_handler, name='stock_order_order_handler'),
    url(r'^order_order_config/$',         orders.order_order_config,  name='stock_order_order_config'),
    
    url(r'^order_transaction_handler/$',    orders.order_transaction_handler, name='stock_order_transaction_handler'),
    url(r'^order_transaction_config/$',     orders.order_transaction_config,  name='stock_order_transaction_config'),
    
    url(r'^order_portfolio_handler/$',    orders.order_portfolio_handler, name='stock_order_portfolio_handler'),
    url(r'^order_portfolio_config/$',     orders.order_portfolio_config,  name='stock_order_portfolio_config'),
    
    url(r'^clean_order_handler/$',        clean.clean_order_handler, name='stock_clean_order_handler'),
    url(r'^clean_order_config/$',         clean.clean_order_config,  name='stock_clean_order_config'),
    
    url(r'^clean_transaction_handler/$',    clean.clean_transaction_handler, name='stock_clean_transaction_handler'),
    url(r'^clean_transaction_config/$',     clean.clean_transaction_config,  name='stock_clean_transaction_config'),
    
    url(r'^clean_portfolio_handler/$',    clean.clean_portfolio_handler, name='stock_clean_portfolio_handler'),
    url(r'^clean_portfolio_config/$',     clean.clean_portfolio_config,  name='stock_clean_portfolio_config'),
    
    #Api to receive form order
    url(r'^order_api/$',                  orders.stock_order_api, name='stock_order_api'),
)
