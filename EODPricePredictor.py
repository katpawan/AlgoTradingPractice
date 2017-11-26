from pandas_datareader import data as web
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV as rcv
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
import matplotlib.pyplot as plt

class EODPricePredictor():
    """ Provide functionality to predict EOD closing price"""
    def __init__(self,link, instrument,startYear):
        self.dbLink = link
        self.instrument = instrument
        self.startyear = startYear
        
    def extractHistoricalData(self):
        """ Extract historical open/Close data from history """
        self.df = web.DataReader(self.dbLink,data_source=self.instrument,start=self.startyear)
        self.df=self.df[['Open','High','Low','Close']]

        self.df['open']=self.df['Open'].shift(1)
        self.df['high']=self.df['High'].shift(1)
        self.df['low']=self.df['Low'].shift(1)
        self.df['close']=self.df['Close'].shift(1)

    def intializeAlgo(self):
        #Creating hyper-parameters
        self.X=self.df[['open','high','low','close']]
        self.y=self.df['Close']
        
        imp = Imputer(missing_values='NaN',strategy='mean', axis=0)
        self.X=imp.fit_transform(self.X,self.y)
        steps = [('imputation', imp),
        		 ('scaler',StandardScaler()),
        		 ('lasso',Lasso())]
        pipeline =Pipeline(memory=None,steps=steps)        
        parameters = {'lasso__alpha':np.arange(0.0001,10,.0001),
        			  'lasso__max_iter':np.random.uniform(100,100000,4)}        			  
        self.reg = rcv(pipeline,parameters,cv=5) 
        #print self.X[:self.X.shape[0]-1]
        #print self.X[-1:]           
        self.reg.fit(self.X[:self.X.shape[0]-1],self.y[:self.X.shape[0]-1])  
        best_alpha = self.reg.best_params_['lasso__alpha']
        best_iter = self.reg.best_params_['lasso__max_iter']
        self.reg1 = Lasso(alpha=best_alpha,max_iter=best_iter)
        
        
    def trainAlgo(self):          
        self.reg1.fit(self.X[:self.X.shape[0]-1],self.y[:self.X.shape[0]-1])
        
    def testAlgo(self):
        #Splittng data into test and train sets        
        split = int(90*len(self.X)/100)
        self.reg.fit(self.X[:split],self.y[:split])        
        self.reg1.fit(self.X[:split],self.y[:split])
        self.df['predict']=self.df['Close']
        
        forcast_set=self.reg1.predict(self.X[split:])
        rowCount = -1
        #print split
        #print rowCount
        for i in forcast_set:
            self.df['predict'].iloc[split+rowCount]=i
            rowCount=rowCount+1
    
        self.df['Error']=np.abs(self.df['predict']-self.df['Close'])
        e = np.mean(self.df['Error'][split:])
        print(e)

        coef= self.reg1.score(self.X[split:],self.y[split:])
        print(coef)

    def getTodayPrice(self):
        forcast_set=self.reg1.predict(self.X[-1:])
        return forcast_set
        

pp = EODPricePredictor(link='AUDCAD=X', instrument='yahoo',startYear='2015')
pp.extractHistoricalData()
pp.intializeAlgo()
pp.trainAlgo()
#pp.testAlgo()
todayPrice=pp.getTodayPrice()
print(todayPrice)
