# -*- coding: utf-8 -*-
import numpy as np
import heston_calibration
from scipy.optimize import fmin
import os
import datetime as dt
# sample market data
date_JNJ=(dt.date(2017, 6, 16) - dt.date.today()).days / 365.0
date_TSLA=(dt.date(2017,11,17)-dt.date.today()).days/365.0
date_DUK=(dt.date(2017,7,21)-dt.date.today()).days/365.0
# parameter calibration(kappa, theta, sigma, rho, v0)
def calibrate(init_val, market_datas):
    def error(x,market_datas):
        kappa, theta, sigma, rho, v0 = x

        result = 0.0
        for market_data in market_datas:
            s0, k, market_price, r, T = market_data
            # print s0, k, market_price, r, T
            heston_price = heston_calibration.c_p(kappa, theta, sigma, rho, v0, r, T, s0, k)
            result += (heston_price - market_price) ** 2
        return result
    opt = fmin(error, init_val, args=(market_datas,), maxiter=200)
    return opt


if __name__ =='__main__':
    market_datas=[
        [123.86, 85.0, 36.1, 0.0051213, date_JNJ],
        [123.86, 90.0, 31.78, 0.0051213, date_JNJ],
        [123.86, 95.0, 26.77, 0.0051213, date_JNJ],
        [123.86, 100.0, 24.1, 0.0051213, date_JNJ],
        [123.86, 105.0, 19.05, 0.0051213, date_JNJ],
        [123.86, 110.0, 14.52, 0.0051213, date_JNJ],
        [123.86, 115.0, 9.66, 0.0051213, date_JNJ],
        [123.86, 120.0, 5.74, 0.0051213, date_JNJ],
        [123.86, 125.0, 2.86, 0.0051213, date_JNJ],
        [123.86, 130.0, 1.16, 0.0051213, date_JNJ],
        [123.86, 135.0, 0.42, 0.0051213, date_JNJ]]
    print(market_datas)
    # Initialize kappa, theta, sigma, rho, v0
    init_val = [1.1, 0.1, 0.4, -0.0, 0.1]
    # calibration of parameters
    kappa, theta, sigma, rho, v0 = calibrate(init_val, market_datas)
    #
    print (kappa, theta, sigma, rho, v0)
    market_prices = np.array([])
    heston_prices = np.array([])
    K = np.array([])
    for market_data in market_datas:
        s0, k, market_price, r, T = market_data
        heston_prices = np.append(heston_prices, heston_calibration.c_p(kappa, theta, sigma, rho, v0, r, T, s0, k))
        market_prices = np.append(market_prices, market_price)
        K = np.append(K, k)

    stock='JNJ'
    # plot result
    T = date_JNJ

    # risk free rate
    r = 0.0051213
    st_market = 123.68
    k_market = 110
    print (heston_calibration.c_p(kappa, theta, sigma, rho, v0, r, T, st_market, k_market))
    c_p1 = heston_calibration.c_p(kappa, theta, sigma, rho, v0, r, T, 123.680001, 110)
    delta_c = (c_p1 - heston_calibration.c_p(kappa, theta, sigma, rho, v0, r, T, st_market, k_market)) / 0.000001
    delta_p = delta_c - 1
    if stock=='JNJ':
        delta_heston=delta_p
        volume=4000
    elif stock=='TSLA':
        delta_heston=delta_c
        volume=6000
    else:
        delta_heston=delta_c
        volume=1000
    Hedge_Shares=int(round(abs(delta_heston)*volume))
    print (Hedge_Shares)