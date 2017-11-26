from MyTrader import MyTrader
import configparser
from oandapyV20 import API
import json
import Data as Strategy
# import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing


#Get Trading Strategy
def GetTradingStrategy():
    TradingStrategy = Strategy.StrategyMaker()
    return TradingStrategy



def AlgoTrader():
    #api = API(access_token="77e52f20c91e859b1edbf6f63a049994-0d58a82089e68f5437225b0daffbad96")
    #accountID = "101-001-7189583-001"
    api = API(access_token="280131fad16391b7433e29967e7fb384-9b1ad7bee86ec27e2d9234147accbea3")
    accountID = "101-011-7185005-001"
    
    config = configparser.ConfigParser()  # 3
    config.read('oanda.cfg')  # 4
    
    mt = MyTrader(momentum=12, environment='practice',
                  access_token=config['oanda']['access_token'])
    
    
    
    params = {"instruments": "AUD_CAD"
              }
    r = pricing.PricingStream(accountID=accountID, params=params)
    #rv = api.request(r)
    maxrecs = 100
    
    
    #mt.rates(account_id=config['oanda']['account_id'],
    #        instruments=['DE30_EUR'], ignore_heartbeat=True)
    dict_o = {}
    dict_i = {}
    ignore_heartbeat=True
    for i in range(250):
        #print(i)
        rv = api.request(r)    
        for line in rv:
            dict_o.clear()
            dict_i.clear()
            dict_i['ask'] = float(line['closeoutAsk'])
            dict_i['bid'] = float(line['closeoutBid'])
            dict_i['instrument'] = line['instrument']
            dict_i['time'] = line['time']
            dict_o['tick'] = dict_i;
            #data = json.loads(line.decode("utf-8"))
            mt.on_success(json.loads(json.dumps(dict_o)))
            break;
    print("end")
            
            
        
    
    
    # =============================================================================
    # config = configparser.ConfigParser()  # 3
    # config.read('oanda.cfg')  # 4
    # mt = MyTrader(momentum=12, environment='practice',
    #               access_token=config['oanda']['access_token'])
    # mt.rates(account_id=config['oanda']['account_id'],
    #            instruments=['DE30_EUR'],
    #            ignore_heartbeat=True)
    # =============================================================================
    
def main():
  TradingStrategy = GetTradingStrategy()
  print("\n The Trading Strategy Being used is:",TradingStrategy)
  

if __name__ == '__main__':
  main()