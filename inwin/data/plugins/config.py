from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class clean_config_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Clean Config Tradingdate")
    #render_template = "test_fund_trading_grid.html"
    render_template = "tradingdate.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(clean_config_Plugin)