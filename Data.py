import configparser  # 1
import oandapy as opy  # 2
import pandas as pd  # 6
import numpy as np  # 11
import seaborn as sns
import matplotlib.pyplot as plt
import operator

def StrategyMaker():
    print('\n !!! Connecting User !!!')
    config = configparser.ConfigParser()  # 3
    config.read('oanda.cfg')  # 4
    oanda = opy.API(environment='practice',
                    access_token=config['oanda']['access_token'])# 5
    
    print('\n !!! Importing Market Data !!!')
    data = oanda.get_history(instrument='EUR_USD',  # our instrument
                             start='2017-11-24',  # start data
                             end='2017-11-26',  # end date
                             granularity='M1')  # minute bars  # 7
    #data = oanda.rates(account_id=config['oanda']['account_id'],
     #        instruments=['DE30_EUR'], ignore_heartbeat=True);
     
    print('\n !!! Creating DataFrame !!!')
    df = pd.DataFrame(data['candles']).set_index('time')  # 8
    df.index = pd.DatetimeIndex(df.index)  # 9
    #df.info()  # 10
    
    print('\n !!! Calculating Returns !!!')
    df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))  # 12
    df.fillna(0,inplace=True)
    
    print('\n !!! Calculating Positions !!!')
    cols = []  # 13
    for momentum in [15, 30, 60, 120]:  # 14
        col = 'position_%s' % momentum  # 15
        df[col] = np.sign(df['returns'].rolling(momentum).mean())  # 16
        cols.append(col)  # 17
    
    sns.set()  # 18
    
    print('\n !!! Calculating strategy !!!') 
    strats = ['returns']  # 19
    for col in cols:  # 20
        strat = 'strategy_%s' % col.split('_')[1]  # 21
        df[strat] = df[col].shift(1) * df['returns']  # 22
        strats.append(strat)  # 23
    
    #Get the best strategy
    Strat_Mean = {}    
    for strat in strats:
        Strat_Mean[strat] = df[strat].mean()
    print(Strat_Mean)
    BestStrategy = max(Strat_Mean.items(), key=operator.itemgetter(1))[0]
    

    print('\n !!! Plot for various strategies and Returns !!!')
    df[strats].dropna().cumsum().apply(np.exp).plot()  # 24
    plt.show()
    return BestStrategy

def main():
  BestStrategy = StrategyMaker()
  print("\n The Best Strategy: ",BestStrategy)
  print("!!! Inside Data.py !!!")  

if __name__ == '__main__':
  main()