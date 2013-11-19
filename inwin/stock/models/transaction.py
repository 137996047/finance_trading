import logging
import sys
from django.db import models
from django.db.models import Q
#from inwin.account.models import identity
#from jqgrid import JqGrid
#from django.core.urlresolvers import reverse_lazy
#from django.utils.translation import ugettext as _
# Create your models here.
from django.contrib.auth.models import User
from inwin.data.models.stockdata import stockclose,tradingparameter
class stock_orderManager(models.Manager):
    def placeorder(self,F_SKID,F_TSType,F_Qty,F_Price,F_Market,F_OrderType,F_Date,F_CurID,F_User):
        placeorder=stock_order.objects.create(F_SKID=F_SKID,F_TSType=F_TSType,F_Qty=F_Qty,F_Price=F_Price,F_Market=F_Market,F_OrderType=F_OrderType,F_Date=F_Date,F_CurID=F_CurID,F_User=F_User)
        placeorder.save()
class stock_order(models.Model):
    F_Date= models.DateField('Trading Date')
    F_SKID= models.CharField(max_length=8)
    F_TSType= models.CharField(max_length=1)
    F_CurID=models.CharField(max_length=8)
    F_OrderType= models.CharField(max_length=1)
    F_Market= models.CharField(max_length=2)
    F_Qty=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Price=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Status= models.CharField(max_length=1, null=True, blank=True)
    F_Note=models.CharField(max_length=128, null=True, blank=True)
    F_ClosePrice=models.DecimalField(max_digits=28, decimal_places=4)
    F_User= models.ForeignKey(User, related_name='stock_order_user')
    objects = stock_orderManager()
    #identity = models.ForeignKey(identity, related_name='stock_identity_transaction') 
    class Meta:
        app_label = 'stock'
        db_table = 'd_eq008'
class stock_transactionManager(models.Manager):
    def executeorder(self,order):
        taxrate=tradingparameter.objects.getTaxRate(order.market)
        feerate=tradingparameter.objects.getFeeRate(order.market)
        gentrans=stock_transaction.objects.create(F_Date= tradingdate,
                                                     F_SKID= order.F_SKID,
                                                     F_TSType= order.F_TSType,
                                                     F_Market= order.F_Market,
                                                     F_CurID= order.F_CurID,
                                                     F_Amt= order.F_ClosePrice*order.F_Qty,
                                                     F_Qty= order.F_Qty,
                                                     F_Rate= 1,
                                                     F_Price= order.F_ClosePrice,
                                                     F_Fee= order.F_ClosePrice*order.F_Qty*feerate,
                                                     F_Exp= 0,
                                                     F_Tax= order.F_ClosePrice*order.F_Qty*taxrate,
                                                     F_Status= '1',
                                                     F_Cost= order.F_ClosePrice*order.F_Qty*(1+feerate+taxrate),
                                                     F_Net= 0,
                                                     F_SettleDate=None,
                                                     F_Payable=order.F_ClosePrice*order.F_Qty*(1+feerate+taxrate),
                                                     F_Receivable=0,
                                                     F_Note= '',
                                                     F_User= order.F_User)
        gentrans.save()
class stock_transaction(models.Model):
    F_Date= models.DateField('Trading Date')
    F_SKID= models.CharField(max_length=8)
    F_TSType= models.CharField(max_length=1)
    F_Market= models.CharField(max_length=2)
    F_CurID=models.CharField(max_length=8)
    F_Amt=models.DecimalField(max_digits=28, decimal_places=4)
    F_Qty=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Rate=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Price=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Fee=models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    F_Exp=models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    F_Tax=models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    F_Status= models.CharField(max_length=1, null=True, blank=True)
    F_Cost=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Net=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_SettleDate=models.DateTimeField('Settle Date', null=True, blank=True)
    F_Payable=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Receivable=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Note=models.CharField(max_length=128, null=True, blank=True)
    F_User= models.ForeignKey(User, related_name='stock_transaction_user')
    objects = stock_transactionManager()
    #identity = models.ForeignKey(identity, related_name='stock_identity_transaction') 
    class Meta:
        app_label = 'stock'
        db_table = 'd_eq010'
        
        
        
class stock_portfolio(models.Model):
    F_Date= models.DateField('Portfolio Date')
    F_SettleDate= models.DateTimeField('Portfolio Settle Date')
    F_SKID= models.CharField(max_length=8)
    F_CurID=models.CharField(max_length=8)
    F_Qty=models.DecimalField(max_digits=28, decimal_places=4)
    F_Cost=models.DecimalField(max_digits=28, decimal_places=4)
    F_AvgCost=models.DecimalField(max_digits=28, decimal_places=4)
    F_AvgRate=models.DecimalField(max_digits=28, decimal_places=4)
    F_ClosePrice=models.DecimalField(max_digits=28, decimal_places=4)
    F_User= models.ForeignKey(User, related_name='stock_portfolio_user')
    #identity = models.ForeignKey(identity, related_name='stock_identity_portfolio')
    class Meta:
        app_label = 'stock'
        db_table = 'd_eq080'    
        
#class ExampleGrid(JqGrid):
#    model = transaction # could also be a queryset
#    fields = ['F_Note','F_Date','F_SKID','F_TSType','F_CurID','F_Amt','F_Qty','F_Rate','F_Nav','F_Fee','F_Exp','F_Status','F_Cost','F_Net','F_SettleDate','F_Payable','F_Receivable'] # optional 
#    url = reverse_lazy('grid_handler')
#    caption = 'My First Grid' # optional
#    colmodel_overrides = {
#        'F_Note': { 'editable': True, 'index':'F_Note', 'label':_('Note')},
#        'F_Date': { 'editable': True, 'index':'F_Date', 'label':_('Trading Date')},
#        'F_TSType': { 'editable': True, 'edittype':'select', 'label': _('Trading Type')},
#    }

def FillClosePrice(market,tradingdate):
    try:
        stock_order.objects.raw('update d_eq008,stockclose set d_eq008.F_ClosePrice=stockclose.Close where (d_eq008.F_Status IS NULL or d_eq008.F_Status=\'1\') AND (stockclose.stocksymbol_id=concat(d_eq008.F_SKID,\'.\',d_eq008.F_Market) and stockclose.tDate=d_eq008.F_Date);')
    except:
        logging.CRITICAL("FillClosePrice error:", sys.exc_info()[0])

def Match(market,tradingdate):
    #tradingparameter.objects.setDefault()
    taxrate=tradingparameter.objects.getTaxRate(market)
    feerate=tradingparameter.objects.getFeeRate(market)
    message=''
    FillClosePrice(market,tradingdate)
    orders=stock_order.objects.filter(F_Market=market).filter(F_Date__lte=tradingdate).filter(Q(F_Status=None) | Q(F_Status='1'))
    for order in orders:
        #F_TSType=='1' Buy   F_TSType=='2' Sell
        if order.F_ClosePrice==None:
            message = message + ' No Price:'+order.F_SKID
        else:
            if order.F_TSType=='1':    
                if order.F_ClosePrice<=order.F_Price:
                    transaction=stock_transaction.objects.create(F_Date= tradingdate,
                                                     F_SKID= order.F_SKID,
                                                     F_TSType= order.F_TSType,
                                                     F_Market= order.F_Market,
                                                     F_CurID= order.F_CurID,
                                                     F_Amt= order.F_ClosePrice*order.F_Qty,
                                                     F_Qty= order.F_Qty,
                                                     F_Rate= 1,
                                                     F_Price= order.F_ClosePrice,
                                                     F_Fee= order.F_ClosePrice*order.F_Qty*feerate,
                                                     F_Exp= 0,
                                                     F_Tax= order.F_ClosePrice*order.F_Qty*taxrate,
                                                     F_Status= '1',
                                                     F_Cost= order.F_ClosePrice*order.F_Qty*(1+feerate+taxrate),
                                                     F_Net= 0,
                                                     F_SettleDate=None,
                                                     F_Payable=order.F_ClosePrice*order.F_Qty*(1+feerate+taxrate),
                                                     F_Receivable=0,
                                                     F_Note= '',
                                                     F_User= order.F_User)
                    #transaction.save()
                    order.F_Status='3'
                    order.save()
                else:
                    order.F_Status='4'
                    order.save()
            elif order.F_TSType=='2': 
                if order.F_ClosePrice>=order.F_Price:
                    transaction=stock_transaction.objects.create(F_Date= tradingdate,
                                                     F_SKID= order.F_SKID,
                                                     F_TSType= order.F_TSType,
                                                     F_Market= order.F_Market,
                                                     F_CurID= order.F_CurID,
                                                     F_Amt= order.F_ClosePrice*order.F_Qty,
                                                     F_Qty= order.F_Qty,
                                                     F_Rate= 1,
                                                     F_Price= order.F_ClosePrice,
                                                     F_Fee= order.F_ClosePrice*order.F_Qty*feerate,
                                                     F_Exp= 0,
                                                     F_Tax= order.F_ClosePrice*order.F_Qty*taxrate,
                                                     F_Status= '1',
                                                     #-1 means unhandle
                                                     F_Cost= -1,            
                                                     F_Net= -1,
                                                     F_SettleDate=None,
                                                     F_Payable=0,
                                                     F_Receivable=order.F_ClosePrice*order.F_Qty*(1-feerate-taxrate),
                                                     F_Note= '',
                                                     F_User= order.F_User)
                    #transaction.save()
                    order.F_Status='3'
                    order.save()
                else:
                    order.F_Status='4'
                    order.save()
            else:
                order.F_Status='4'
                order.save()
    return message

def Settle(market,tradingdate):
    taxrate=tradingparameter.objects.getTaxRate(market)
    feerate=tradingparameter.objects.getFeeRate(market)
    orders=stock_order.objects.filter(F_Market=market).filter(F_Date__lte=tradingdate).filter(Q(F_Status=None) | Q(F_Status='1'))
    for order in orders:
        
        #F_TSType=='1' Buy   F_TSType=='2' Sell
        if order.F_TSType=='1':    
            if order.F_ClosePrice<=order.F_Price:
                stock_transaction.objects.create(F_Date= tradingdate,
                                                 F_SKID= order.F_SKID,
                                                 F_TSType= order.F_TSType,
                                                 F_Market= order.F_Market,
                                                 F_CurID= order.F_CurID,
                                                 F_Amt= order.F_ClosePrice*order.F_Qty,
                                                 F_Qty= order.F_Qty,
                                                 F_Rate= 1,
                                                 F_Price= order.F_ClosePrice,
                                                 F_Fee= order.F_ClosePrice*order.F_Qty*order.feerate,
                                                 F_Exp= 0,
                                                 F_Tax= order.F_ClosePrice*order.F_Qty*order.taxrate,
                                                 F_Status= '1',
                                                 F_Cost= order.F_ClosePrice*order.F_Qty*(1+order.feerate+order.taxrate),
                                                 F_Net= 0,
                                                 F_SettleDate=None,
                                                 F_Payable=order.F_ClosePrice*order.F_Qty*(1+order.feerate+order.taxrate),
                                                 F_Receivable=0,
                                                 F_Note= '',
                                                 F_User= order.F_User)
            else:
                order.F_Status='4'
                order.save()
        elif order.F_TSType=='2': 
            if order.F_ClosePrice>=order.F_Price:
                stock_transaction.objects.create(F_Date= tradingdate,
                                                 F_SKID= order.F_SKID,
                                                 F_TSType= order.F_TSType,
                                                 F_Market= order.F_Market,
                                                 F_CurID= order.F_CurID,
                                                 F_Amt= order.F_ClosePrice*order.F_Qty,
                                                 F_Qty= order.F_Qty,
                                                 F_Rate= 1,
                                                 F_Price= order.F_ClosePrice,
                                                 F_Fee= order.F_ClosePrice*order.F_Qty*order.feerate,
                                                 F_Exp= 0,
                                                 F_Tax= order.F_ClosePrice*order.F_Qty*order.taxrate,
                                                 F_Status= '1',
                                                 #-1 means unhandle
                                                 F_Cost= -1,            
                                                 F_Net= -1,
                                                 F_SettleDate=None,
                                                 F_Payable=0,
                                                 F_Receivable=order.F_ClosePrice*order.F_Qty*(1-order.feerate-order.taxrate),
                                                 F_Note= '',
                                                 F_User= order.F_User)
            else:
                order.F_Status='4'
                order.save()
        else:
            order.F_Status='4'
            order.save()
    
    