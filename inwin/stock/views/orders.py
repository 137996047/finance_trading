'''
Created on 2013/3/10

@author: yhuang
'''
import logging
#from django.shortcuts import render
from django.shortcuts import render_to_response
#from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
# Create your views here.
from django.utils.translation import ugettext as _
from jqgrid import JqGrid
from django.core.urlresolvers import reverse_lazy
from inwin.data.models.stockdata import stocksymbol
from inwin.stock.models.transaction import stock_order as placeorder
from inwin.stock.models.transaction import stock_transaction
from inwin.stock.models.transaction import stock_portfolio
from inwin.stock.orderform import orderform
from inwin.utils.http import get_request_info

TSTYPE_CHOICES = { 'value':{'1': _('purchase'),'2': _('withdraw'),'3': _('dividend'),'4': _('interest')}}
Date_picker = { 'dataInit':'pickdates' }

def order_crispy_view(request):
    logging.debug(get_request_info(request))
    if request.method == 'POST':
        placeorderform = orderform(request.POST)
        #if orderform.is_valid() :
        if placeorderform.is_valid():
                F_SKID= placeorderform.data['F_SKID']
                F_TSType= placeorderform.data['F_TSType']
                F_Qty= placeorderform.data['F_Qty']
                F_Price= placeorderform.data['F_Price']
                F_OrderType= placeorderform.data['F_OrderType']
                F_Market= placeorderform.data['F_Market']
                F_Date= placeorderform.data['F_Date']
        F_SKID= placeorderform.data['F_SKID']
        F_TSType= placeorderform.data['F_TSType']
        F_Qty= placeorderform.data['F_Qty']
        F_Price= placeorderform.data['F_Price']
        F_OrderType= placeorderform.data['F_OrderType']
        F_Market= placeorderform.data['F_Market']
        F_Date= placeorderform.data['F_Date'] 
        F_CurID='HKD'
        placeorder.objects.placeorder(F_SKID,F_TSType,F_Qty,F_Price,F_Market,F_OrderType,F_Date,F_CurID)     

    else:
        placeorderform = orderform()

    data = {
        'orderform': placeorderform,
    }
    #template=get_template('stock_trading.html')
    
    #return render(request, 'stock_trading.html', data)
    return render_to_response('stock_trading.html', data, context_instance=RequestContext(request))

def stock_order_api(request):
    logging.debug(get_request_info(request))
    message="success"
    if request.method == 'POST':
        placeorderform = orderform(request.POST)
        #if orderform.is_valid() :
        if placeorderform.is_valid():
                F_SKID= placeorderform.data['F_SKID']
                F_TSType= placeorderform.data['F_TSType']
                F_Qty= placeorderform.data['F_Qty']
                F_Price= placeorderform.data['F_Price']
                F_OrderType= placeorderform.data['F_OrderType']
                F_Market= placeorderform.data['F_Market']
                F_Date= placeorderform.data['F_Date']
        F_SKID= placeorderform.data['F_SKID']
        F_TSType= placeorderform.data['F_TSType']
        F_Qty= placeorderform.data['F_Qty']
        F_Price= placeorderform.data['F_Price']
        F_OrderType= placeorderform.data['F_OrderType']
        F_Market= placeorderform.data['F_Market']
        F_Date= placeorderform.data['F_Date']  
        F_CurID='HKD'
        if stocksymbol.objects.CheckSymbol(symbol=F_SKID, market=F_Market):
            placeorder.objects.placeorder(F_SKID,F_TSType,F_Qty,F_Price,F_Market,F_OrderType,F_Date,F_CurID,request.user)  
        else:
            message="Symbol Error!"
    else:
        pass
    
    return HttpResponse(message, mimetype="application/json")

def query_grid(request):
    return render_to_response('stock_trading_grid.html', None, context_instance=RequestContext(request))

def query_grid_2(request):
    return render_to_response('stock_trading_grid_2.html', None, context_instance=RequestContext(request))


def query_grid_1(request):
    return render_to_response('stock_trading_grid_1.html', None, context_instance=RequestContext(request))

class order_order_grid(JqGrid):
    model = placeorder # could also be a queryset
    fields = ['id','F_Date','F_SKID','F_TSType','F_Qty','F_Price','F_CurID','F_OrderType','F_Market','F_Status','F_Note'] # optional 
    url = reverse_lazy('stock_order_order_handler')
    
    caption = _('Stock Trading Order List') # optional
    extra_config = {'height':'200','width':'100%',}
    colmodel_overrides = {
        'id': { 'editable': False, 'index':'id', 'label':_('id')},
        'F_Date': { 'editable': False, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_SKID': { 'editable': True, 'index':'F_SKID', 'label':_('StockID')},
        'F_TSType': { 'editable': True, 'edittype':'select', 'editoptions':TSTYPE_CHOICES ,'label': _('Trading Type')},
        'F_Qty':{ 'editable': True, 'index':'F_Qty', 'label':_('Qty')},
        'F_Price':{ 'editable': True, 'index':'F_Price', 'label':_('Price')},
        'F_CurID':{ 'editable': False, 'index':'F_CurID', 'label':_('Currency')},
        'F_OrderType':{ 'editable': False, 'index':'F_OrderType', 'label':_('OrderType')},
        'F_Marekt':{ 'editable': False, 'index':'F_Market', 'label':_('Market')},
        'F_Status':{ 'editable': False, 'index':'F_Status', 'label':_('Settle Status')},
        'F_Note': { 'editable': False, 'index':'F_Note', 'label':_('Note')},
    }

    
def order_order_handler(request):
    grid = order_order_grid()
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

def order_order_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = order_order_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")

class order_transaction_grid(JqGrid):
    model = stock_transaction # could also be a queryset
    fields = ['id','F_Date','F_SKID','F_TSType','F_CurID','F_Amt','F_Qty','F_Rate','F_Price','F_Fee','F_Exp','F_Status','F_Cost','F_Net','F_SettleDate','F_Payable','F_Receivable','F_Note'] # optional 
    url = reverse_lazy('stock_order_transaction_handler')
    
    caption = _('Stock Trading Transaction List') # optional
    colmodel_overrides = {
        'id': { 'editable': False, 'index':'id', 'label':_('id')},
        'F_Date': { 'editable': True, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_SKID': { 'editable': True, 'index':'F_Date', 'label':_('StockID')},
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
    }

    
def order_transaction_handler(request):
    grid = order_transaction_grid()
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

def order_transaction_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = order_transaction_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")

class order_portfolio_grid(JqGrid):
    model = stock_portfolio # could also be a queryset
    fields = ['id','F_Date','F_SettleDate','F_SKID','F_CurID','F_Qty','F_Cost','F_AvgCost','F_AvgRate','F_ClosePrice'] # optional 
    url = reverse_lazy('stock_order_portfolio_handler')
    
    caption = _('Stock Trading Portfolio List') # optional
    colmodel_overrides = {
        'id': { 'editable': False, 'index':'id', 'label':_('id')},
        'F_Date': { 'editable': False, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_SKID': { 'editable': True, 'index':'F_Date', 'label':_('StockID')},
        'F_SettleDate': { 'editable': False, 'index':'F_Date', 'label':_('Trading Date'),'sorttype':'date', 'searchrules':'{required:true,date:true}'},
        'F_CurID':{ 'editable': False, 'index':'F_Date', 'label':_('Currency')},
        'F_Qty':{ 'editable': True, 'index':'F_Date', 'label':_('Qty')},
        'F_Cost':{ 'editable': True, 'index':'F_Date', 'label':_('F_Cost')},
        'F_AvgCost':{ 'editable': False, 'index':'F_Date', 'label':_('F_AvgCost')},
        'F_AvgRate':{ 'editable': False, 'index':'F_Date', 'label':_('F_AvgRate')},
        'F_ClosePrice':{ 'editable': True, 'index':'F_Date', 'label':_('F_ClosePrice')},
    }

    
def order_portfolio_handler(request):
    grid = order_portfolio_grid()
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

def order_portfolio_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = order_portfolio_grid()
    return HttpResponse(grid.get_config(), mimetype="application/json")