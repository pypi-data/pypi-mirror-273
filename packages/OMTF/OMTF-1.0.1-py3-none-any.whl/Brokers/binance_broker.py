
import datetime as dt
import os

import pandas as pd

# from binance import ThreadedWebsocketManager
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException


# Clase encargada de la conexion con binance
class BinanceConnect:

    token_path: str = os.path.join('keys')

    def __init__(self,api_key:str,api_secret:str,mode:bool=False):
        
        self.api_key: str = api_key
        self.api_secret: str = api_secret

        # En funcion de si operamos en demo o no nos conectamos a una api u otra
        if mode:
            self.client = Client(self.api_key, self.api_secret)
        else:
            self.client = Client(self.api_key, self.api_secret)
            self.client.API_URL = 'https://testnet.binance.vision/api'
        
        # Ampliamos la ventana de tiempo aceptada
        self.client.recvWindow = 10000

        # Test para ver la diferencia entre las horas del ordenador y el servidor
        # for i in range(1, 10):
        #     local_time1 = int(time.time() * 1000)
        #     server_time = self.client.get_server_time()
        #     diff1 = server_time['serverTime'] - local_time1
        #     local_time2 = int(time.time() * 1000)
        #     diff2 = local_time2 - server_time['serverTime']
        #     print("local1: %s server:%s local2: %s diff1:%s diff2:%s" % (local_time1, server_time['serverTime'], local_time2, diff1, diff2))
        #     time.sleep(2)

    # Funcion para importar detalles de la cuenta
    def accountInfo(self) -> dict:

        self.account: dict = self.client.get_account()

        balance: dict = {}
        for b in self.account['balances']:
            if float(b['free']) != 0. or float(b['locked']) != 0.:
                balance[b['asset']] = {}
                balance[b['asset']]['free'] = float(b['free'])
                balance[b['asset']]['locked'] = float(b['locked'])

        self.account['balances'] = balance

        return self.account

    # Funcion para importr el balance en un ticker
    def assetBalance(self,cripto:str) -> dict:

        self.balance: dict = self.client.get_asset_balance(asset=cripto)

        return self.balance

    # Funcion para importar detalles del ticker
    def assetDetails(self,cripto:(str|list)) -> dict:

        if isinstance(cripto, str):
            cripto: list = [cripto]

        details: dict = self.client.get_asset_details()
        for a in details:
            if a in cripto:
                self.details: dict = {}
                self.details[a] = details[a]
        
        return self.details

    # Funcion para importar el ultimo precio del par
    def lastPrice(self,pair:str) -> (list | dict):

        data = self.client.get_symbol_ticker(symbol=pair)

        return data

    # Funcion para importar informacion del simbolo
    def pairInfo(self,pair:str) -> dict:

        info: dict = self.client.get_symbol_info(pair)

        return info

    # Funcion para calcular el tamaño minimo de la operacion
    def pairMinSize(self,pair:str) -> (float | None):

        try:
            info: dict = self.pairInfo(pair=pair)
            min_notional: float = float([k for k in info['filters'] if k['filterType'] == 'NOTIONAL'][0]['minNotional'])
            price: float = float(self.lastPrice(pair=pair)['price'])
            #print(min_notional,price,min_notional/price)
            self.min_size: float = -(-min_notional//price)
        except:
            self.min_size = None

        return self.min_size

    # Funcion para importar las x ultimas velas de un timeframe de un par
    def getCandles(self,pair:str,tf:str='5m',limit:int=1000, 
                   start:dt.datetime=None, end:dt.datetime=None) -> pd.DataFrame:
        
        '''
        TimeFrames validos - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        '''

        # Cogemos el periodo de tiempo de los ultimos datos disponibles
        if start != None or end != None:
            bars: dict = self.client.get_klines(symbol=pair,interval=tf, 
                                                startTime=int(start.timestamp()*1e3), 
                                                endTime=int(end.timestamp()*1e3)) 
        else:
            bars: dict = self.client.get_klines(symbol=pair,interval=tf,limit=limit) 

        self.df: pd.DataFrame = pd.DataFrame(bars, columns=['Date', 'Open', 'High', 'Low', 'Close','Volume','Close Time','Base Volume','Number trades','TBB','TBQ','I'])
        self.df: pd.DataFrame = self.df.drop(columns=['Close Time','TBB','TBQ','I'])

        # Formateamos las fechas para que correspondan a las locales
        self.df['Date'] = pd.to_datetime(self.df['Date'] // 1000, unit='s')
        self.df.set_index('Date', inplace=True)
        for c in self.df.columns:
            if c not in ['Date', 'Number trades']:
                self.df[c] = self.df[c].astype(float)

        return self.df

    # Funcion para importar el libro de ordenes (Level 2)
    def orderBook(self,pair:str) -> dict:

        depth: dict = self.client.get_order_book(symbol=pair)
        self.book: dict = {}
        # Preparamos los bids
        self.book['bids'] = pd.DataFrame(depth['bids'],columns=['Price','Volume'])
        self.book['bids']['Price'] = pd.to_numeric(self.book['bids']['Price'])
        self.book['bids']['Volume'] = pd.to_numeric(self.book['bids']['Volume'])
        self.book['bids']['Base Volume'] = self.book['bids']['Price'] * self.book['bids']['Volume']
        # Preparamos los asks
        self.book['asks'] = pd.DataFrame(depth['asks'],columns=['Price','Volume'])
        self.book['asks']['Price'] = pd.to_numeric(self.book['asks']['Price'])
        self.book['asks']['Volume'] = pd.to_numeric(self.book['asks']['Volume'])
        self.book['asks']['Base Volume'] = self.book['asks']['Price'] * self.book['asks']['Volume']

        self.book['bidsSum'] = {'volume':self.book['bids']['Volume'].sum(skipna=True),
                            'base volume':self.book['bids']['Base Volume'].sum(skipna=True)}
        self.book['asksSum'] = {'volume':self.book['asks']['Volume'].sum(skipna=True),
                            'base volume':self.book['asks']['Base Volume'].sum(skipna=True)}

        return self.book

    # Funcion para importar el time and sales
    def timesSales(self,pair:str,limit:int=50,descending:bool=False) -> pd.DataFrame:

        trades: list = self.client.get_recent_trades(symbol=pair,limit=limit)


        self.tape: pd.DataFrame = pd.DataFrame(trades)
        self.tape.columns = ['ID', 'Price', 'Size', 'Base Size', 'DateTime', 'Side', 'IsBestMatch']
        self.tape['Side'] = self.tape['Side'].apply(lambda x: 'Buy' if x else 'Sell')

        # Formateamos las fechas para que correspondan a las locales
        self.tape['DateTime'] = pd.to_datetime(self.tape['DateTime'] // 1000, unit='s')
        for c in self.tape.columns:
            if c in ['Price', 'Size', 'Base Size']:
                self.tape[c] = self.tape[c].astype(float)
        
        if descending:
            self.tape.sort_values('ID', ascending=False, inplace=True)
            self.tape.reset_index(drop=True, inplace=True)

        return self.tape
    
    # Funcion para importar las ordenes abiertas
    def openOrders(self,pair:str='') -> (list | dict):

        if pair == '':
            orders = self.client.get_open_orders()
        else:
            orders = self.client.get_open_orders(symbol=pair)

        return orders

    # Funcion para importar todas las ordenes
    def allOrders(self,pair:str,orderid=None) -> (list | dict):

        if orderid == None:
            orders = self.client.get_all_orders(symbol=pair)
        else:
            orders = self.client.get_all_orders(symbol=pair,orderId=int(orderid))

        return orders

    # Funcion para cancelar una orden
    def orderCancel(self,pair:str,orderid:int) -> dict:

        cancel: dict = self.client.cancel_order(symbol=pair,orderId=orderid)

        return cancel

    # Funcion para importar mis operaciones
    def getTrades(self,pair:str) -> (list | dict):

        trades = self.client.get_my_trades(symbol=pair)

        return trades

    # Funcion para abrir cualquier tipo de orden
    def openOrder(self,side:str,ticker:str,stopprice:float=0.0,limitprice:float=0.0,quantity:int=1,
                   timeInForce:str='GTC',test:bool=True) -> dict:

        if test:
            if limitprice == 0.0 and stopprice == 0.0:
                if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,
                                    type=ORDER_TYPE_MARKET,quantity=abs(quantity))
                elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,
                                    type=ORDER_TYPE_MARKET,quantity=abs(quantity))
                else:
                    self.order = None
            elif limitprice != 0 and stopprice == 0.0:
                if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,
                                    type=ORDER_TYPE_LIMIT,quantity=abs(quantity),price=str(limitprice))
                elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,
                                    type=ORDER_TYPE_LIMIT,quantity=abs(quantity),price=str(limitprice))
                else:
                    self.order = None
            elif limitprice != 0 and stopprice != 0:
                if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                    if timeInForce in ['GTC','gtc','Gtc']:
                        self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                                stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['IOC','ioc','Ioc']:
                        self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                                stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['FOK','fok','Fok']:
                        self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                                stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                    if timeInForce in ['GTC','gtc','Gtc']:
                        self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                                stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['IOC','ioc','Ioc']:
                        self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                                stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['FOK','fok','Fok']:
                        self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                                stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                else:
                    self.order = None
            elif stopprice != 0.0 and limitprice == 0.0:
                if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                    if timeInForce in ['GTC','gtc','Gtc']:
                        self.order: dict = self.client.create_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS,
                                                            stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['IOC','ioc','Ioc']:
                        self.order: dict = self.client.create_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS,
                                                            stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['FOK','fok','Fok']:
                        self.order: dict = self.client.create_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS,
                                                            stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                    if timeInForce in ['GTC','gtc','Gtc']:
                        self.order: dict = self.client.create_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS,
                                                            stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['IOC','ioc','Ioc']:
                        self.order: dict = self.client.create_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS,
                                                            stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['FOK','fok','Fok']:
                        self.order: dict = self.client.create_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS,
                                                            stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                else:
                    self.order = None


        else:
            if limitprice == 0.0:
                if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                    self.order: dict = self.client.order_market_buy(symbol=ticker,quantity=abs(quantity))
                elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                    self.order: dict = self.client.order_market_sell(symbol=ticker,quantity=abs(quantity))
                else:
                    self.order = None
            elif limitprice != 0:
                if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                    self.order: dict = self.client.order_limit_buy(symbol=ticker,quantity=abs(quantity),price=str(limitprice))
                elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                    self.order: dict = self.client.order_limit_sell(symbol=ticker,quantity=abs(quantity),price=str(limitprice))
                else:
                    self.order = None
            elif limitprice != 0 and stopprice != 0:
                if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                    if timeInForce in ['GTC','gtc','Gtc']:
                        self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_BUY,stopLimitInForce=TIME_IN_FORCE_GTC,
                                                                    quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['IOC','ioc','Ioc']:
                        self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_BUY,stopLimitInForce=TIME_IN_FORCE_IOC,
                                                                    quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['FOK','fok','Fok']:
                        self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_BUY,stopLimitInForce=TIME_IN_FORCE_FOK,
                                                                    quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                    if timeInForce in ['GTC','gtc','Gtc']:
                        self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_SELL,stopLimitInForce=TIME_IN_FORCE_GTC,
                                                                    quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['IOC','ioc','Ioc']:
                        self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_SELL,stopLimitInForce=TIME_IN_FORCE_IOC,
                                                                    quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                    elif timeInForce in ['FOK','fok','Fok']:
                        self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_SELL,stopLimitInForce=TIME_IN_FORCE_FOK,
                                                                    quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                else:
                    self.order = None

        return self.order

    # Funcion para introducir ordenes a mercado
    def marketOrder(self,side:str,ticker:str,quantity:int=1,test:bool=True) -> dict:

        if test:
            if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,
                                type=ORDER_TYPE_MARKET,quantity=abs(quantity))
            elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,
                                type=ORDER_TYPE_MARKET,quantity=abs(quantity))
            else:
                self.order = None
        else:
            if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                self.order: dict = self.client.order_market_buy(symbol=ticker,quantity=abs(quantity))
            elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                self.order: dict = self.client.order_market_sell(symbol=ticker,quantity=abs(quantity))
            else:
                self.order = None
        
        return self.order

    # Funcion para introducir ordenes limitadas
    def limitOrder(self,side:str,ticker:str,price:float,quantity:int=1,test:bool=True) -> dict:

        if test:
            if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,
                                type=ORDER_TYPE_LIMIT,quantity=abs(quantity),price=str(price))
            elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,
                                type=ORDER_TYPE_LIMIT,quantity=abs(quantity),price=str(price))
            else:
                self.order = None
        else:
            if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                self.order: dict = self.client.order_limit_buy(symbol=ticker,quantity=abs(quantity),price=str(price))
            elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                self.order: dict = self.client.order_limit_sell(symbol=ticker,quantity=abs(quantity),price=str(price))
            else:
                self.order = None
        
        return self.order

    # Funcion para introducir ordenes OCO
    def ocoOrder(self,side:str,ticker:str,stopprice:float,limitprice:float,quantity:int=1,
                  timeInForce:str='GTC',test:bool=True) -> dict:

        if test:
            if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                if timeInForce in ['GTC','gtc','Gtc']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                            stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['IOC','ioc','Ioc']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                            stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['FOK','fok','Fok']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_BUY,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                            stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)

            elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                if timeInForce in ['GTC','gtc','Gtc']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                            stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['IOC','ioc','Ioc']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                            stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['FOK','fok','Fok']:
                    self.order: dict = self.client.create_test_order(symbol=ticker,side=SIDE_SELL,type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                                            stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)

            else:
                self.order = None

        else:
            if side in ['b','B','Buy','buy','Compra','C','c','compra']:
                if timeInForce in ['GTC','gtc','Gtc']:
                    self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_BUY,stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['IOC','ioc','Ioc']:
                    self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_BUY,stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['FOK','fok','Fok']:
                    self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_BUY,stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)

            elif side in ['s','S','Sell','sell','venta','Venta','v','V']:
                if timeInForce in ['GTC','gtc','Gtc']:
                    self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_SELL,stopLimitInForce=TIME_IN_FORCE_GTC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['IOC','ioc','Ioc']:
                    self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_SELL,stopLimitInForce=TIME_IN_FORCE_IOC,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)
                elif timeInForce in ['FOK','fok','Fok']:
                    self.order: dict = self.client.create_oco_order(symbol=ticker,side=SIDE_SELL,stopLimitInForce=TIME_IN_FORCE_FOK,quantity=abs(quantity),stopPrice=str(stopprice),price=limitprice)

            else:
                self.order = None
        
        return self.order
    
    def exchangeInfo(self) -> dict:

        ex: dict = self.client.get_exchange_info()

        return ex
    
    def availableSymbols(self) -> pd.DataFrame:

        return pd.DataFrame(self.exchangeInfo()['symbols'])
    

if __name__ == '__main__':

    key = 'TwUpIi6qrTCLpd8hu1bAlktxOBD4MojMdkQjakaHnIdqZfASnfH52MeDuVgVZvi2'
    secret = 'PzNxcgm5xWpgZqesleiveySPnSh0W9hR2fmLqoVjMd5oYmRVweyydBx9FjzVOUrs'

    #key = 'mFcOiylrUrE95gU2BXsigm3CRhrBrh9NQclFp9ORqcQBfXG6I1UIMr2EWTJzoRJg'
    #secret = 'd1YUe6UTeoyzccamRtYXYd9cMFgTnsOWSIKqMvKyWy1msjxmWhuDSLcm7dKcElSq'
    binance = BinanceConnect(key, secret, mode=True)
    acc_info = binance.accountInfo()
    binance.availableSymbols()