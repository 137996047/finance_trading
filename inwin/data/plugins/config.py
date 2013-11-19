from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from inwin.data.form import date_form
from inwin.data.models.stockdata import tradingparameter

class tradingdate_config_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Tradingdate Config Tradingdate")
    #render_template = "test_fund_trading_grid.html"
    render_template = "tradingdate.html"
    
    
    def render(self, context, instance, placeholder):
        parameter=tradingparameter.objects.getTradingParameter()
        context.update({
            'object':instance,
            'placeholder':placeholder,
            'parameter':  parameter,
        })
        return context

plugin_pool.register_plugin(tradingdate_config_Plugin)


class matching_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Trading Matching")
    #render_template = "test_fund_trading_grid.html"
    render_template = "tradingmatch.html"
    
    
    def render(self, context, instance, placeholder):
        parameter=tradingparameter.objects.getTradingParameter()
        context.update({
            'object':instance,
            'placeholder':placeholder,
            'parameter':  parameter,
        })
        return context

plugin_pool.register_plugin(matching_Plugin)

class settle_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Settle Transaction")
    #render_template = "test_fund_trading_grid.html"
    render_template = "tradingsettle.html"
    
    
    def render(self, context, instance, placeholder):
        parameter=tradingparameter.objects.getTradingParameter()
        context.update({
            'object':instance,
            'placeholder':placeholder,
            'parameter':  parameter,
        })
        return context

plugin_pool.register_plugin(settle_Plugin)