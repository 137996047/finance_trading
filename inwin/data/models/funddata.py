'''
Created on 2013/2/24

@author: yhuang
'''
from django.db import models
from django.utils.translation import ugettext as _
import datetime
import logging
import sys
#import feedparser
#import sys
#import time
#from time import mktime 
from django.db.models import Min

class fundsymbolManager(models.Manager):
    def GetbySymbol(self,symbol):
        try:
            return fundsymbol.objects.get(Symbol=symbol)
        except:
            return None       
    def CheckSymbol(self,symbol):
        try:
            fund=fundsymbol.objects.get(Symbol=symbol)
            if fund==None:
                return False
            else:
                return True
        except:
            return False
    def CreateUpdate(self,Symbol,ISIN,TDCCID,InvestMarket,Name,TDCCName,CUR,RLevel):
        try:
            symbolobject=fundsymbol.objects.get(Symbol=Symbol)
            if symbolobject==None:
                symbolobject=fundsymbol(Symbol=Symbol,ISIN=ISIN,TDCCID=TDCCID,InvestMarket=InvestMarket,Name=Name,TDCCName=TDCCName,CUR=CUR,RLevel=RLevel)
            else:
                symbolobject.Symbol=Symbol
                symbolobject.ISIN=ISIN
                symbolobject.TDCCID=TDCCID
                symbolobject.InvestMarket=InvestMarket
                symbolobject.Name=Name
                symbolobject.TDCCName=TDCCName
                symbolobject.CUR=CUR
                symbolobject.RLevel=RLevel
            symbolobject.save()
        except:
            try:
                symbolobject=fundsymbol(Symbol=Symbol,ISIN=ISIN,TDCCID=TDCCID,InvestMarket=InvestMarket,Name=Name,TDCCName=TDCCName,CUR=CUR,RLevel=RLevel)
                symbolobject.save()
            except Exception, e:
                        print '(fundsymbol)CreateUpdate:'+Symbol+' ->'+unicode(e)+unicode(sys.exc_info()[0]) 

    def Insert(self,fundsymbol):
        try:
            symbolobject=self.get(Symbol=fundsymbol.Symbol)
            if symbolobject==None:
                fundsymbol.save()
            else:
                symbolobject.Symbol=fundsymbol.Symbol
                symbolobject.ISIN=fundsymbol.ISIN
                symbolobject.TDCCID=fundsymbol.TDCCID
                symbolobject.InvestMarket=fundsymbol.InvestMarket
                symbolobject.Name=fundsymbol.Name
                symbolobject.TDCCName=fundsymbol.TDCCName
                symbolobject.CUR=fundsymbol.CUR
                symbolobject.RLevel=fundsymbol.RLevel
            symbolobject.save()
        except:
            symbolobject=fundsymbol(Symbol=fundsymbol.Symbol,ISIN=fundsymbol.ISIN,TDCCID=fundsymbol.TDCCID,InvestMarket=fundsymbol.InvestMarket,Name=fundsymbol.Name,TDCCName=fundsymbol.TDCCName,CUR=fundsymbol.CUR,RLevel=fundsymbol.RLevel)
            symbolobject.save()
            
class fundsymbol(models.Model):
    """
    The DB to store the fund Symbol
    """
    Symbol = models.CharField(max_length=11,primary_key=True)
    ISIN = models.CharField(max_length=500)
    TDCCID = models.CharField(max_length=100)
    InvestMarket = models.CharField(max_length=20)
    Name = models.CharField(max_length=500,verbose_name=_('funddj Name'))
    TDCCName = models.CharField(max_length=400,verbose_name=_('TDCC Name'))
    CUR = models.CharField(max_length=20,verbose_name=_('Currency'))
    RLevel=models.CharField(max_length=10,verbose_name=_('Risk Level'))

    # Denormalised data, transplanted from Question

    objects = fundsymbolManager()


    def __unicode__(self):
        return u'Symbol:%s' % (self.Symbol)

    class Meta:
        app_label = 'data'
        db_table = u'fundsymbol'
        verbose_name = _('fund symbol')
        verbose_name_plural = _('fund symbol')
        
class fundcategory(models.Model):
    """
    The DB to store the Fund Category Group Relation
    """
    Symbol = models.CharField(max_length=11,primary_key=True)
    Type = models.CharField(max_length=8)
    InvestType = models.CharField(max_length=8)
    InvestMarket = models.CharField(max_length=8)
    #categoryid = models.CharField(max_length=11,primary_key=True)
    Name = models.CharField(max_length=40,verbose_name=_('Group Name'))
    tagnames = models.CharField(max_length=125)
    Parsing_Keys = models.CharField(max_length=125)

    def __unicode__(self):
        return u'Category ID:%s  Category Name:%s' % (self.categoryid,self.Name)

    class Meta:
        app_label = 'data'
        db_table = u'fundcategory'
        verbose_name = _('fundcategory')
        verbose_name_plural = _('fundcategory')
        
class fundnavManager(models.Manager):
    def Insert(self,Symbol,tDate,Nav):
        try:
            try:
                symbolobject=fundsymbol.objects.GetbySymbol(Symbol)
            except:
                logging.debug('Can''t find fund by symbol: %s' % ','.join(Symbol))
                return
            if symbolobject==None:
                logging.debug('Can''t find fund by symbol: %s' % ','.join(Symbol))
                return
            CloseTick=fundnav.objects.get(Symbol=symbolobject,tDate=tDate)
            if CloseTick==None:
                CloseTick=fundnav(Symbol=symbolobject,tDate=tDate,Nav=Nav)
            else:
                CloseTick.Symbol=Symbol
                CloseTick.tDate=tDate
                CloseTick.Nav=Nav
            CloseTick.save()
        except:
            CloseTick=fundnav(Symbol=symbolobject,tDate=tDate,Nav=Nav)
            CloseTick.save()
    def Get(self,Symbol,beginDate,endDate):
        return fundnav.objects.filter(Symbol=Symbol,tDate__gte=beginDate,tDate__lte=endDate)

        

class fundnav(models.Model):
    """
    The DB to store the fund Close price
    """
    Symbol = models.ForeignKey(fundsymbol, null=True, blank=True)
    tDate = models.DateField(default=datetime.date.today(),verbose_name=_('Trans_Date'))
    Nav=models.FloatField(default=0,verbose_name=_('Nav'))
    objects = fundnavManager()


    def __unicode__(self):
        return u'Symbol:%s' % (self.Symbol)

    class Meta:
        app_label = 'data'
        db_table = u'fundnav'
        verbose_name = _('fundnav')
        verbose_name_plural = _('fundnav')
        
class fundscaleManager(models.Manager):
    def Insert(self,Symbol,tDate,Scale):
        try:
            try:
                symbolobject=fundsymbol.objects.GetbySymbol(Symbol)
            except:
                logging.debug('Can''t find fund by symbol: %s' % ','.join(Symbol))
                return
            if symbolobject==None:
                logging.debug('Can''t find fund by symbol: %s' % ','.join(Symbol))
                return
            ScaleTick=fundscale.objects.get(Symbol=symbolobject,tDate=tDate)
            if ScaleTick==None:
                ScaleTick=fundscale(Symbol=symbolobject,tDate=tDate,Scale=Scale)
            else:
                ScaleTick.Symbol=Symbol
                ScaleTick.tDate=tDate
                ScaleTick.Scale=Scale
            ScaleTick.save()
        except:
            ScaleTick=fundscale(Symbol=symbolobject,tDate=tDate,Scale=Scale)
            ScaleTick.save()
    def Get(self,Symbol,beginDate,endDate):
        return fundscale.objects.filter(Symbol=Symbol,tDate__gte=beginDate,tDate__lte=endDate)

        

class fundscale(models.Model):
    """
    The DB to store the fund Close price
    """
    Symbol = models.ForeignKey(fundsymbol, null=True, blank=True)
    tDate = models.DateField(default=datetime.date.today(),verbose_name=_('Trans_Date'))
    Scale=models.BigIntegerField(default=0,verbose_name=_('Scale'))
    CUR = models.CharField(max_length=20,verbose_name=_('Currency'))
    Scale_NTD = models.BigIntegerField(default=0,verbose_name=_('NTD Scale'))
    objects = fundscaleManager()


    def __unicode__(self):
        return u'Symbol:%s Scale:%s' % (self.Symbol,self.scale)

    class Meta:
        app_label = 'data'
        db_table = u'fundscale'
        verbose_name = _('fundscale')
        verbose_name_plural = _('fundscale')