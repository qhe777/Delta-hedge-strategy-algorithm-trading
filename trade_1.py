# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Make connection to TWS by API, build the automated hedge trading strategy
from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order 
from garch3 import Garch3
from stock_price import options
from bsm import Delta_BS
print(Delta_BS)

def make_contract(symbol, sec_type, exch, prim_exch, curr):
    Contract.m_symbol=symbol
    Contract.m_secType=sec_type
    Contract.m_exchange=exch
    Contract.m_primaryExch=prim_exch
    Contract.m_currency=curr
    return Contract

def make_order(action, quantity, price=None):
    if price is not None:
        order=Order()
        order.m_orderType='LMT'
        order.m_totalQuantity=quantity
        order.m_action=action
        order.m_lmtPrice=price
    else:
        order=Order()
        order.m_orderType='MKT'
        order.m_totalQuantity=quantity
        order.m_action=action
    return order
def main():
    conn=Connection.create(port=7496,clientId=937)
    conn.connect()
    
    oid=60002
    quantity=int(round(abs(Delta_BS)*options.volume()))
    print (quantity)
    cont=make_contract(options.stk,'STK','SMART','SMART','USD')
    
    offer=make_order('BUY',quantity, None)
    
    conn.placeOrder(oid, cont, offer)
    conn.disconnect()

main()


    
    
    
