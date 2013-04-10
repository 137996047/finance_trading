from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class fund_order_order_current_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Fund Order Current")
    #render_template = "test_fund_trading_grid.html"
    render_template = "fund_order_order.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(fund_order_order_current_Plugin)

class fund_order_order_record_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Fund Order Record")
    render_template = "fund_order_order.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(fund_order_order_record_Plugin)

class fund_order_transaction_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Fund Order Transaction")
    render_template = "fund_order_transaction.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(fund_order_transaction_Plugin)

class fund_order_portfolio_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Fund Order Portfolio")
    render_template = "fund_order_portfolio.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(fund_order_portfolio_Plugin)