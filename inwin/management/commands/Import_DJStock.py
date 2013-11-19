'''
Created on 2013/2/24

@author: yhuang
'''
"""Fetch the fund basic information
"""
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from inwin.data.models.stockdata import stockclose
#from django.utils.translation import ugettext as _
import sys
#from time import mktime 
#import datetime



class Command(BaseCommand):
    "The command class itself"

    help = """
    """
    option_list = BaseCommand.option_list + (
        make_option('--closefile',
            action = 'store',
            type = 'str',
            dest = 'closefile',
            default = None,
            help = 'file path **required** !'
        ),
        make_option('--market',
            action = 'store',
            type = 'str',
            dest = 'market',
            default = None,
            help = 'file path **required** !'
        ),
    )


    def handle(self, *args, **options):
        """import stock daily price into database
        """

        if options['closefile'] is None:
            raise CommandError('the --file argument is required')
        try:
            filename = options['closefile']
            Market = options['market']
            f = open(filename)
            for line in f:
                try:
                    tline=line.split(",")
                    tick_date = tline[0].encode('utf-8')[0:10]
                    tick_symbol = tline[1].encode('utf-8')+"."+Market
                    tick_open = tline[2].encode('utf-8')
                    tick_high = tline[3].encode('utf-8')
                    tick_low = tline[4].encode('utf-8')
                    tick_close = tline[5].encode('utf-8')
                    tick_volume= tline[6].encode('utf-8')
                    if Market!='HK' or tick_symbol<'2800':
                        stockclose.objects.Insert(Symbol=tick_symbol,tDate=tick_date,Open=tick_open,High=tick_high,Low=tick_low,Close=tick_close,Volume=tick_volume)
                    #print "Insert:"+tick_symbol+" Date:"+ tick_date
                except Exception, e:
                    print '(stockclose)Insert Error:'+tick_symbol+' ->'+unicode(e)+unicode(sys.exc_info()[0])      
                        
            f.close()
        except:
            print "Unexpected error(file open ?):", sys.exc_info()[0]
            
        print '(stockclose) Finish Task !!! '