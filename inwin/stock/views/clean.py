import logging
from inwin.utils.http import get_request_info
#from django.shortcuts import render
from django.shortcuts import render_to_response
#from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
# Create your views here.
from django.utils.translation import ugettext as _
from inwin.stock.models.transaction import stock_transaction,stock_portfolio
#from inwin.data.models.stockdata import stocksymbol
from jqgrid import JqGrid
from django.core.urlresolvers import reverse_lazy
from datetime import date
TSTYPE_CHOICES = { 'value':{'1': _('purchase'),'2': _('withdraw'),'3': _('dividend'),'4': _('interest')}}
Date_picker = { 'dataInit':'pickdates' }

def clean_stock_record(request):
    #template=get_template('stock_trading.html')
    
    #return render(request, 'stock_trading.html', data)
    return render_to_response('stockclean_record.html', None, context_instance=RequestContext(request))

"""
   The jason api for grid handling
"""    
class clean_order_grid(JqGrid):
    model = stock_transaction # could also be a queryset
    fields = ['id','F_Date','F_SKID','F_TSType','F_Qty','F_Price','F_CurID','F_OrderType','F_Market','F_Status','F_Note','F_User'] # optional 
    url = reverse_lazy('stockclean_record_handler')
    #queryset = stock_transaction.objects.filter(F_Date__range=[date.today(),date.today()]).values(*fields)
    caption = _('tock Trading Settle Clean Order List') # optional
    colmodel_overrides = {
        'id': { 'editable': False, 'index':'id', 'label':_('id')},
        'F_Date': { 'editable': False, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_SKID': { 'editable': True, 'index':'F_Date', 'label':_('stockID')},
        'F_TSType': { 'editable': True, 'edittype':'select', 'editoptions':TSTYPE_CHOICES ,'label': _('Trading Type')},
        'F_Qty':{ 'editable': True, 'index':'F_Date', 'label':_('Qty')},
        'F_Price':{ 'editable': True, 'index':'F_Date', 'label':_('Price')},
        'F_CurID':{ 'editable': False, 'index':'F_Date', 'label':_('Currency')},
        'F_OrderType':{ 'editable': False, 'index':'F_Date', 'label':_('OrderType')},
        'F_Marekt':{ 'editable': False, 'index':'F_Date', 'label':_('Market')},
        'F_Status':{ 'editable': False, 'index':'F_Date', 'label':_('Settle Status')},
        'F_Note': { 'editable': False, 'index':'F_Note', 'label':_('Note')},
        'F_User':{ 'editable': False, 'index':'F_Date', 'label':_('User ID')},
    }


def clean_order_handler(request):
    grid = clean_order_grid()
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

def clean_order_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = clean_order_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")
 
class clean_transaction_grid(JqGrid):
    
    fields = ['id','F_Date','F_SKID','F_TSType','F_CurID','F_Amt','F_Qty','F_Rate','F_Price','F_Fee','F_Exp','F_Status','F_Cost','F_Net','F_SettleDate','F_Payable','F_Receivable','F_Note','F_User'] # optional 
    url = reverse_lazy('stockclean_order_handler')
    queryset = stock_transaction.objects.filter(F_Date__range=[date.today(),date.today()]).values(*fields)
    caption = _('Stock Trading Settle Clean Transaction List') # optional
    colmodel_overrides = {
        'id': { 'editable': False, 'index':'id', 'label':_('id')},
        'F_Date': { 'editable': True, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_SKID': { 'editable': True, 'index':'F_Date', 'label':_('stockID')},
        'F_TSType': { 'editable': True, 'edittype':'select', 'editoptions':TSTYPE_CHOICES ,'label': _('Trading Type')},
        'F_CurID':{ 'editable': True, 'index':'F_Date', 'label':_('Currency')},
        'F_Amt':{ 'editable': True, 'index':'F_Date', 'label':_('Amount')},
        'F_Qty':{ 'editable': False, 'index':'F_Date', 'label':_('Quantity')},
        'F_Rate':{ 'editable': False, 'index':'F_Date', 'label':_('Rate')},
        'F_Price':{ 'editable': False, 'index':'F_Date', 'label':_('Price')},
        'F_Fee':{ 'editable': False, 'index':'F_Date', 'label':_('Fee')},
        'F_Exp':{ 'editable': False, 'index':'F_Date', 'label':_('Expense')},
        'F_Tax':{ 'editable': False, 'index':'F_Date', 'label':_('Expense')},
        'F_Status':{ 'editable': False, 'index':'F_Date', 'label':_('Settle Status')},
        'F_Cost':{ 'editable': False, 'index':'F_Date', 'label':_('Cost')},
        'F_Net':{ 'editable': False, 'index':'F_Date', 'label':_('Net')},
        'F_SettleDate':{ 'editable': False, 'index':'F_Date', 'label':_('Settle Date')},
        'F_Payable':{ 'editable': False, 'index':'F_Date', 'label':_('Pay Amount')},
        'F_Receivable':{ 'editable': False, 'index':'F_Date', 'label':_('Receive Amount')},
        'F_Note': { 'editable': True, 'index':'F_Note', 'label':_('Note')},
        'F_User':{ 'editable': False, 'index':'F_Date', 'label':_('User ID')},
    }


def clean_transaction_handler(request):
    grid = clean_transaction_grid()
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

def clean_transaction_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = clean_transaction_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")

"""
   The jason api for portfolio grid handling
"""    
class clean_portfolio_grid(JqGrid):
    
    fields = ['id','F_Date','F_SettleDate','F_SKID','F_CurID','F_Qty','F_Cost','F_AvgCost','F_AvgRate','F_ClosePrice','F_User'] # optional 
    url = reverse_lazy('stockclean_order_handler')
    queryset = stock_portfolio.objects.filter(F_Date__range=[date.today(),date.today()]).values(*fields)
    caption = _('Stock Trading Settle Clean Portfolio List') # optional
    colmodel_overrides = {
        'id': { 'editable': False, 'index':'id', 'label':_('id')},
        'F_Date': { 'editable': False, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_SKID': { 'editable': True, 'index':'F_Date', 'label':_('stockID')},
        'F_SettleDate': { 'editable': False, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_CurID':{ 'editable': False, 'index':'F_Date', 'label':_('Currency')},
        'F_Qty':{ 'editable': True, 'index':'F_Date', 'label':_('Qty')},
        'F_Cost':{ 'editable': True, 'index':'F_Date', 'label':_('F_Cost')},
        'F_AvgCost':{ 'editable': False, 'index':'F_Date', 'label':_('F_AvgCost')},
        'F_AvgRate':{ 'editable': False, 'index':'F_Date', 'label':_('F_AvgRate')},
        'F_ClosePrice':{ 'editable': True, 'index':'F_Date', 'label':_('F_ClosePrice')},
        'F_User': { 'editable': False, 'index':'F_Note', 'label':_('F_User')},
    }


def clean_portfolio_handler(request):
    grid = clean_portfolio_grid()
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

def clean_portfolio_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = clean_portfolio_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")