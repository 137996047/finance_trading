'''
Created on 2013/3/23

@author: yhuang
'''
from django.core.management.base import NoArgsCommand
from inwin.data.models.stockdata import tradingdate
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        message = "generate 1000 days for trading date table"
        tradingdate.objects.initial()
        print message
