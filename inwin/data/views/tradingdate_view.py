import logging
import sys
#from inwin.utils.http import get_request_info
#from django.shortcuts import render
from django.shortcuts import render_to_response
#from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
# Create your views here.
from django.utils.translation import ugettext as _
#from inwin.data.models import stockdata
from inwin.data.models.stockdata import tradingdate,tradingparameter
from inwin.data.form import date_form
from inwin.stock.models.transaction import Match,Settle
from jqgrid import JqGrid
from django.core.urlresolvers import reverse_lazy
from datetime import date
from django.shortcuts import get_object_or_404
from django.utils import simplejson
"""
   The jason api for grid handling
"""    
class tradingdate_grid(JqGrid):
    model = tradingdate # could also be a queryset
    fields = ['tDate','HK','US','TW','CN','Opened','Settled'] # optional 
    url = reverse_lazy('tradingdate_handler')
    #queryset = tradingdate.objects.filter(tDate__range=[date.today(),date.today()]).values(*fields)
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

def tradingdate_setting(request):
    if request.method == "POST":
        try:
            f_date = request.POST['F_Date']
            f_market = request.POST['F_Market']
            tradingdate=tradingparameter.objects.setTradingDate(f_date, f_market)
            if tradingdate!=None:
                data = simplejson.dumps({
                    'message': _('successful'),
                    'F_Date': tradingdate,
                })
            else:    
                data = simplejson.dumps({
                    'message': _('fail'),
                    'F_Date': None,
                })

        except:
            data = simplejson.dumps({
                'message': unicode(sys.exc_info()[0]),
                'F_Date': None,
            })
    return HttpResponse(data, mimetype = 'application/json')

def trading_match(request):
    if request.method == "POST":
        try:
            f_market = request.POST['F_Market']
            #user = request.user
            tradingdate=tradingparameter.objects.getTradingDate(f_market)
            if f_market == 'ALL':
                Match('TW',tradingparameter.objects.getTradingDate('TW'))
                Match('HK',tradingparameter.objects.getTradingDate('HK'))
                Match('US',tradingparameter.objects.getTradingDate('US'))
                Match('CN',tradingparameter.objects.getTradingDate('CN'))
            else:
                message=Match(f_market,tradingdate)
                
                if tradingdate!=None:
                    data = simplejson.dumps({
                        'message': _('successful') + message,
                        'F_Date': tradingdate.strftime("%Y-%m-%d"),
                    })
                else:    
                    data = simplejson.dumps({
                        'message': _('fail! Please set trading date first') + message,
                        'F_Date': None,
                    })
            

        except  Exception, e:
            data = simplejson.dumps({
                'message': unicode(e)+unicode(sys.exc_info()[0]),
                'F_Date': None,
            })
    return HttpResponse(data, mimetype = 'application/json')

def trading_settle(request):
    if request.method == "POST":
        try:
            f_market = request.POST['F_Market']
            #user = request.user
            tradingdate=tradingparameter.objects.getTradingDate(f_market)
            if f_market == 'ALL':
                Settle('TW',tradingparameter.objects.getTradingDate('TW'))
                Settle('HK',tradingparameter.objects.getTradingDate('HK'))
                Settle('US',tradingparameter.objects.getTradingDate('US'))
                Settle('CN',tradingparameter.objects.getTradingDate('CN'))
            else:
                Settle(f_market,tradingdate)
                
                if tradingdate!=None:
                    data = simplejson.dumps({
                        'message': _('successful'),
                        'F_Date': tradingdate.strftime("%Y-%m-%d"),
                    })
                else:    
                    data = simplejson.dumps({
                        'message': _('fail! Please set trading date first'),
                        'F_Date': None,
                    })
            

        except:
            data = simplejson.dumps({
                'message': unicode(sys.exc_info()[0]),
                'F_Date': None,
            })
    return HttpResponse(data, mimetype = 'application/json')
def tradingdate_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = tradingdate_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")

def update_trading_date(request, space_name):

    """
    Saves the note content and position within the table.
    """
    #place = get_object_or_404(Space, url=space_name)
    tdate_form = date_form(request.POST or None)

    if request.method == "POST" and request.is_ajax:
        msg = "The operation has been received correctly."          
        print request.POST

    else:
        msg = "GET petitions are not allowed for this view."

    return HttpResponse(msg)