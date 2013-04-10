'''
Created on 2013/2/24

@author: yhuang
'''
from django.db import models
from django.utils.translation import ugettext as _
import datetime
import logging
#import feedparser
#import sys
#import time
#from time import mktime 
from django.db.models import Min

class tradingdateManager(models.Manager):
    def getCurrentDate(self,market):
        if market=='HK':
            today=datetime.date.today()
            try:
                currenttradingdate=tradingdate.objects.filter(HK='Y').filter(tDate__gte=today).aggregate(Min('tDate'))
                return currenttradingdate['tDate__min']
            except:
                return today
    def initial(self):
        for d in range(1000):
            try:
                adddate=datetime.date.today()+ datetime.timedelta(days=d)
                temptradingdate=tradingdate.objects.create(tDate=adddate)
                if adddate.weekday()==5 or adddate.weekday()==6:
                    temptradingdate.HK='N'
                    temptradingdate.US='N'
                    temptradingdate.TW='N'
                    temptradingdate.CN='N'
                temptradingdate.save()
            except:
                pass
            
class tradingdate(models.Model):
    tDate = models.DateField(default=datetime.date.today(),verbose_name=_('Trans_Date'),primary_key=True)
    HK = models.CharField(max_length=1,default='Y',verbose_name=_('HK Exchange'))
    US = models.CharField(max_length=1,default='Y',verbose_name=_('US Exchange'))
    TW = models.CharField(max_length=1,default='Y',verbose_name=_('TW Exchange'))
    CN = models.CharField(max_length=1,default='Y',verbose_name=_('CN Exchange'))
    Opened = models.BooleanField(default=False,verbose_name=_('Market Open'))
    Settled = models.BooleanField(default=False,verbose_name=_('Is Settled'))
    objects = tradingdateManager()
    class Meta:
        app_label = 'data'
        db_table = u'tradingdate'
        verbose_name = _('trading date')
        verbose_name_plural = _('trading date')
        
class stocksymbolManager(models.Manager):
    def GetbySymbol(self,symbol):
        try:
            return stocksymbol.objects.get(Symbol=symbol)
        except:
            return None
    def GetbySymbolKey(self,symbolkey):
        try:
            return stocksymbol.objects.get(SymbolKey=symbolkey)
        except:
            return None
        
    def CheckSymbol(self,symbol,market):
        try:
            stock=stocksymbol.objects.get(Symbol=symbol,Market=market)
            if stock==None:
                return False
            else:
                return True
        except:
            return False
    def CreateUpdate(self,SymbolKey,Symbol,Market,Name,SName,CUR,Unit,Reference,EName,SEName,Uplimit,Downlimit):
        try:
            symbolobject=stocksymbol.objects.get(SymbolKey=SymbolKey)
            if symbolobject==None:
                symbolobject=stocksymbol(SymbolKey=SymbolKey,Symbol=Symbol,Market=Market,Name=Name,SName=SName,CUR=CUR,Unit=Unit,Reference=Reference,EName=EName,SEName=SEName,Uplimit=Uplimit,Downlimit=Downlimit)
            else:
                symbolobject.Symbol=Symbol
                symbolobject.Market=Market
                symbolobject.Name=Name
                symbolobject.SName=SName
                symbolobject.CUR=CUR
                symbolobject.Unit=Unit
                symbolobject.Reference=Reference
                symbolobject.EName=EName
                symbolobject.SEName=SEName
                symbolobject.Uplimit=Uplimit
                symbolobject.Downlimit=Downlimit
            symbolobject.save()
        except:
            symbolobject=stocksymbol(SymbolKey=SymbolKey,Symbol=Symbol,Market=Market,Name=Name,SName=SName,CUR=CUR,Unit=Unit,Reference=Reference,EName=EName,SEName=SEName,Uplimit=Uplimit,Downlimit=Downlimit)
            symbolobject.save()

    def Insert(self,stocksymbol):
        try:
            symbolobject=self.get(SymbolKey=stocksymbol.SymbolKey)
            if symbolobject==None:
                stocksymbol.save()
            else:
                symbolobject.Symbol=stocksymbol.Symbol
                symbolobject.Name=stocksymbol.Name
                symbolobject.SName=stocksymbol.SName
                symbolobject.CUR=stocksymbol.CUR
                symbolobject.Unit=stocksymbol.Unit
                symbolobject.Reference=stocksymbol.Reference
                symbolobject.EName=stocksymbol.EName
                symbolobject.SEName=stocksymbol.SEName
            symbolobject.save()
        except:
            symbolobject=stocksymbol(SymbolKey=stocksymbol.SymbolKey,Symbol=stocksymbol.Symbol,Market=stocksymbol.Market,Name=stocksymbol.Name,SName=stocksymbol.SName,CUR=stocksymbol.CUR,Unit=stocksymbol.Unit,Reference=stocksymbol.Reference,EName=stocksymbol.EName,SEName=stocksymbol.SEName,Uplimit=stocksymbol.Uplimit,Downlimit=stocksymbol.Downlimit)
            symbolobject.save()
            
class stocksymbol(models.Model):
    """
    The DB to store the Stock Symbol
    """
    SymbolKey = models.CharField(max_length=14,primary_key=True)
    Symbol = models.CharField(max_length=11)
    Market = models.CharField(max_length=8)
    Name = models.CharField(max_length=50,verbose_name=_('Stock Name'))
    SName = models.CharField(max_length=80,verbose_name=_('Short Name'))
    CUR = models.CharField(max_length=5,verbose_name=_('Currency'))
    Unit=models.IntegerField(default=0,verbose_name=_('Unit'))
    Reference=models.FloatField(default=0,verbose_name=_('Reference'))
    EName = models.CharField(max_length=80,verbose_name=_('Stock English Name'))
    SEName = models.CharField(max_length=160,verbose_name=_('Short English Name'))
    Uplimit=models.FloatField(default=0,verbose_name=_('Uplimit'))
    Downlimit=models.FloatField(default=0,verbose_name=_('Downlimit'))

    # Denormalised data, transplanted from Question
    tagnames = models.CharField(max_length=125)
    Parsing_Keys = models.CharField(max_length=125)
    objects = stocksymbolManager()


    def __unicode__(self):
        return u'Symbol:%s' % (self.Symbol)

    class Meta:
        app_label = 'data'
        db_table = u'stocksymbol'
        verbose_name = _('stock symbol')
        verbose_name_plural = _('stock symbol')
        
        
class stockcloseManager(models.Manager):
    def Insert(self,Symbol,tDate,Open,High,Low,Close,Volume):
        try:
            try:
                symbolobject=stocksymbol.objects.GetbySymbolKey(Symbol)
            except:
                logging.debug('Can''t find stock by symbol: %s' % ','.join(Symbol))
                return
            if symbolobject==None:
                logging.debug('Can''t find stock by symbol: %s' % ','.join(Symbol))
                return
            CloseTick=stockclose.objects.get(Symbol=symbolobject,tDate=tDate)
            if CloseTick==None:
                CloseTick=stockclose(Symbol=symbolobject,tDate=tDate,Open=Open,High=High,Low=Low,Close=Close,Volume=Volume)
            else:
                CloseTick.Symbol=Symbol
                CloseTick.tDate=tDate
                CloseTick.Open=Open
                CloseTick.High=High            
                CloseTick.Low=Low
                CloseTick.Close=Close
                CloseTick.Volume=Volume
            CloseTick.save()
        except:
            CloseTick=stockclose(Symbol=symbolobject,tDate=tDate,Open=Open,High=High,Low=Low,Close=Close,Volume=Volume)
            CloseTick.save()
    def Get(self,Symbol,beginDate,endDate):
        return stockclose.objects.filter(Symbol=Symbol,tDate__gte=beginDate,tDate__lte=endDate)

        

class stockclose(models.Model):
    """
    The DB to store the Stock Close price
    """
    Symbol = models.ForeignKey(stocksymbol, null=True, blank=True)
    tDate = models.DateField(default=datetime.date.today(),verbose_name=_('Trans_Date'))
    Open=models.FloatField(default=0,verbose_name=_('Open'))
    High=models.FloatField(default=0,verbose_name=_('High'))
    Low=models.FloatField(default=0,verbose_name=_('Low'))
    Close=models.FloatField(default=0,verbose_name=_('Close'))
    Volume=models.BigIntegerField(default=0,verbose_name=_('Volume'))
    objects = stockcloseManager()


    def __unicode__(self):
        return u'Symbol:%s' % (self.Symbol)

    class Meta:
        app_label = 'data'
        db_table = u'stockclose'
        verbose_name = _('stockclose')
        verbose_name_plural = _('stockclose')
    
class stockclose_us(stockclose):
    class Meta:
        app_label = 'data'
        db_table = u'stockclose_us'
        verbose_name = _('stockclose_us')
        verbose_name_plural = _('stockclose_us')
        
class stockindustry(models.Model):
    """
    The DB to store the Stock Close proce
    """
    ID = models.CharField(max_length=8,primary_key=True)
    Name = models.CharField(max_length=50,verbose_name=_('Industry Name'))
    CNName = models.CharField(max_length=50,verbose_name=_('Industry Chinese Name'))
    dimen1 = models.CharField(max_length=8,verbose_name=_('Dimension 1'))
    dimen2 = models.CharField(max_length=8,verbose_name=_('Dimension 2'))
    dimen3 = models.CharField(max_length=8,verbose_name=_('Dimension 3'))
    dimen4 = models.CharField(max_length=8,verbose_name=_('Dimension 4'))
    dimen5 = models.CharField(max_length=8,verbose_name=_('Dimension 5'))
    dimen6 = models.CharField(max_length=8,verbose_name=_('Dimension 6'))
    def __unicode__(self):
        return u'Industry Name:%s' % (self.Name)

    class Meta:
        app_label = 'data'
        db_table = u'stockindustry'
        verbose_name = _('stockindustry')
        verbose_name_plural = _('stockindustry')


class stockindustryratio(models.Model):
    """
    The DB to store the Stock Close price
    """
    Symbol = models.ForeignKey(stocksymbol, null=True, blank=True)
    #Market = models.CharField(max_length=8)
    Industry = models.ForeignKey(stockindustry, null=True, blank=True)
    PRatio = models.FloatField(default=0,verbose_name=_('Revenue Ration'))

    def __unicode__(self):
        return u'Symbol:%s' % (self.Symbol)

    class Meta:
        app_label = 'data'
        db_table = u'stockindustryratio'
        verbose_name = _('stockindustryratio')
        verbose_name_plural = _('stockindustryratio')


class stockconceptgroup(models.Model):
    """
    The DB to store the Stock Concept Group Relation
    """
    GroupSymbol = models.CharField(max_length=11,primary_key=True)
    Name = models.CharField(max_length=40,verbose_name=_('Group Name'))
    Parsing_Keys = models.CharField(max_length=125)

    def __unicode__(self):
        return u'GroupSymbol:%s' % (self.GroupSymbol)

    class Meta:
        app_label = 'data'
        db_table = u'stockconceptgroup'
        verbose_name = _('stockconceptgroup')
        verbose_name_plural = _('stockconceptgroup')

class stockconceptgrouprelation(models.Model):
    """
    The DB to store the Stock Concept Group Relation
    """
    group = models.ForeignKey(stockconceptgroup)
    stock = models.ForeignKey(stocksymbol)

    def __unicode__(self):
        return u'stockconceptgrouprelation:%s %s' % (self.group.Name,self.stock.Name)

    class Meta:
        app_label = 'data'
        db_table = u'stockconceptgrouprelation'
        verbose_name = _('stockconceptgrouprelation')
        verbose_name_plural = _('stockconceptgrouprelation')
