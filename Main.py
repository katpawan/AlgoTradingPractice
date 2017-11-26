from MyTrader import MyTrader
import configparser
from oandapyV20 import API
import json
import oandapyV20.endpoints.pricing as pricing

config = configparser.ConfigParser() 
config.read('oanda.cfg') 
mt = MyTrader(momentum=5, environment='practice',
              access_token=config['oanda']['access_token'])
accountID = config['oanda']['accountID']
api = API(access_token=(config['oanda']['access_token'].replace("'","")))

params = {"instruments": "AUD_CAD"
          }
r = pricing.PricingStream(accountID=accountID, params=params)
rv = api.request(r)
maxrecs = 100


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