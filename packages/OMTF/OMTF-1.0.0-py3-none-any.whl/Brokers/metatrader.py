
import datetime as dt
import os
import pytz

import MetaTrader5 as mt5
import numpy as np
import pandas as pd


class Mt5Connect():
    
    real: dict = {'username':'7094662', 'password':'Onemade3680', 'server':'ICMarketsSC-MT5-2'}

    def __init__(self, user:int=50924546, password:str='CbIDQI9F', 
                 server:str='ICMarketsSC-Demo',path:str=None) -> None:

        '''
        Generate commissions configuration.

        Parameters
        ----------
        user: str
            User of the MetaTrader5 account.
        password: str
            Password asociated to the MetaTrader5 acount.
        server: str
            Server of the MetaTrader5 account.
        '''
        
        mt5.initialize()

        self.user: int = user
        self.password: str = password
        self.server: str = server
        authorized = mt5.login(user, password, server) 

        if authorized:
            print('Connected: Connecting to MT5 Client')
        else:
            print(f"Failed to connect at account #{user}, error code: {mt5.last_error()}")

    def getInfo(self) -> dict:

        self.account_info: dict = mt5.account_info()._asdict()
        
        return self.account_info

    def getHistoryOrders(self) -> pd.DataFrame:

        history = mt5.history_orders_get(dt.datetime(2020,1,1),dt.datetime.now())
        
        df = pd.DataFrame(list(history),columns=history[0]._asdict().keys())
        df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
        df['time_setup_msc'] = pd.to_datetime(df['time_setup_msc'], unit='ms')
        df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
        df['time_done_msc'] = pd.to_datetime(df['time_done_msc'], unit='ms')
        df['Type'] = np.where(df['Type'] == 0, 'Buy', 'Sell')
        print(df)

        return df

    def symbolInfo(self,pair:str):

        if '_' in ticker:
            ticker = ticker.replace('_','')
        elif '/' in ticker:
            ticker = ticker.replace('/','')
        
        return mt5.symbol_info(pair)

    def openPosition(self, pair:str, order_type:str, order_side:str, risk:float, 
                      price:float=None, deviation:int=20,
                      sl_margin:float=None, tp_margin:float=None,
                      comment:str='Entered with a Python bot.'):

        symbol_info = mt5.symbol_info(pair)
        account_info = self.get_info()
        if symbol_info is None:
            print(pair, 'not found')
            return

        if not symbol_info.visible:
            print(pair, 'is not visible, trying to switch on')
            if not mt5.symbol_select(pair, True):
                print(f"symbol_select({pair}) failed, exit")
                return
        print(pair, 'found!')

        size: float = (risk * float(account_info['balance']) / (sl_margin / symbol_info.point)) * 100//1/100
        if size < symbol_info.volume_min:
            size = symbol_info.volume_min
        elif size > symbol_info.volume_max:
            size = symbol_info.volume_max 
            
        request: dict = {
            'action': order_type,
            'symbol': pair,
            'volume': float(size),
            'type': order_side,
            'deviation': deviation,
            'magic': 20031999,
            'comment': comment,
            'type_time': mt5.ORDER_TIME_GTC,
            'type_filling': mt5.ORDER_FILLING_IOC,
        }
        
        if('buy' in order_side.lower()):
            ask = mt5.symbol_info_tick(pair).ask
            request['price'] = ask
            request['type'] = mt5.ORDER_TYPE_BUY
            request['action'] = mt5.TRADE_ACTION_DEAL
            request['type_filling'] = mt5.ORDER_FILLING_IOC
            if 'limit' not in order_side:
                if price > ask + deviation:
                    request['price'] = price
                    request['stopprice'] = price
                    request['type'] = mt5.ORDER_TYPE_BUY_STOP_LIMIT
                    request['action'] = mt5.TRADE_ACTION_PENDING
                    request['type_filling'] = mt5.ORDER_FILLING_RETURN
                elif price < ask - deviation:
                    request['price'] = price
                    request['type'] = mt5.ORDER_TYPE_BUY_LIMIT
                    request['action'] = mt5.TRADE_ACTION_PENDING
                    request['type_filling'] = mt5.ORDER_FILLING_RETURN
                    
            if(sl_margin):
                request['sl'] = request['price'] - sl_margin
            if(tp_margin):
                request['tp'] = request['price'] + tp_margin
                
        elif('sell' in order_side.lower()):
            bid = mt5.symbol_info_tick(pair).bid
            request['price'] = bid
            request['type'] = mt5.ORDER_TYPE_SELL
            request['action'] = mt5.TRADE_ACTION_DEAL
            request['type_filling'] = mt5.ORDER_FILLING_IOC
            if 'limit' not in order_side:
                if price < bid - deviation:
                    request['price'] = price
                    request['stopprice'] = price
                    request['type'] = mt5.ORDER_TYPE_SELL_STOP_LIMIT
                    request['action'] = mt5.TRADE_ACTION_PENDING
                    request['type_filling'] = mt5.ORDER_FILLING_RETURN
                elif price > bid + deviation:
                    request['price'] = price
                    request['type'] = mt5.ORDER_TYPE_SELL_LIMIT
                    request['action'] = mt5.TRADE_ACTION_PENDING
                    request['type_filling'] = mt5.ORDER_FILLING_RETURN
                        
            if(sl_margin):
                request['sl'] = request['price'] + sl_margin
            if(tp_margin):
                request['tp'] = request['price'] - tp_margin
        
        print(size)
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print('Failed to send order :(')
        else:
            print ('Order successfully placed!')

    def getPositions(self, symbol:str=None) -> pd.DataFrame:

        if(symbol is None):
            res = mt5.positions_get()
        else:
            res = mt5.positions_get(symbol=symbol)

        if(res is not None and res != ()):
            df: pd.DataFrame = pd.DataFrame(list(res),columns=res[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        
        return pd.DataFrame()

    def closePosition(self, deal_id=None, deviation:int=10) -> list:

        open_positions: pd.DataFrame = self.getPositions()
        if deal_id:
            open_positions: pd.DataFrame = open_positions[open_positions['ticket'] == deal_id]
            
        close_data: list = []
        for i in open_positions.index:
            
            order_type  = open_positions['type'].loc[i]
            symbol = open_positions['symbol'].loc[i]
            if(order_type == mt5.ORDER_TYPE_BUY):
                mt5_order_type = mt5.ORDER_TYPE_SELL
                price = mt5.symbol_info_tick(symbol).bid
            else:
                mt5_order_type = mt5.ORDER_TYPE_BUY
                price = mt5.symbol_info_tick(symbol).ask

            close_request: dict = {
                'action': mt5.TRADE_ACTION_DEAL,
                'symbol': symbol,
                'volume': float(open_positions['volume'].loc[i]),
                'type': mt5_order_type,
                'position': int(open_positions['ticket'].loc[i]),
                'price': price,
                'deviation': deviation,
                'magic': 20031999,
                'comment': 'FXGap',
                'type_time': mt5.ORDER_TIME_GTC,
                'type_filling': mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(close_request)
           
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Failed to close order :(")
            else:
                print ("Order successfully closed!")
            
            # Data recopilation
            account_info = self.getInfo()
            close_data_symbol: dict = {
                'ID': int(open_positions['ticket'].loc[i]),
                'Ticker': symbol,
                'Type': order_type,
                'Size': float(open_positions['volume'].loc[i]),
                'Entry': open_positions['price_open'].loc[i],
                'Exit': price,
                'SL': open_positions['sl'].loc[i],
                'TP': open_positions['tp'].loc[i],
                'Profit': open_positions['profit'].loc[i],
                'Date': open_positions['time'].loc[i],
                'Balance': float(account_info['balance']),
                'result': result
            }

            close_data.append(close_data_symbol)

        return close_data

    def closePositonsBySymbol(self, symbol:str) -> pd.DataFrame:

        open_positions: pd.DataFrame = self.getPositions(symbol)
        open_positions['ticket'].apply(lambda x: self.closePosition(x))

    def _timeframeMatch(self, timeframe:str):
        
        # Asignamos el timeframe
        match timeframe:
            case 'M1':
                return mt5.TIMEFRAME_M1
            case 'M2':
                return mt5.TIMEFRAME_M2
            case 'M3':
                return mt5.TIMEFRAME_M3
            case 'M4':
                return mt5.TIMEFRAME_M4
            case 'M5':
                return mt5.TIMEFRAME_M5
            case 'M6':
                return mt5.TIMEFRAME_M6
            case 'M10':
                return mt5.TIMEFRAME_M10
            case 'M12':
                return mt5.TIMEFRAME_M12
            case 'M15':
                return mt5.TIMEFRAME_M15
            case 'M20':
                return mt5.TIMEFRAME_M20
            case 'M30':
                return mt5.TIMEFRAME_M30
            case 'H1':
                return mt5.TIMEFRAME_H1
            case 'H2':
                return mt5.TIMEFRAME_H2
            case 'H3':
                return mt5.TIMEFRAME_H3
            case 'H4':
                return mt5.TIMEFRAME_H4
            case 'H6':
                return mt5.TIMEFRAME_H6
            case 'H8':
                return mt5.TIMEFRAME_H8
            case 'H12':
                return mt5.TIMEFRAME_H12
            case 'D1':
                return mt5.TIMEFRAME_D1
            case 'W1':
                return mt5.TIMEFRAME_W1
            case 'MN1':
                return mt5.TIMEFRAME_MN1

    def getCandles(self,ticker:str,timeframe=mt5.TIMEFRAME_D1,
                    init_date:dt.datetime=None,
                    final_date:dt.datetime=None, 
                    bars:int=1000, tillbar:int=0) -> pd.DataFrame:
        
        if bars == None:
            if init_date == None:
                init_date = dt.datetime.now() - dt.timedelta(days=15)
            if final_date == None:
                final_date = dt.datetime.now() + dt.timedelta(hours=3)
            ohlc: pd.DataFrame = pd.DataFrame(mt5.copy_rates_range(ticker, timeframe,
                                                init_date, final_date)).ffill()
        else:
            ohlc: pd.DataFrame = pd.DataFrame(mt5.copy_rates_from_pos(ticker, timeframe, 
                                                        tillbar, bars)).ffill()
                                                
        if not ohlc.empty:
            ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
            ohlc.drop(['real_volume'], axis=1, inplace=True)    
            ohlc.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close',
                'time':'DateTime','tick_volume':'Volume','spread':'Spread'}, inplace=True)
        else:
            print(f'No data for {ticker}!')

        return ohlc
    
    def checkExecution(self, result=None) -> bool:
        '''
        Chequea la ejecucion de la orden de compra o venta
        '''

        if result == None:
            result = self.result

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.executioncheck = True
            return self.executioncheck
            #print("- Orden no enviada, retcode={}".format(result.retcode))
            #quit()
        else:
            self.executioncheck = False
            return self.executioncheck
            #print("- Orden enviada, ", result)
            #print("- Posicion abierta con ticket: {}".format(result.order))
            
    def checkOrder(self,search:str,datatype:str='ticket') -> pd.DataFrame:

        if datatype == 'ticket':
            # Buscamos la orden por el ticket
            orders = mt5.orders_get(ticket=search)
            self.orders_df = pd.DataFrame(list(orders),columns=list(orders)[0]._asdict().keys())

        elif datatype == 'ticker':
            # Buscamos las ordenes por el par
            orders = mt5.orders_get(symbol=search)
            self.orders_df = pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())

        elif datatype == 'currency':
            # Buscamos las ordenes por divisa en el par
            orders = mt5.orders_get(group='*'+search+'*')
            self.orders_df = pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())

        return self.orders_df

    def modifyPosition(self, ticket:str, new_sl:float, new_tp:float, 
                        deviation:int=10, comment:str='Position modified using Python') -> None:

        request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": ticket,
        "sl": new_sl,
        "tp": new_tp,
        "deviation": deviation,
        "magic": 20031999,
        "comment": comment,
        }
    
        self.result = mt5.order_check(request)
        
    def estimateProfit(self, ticker:str, size:float, price_movement:float) -> None:
        '''
        Estima lo que creemos que vamos a ganar con una cierta posicion
        en funcion del recorrido que esperamos de la posicion
        '''
        if '_' in ticker:
            ticker = ticker.replace('_','')
        elif '/' in ticker:
            ticker = ticker.replace('/','')
        # Importamos la moneda que usamos
        account_currency = mt5.account_info().currency
        # arrange the symbol list
        symbols: str = ticker
        # estimate profit for buying and selling
        for symbol in symbols:
            point = mt5.symbol_info(symbol).point
            symbol_tick = mt5.symbol_info_tick(symbol)
            
            ask = symbol_tick.ask
            buy_profit = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY,symbol,size,ask,ask+price_movement*point)
            print(f"   Comprar {size} lotes de {symbol}: el beneficio para {price_movement} puntos => {buy_profit} {account_currency}")
            
            bid = symbol_tick.bid
            sell_profit = mt5.order_calc_profit(mt5.ORDER_TYPE_SELL,symbol,size,bid,bid-price_movement*point)
            print(f"   Vender {size} lotes de {symbol}: el beneficio para {price_movement} puntos => {sell_profit} {account_currency}")
            
            print()


'''
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

def your_function(a):
    return a * 2

if __name__ == "__main__": # This is important, so that forked process doesn't start this all over again
    with Pool() as pool:
        results = []

        for i in range(10):
            async_result = pool.apply_async(your_function, (i,))
            results.append(async_result)

        results = [r.get() for r in results]
        print(results)
'''


if __name__ == '__main__':

    traded_symbols = ['USDCHF', 'EURUSD', 'USDJPY', 'NZDUSD', 'GBPCHF', 'GBPJPY', 'USDCAD', 'EURAUD']
    traded_symbols = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 
                    'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 
                    'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 
                    'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY']
    intraday = False

    mt5con = Mt5Connect(7094662,'Onemade3680','ICMarketsSC-MT5-2')#5255861,'onemade3680','ICMarketsSC-MT5')

    # Descargar datos intradía de la sesion
    date = '2022-08-24'#'2020-01-01'
    final = '2022-09-27'#'2022-09-08'

    if intraday:
        date = dt.datetime.strptime(date + ' 00:00', '%Y-%m-%d %H:%M')
        final = dt.datetime.strptime(final, '%Y-%m-%d')

        utc_tz = pytz.timezone('UTC')
        mad_tz = pytz.timezone('Europe/Madrid')

        while date < final:

            # get an 'offset-aware' datetime
            utc_date = utc_tz.localize(date)
            from_date = utc_date.astimezone(mad_tz)
            to_date = dt.datetime.strptime(dt.datetime.strftime(date, '%Y-%m-%d') + ' 23:59', '%Y-%m-%d %H:%M')
            utc_date = utc_tz.localize(to_date)
            to_date = utc_date.astimezone(mad_tz)

            for t in traded_symbols:

                if not os.path.exists(os.path.join('Tickers',t)):
                    os.mkdir(os.path.join('Tickers',t))

                if os.path.exists(os.path.join(os.path.abspath(os.getcwd()),'Tickers',t,dt.datetime.strftime(date, '%Y%m%d')+'.csv')):
                    continue

                ohlc = mt5con.get_candles(t, mt5.TIMEFRAME_M1, 
                                        from_date,
                                        to_date)

                if ohlc.empty:
                    continue

                # Store data
                path = os.path.join(os.path.abspath(os.getcwd()),'Tickers',t,dt.datetime.strftime(date, '%Y%m%d')+'.csv')
                header = not os.path.isfile(path)
                ohlc.to_csv(path, mode='a', header=header)

            date = date + dt.timedelta(days=1)
        
    else:
        date = dt.datetime.strptime(date + ' 00:00', '%Y-%m-%d %H:%M')
        final = dt.datetime.strptime(final + ' 00:00', '%Y-%m-%d %H:%M')
        
        # get an 'offset-aware' datetime
        from_date = pytz.timezone('UTC').localize(date)
        to_date = pytz.timezone('UTC').localize(final)

        for t in traded_symbols:
            ohlc = mt5con.get_candles(t, mt5.TIMEFRAME_D1, 
                                    from_date,
                                    to_date)
                                    
            if ohlc.empty:
                print(f'{t} ohlc is empty')
                continue
            #ohlc = acr(ohlc,n=20,dataname='ATR')


            # Store data
            if not os.path.exists(os.path.join('Tickers',t)):
                os.mkdir(os.path.join('Tickers',t))
            
            path = os.path.join(os.path.abspath(os.getcwd()),'Tickers',t,'daily.csv')
            if os.path.isfile(path):
                ohlc.to_csv(path, mode='a', header=False)

            else:
                ohlc.to_csv(path, mode='w', header=True)


            '''
            # Store data
            if not os.path.exists('Daily'):
                os.mkdir(t)
            
            path = os.path.join(os.path.abspath(os.getcwd()),'Daily',t+'.csv')
            if os.path.isfile(path):
                ohlc.to_csv(path, mode='a', header=False)

            else:
                ohlc.to_csv(path, mode='w', header=True)
            '''
