import numpy as np
import scipy.stats as ss
from stock_price import options

#Using real time stock price and volatility to calculate the Delta by B-S model
f=open('1.txt')
a=0.0
for line in f:
    a=a+float(line)
S0=a*0.5
print(S0)

K = options.strike()
print(K)
r=0.0051213

sigma =options.get_vola()
print(sigma)
T = options.maturity()
print(T)
Otype=options.action()


# Black and Scholes
def d1(S0, K, r, sigma, T):
    return (np.log(S0 / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))


def d2(S0, K, r, sigma, T):
    return (np.log(S0 / K) + (r - sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))


def Delta_BlackScholes(type, S0, K, r, sigma, T):
    if type == 'C':
        return ss.norm.cdf(d1(S0, K, r, sigma, T))
    else:
        return ss.norm.cdf(d1(S0, K, r, sigma, T))-1

Delta_BS = Delta_BlackScholes(Otype,S0, K, r, sigma, T)
print(Delta_BS)
print(round(abs(Delta_BS)*options.volume()))

