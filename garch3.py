#Garch
import datetime as dt
import pandas_datareader.data as web
import numpy as np
from arch import arch_model

class Garch3:    
    def __init__(self,stock):
        self.stk=stock
        
    def expire(self):
        if self.stk=='JNJ':
            
            t=dt.date(2017,6,16)
            return t
        elif self.stk=='TSLA':
            t=dt.date(2017,11,17)
            return t
        else:
            t=dt.date(2017,7,21)
            return t
    def maturity(self):
        if self.stk=='JNJ':
            
            t=(dt.date(2017,6,16)-dt.date.today()).days/365
            return t
        elif self.stk=='TSLA':
            t=(dt.date(2017,11,17)-dt.date.today()).days/365
            return t
        else:
            t=(dt.date(2017,7,21)-dt.date.today()).days/365
            return t
    def strike(self):
        if self.stk=='JNJ':
            return 110
        elif self.stk=='TSLA':
            return 240
        else:
            return 75
    def action(self):
        if self.stk=='JNJ':
            return 'P'
        elif self.stk=='TSLA':
            return 'C'
        else:
            return 'C'
    def volume(self):
        if self.stk=='JNJ':
            return 4000
        elif self.stk=='TSLA':
            return 6000
        else:
            return 1000

#Using GARCH(1,1) model to forecast volatility
    def get_vola(self):
        st = (dt.date.today()-dt.timedelta(365))
        en = dt.date.today()
        f = web.DataReader(self.stk, 'yahoo', st, en)
        leng=f.shape
        length=leng[0]
        returns = f['Adj Close'].pct_change().dropna()
        stdev=np.std(returns)        
        am = arch_model(returns)
        res = am.fit(update_freq=5)
        f2=res.params['alpha[1]']*res.resid**2
        f1=stdev**2*res.params['beta[1]']
        forecast_vol=np.sqrt(res.params['omega']+f2+f1)
        forecast_vol_annual=forecast_vol*(length-1)**0.5
        return (forecast_vol_annual[length-2])






    
    



