from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class stock_order_order_current_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Stock Order Current")
    #render_template = "test_fund_trading_grid.html"
    render_template = "stock_order_order.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(stock_order_order_current_Plugin)

class stock_order_order_record_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Stock Order Record")
    render_template = "stock_order_order.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(stock_order_order_record_Plugin)

class stock_order_transaction_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Stock Order Transaction")
    render_template = "stock_order_transaction.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(stock_order_transaction_Plugin)

class stock_order_portfolio_Plugin(CMSPluginBase):
    model = CMSPlugin
    module = _('inwin')
    name = _("Stock Order Portfolio")
    render_template = "stock_order_portfolio.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(stock_order_portfolio_Plugin)