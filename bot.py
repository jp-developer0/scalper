import config
from binance.client import Client
from binance.enums import *
import time
import datetime
import numpy as np

client = Client(config.API_KEY, config.API_SECRET, tld='com')
symbolTicker = 'BTCBUSD'
quantityOrders = 0.0013

def tendencia():
    x = []
    y = []
    sum = 0
    ma50_i = 0

    resp = False

    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "18 hour ago UTC")

    if (len(klines) != 72):
        return False
    for i in range (56,72):
        for j in range (i-50,i):
          sum = sum + float(klines[i][4])
        ma50_i = round(sum / 50,2)
        sum = 0
        x.append(i)
        y.append(float(ma50_i))

    modelo = np.polyfit(x,y,1)
    if (modelo[0]>0):
        resp = True

    return resp

def _ma50_():

    ma50_local = 0
    sum = 0

    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "15 hour ago UTC")

    if (len(klines)==60):
        for i in range (10,60):
            sum = sum + float(klines[i][4])
        ma50_local = sum / 50

    return ma50_local

while 1:

    orders = client.get_open_orders(symbol=symbolTicker)

    if (len(orders) != 0):
        print("THERE IS OPEN ORDERS")
        time.sleep(10)
        continue

    # get price
    list_of_tickers = client.get_all_tickers()
    for tick_2 in list_of_tickers:
        if tick_2['symbol'] == symbolTicker:
            symbolPrice = float(tick_2['price'])
    # get price

    ma50 = _ma50_()
    if (ma50 == 0): continue

    print("***** " + symbolTicker + " *******")
    print("Actual MA50 " + str(round(ma50,2)))
    print("Actual Price " + str(round(symbolPrice,2)))
    print("Price to Buy " + str(round(ma50*0.995,2)))

    if (not tendencia()):
        print ("TENDENCIA BAJISTA")
        time.sleep(10)
        continue
    else:
        print ("ALCISTA")

    if (symbolPrice < ma50*0.995):
        print ("BUY")

        order = client.order_market_buy(
            symbol = symbolTicker,
            quantity = quantityOrders
        )

        time.sleep(5)

        orderOCO = client.order_oco_sell(
            symbol = symbolTicker,
            quantity = quantityOrders,
            price = round(symbolPrice*1.02,2),
            stopPrice = round(symbolPrice*0.995,2),
            stopLimitPrice = round(symbolPrice*0.994,2),
            stopLimitTimeInForce = 'GTC'
        )
        time.sleep(20)
