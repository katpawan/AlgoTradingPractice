import configparser
import oandapy as opy
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


print('Import Done!')
config = configparser.ConfigParser()
config.read('oanda.cfg')
oanda = opy.API(environment='practice',
                access_token=config['oanda']['access_token'])
data = oanda.get_history(instrument='EUR_USD',  # our instrument
                         start='2010-12-08',  # start data
                         end='2016-12-10',  # end date
                         granularity='D')  # minute bars
data = oanda.rates(account_id=config['oanda']['account_id'],
         instruments=['DE30_EUR'], ignore_heartbeat=True);
print('Connected!')
df = pd.DataFrame(data['candles']).set_index('time') 
df.index = pd.DatetimeIndex(df.index) 
df.info()  \
print('Calculating Returns')
df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1)) 
cols = []  
print('Calculating Positions')
for momentum in [15, 30, 60, 120]:  
    col = 'position_%s' % momentum  
    df[col] = np.sign(df['returns'].rolling(momentum).mean())  
    cols.append(col)  

sns.set()  

strats = ['returns']  
print('Calculating strategy')
for col in cols:  
    strat = 'strategy_%s' % col.split('_')[1]  
    df[strat] = df[col].shift(1) * df['returns']  
    strats.append(strat)  
df[strats].dropna().cumsum().apply(np.exp).plot()  
plt.show()
