'''
Created on 2013/2/24

@author: yhuang
'''
"""Fetch the fund basic information
"""
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from inwin.data.models.funddata import fundnav,fundsymbol
#from django.utils.translation import ugettext as _
import sys
#from time import mktime 
#import datetime



class Command(BaseCommand):
    "The command class itself"

    help = """
    """
    option_list = BaseCommand.option_list + (
        make_option('--symbolfile',
            action = 'store',
            type = 'str',
            dest = 'symbolfile',
            default = None,
            help = 'filename **required**, for the symbol '
        ),
        make_option('--navfile',
            action = 'store',
            type = 'str',
            dest = 'navfile',
            default = None,
            help = 'file path **required** !'
        ),
    )


    def handle(self, *args, **options):
        """import stock daily price into database
        """

        try:
            symbolfile_FileName = options['symbolfile']
        except:
            symbolfile_FileName = None
        
        try:
            navfile_FileName = options['navfile']
        except:
            navfile_FileName = None
            
        if symbolfile_FileName != None:
            try:
                f = open(symbolfile_FileName)
                for line in f:
                    try:
                        tline=line.split(",")
                        tick_Symbol = tline[0].encode('utf-8').strip()
                        tick_ISIN = tline[1].encode('utf-8').strip()
                        tick_TDCCID = tline[2].encode('utf-8').strip()
                        tick_InvestMarket = tline[3].encode('utf-8').strip()
                        tick_Name = tline[4].encode('utf-8').strip()
                        tick_TDCCName = tline[5].encode('utf-8').strip()
                        tick_CUR = tline[6].encode('utf-8').strip()
                        tick_RLevel= tline[7].encode('utf-8').strip()
                        fundsymbol.objects.CreateUpdate(Symbol=tick_Symbol,ISIN=tick_ISIN,TDCCID=tick_TDCCID,InvestMarket=tick_InvestMarket,Name=tick_Name,TDCCName=tick_TDCCName,CUR=tick_CUR,RLevel=tick_RLevel)
                        #print "Insert:"+tick_symbol+" Date:"+ tick_date
                    except Exception, e:
                        print '(fundsymbol)Insert Error:'+tick_Symbol+' ->'+unicode(e)+unicode(sys.exc_info()[0])      
                            
                f.close()
            except:
                print "Unexpected error:", sys.exc_info()[0]
                
        if navfile_FileName != None:
            try:
                f = open(navfile_FileName)
                for line in f:
                    try:
                        tline=line.split(",")
                        tick_Symbol = tline[0].encode('utf-8').strip()
                        tick_tDate = tline[1].encode('utf-8')[0:10]
                        tick_Nav = tline[2].encode('utf-8')
                        fundnav.objects.Insert(Symbol=tick_Symbol,tDate=tick_tDate,Nav=tick_Nav)
                        #print "Insert:"+tick_symbol+" Date:"+ tick_date
                    except Exception, e:
                        print '(fundnav)Insert Error:'+tick_Symbol+' ->'+tick_tDate+' ->'+unicode(e)+unicode(sys.exc_info()[0])      
                            
                f.close()
            except:
                print "Unexpected error:", sys.exc_info()[0]