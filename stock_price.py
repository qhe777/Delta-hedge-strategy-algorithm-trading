#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:31:42 2017

@author: qh777
"""
#Download the realtime stock price from TWS to a temporary txt file
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep
from garch3 import Garch3

options=Garch3('TSLA')

# print all messages from TWS
def watcher(msg):
    print(msg)

# show Bid and Ask quotes
def my_BidAsk(msg):
    if msg.field == 1:
        a=('%s:%s: bid: %s' % (contractTuple[0],
                       contractTuple[6], msg.price))
        c=msg.price
        f.write(str(c)+'\n')
        print(a)
    elif msg.field == 2:
        b=('%s:%s: ask: %s' % (contractTuple[0], contractTuple[6], msg.price))
        d=msg.price
        
        f.write(str(d)+'\n')
        
        print(b)
        
def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    return newContract

if __name__ == '__main__':
    f=open('1.txt','w')

    con = ibConnection()
    con.registerAll(watcher)
    showBidAskOnly = True  # set False to see the raw messages
    if showBidAskOnly:
        con.unregister(watcher, message.tickSize, message.tickPrice,
                       message.tickString, message.tickOptionComputation)
        con.register(my_BidAsk, message.tickPrice)
    con.connect()
    sleep(1)
    tickId = 1
    
    contractTuple = (options.stk, 'STK', 'SMART', 'USD', '', 0.0, '')

    stkContract = makeStkContract(contractTuple)
    print ('* * * * REQUESTING MARKET DATA * * * *')
    con.reqMktData(tickId, stkContract, '', True)
    sleep(10)
    print ('* * * * CANCELING MARKET DATA * * * *')
    
    con.cancelMktData(tickId)
    sleep(1)
    con.disconnect()
    sleep(1)
    
    f.close()
