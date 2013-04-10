"""management command that
creates the askbot user account programmatically
the command can add password, but it will not create
associations with any of the federated login providers

Input file have change to big5

"""
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from inwin.data.models.stockdata import stockclose,stockindustry,stocksymbol,stockconceptgroup,stockindustryratio,stockconceptgrouprelation
#from inwin.data.models import stockclose
import sys
import csv

class Command(BaseCommand):
    "The command class itself"

    help = """
    """
    option_list = BaseCommand.option_list + (
        make_option('--stocksymbol',
            action = 'store',
            type = 'str',
            dest = 'stocksymbol_file',
            default = None,
            help = 'filename **required**, for the symbol '
        ),
        make_option('--stockindustryratio',
            action = 'store',
            type = 'str',
            dest = 'stockindustryratio_file',
            default = None,
            help = 'filename **required**, for the symbol industry ratio '
        ),
        make_option('--stockindustry',
            action = 'store',
            type = 'str',
            dest = 'stockindustry_file',
            default = None,
            help = 'filename **required**, for the stockindustry '
        ),
        make_option('--stockconceptgroup',
            action = 'store',
            type = 'str',
            dest = 'stockconceptgroup_file',
            default = None,
            help = 'filename **required**, for the Stock_ConceptGroup '
        ),
        make_option('--stockconceptgrouprelation',
            action = 'store',
            type = 'str',
            dest = 'stockconceptgrouprelation_file',
            default = None,
            help = 'filename **required**, for the Stock_ConceptGroupRalation'
        ),
        
    )

    def handle(self, *args, **options):
        """insert tag relation
        """
        """if options['Symbol'] is None:
            raise CommandError('the --Symbol argument is required')
        
        if options['stockindustryratio'] is None:
            raise CommandError('the --stockindustryratio argument is required')
        
        if options['stockindustry'] is None:
            raise CommandError('the --stockindustry argument is required')
        """
        try:
            stocksymbol_FileName = options['stocksymbol_file']
        except:
            stocksymbol_FileName = None
        
        try:
            stockindustryratio_FileName = options['stockindustryratio_file']
        except:
            stockindustryratio_FileName = None
        
        try:
            stockindustry_FileName = options['stockindustry_file']
        except:
            stockindustry_FileName = None
            
        try:
            stockconceptgroup_FileName = options['stockconceptgroup_file']
        except:
            stockconceptgroup_FileName = None
            
        try:
            stockstockconceptgrouprelation_FileName = options['stockconceptgrouprelation']
        except:
            stockstockconceptgrouprelation_FileName = None
            
        mapping = {u'AS':u'TW',u'AD':u'TW',u'SH':u'SH',u'SZ':u'SZ',u'HK':u'HK',u'US':u'US',u'JP':u'JP',u'KS':u'KR',u'SI':u'SG',u'AM':u''}
              
        if stocksymbol_FileName != None:
            try:
                with open(stocksymbol_FileName, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
               
                    #stocksymbolManager.all().delete()
                    for tline in spamreader:
                        try:
                            #tline=line.split(",")
                            Market = tline[1].decode('big5').strip()
                            Symbol = tline[0].decode('big5').strip()
                            if Market==None or Market=='':
                                SymbolKey = tline[0].decode('big5').strip()
                            else:
                                SymbolKey = tline[0].decode('big5').strip()+"."+Market
                            Name = tline[2].decode('big5').strip()
                            SName = tline[3].decode('big5').strip()
                            CUR = tline[4].decode('big5').strip()
                            Unit = tline[5].decode('big5').strip()
                            Reference = tline[6].decode('big5').strip()
                            EName = tline[7].decode('big5').strip()
                            SEName = tline[8].decode('big5').strip()
                            Uplimit = tline[9].decode('big5').strip()
                            Downlimit = tline[10].decode('big5').strip()
                            #PRatio = tline[4].decode('big5')
                            #symbolobject=
                            stocksymbol.objects.CreateUpdate(SymbolKey=SymbolKey,Symbol=Symbol,Market=Market,Name=Name,SName=SName,CUR=CUR,Unit=Unit,Reference=Reference,EName=EName,SEName=SEName,Uplimit=Uplimit,Downlimit=Downlimit)
                            #indratio = stocksymbol.objects.Insert(Symbol=Symbol,Market=Market,Name=Name,SName=SName,CUR=CUR,Unit=Unit,Reference=Reference,EName=EName,SEName=SEName,Uplimit=Uplimit,Downlimit=Downlimit)
                            #stocksymbol.objects.Insert(symbolobject)
                            #symbolobject.save()
                        except Exception, e:
                            print '(stocksymbol)Symbol:'+tline[0].decode('big5')+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
            except Exception, e:
                print '(stocksymbol)FileName Error:'+unicode(e)+unicode(sys.exc_info()[0])      
                        
        if stockindustry_FileName != None:
            try:
                with open(stockindustry_FileName, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
                    stockindustry.objects.all().delete()
                    for tline in spamreader:
                        try:
                            ID = tline[0].decode('big5')
                            Name = tline[1].decode('big5')
                            CNName = tline[2].decode('big5')
                            dimen1 = tline[3].decode('big5')
                            dimen2 = tline[4].decode('big5')
                            dimen3 = tline[5].decode('big5')
                            dimen4 = tline[6].decode('big5')
                            dimen5 = tline[7].decode('big5')
                            dimen6 = tline[8].decode('big5')
                            industry = stockindustry.objects.create(ID=ID,Name=Name,CNName=CNName,dimen1=dimen1,dimen2=dimen2,dimen3=dimen3,dimen4=dimen4,dimen5=dimen5,dimen6=dimen6)
                        except Exception, e:
                            print '(stockindustry)ID:'+tline[0].decode('big5')+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
            except Exception, e:
                print '(stockindustry)FileName Error:'+unicode(e)+unicode(sys.exc_info()[0])
        if stockindustryratio_FileName != None:
            try:
                with open(stockindustryratio_FileName, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
               
                    stockindustryratio.objects.all().delete()
                    for tline in spamreader:
                        try:
                            Market = mapping[tline[0].decode('big5')[0:2]]
                            Symbol = tline[0].decode('big5')[2:8].strip()
                            if Market==None or Market=='':
                                continue
                            try:
                                stocksymbolobject=stocksymbol.objects.get(Symbol=Symbol,Market=Market)
                                if stocksymbolobject==None or stocksymbolobject=='':
                                    continue
                            except Exception, e:
                                print '(stockindustryratio)Symbol:'+Symbol+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
                                continue
                            try:
                                IndID = tline[2].decode('big5')
                                Industry= stockindustry.objects.get(ID=IndID)
                                if Industry==None or Industry=='':
                                    continue
                            except Exception, e:
                                print '(stockindustryratio)IndID:'+IndID+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
                                continue
                        
                            PRatio = tline[4].decode('big5')
                            indratio = stockindustryratio.objects.create(Symbol=stocksymbolobject,Industry=Industry,PRatio=PRatio)
                        except Exception, e:
                            print '(stockindustryratio)Symbol:'+Symbol+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
                    
            except Exception, e:
                print '(stockindustry)FileName Error:'+unicode(e)+unicode(sys.exc_info()[0])      

        if stockconceptgroup_FileName != None:
            try:
                with open(stockconceptgroup_FileName, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
               
                    stockconceptgroup.objects.all().delete()
                    for tline in spamreader:
                        try:
                            #tline=line.split(",")
                            Market = tline[2].decode('big5').strip()
                            GroupSymbol = tline[0].decode('big5').strip()+"."+Market
                            Name = tline[1].decode('big5').strip()
                            
                            indratio = stockconceptgroup.objects.create(GroupSymbol=GroupSymbol,Name=Name)
                        except Exception, e:
                            print '(stockconceptgroup)GroupSymbol:'+tline[0].decode('big5')+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
            except Exception, e:
                print '(stockindustry)FileName Error:'+unicode(e)+unicode(sys.exc_info()[0])      
                        
        if stockstockconceptgrouprelation_FileName != None:
            try:
                with open(stockstockconceptgrouprelation_FileName, 'rb') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
               
                    stockconceptgrouprelation.objects.all().delete()
                    for tline in spamreader:
                        try:
                            Market = mapping[tline[0].decode('big5')[0:2]]
                            StockSymbol = tline[0].decode('big5')[2:8].strip()+"."+Market
                            if Market==None or Market=='':
                                continue
                            GroupSymbol = tline[2].decode('big5').strip()+"."+Market
                            
                            try:
                                stocksymbolobject=stocksymbol.objects.get(Symbol=StockSymbol,Market=Market)
                                if stocksymbolobject==None or stocksymbolobject=='':
                                    continue
                            except Exception, e:
                                print '(ConceptGroupRalation)StockSymbol:'+StockSymbol+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
                                continue
                            try:
                                group= stockconceptgroup.objects.get(GroupSymbol=GroupSymbol)
                                if group==None or group=='':
                                    continue
                            except Exception, e:
                                print '(ConceptGroupRalation)GroupSymbol:'+GroupSymbol+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
                                continue
    
                            grouprelation = stockconceptgrouprelation.objects.create(stock=stocksymbolobject,group=group)
                        except Exception, e:
                            print '(ConceptGroupRalation)ConceptGroupRalation:'+tline[0].decode('big5')+tline[2].decode('big5')+' reason:'+unicode(e)+unicode(sys.exc_info()[0])
            except Exception, e:
                print '(stockindustry)FileName Error:'+unicode(e)+unicode(sys.exc_info()[0])                       

        stocks = stocksymbol.objects.all()
        for stock in stocks:
            Inds = stockindustryratio.objects.filter(Symbol=stock)
            tagName=""
            for Ind in Inds:
                if not (Ind.Industry.Name.strip() in tagName):
                    tagName= tagName + Ind.Industry.Name.strip() + ' '
            stock.tagnames=tagName
            stock.save()