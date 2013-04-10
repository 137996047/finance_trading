import logging
#from inwin.utils.http import get_request_info
#from django.shortcuts import render
from django.shortcuts import render_to_response
#from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
# Create your views here.
from django.utils.translation import ugettext as _
#from inwin.data.models import stockdata
from inwin.data.models.stockdata import tradingdate
from jqgrid import JqGrid
from django.core.urlresolvers import reverse_lazy
from datetime import date


"""
   The jason api for grid handling
"""    
class tradingdate_grid(JqGrid):
    model = tradingdate # could also be a queryset
    fields = ['tDate','HK','US','TW','CN','Opened','Settled'] # optional 
    url = reverse_lazy('tradingdate_handler')
    #queryset = stock_transaction.objects.filter(F_Date__range=[date.today(),date.today()]).values(*fields)
    caption = _('Trading Date Config') # optional
    extra_config = {'sortname': 'tDate'}
    #extra_config = {'onSelectRow': 'function(id){if(id && id!==lastsel2){jQuery("#tradingdate_table").jqGrid("restoreRow",lastsel2);jQuery("#tradingdate_table").jqGrid("editRow",id,true);lastsel2=id;}}'}
    colmodel_overrides = {
        'tDate': { 'editable': False, 'index':'tDate', 'label':_('Trading Date')},
        'HK': { 'editable': True, 'index':'HK', 'label':_('HK'),'edittype':'"checkbox"','editoptions': '{value:"Y:N"}'},
        'US': { 'editable': True, 'index':'US', 'label':_('US'),'edittype':'"checkbox"','editoptions': '{value:"Y:N"}'},
        'TW': { 'editable': True, 'index':'TW', 'label':_('TW'),'edittype':'"checkbox"','editoptions': '{value:"Y:N"}'},
        'CN': { 'editable': True, 'index':'CN', 'label':_('CN'),'edittype':'"checkbox"','editoptions': '{value:"Y:N"}'},
        'Opened':{ 'editable': False, 'index':'Opened', 'label':_('Opened')},
        'Settled':{ 'editable': False, 'index':'Settled', 'label':_('Settled')},
    }


def tradingdate_handler(request):
    grid = tradingdate_grid()
    if request.method == 'POST':
        functions = {
                     'edit': grid.edit_queryset,
                     'add': grid.add_queryset,
                     'del': grid.del_queryset,
                     }
        fun=functions[request.POST['oper']]
        fun(request)
    #else:
        
    
    return HttpResponse(grid.get_json(request), mimetype="application/json")

def tradingdate_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = tradingdate_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")