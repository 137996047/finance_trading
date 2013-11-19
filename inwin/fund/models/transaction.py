from django.db import models
#from inwin.account.models import identity
#from jqgrid import JqGrid
#from django.core.urlresolvers import reverse_lazy
#from django.utils.translation import ugettext as _
# Create your models here.
from django.contrib.auth.models import User
class fund_orderManager(models.Manager):
    def placeorder(self,F_SKID,F_TSType,F_Amt,F_Market,F_OrderType,F_Date,F_CurID):
        placeorder=fund_order.objects.create(F_SKID=F_SKID,F_TSType=F_TSType,F_Amt=F_Amt,F_Market=F_Market,F_OrderType=F_OrderType,F_Date=F_Date,F_CurID=F_CurID)
        placeorder.save()
class fund_order(models.Model):
    F_Date= models.DateField('Trading Date')
    F_SKID= models.CharField(max_length=8)
    F_TSType= models.CharField(max_length=1)
    F_CurID=models.CharField(max_length=8)
    F_OrderType= models.CharField(max_length=1)
    F_Market= models.CharField(max_length=2)
    F_Amt=models.DecimalField(max_digits=28, decimal_places=4)
    F_Note=models.CharField(max_length=128, null=True, blank=True)
    F_User= models.ForeignKey(User, related_name='fund_order_user')
    
    objects = fund_orderManager()
    #identity = models.ForeignKey(identity, related_name='identity_transaction') 
    class Meta:
        app_label = 'fund'
        db_table = 'd_fd008'

class fund_transactionManager(models.Manager):
    def executeorder(self,F_SKID,F_TSType,F_Amt,F_Market,F_OrderType,F_Date,F_CurID):
        gentrans=fund_transaction.objects.create(F_SKID=F_SKID,F_TSType=F_TSType,F_Amt=F_Amt,F_Market=F_Market,F_OrderType=F_OrderType,F_Date=F_Date,F_CurID=F_CurID)
        gentrans.save()
class fund_transaction(models.Model):
    F_Date= models.DateField('Trading Date')
    F_SKID= models.CharField(max_length=8)
    F_TSType= models.CharField(max_length=1)
    F_Market= models.CharField(max_length=2)
    F_CurID=models.CharField(max_length=8)
    F_Amt=models.DecimalField(max_digits=28, decimal_places=4)
    F_Qty=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Rate=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Nav=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Fee=models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    F_Exp=models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    F_Status= models.CharField(max_length=1, null=True, blank=True)
    F_Cost=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Net=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_SettleDate=models.DateTimeField('Settle Date', null=True, blank=True)
    F_Payable=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Receivable=models.DecimalField(max_digits=28, decimal_places=4, null=True, blank=True)
    F_Note=models.CharField(max_length=128, null=True, blank=True)
    F_User= models.ForeignKey(User, related_name='fund_transaction_user')
    objects = fund_transactionManager()
    #identity = models.ForeignKey(identity, related_name='identity_transaction') 
    class Meta:
        app_label = 'fund'
        db_table = 'd_fd010'
        
        
class fund_portfolio(models.Model):
    F_Date= models.DateField('Portfolio Date')
    F_SettleDate= models.DateTimeField('Portfolio Settle Date')
    F_SKID= models.CharField(max_length=8)
    F_CurID=models.CharField(max_length=8)
    F_Qty=models.DecimalField(max_digits=28, decimal_places=4)
    F_Cost=models.DecimalField(max_digits=28, decimal_places=4)
    F_AvgCost=models.DecimalField(max_digits=28, decimal_places=4)
    F_AvgRate=models.DecimalField(max_digits=28, decimal_places=4)
    F_Nav=models.DecimalField(max_digits=28, decimal_places=4)
    F_DRpt_Nav=models.DecimalField(max_digits=28, decimal_places=4)
    F_User= models.ForeignKey(User, related_name='fund_portfolio_user')
    
    #identity = models.ForeignKey(identity, related_name='identity_portfolio')
    class Meta:
        app_label = 'fund'
        db_table = 'd_fd080'    
        
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
    