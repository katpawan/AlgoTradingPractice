import numpy as np
import oandapy as opy
import pandas as pd
import json
import configparser
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
config = configparser.ConfigParser()  
config.read('oanda.cfg')  
oanda = opy.API(environment='practice',
                access_token=config['oanda']['access_token'])

api = API(access_token=(config['oanda']['access_token'].replace("'","")))
accountID = config['oanda']['accountID']
class MyTrader(opy.Streamer):  
    def __init__(self, momentum, *args, **kwargs):  
        opy.Streamer.__init__(self, *args, **kwargs)  
        self.ticks = 0  
        self.position = 0  
        self.df = pd.DataFrame()  
        self.momentum = momentum  
        self.units = 100000  

    def create_order(self, side, units):  # 33
        #order = oanda.create_order(config['oanda']['account_id'],instrument='EUR_USD', units=units, side=side,type='market')  # 34
        #print('\n', order)  
        dict_o = {}
        dict_i = {}
        dict_i["instrument"] = "AUD_CAD"
        if(side=='sell'):
    	    units *= -1
        dict_i["units"] = units
        dict_i["type"] = "MARKET"
        dict_i["positionFill"] = "DEFAULT"
        dict_o['order']=dict_i
        r=orders.OrderCreate(accountID, data=json.loads(json.dumps(dict_o)))
        api.request(r)
        print('\n',r.response)

    def on_success(self, data):  
        self.ticks += 1  
        # print(self.ticks, end=', ')
        # appends the new tick data to the DataFrame object
        self.df = self.df.append(pd.DataFrame(data['tick'],
                                              index=[data['tick']['time']]))  
        # transforms the time information to a DatetimeIndex object
        self.df.index = pd.DatetimeIndex(self.df['time'])  
        #---------------------THIS PART HAS TO BE REVIEWED-------------------------##
        # resamples the data set to a new, homogeneous interval
        #dfr = self.df.resample('5s').last()
        dfr = self.df  # 40
        #--------------------------------------------------------------------------##
        # calculates the log returns
        dfr['returns'] = np.log(dfr['ask'] / dfr['ask'].shift(1))
        # derives the positioning according to the momentum strategy
        dfr['position'] = np.sign(dfr['returns'].rolling(self.momentum).mean())
        if dfr['position'].ix[-1] == 1:  # 43
            # go long
            if self.position == 0:
                self.create_order('buy', self.units)
            elif self.position == -1:  # 46
                self.create_order('buy', self.units * 2)
            self.position = 1
        elif dfr['position'].ix[-1] == -1:
            # go short
            if self.position == 0:
                self.create_order('sell', self.units)
            elif self.position == 1:
                self.create_order('sell', self.units * 2)
            self.position = -1  
        if self.ticks == 250:
            # close out the position
            if self.position == 1:  
                self.create_order('sell', self.units)  
            elif self.position == -1:
                self.create_order('buy', self.units)  
            self.disconnect()
