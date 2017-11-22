import configparser  # 1
import oandapy as opy  # 2
import pandas as pd  # 6
import numpy as np  # 11
import seaborn as sns
import matplotlib.pyplot as plt


print('Import Done!')
config = configparser.ConfigParser()  # 3
config.read('oanda.cfg')  # 4
oanda = opy.API(environment='practice',
                access_token=config['oanda']['access_token'])  # 5
data = oanda.get_history(instrument='EUR_USD',  # our instrument
                         start='2010-12-08',  # start data
                         end='2016-12-10',  # end date
                         granularity='D')  # minute bars  # 7
data = oanda.rates(account_id=config['oanda']['account_id'],
         instruments=['DE30_EUR'], ignore_heartbeat=True);
print('Connected!')
df = pd.DataFrame(data['candles']).set_index('time')  # 8
df.index = pd.DatetimeIndex(df.index)  # 9
df.info()  # 10
print('Calculating Returns')
df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))  # 12
cols = []  # 13
print('Calculating Positions')
for momentum in [15, 30, 60, 120]:  # 14
    col = 'position_%s' % momentum  # 15
    df[col] = np.sign(df['returns'].rolling(momentum).mean())  # 16
    cols.append(col)  # 17

sns.set()  # 18

strats = ['returns']  # 19
print('Calculating strategy')
for col in cols:  # 20
    strat = 'strategy_%s' % col.split('_')[1]  # 21
    df[strat] = df[col].shift(1) * df['returns']  # 22
    strats.append(strat)  # 23
df[strats].dropna().cumsum().apply(np.exp).plot()  # 24
plt.show()
