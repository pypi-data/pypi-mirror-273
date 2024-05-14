
import datetime as dt
import time

import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import pytz


def debug_print(level:int=0,text:list=['Done'],printlevel:int=0):

    '''
    Funcion para imprimir mensaje de debug cuando el nivel de debug es inferior al asignado al print
    0: trace
    1: debug
    2: warning
    3: error
    4: critical
    5: alert
    '''

    # Vemos el mensaje a escribir
    if level == 0:
        message = '[trace]'
    elif level == 1:
        message = '[debug]'
    elif level == 2:
        message = '[warning]'
    elif level == 3:
        message = '[error]'
    elif level == 4:
        message = '[critical]'
    elif level == 5:
        message = '[alert]'
    
    # Imprimimos el mensaje y el nivel solo cuando el print está por encima del nivel pedido
    if level <= printlevel:
        for t in text:
            print(message,t)


class Mt5Connect():

    def __init__(self, user:int=50924546, password:str='CbIDQI9F', server:str='ICMarketsSC-Demo'):

        mt5.initialize()

        self.user = user
        self.password = password
        self.server = server
        authorized = mt5.login(user, password, server)

        if authorized:
            print('Connected: Connecting to MT5 Client')
        else:
            print(f"Failed to connect at account #{user}, error code: {mt5.last_error()}")

    def get_info(self):

        self.account_info = mt5.account_info()._asdict()
        
        return self.account_info

    def get_history_deals(self,date_from=None,date_to=None):
        
        date_to = dt.datetime.today() if date_to == None else date_to
        date_from = date_to-dt.timedelta(days=1) if date_from == None else date_from
        history = mt5.history_deals_get(date_from,date_to)
        
        if len(history) > 0:
            df = pd.DataFrame(list(history),columns=history[0]._asdict().keys())
            
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df['time_msc'] = pd.to_datetime(df['time_msc'], unit='ms')
            df['type'] = np.where(df['type'] == 0, 'Buy', 'Sell')
            df['entry'] = np.where(df['entry'] == 0, 'Entry', 'Exit')
            df['day'] = df['time'].apply(lambda x: x.day)
        else:
            df = pd.DataFrame()

        return df

    def get_history_orders(self,date_from=None,date_to=None):
        
        date_to = dt.datetime.today() if date_to == None else date_to
        date_from = date_to-dt.timedelta(days=1) if date_from == None else date_from
        history = mt5.history_orders_get(date_from,date_to)
        
        if len(history) > 0:
            df = pd.DataFrame(list(history),columns=history[0]._asdict().keys())
        
            df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
            df['time_setup_msc'] = pd.to_datetime(df['time_setup_msc'], unit='ms')
            df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
            df['time_done_msc'] = pd.to_datetime(df['time_done_msc'], unit='ms')
            df['type'] = np.where(df['type'] == 0, 'Buy', 'Sell')
            df['day'] = df['time_setup'].apply(lambda x: x.day)
        else:
            df = pd.DataFrame()

        return df

    def symbolInfo(self,pair:str):
        
        return mt5.symbol_info(pair)._asdict()

    def open_position(self, pair:str, order_type:str, risk:float, sl_pct:float=None, tp_pct:float=None):

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

        point = symbol_info.point
        
        tp = False
        if(order_type == 'BUY'):
            order = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(pair).ask
            if(sl_pct):
                sl = price * (1 - sl_pct)
                print(price,sl_pct,sl)
            if(tp_pct):
                tp = price * (1 + tp_pct)
                
        if(order_type == 'SELL'):
            order = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(pair).bid
            if(sl_pct):
                sl = price * (1 + sl_pct)
            if(tp_pct):
                tp = price * (1 - tp_pct)

        size = (risk * float(account_info['balance']) / ((float(price) * sl_pct) / symbol_info.point)) * 100//1/100
        if size < symbol_info.volume_min:
            size = symbol_info.volume_min
        elif size > symbol_info.volume_max:
            size = symbol_info.volume_max 

        digits = mt5.symbol_info(pair).digits
        
        request = {
            'action': mt5.TRADE_ACTION_DEAL,
            'symbol': pair,
            'volume': float(size),
            'type': order,
            'price': round(price,digits),
            'sl': round(sl,digits),
            'magic': 20031999,
            'comment': 'FXGap',
            'type_time': mt5.ORDER_TIME_GTC,
            'type_filling': mt5.ORDER_FILLING_IOC,
        }

        if tp:
            request['tp'] = tp
        
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print('Failed to send order: ', result)
            return False
        else:
            print ('Order successfully placed!')
        
        return True

    def positions_get(self, symbol=None):

        if(symbol is None):
            res = mt5.positions_get()
        else:
            res = mt5.positions_get(symbol=symbol)

        if(res is not None and res != ()):
            df = pd.DataFrame(list(res),columns=res[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        
        return pd.DataFrame()

    def close_positions(self, deal_id=None, deviation:int=10):

        open_positions = self.positions_get()
        if deal_id:
            open_positions = open_positions[open_positions['ticket'] == deal_id]
            
        close_data = []
        for i in range(len(open_positions)):
            
            deal_id = int(open_positions['ticket'][i])
            order_type  = open_positions['type'][i]
            symbol = open_positions['symbol'][i]
            volume = float(open_positions['volume'][i])
            if(order_type == mt5.ORDER_TYPE_BUY):
                mt5_order_type = mt5.ORDER_TYPE_SELL
                price = mt5.symbol_info_tick(symbol).bid
            else:
                mt5_order_type = mt5.ORDER_TYPE_BUY
                price = mt5.symbol_info_tick(symbol).ask

            close_request={
                'action': mt5.TRADE_ACTION_DEAL,
                'symbol': symbol,
                'volume': volume,
                'type': mt5_order_type,
                'position': deal_id,
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
            account_info = self.get_info()
            close_data_symbol = {
                'ID': deal_id,
                'Ticker': symbol,
                'Type': order_type,
                'Size': volume,
                'Entry': open_positions['price_open'][i],
                'Exit': price,
                'SL': open_positions['sl'][i],
                'TP': open_positions['tp'][i],
                'Profit': open_positions['profit'][i],
                'Date': open_positions['time'][i],
                'Balance': float(account_info['balance'])
            }

            close_data.append(close_data_symbol)

        return close_data

    def close_positons_by_symbol(self, symbol):

        open_positions = self.positions_get(symbol)
        open_positions['ticket'].apply(lambda x: self.close_positions(x))

    def get_candles(self,ticker:str,timeframe=mt5.TIMEFRAME_D1,
                    init_date:dt.datetime=None,
                    final_date:dt.datetime=None,limit:int=1000) -> pd.DataFrame:
        
        if init_date == None:

            if final_date == None:
                final_date = dt.datetime.now()
            ohlc = pd.DataFrame(mt5.copy_rates_from(ticker, timeframe, 
                                                    final_date, limit))
            
        elif final_date == None:
            final_date = dt.datetime.now()
            ohlc = pd.DataFrame(mt5.copy_rates_range(ticker, timeframe,
                                                    init_date, final_date))

        if not ohlc.empty:
            ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
            ohlc = ohlc.drop(['real_volume'],axis=1)    
            ohlc = ohlc.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close',\
                'time':'DateTime','tick_volume':'Volume','spread':'Spread'})

        return ohlc

class TechnicalAnalysis:

    '''
    Class incharged of calculating channels, trendlines and support and resistance levels.
    '''

    new_minmax = False
    old_minmax = {}
    minmax = []
    u_trendlines = {}
    d_trendlines = {}
    u_channels = {}
    d_channels = {}
    

    def __init__(self,debug_level:int=5): #,ohlc_df,tf:str='M5'
        #self.ohlc_df = ohlc_df
        self.debug_level = debug_level
        
        self.mt5con = Mt5Connect(7094662,'Onemade3680','ICMarketsSC-MT5-2')#5255861,'onemade3680','ICMarketsSC-MT5')
        #self.tf = tf
        
    # Funcion para ver si hay nuevos extremos
    def check_minmax(self,pa_type:str='channel',maxdatatype='High',mindatatype='Low',frac_l=5,frac_r=5):

        if 0 in self.minmax:
            minmax = [i for i in self.minmax if i != 0]
        else:
            minmax = self.minmax
        # minmax = self.fractal(left_n=frac_l,right_n=frac_r,maxdatatype=maxdatatype,mindatatype=mindatatype,formatreturn='list',separate=False,zeros=False)

        if self.old_minmax[self.tf][self.ticker][pa_type] == minmax:
            debug_print(level=self.debug_level,text=['Hemos checkeado los minmax y dan iguales'],printlevel=0)
            self.new_minmax = False
        else:
            debug_print(level=self.debug_level,text=['Hemos checkeado los minmax no dan iguales',self.old_minmax[self.tf][self.ticker][pa_type],minmax],printlevel=0)
            self.new_minmax = True
            self.old_minmax[self.tf][self.ticker][pa_type] = minmax

    # Funcion para importar los datos
    def data(self,df:pd.DataFrame=None,tf=mt5.TIMEFRAME_M1,ticker:str='USDCHF',n:int=2000):
        
        # Guardamos los tf en los diccionarios
        self.tf = tf
        self.old_minmax[self.tf] = {} if self.tf not in self.old_minmax.keys() else self.old_minmax[self.tf]
        self.u_trendlines[self.tf] = {} if self.tf not in self.u_trendlines.keys() else self.u_trendlines[self.tf]
        self.d_trendlines[self.tf] = {} if self.tf not in self.d_trendlines.keys() else self.d_trendlines[self.tf]
        self.u_channels[self.tf] = {} if self.tf not in self.u_channels.keys() else self.u_channels[self.tf]
        self.d_channels[self.tf] = {} if self.tf not in self.d_channels.keys() else self.d_channels[self.tf]
        # Guardamos los tickers en los diccionarios
        self.ticker = ticker
        self.old_minmax[self.tf][self.ticker] = {'channel':[],'trendline':[]} if self.ticker not in self.old_minmax[self.tf].keys() else self.old_minmax[self.tf][self.ticker]
        self.u_trendlines[self.tf][self.ticker] = [] if self.ticker not in self.u_trendlines[self.tf].keys() else self.u_trendlines[self.tf][self.ticker]
        self.d_trendlines[self.tf][self.ticker] = [] if self.ticker not in self.d_trendlines[self.tf].keys() else self.d_trendlines[self.tf][self.ticker]
        self.u_channels[self.tf][self.ticker] = [] if self.ticker not in self.u_channels[self.tf].keys() else self.u_channels[self.tf][self.ticker]
        self.d_channels[self.tf][self.ticker] = [] if self.ticker not in self.d_channels[self.tf].keys() else self.d_channels[self.tf][self.ticker]

        if not isinstance(df,pd.DataFrame):
            temp = ''
            while not isinstance(temp,pd.DataFrame):
                try:
                    
                    utc_tz = pytz.timezone('UTC')
                    mad_tz = pytz.timezone('Europe/Madrid')
                    utc_date = utc_tz.localize(dt.datetime.now())
                    to_date = utc_date.astimezone(mad_tz) + dt.timedelta(hours=1)
                    to_date = dt.datetime.strptime(
                            dt.datetime.strftime(to_date,'%Y-%m-%d %H:%M:%S'),
                            '%Y-%m-%d %H:%M:%S')
                    temp = self.mt5con.get_candles(ticker,tf, final_date=to_date, limit=n)
                except Exception as e:
                    debug_print(level=self.debug_level,text=['TF:'+str(tf)+' Ticker:'+ticker],printlevel=0)
                    debug_print(level=self.debug_level,text=[e],printlevel=0)
                    time.sleep(50)
                    continue

            self.ohlc_df = temp

        else:
            self.ohlc_df = df

        self.point =  6-len(str(int(self.ohlc_df['Close'].tolist()[1])))

    # Funcion que calcula el ATR
    def atr(self,n:int=20,mode='s',dataname:str='ATR',tr:bool=False):
        ''' 
        Funcion para calcular el ATR en modo simple o exponencial
        '''

        # Definimos variables y calculos necesarios para el TR
        df = self.ohlc_df.copy()
        df['H-L'] = abs(df['High']-df['Low'])
        df['H-PC'] = abs(df['High']-df['Close'].shift(1))
        df['L-PC'] = abs(df['Low']-df['Close'].shift(1))

        # Hallamos el máximo para obtener el TR
        df[dataname+'TR'] = df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)

        # Calculamos la media del TR según el modo (s=simple o e=exponencial)
        if mode == 's':
            df[dataname] = df[dataname+'TR'].rolling(n).mean()
        elif mode == 'e':
            df[dataname] = df[dataname+'TR'].ewm(span=n,adjust=False,min_periods=n).mean()
        else:
            df[dataname] = df[dataname+'TR'].rolling(n).mean()

        # Eliminamos del DataFrame del precio todos los datos que no sean el ATR o TR
        if tr:
            df = df.drop(['H-L','H-PC','L-PC'],axis=1)
        else:
            df = df.drop(['H-L','H-PC','L-PC',dataname+'TR'],axis=1)

        self.ohlc_df = df

        return self.ohlc_df

    # Fractals indicator
    def fractal(self,left_n:int=5,right_n:int=5,maxdatatype='High',mindatatype='Low',formatreturn='dataframe',separate:bool=False,zeros:bool=False,data=None):

        '''
        Function for obtaining turning points in timeseries with a minimun porcentage change
        '''
        
        if not isinstance(data,pd.DataFrame):
            data = self.ohlc_df
            
        # Definimos variables
        max_data = data[maxdatatype].tolist()
        min_data = data[mindatatype].tolist()
        minmax = [0]*len(max_data)
        mini = [0]*len(min_data)
        maxi = [0]*len(max_data)

        # Si el precio está por encima de los left_n y right_n ultimos precios es maximo
        # Si el precio está por debajo de los left_n y right_n ultimos precios es minimo
        for i in range(left_n+1,len(max_data)-right_n):

            #if i>left_n:
            if all(j<=max_data[i] for j in max_data[i-left_n:i]) and all(j<max_data[i] for j in max_data[i+1:i+right_n+1]):
                minmax[i] = max_data[i]
                maxi[i] = max_data[i]
            elif all(j>=min_data[i] for j in min_data[i-left_n:i]) and all(j>min_data[i] for j in min_data[i+1:i+right_n+1]):
                minmax[i] = min_data[i]
                mini[i] = min_data[i]
            
        self.minmax = minmax
        if formatreturn == 'dataframe':
            # Formamos el DataFrame
            minmax_frame = pd.DataFrame(minmax,columns=['MinMax'])
            if not zeros:
                self.minmax_frame = minmax_frame[minmax_frame.values.sum(axis=1) != 0]
            
            return self.minmax_frame
        
        else:
            if not zeros:
                # Si queremos los datos como lista
                self.minmax = [i for i in self.minmax if i != 0]
                maxi = [i for i in maxi if i != 0]
                mini = [i for i in mini if i != 0]

            if separate:
                return self.minmax,maxi,mini
            else:
                return self.minmax

    # Support and resistance
    def suportresistance(self,n:int=4,prox:float=0.0001,atr:bool=True,t_max:int=10,t_min:int=2,datatype='Close',plot:bool=False,pivottype='Smooth',frac_l:int=5,frac_r:int=5):
        '''
        Función que nos devuelve un dataframe con las resistencias y soportes en nuestro
        periodo de tiempo. Nos dará más o menos valores en función del rango del rebote 't'
        (condicion del bucle if de la condición para contar en funcion del rango de proximidad 
        'prox') y del decimal de redondeo 'n'. Sería conveniente optimizar dichos parámetros 
        para cada timeframe por las logitudes de movimientos.
        '''

        indice = self.ohlc_df.index
        minmax,mini,maxi = self.fractal(left_n=frac_l,right_n=frac_r,formatreturn='list',separate=True)
        atr_df = self.atr()
        atr_list = atr_df['ATR'].tolist()
        
        supres = []
        points = []
        for i in range(len(minmax)-1):
            if minmax[i] != 0 and minmax[i] not in points:
                c = 1
                average = [minmax[i]]
                points.append(minmax[i])
                for x in range(len(minmax)-1):
                    if atr and minmax[x] >= minmax[i]-atr_list[i] and minmax[x] <= minmax[i]+atr_list[i]:
                        average.append(minmax[x])
                        points.append(minmax[x])
                        c += 1
                    elif not atr and minmax[x] >= minmax[i]*(1-prox) and minmax[x] <= minmax[i]*(1+prox):
                        average.append(minmax[x])
                        points.append(minmax[x])
                        c += 1

                if t_max>c and c>t_min:
                    supres.append(np.sum(average)/c)

        n = n+1-len(str(int(minmax[1])))
        supres = [round(i,n) for i in supres if i != 0]
        # Eliminamos los valores duplicados convirtiendo la lista a diccionario y viceversa.
        supres = list(dict.fromkeys(supres))
        # Añadimos el máximo y el mínimo a las resistencias y soportes.
        supres.append(min(minmax))
        supres.append(max(minmax))

        self.sup = []
        self.res = []
        if plot:

            for sr in supres:
                if self.ohlc_df[datatype].tolist()[-1] > sr:
                    self.sup.append(sr)
                else:
                    self.res.append(sr)
            
            supres = [supres]*len(self.ohlc_df[datatype])
            self.supres_df = pd.DataFrame(supres)
            self.supres_df.index = indice

            return self.supres_df, self.sup, self.res

        else:

            for sr in supres:
                if self.ohlc_df[datatype].tolist()[-1] > sr:
                    self.sup.append(sr)
                else:
                    self.res.append(sr)
            
            return self.sup, self.res

    # Funcion que calcula la pendiente y el corte con el eje y en funcion de dos puntos
    def lineFunction(self,y1,y0,x1,x0):
        '''
        Function to get m and n of a line based on two points
        '''

        m = (float(y1) - float(y0))/(float(x1) - float(x0))
        n = float(y0) - m*float(x0)
        return m,n

    # Trendline
    def trendline(self,trendtype='u',window:int=0,maxdatatype='High',mindatatype='Low',result='list',pivottype='Smooth',frac_l:int=5,frac_r:int=5,cross='minmax'):

        '''
        Function to get a trendline for a determined time period (window)
        :window: Must be int. Number of candles used for calculation.
        :trendtype: Can be 'u' (Up) or 'd' (Down)
        :maxdatatype: Data from ohlc to use for the highs of a downwards trendline
        :mindatatype: Data from ohlc to use for the lows of the upwards trendline
        '''

        if window != 0:
            ohlc_df_window = self.ohlc_df[-window:].copy()
        else:
            ohlc_df_window = self.ohlc_df
            
        minmax,maxi_price,mini_price = self.fractal(left_n=frac_l,right_n=frac_r,maxdatatype=maxdatatype,mindatatype=mindatatype,formatreturn='list',separate=True,zeros=True,data=ohlc_df_window)
        maxi = [i for i in maxi_price if i != 0]
        mini = [i for i in mini_price if i != 0]
        closeprice = ohlc_df_window['Close'].tolist()
        trendline_dict = {'m':0,'n':0,'last_x':0,'trendline':'No hay trendlines','min':[],'max':[],'minmax':[]}
        point = 6-len(str(int(self.ohlc_df['Close'].tolist()[1])))

        if trendtype in ['d','D','down','DOWN','Down']:

            maxprice = ohlc_df_window[maxdatatype].tolist()
            try:
                all_max = max(maxi)
            except:
                return trendline_dict

            # all_max_index = len(maxi)-maxi[::-1].index(all_max)-1
            all_max_index = 0
            for i in range(1,len(maxi)):
               if all_max == maxi[-i]:
                    all_max_index = len(maxi)-i
                    break

            # all_max_price_index = len(maxprice)-maxprice[::-1].index(all_max)-1
            all_max_price_index = 0
            for i in range(1,len(maxprice)):
                if all_max == maxprice[-i]:
                    all_max_price_index = len(maxprice)-i
                    break
            
            for p in range(all_max_index+1,len(maxi)):
                
                # new_max_price_index = len(maxprice)-maxprice[::-1].index(maxi[p])-1
                new_max_price_index = 0
                for i in range(1,len(maxprice)):
                    if maxi[p] == maxprice[-i]:
                        new_max_price_index = len(maxprice)-i
                        break
                    
                if new_max_price_index-all_max_price_index == 0:
                    continue
                else:
                    m, n = self.lineFunction(y1=maxi[p], y0=all_max, x1=new_max_price_index, x0=all_max_price_index)
                debug_print(level=self.debug_level,text=['M,N: '+str(m)+' '+str(n),' '+str(maxi[p])+' '+str(new_max_price_index)+' '+str(all_max)+' '+str(all_max_price_index)],printlevel=3)

                price_cross = False
                trendline = []
                for x in range(all_max_price_index, len(maxprice)):
                    trendline.append(round(m*x+n,point))
                    if cross in ['minmax','MinMax','MINMAX','Minmax','MM','mm']:
                        if maxi_price[x] != 0 and trendline[-1]-maxi_price[x] < 0:
                            price_cross = True
                            break  
                    elif cross in ['Close','close','CLOSE']:
                        if trendline[-1]-closeprice[x] < 0:
                            price_cross = True
                            break  
                    elif cross in ['High','high','HIGH','Low','low','LOW']:
                        if trendline[-1]-ohlc_df_window['High'].tolist()[x] < 0:
                            price_cross = True
                            break  
                debug_print(level=self.debug_level,text=['TL canceled: '+str(price_cross),str(trendline[-1])+' '+str(trendline[-1]-maxi_price[x])],printlevel=3)

                if not price_cross:
                    trendline_dict = {'m':m,'n':n,'last_x':all_max_price_index+len(trendline)-1,'trendline':trendline,
                                    'min':mini,'max':maxi,'minmax':minmax}
                    if result not in ['list','List','LIST']:
                        trendline_df = pd.DataFrame(trendline,columns=['tl'])
                        trendline_df.index = self.ohlc_df.index[-len(trendline):]
                        trendline_dict['trendline'] = trendline_df
                        return trendline_dict
                    else:
                        return trendline_dict
    
        elif trendtype in ['u','U','UP','up','Up']:
            
            minprice = ohlc_df_window[mindatatype].tolist()
            try:
                all_min = min(mini)
            except:
                return trendline_dict

            # all_min_index = len(mini)-mini[::-1].index(all_min)-1
            all_min_index = 0 #len(mini)-mini[::-1].index(all_min)
            for i in range(1,len(mini)):
                if all_min == mini[-i]:
                    all_min_index = len(mini)-i
                    break

            # all_min_price_index = len(minprice)-minprice[::-1].index(all_min)-1
            all_min_price_index = 0
            for i in range(1,len(minprice)):
                if all_min == minprice[-i]:
                    all_min_price_index = len(minprice)-i
                    break
            
            for p in range(all_min_index+1,len(mini)):

                # new_min_price_index = len(minprice)-minprice[::-1].index(mini[p])-1
                new_min_price_index = 0
                for i in range(1,len(minprice)):
                    if mini[p] == minprice[-i]:
                        new_min_price_index = len(minprice)-i
                        break

                if new_min_price_index-all_min_price_index == 0:
                    continue
                else:
                    m, n = self.lineFunction(y1=mini[p], y0=all_min, x1=new_min_price_index, x0=all_min_price_index)
                debug_print(level=self.debug_level,text=['M,N: '+str(m)+' '+str(n),' '+str(mini[p])+' '+str(new_min_price_index)+' '+str(all_min)+' '+str(all_min_price_index)],printlevel=3)

                price_cross = False
                trendline = []
                for x in range(all_min_price_index, len(minprice)):
                    trendline.append(round(m*x+n,point))
                    if cross in ['minmax','MinMax','MINMAX','Minmax','MM','mm']:
                        if mini_price[x] != 0 and trendline[-1]-mini_price[x] > 0:
                            price_cross = True
                            break  
                    elif cross in ['Close','close','CLOSE']:
                        if trendline[-1]-closeprice[x] > 0:
                            price_cross = True
                            break  
                    elif cross in ['High','high','HIGH','Low','low','LOW']:
                        if trendline[-1]-ohlc_df_window['Low'].tolist()[x] > 0:
                            price_cross = True
                            break  
                    if trendline[-1]-closeprice[x] > 0:
                        price_cross = True
                        break

                debug_print(level=self.debug_level,text=['TL canceled: '+str(price_cross),str(trendline[-1])+' '+str(mini_price[x]-trendline[-1])],printlevel=3)
                if not price_cross:
                    trendline_dict = {'m':m,'n':n,'last_x':all_min_price_index+len(trendline)-1,'trendline':trendline,
                                    'min':mini,'max':maxi,'minmax':minmax}
                    if result not in ['list','List','LIST']:
                        trendline_df = pd.DataFrame(trendline,columns=['tl'])
                        trendline_df.index = self.ohlc_df.index[-len(trendline):]
                        trendline_dict['trendline'] = trendline_df
                        return trendline_dict
                    else:
                        return trendline_dict
        
        return trendline_dict

    # All the trendlines
    def all_trendlines(self,maxdatatype='High',mindatatype='Low',result='list',plot:bool=False,frac_l:int=5,frac_r:int=5):
        
        self.check_minmax(pa_type='trendline',maxdatatype=maxdatatype,mindatatype=mindatatype,frac_l=frac_l,frac_r=frac_r)
        #if not self.new_minmax:
        #    done = self.redraw(pa_type='trendline')
        #    if done:
        #        return self.u_trendlines[self.tf][self.ticker],self.d_trendlines[self.tf][self.ticker]

        minmax,maxi,mini = self.fractal(left_n=frac_l,right_n=frac_r,maxdatatype=maxdatatype,mindatatype=mindatatype,formatreturn='list',separate=True,zeros=False)

        all_min = min(mini)
        # Buscamos el indice del minimo en la lista minmax
        min_index = 0
        for i in range(1,len(mini)):
            if all_min == mini[-i]:
                min_index = len(mini)-i
                break

        # Calculamos las trendlines para los sucesivos minimos
        self.u_trendlines[self.tf][self.ticker] = []
        last_min_index = len(self.ohlc_df[mindatatype].tolist())
        for i in range(min_index,len(mini)):
            # Buscamos el indice del minimo en el precio
            for j in range(1,len(self.ohlc_df[mindatatype])):
                if mini[i] == self.ohlc_df[mindatatype].tolist()[-j]:
                    last_min_index = j
                    break
            
            if plot:
                self.u_trendlines[self.tf][self.ticker].append(self.trendline(trendtype='u',window=last_min_index,result='dataframe',frac_l=frac_l,frac_r=frac_r))
            else:
                self.u_trendlines[self.tf][self.ticker].append(self.trendline(trendtype='u',window=last_min_index,frac_l=frac_l,frac_r=frac_r))

        # Depuramos las trendlines para que no haya repetidas
        trends_n = []
        trends_m = []
        i = 0
        while i < len(self.u_trendlines[self.tf][self.ticker]):
            if self.u_trendlines[self.tf][self.ticker][i]['m'] in trends_m: # and self.u_trendlines[i]['n'] in trends_n:
                self.u_trendlines[self.tf][self.ticker].pop(i)
            else:
                trends_n.append(self.u_trendlines[self.tf][self.ticker][i]['n'])
                trends_m.append(self.u_trendlines[self.tf][self.ticker][i]['m'])
                i += 1

        all_max = max(maxi)
        # Buscamos el indice del maximo en la lista minmax
        max_index = 0
        for i in range(1,len(maxi)):
            if all_max == maxi[-i]:
                max_index = len(maxi)-i
                break
        
        # Calculamos las trendlines para los sucesivos maximos
        self.d_trendlines[self.tf][self.ticker] = []
        last_max_index = len(self.ohlc_df[maxdatatype].tolist())
        for i in range(max_index,len(maxi)):
            # Buscamos el indice del maximo en el precio
            for j in range(1,len(self.ohlc_df[maxdatatype])):
                if maxi[i] == self.ohlc_df[maxdatatype].tolist()[-j]:
                    last_max_index = j
                    break
            
            if plot:
                self.d_trendlines[self.tf][self.ticker].append(self.trendline(trendtype='d',window=last_max_index,result='dataframe',frac_l=frac_l,frac_r=frac_r))
            else:            
                self.d_trendlines[self.tf][self.ticker].append(self.trendline(trendtype='d',window=last_max_index,frac_l=frac_l,frac_r=frac_r))

        # Depuramos las trendlines para que no haya repetidas
        trends_n = []
        trends_m = []
        i = 0
        while i < len(self.d_trendlines[self.tf][self.ticker]):
            if self.d_trendlines[self.tf][self.ticker][i]['m'] in trends_m: # and self.d_trendlines[i]['n'] in trends_n:
                self.d_trendlines[self.tf][self.ticker].pop(i)
            else:
                trends_n.append(self.d_trendlines[self.tf][self.ticker][i]['n'])
                trends_m.append(self.d_trendlines[self.tf][self.ticker][i]['m'])
                i += 1

        return self.u_trendlines[self.tf][self.ticker],self.d_trendlines[self.tf][self.ticker]

    # Channels
    def channel(self,window:int=900,trendtype='u',maxdatatype='High',mindatatype='Low',difdatatype='minmax',result='list',frac_l=5,frac_r=5,mlimit:float=0.1,use_inverse:bool=True):

        if difdatatype in ['Close','close','CLOSE']:
            price = self.ohlc_df['Close'].tolist()
        elif difdatatype in ['open','Open','OPEN']:
            price = self.ohlc_df['Open'].tolist()
        elif difdatatype in ['High','high','HIGH']:
            price = self.ohlc_df['High'].tolist()
        elif difdatatype in ['Low','low','LOW']:
            price = self.ohlc_df['Low'].tolist()

        if trendtype in ['u','U','Up','up','UP']:
            # Up channel
            up_trendline = self.trendline(trendtype='u',window=window,maxdatatype=maxdatatype,mindatatype=mindatatype,result='list',frac_l=frac_l,frac_r=frac_r)
            debug_print(level=self.debug_level,text=['UTL:',up_trendline],printlevel=3)
            n = up_trendline['n']
            m = up_trendline['m']
            if m < mlimit and up_trendline['last_x'] != 0:
                if difdatatype in ['minmax','Minmmax','MinMax','minMax','mm','MM']:
                    minmax,maxi,mini = self.fractal(left_n=frac_l,right_n=frac_r,maxdatatype=maxdatatype,mindatatype=mindatatype,formatreturn='list',separate=True,zeros=True)
                    if use_inverse:
                        price = maxi
                    else:
                        price = mini 
                dif = []
                for i in range(1,len(up_trendline['trendline'])+1):
                    if price[-i] == 0:
                        dif.append(0)
                        continue
                    dif.append(price[-i]-up_trendline['trendline'][-i])
                
                try:
                    new_n = max(dif)+n
                except:
                    new_n = 0

                # Hallamos puntos de la trendline
                trendline = []
                for i in range(up_trendline['last_x']-len(dif)+1,up_trendline['last_x']+1):
                    trendline.append(m*i+new_n)

            else:
                trendline = []
                new_n = 0
                up_trendline['trendline'] = []

            u_channel = {'UpTrend':{'n':new_n,'m':m,'last_x':up_trendline['last_x'],'trendline':trendline},
                        'LowTrend':up_trendline,
                        'min':up_trendline['min'],'max':up_trendline['max'],'minmax':up_trendline['minmax']}
            del u_channel['LowTrend']['max']
            del u_channel['LowTrend']['min']
            del u_channel['LowTrend']['minmax']

            if result != 'list':
                # Cambiamos la trendline superior a df
                if len(trendline)>0:
                    trendline_df = pd.DataFrame(trendline,columns=['tl'])
                    trendline_df.index = self.ohlc_df.index[-len(trendline):]
                    u_channel['UpTrend']['trendline'] = trendline_df
                else:
                    u_channel['UpTrend']['trendline'] = pd.DataFrame(trendline,columns=['tl'])
                # Cambiamos la trendline inferior a df
                if len(up_trendline['trendline'])>0:
                    lower_trend = pd.DataFrame(up_trendline['trendline'],columns=['tl'])
                    lower_trend.index = self.ohlc_df.index[-len(up_trendline['trendline']):]
                    u_channel['LowTrend']['trendline'] = lower_trend
                else:
                    u_channel['LowTrend']['trendline'] = pd.DataFrame(up_trendline['trendline'],columns=['tl'])

            return u_channel

        elif trendtype in ['d','D','Down','down','DOWN']:
            # Down channel
            down_trendline = self.trendline(trendtype='d',window=window,maxdatatype=maxdatatype,mindatatype=mindatatype,result='list',frac_l=frac_l,frac_r=frac_r)
            debug_print(level=self.debug_level,text=['DTL:',down_trendline],printlevel=3)
            n = down_trendline['n']
            m = down_trendline['m']
            if m > -mlimit and down_trendline['last_x'] != 0:
                if difdatatype in ['minmax','Minmmax','MinMax','minMax','mm','MM']:
                    minmax,maxi,mini = self.fractal(left_n=frac_l,right_n=frac_r,maxdatatype=maxdatatype,mindatatype=mindatatype,formatreturn='list',separate=True,zeros=True)
                    if use_inverse:
                        price = mini
                    else:
                        price = maxi 
                dif = []
                for i in range(1,len(down_trendline['trendline'])):
                    if price[-i] == 0:
                        dif.append(0)
                        continue
                    dif.append(down_trendline['trendline'][-i]-price[-i])
                try:
                    new_n = n-max(dif)
                except:
                    new_n = 0
                
                # Hallamos puntos de la trendline
                trendline = []
                for i in range(down_trendline['last_x']-len(dif)+1,down_trendline['last_x']+1):
                    trendline.append(m*i+new_n)

            else:
                trendline = []
                new_n = 0
                down_trendline['trendline'] = []

            d_channel = {'UpTrend':down_trendline,
                        'LowTrend':{'n':new_n,'m':m,'last_x':down_trendline['last_x'],'trendline':trendline},
                        'min':down_trendline['min'],'max':down_trendline['max'],'minmax':down_trendline['minmax']}
            del d_channel['UpTrend']['max']
            del d_channel['UpTrend']['min']
            del d_channel['UpTrend']['minmax']

            if result != 'list':
                # Cambiamos la trendline superior a df
                if len(trendline)>0:
                    trendline_df = pd.DataFrame(trendline,columns=['tl'])
                    trendline_df.index = self.ohlc_df.index[-len(trendline):]
                    d_channel['LowTrend']['trendline'] = trendline_df
                else:
                    d_channel['LowTrend']['trendline'] = pd.DataFrame(trendline,columns=['tl'])
                # Cambiamos la trendline inferior a df
                if len(down_trendline['trendline']) > 0:
                    higher_trend = pd.DataFrame(down_trendline['trendline'],columns=['tl'])
                    higher_trend.index = self.ohlc_df.index[-len(down_trendline['trendline']):]
                    d_channel['UpTrend']['trendline'] = higher_trend
                else:
                    d_channel['UpTrend']['trendline'] = pd.DataFrame(down_trendline['trendline'],columns=['tl'])

            return d_channel

    # All the trendlines
    def all_channels(self,maxdatatype='High',mindatatype='Low',difdatatype='minmax',result='list',
                    plot:bool=False,frac_l:int=5,frac_r:int=5,mlimit:float=0.1,use_inverse:bool=True,
                    redraw:bool=False):
       
        if plot:
            result = 'dataframe'

        # Si no hay nuevos extremos para calcular nuevos 
        self.check_minmax(pa_type='channel',maxdatatype=maxdatatype,mindatatype=mindatatype,frac_l=frac_l,frac_r=frac_r)
        if not self.new_minmax and redraw:
            done = self.redraw(pa_type='channel')
            if done:
                return self.u_channels[self.tf][self.ticker],self.d_channels[self.tf][self.ticker]

        minmax,maxi,mini = self.fractal(left_n=frac_l,right_n=frac_r,maxdatatype=maxdatatype,mindatatype=mindatatype,formatreturn='list',separate=True)

        # Canales alcistas
        all_min = min(mini)
        # Buscamos el indice del minimo en la lista minmax
        min_index = 0
        for i in range(1,len(mini)):
            if all_min == mini[-i]:
                min_index = len(mini)-i
                break

        # Calculamos las trendlines para los sucesivos minimos
        self.u_channels[self.tf][self.ticker] = []
        last_min_index = len(self.ohlc_df[mindatatype].tolist())
        for i in range(min_index,len(mini)):
            # Buscamos el indice del minimo en el precio
            for j in range(1,len(self.ohlc_df[mindatatype])):
                if mini[i] == self.ohlc_df[mindatatype].tolist()[-j]:
                    last_min_index = j #len(self.ohlc_df[mindatatype])-j
                    break

            self.u_channels[self.tf][self.ticker].append(self.channel(window=last_min_index,trendtype='u',maxdatatype=maxdatatype,mindatatype=mindatatype,
                difdatatype=difdatatype,result=result,frac_l=frac_l,frac_r=frac_r,mlimit=mlimit,use_inverse=use_inverse))

        # Depuramos las trendlines para que no haya repetidas
        trends_n = []
        trends_m = []
        i = 0
        while i < len(self.u_channels[self.tf][self.ticker]):
            if self.u_channels[self.tf][self.ticker][i]['LowTrend']['m'] in trends_m: # and self.u_channels[i]['LowTrend']['n'] in trends_n:
                self.u_channels[self.tf][self.ticker].pop(i)
            else:
                trends_n.append(self.u_channels[self.tf][self.ticker][i]['LowTrend']['n'])
                trends_m.append(self.u_channels[self.tf][self.ticker][i]['LowTrend']['m'])
                i += 1

        # Canales bajistas
        all_max = max(maxi)
        # Buscamos el indice del maximo en la lista minmax
        max_index = 0
        for i in range(1,len(maxi)):
            if all_max == maxi[-i]:
                max_index = len(maxi)-i
                break
        
        # Calculamos las trendlines para los sucesivos maximos
        self.d_channels[self.tf][self.ticker] = []
        last_max_index = len(self.ohlc_df[maxdatatype].tolist())
        for i in range(max_index,len(maxi)):
            # Buscamos el indice del maximo en el precio
            for j in range(1,len(self.ohlc_df[maxdatatype])):
                if maxi[i] == self.ohlc_df[maxdatatype].tolist()[-j]:
                    last_max_index = j #len(self.ohlc_df[maxdatatype])-j
                    break

            self.d_channels[self.tf][self.ticker].append(self.channel(window=last_min_index,trendtype='d',maxdatatype=maxdatatype,mindatatype=mindatatype,
                difdatatype=difdatatype,result=result,frac_l=frac_l,frac_r=frac_r,mlimit=mlimit,use_inverse=use_inverse))

        # Depuramos las trendlines para que no haya repetidas
        trends_n = []
        trends_m = []
        i = 0
        while i < len(self.d_channels[self.tf][self.ticker]):
            if self.d_channels[self.tf][self.ticker][i]['UpTrend']['m'] in trends_m: # and self.d_channels[i]['UpTrend']['n'] in trends_n:
                self.d_channels[self.tf][self.ticker].pop(i)
            else:
                trends_n.append(self.d_channels[self.tf][self.ticker][i]['UpTrend']['n'])
                trends_m.append(self.d_channels[self.tf][self.ticker][i]['UpTrend']['m'])
                i += 1
        debug_print(level=self.debug_level,text=['U_CHANNELS:',self.u_channels],printlevel=3)
        debug_print(level=self.debug_level,text=['D_CHANNELS:',self.d_channels],printlevel=3)
        return self.u_channels[self.tf][self.ticker],self.d_channels[self.tf][self.ticker]




# Prueba de los indicadores, solo se ejecuta cuando el archivo se corre directamente
if __name__ == '__main__':

    import matplotlib.pyplot as plt
    graficamos = True
    candle = True
    minmax = True
    sr = True
    tl = False
    all_tl = False
    channels = False
    all_channels = True
    tf = mt5.TIMEFRAME_M1
    ticker = 'USDCHF'
    
    utc_tz = pytz.timezone('UTC')
    mad_tz = pytz.timezone('Europe/Madrid')
    utc_date = utc_tz.localize(dt.datetime.now())
    to_date = utc_date.astimezone(mad_tz) + dt.timedelta(hours=1)
    to_date = dt.datetime.strptime(
            dt.datetime.strftime(to_date,'%Y-%m-%d %H:%M:%S'),
            '%Y-%m-%d %H:%M:%S')
    mt5con = Mt5Connect(7094662,'Onemade3680','ICMarketsSC-MT5-2')#5255861,'onemade3680','ICMarketsSC-MT5')
    ohlcv = mt5con.get_candles(ticker, tf,final_date=to_date, limit=2000)

    ta = TechnicalAnalysis(debug_level=5)
    ta.data(tf=tf,ticker=ticker, n=2000)
    minmax = ta.fractal(left_n=10,right_n=10)
    supres,sup,res = ta.suportresistance(n=4,prox=0.0001,plot=True,pivottype='fractal',
                                        frac_l=10,frac_r=10)
    upc,downc = ta.all_channels(plot=True,frac_l=10,frac_r=10)
        

    plotly = True
    if plotly:
        
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        temp_df = ohlcv
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.0, row_heights=[5],
                                    specs=[[{'secondary_y': False}]])

        fig.add_trace(go.Candlestick(x=temp_df['DateTime'],open=temp_df['Open'],high=temp_df['High'],low=temp_df['Low'],close=temp_df['Close'], 
                                    name='Price'), row=1, col=1)

        # Imprimimos los puntos de giro
        fig.add_trace(go.Scatter(x=ohlcv.iloc[minmax.index]['DateTime'],y=minmax['MinMax'], name='Fractal', mode='markers', marker_color='gray'), row=1, col=1)

        # Imprimimos soportes y resistencias
        if sr:
            for col in supres.columns:
                fig.add_trace(go.Scatter(x=ohlcv.iloc[supres.index]['DateTime'],y=supres[col],
                                        line=dict(color='gray', width=0.75)), row=1, col=1)

        if all_channels:
            for tl in upc:
                if isinstance(tl['UpTrend']['trendline'],pd.DataFrame) and isinstance(tl['LowTrend']['trendline'],pd.DataFrame):
                    fig.add_trace(go.Scatter(x=ohlcv.iloc[tl['UpTrend']['trendline'].index]['DateTime'],y=tl['UpTrend']['trendline']['tl'],
                                            line=dict(color='green', width=2)), row=1, col=1)
                    fig.add_trace(go.Scatter(x=ohlcv.iloc[tl['LowTrend']['trendline'].index]['DateTime'],y=tl['LowTrend']['trendline']['tl'],marker_color='red'), row=1, col=1)

            for tl in downc:
                if isinstance(tl['UpTrend']['trendline'],pd.DataFrame) and isinstance(tl['LowTrend']['trendline'],pd.DataFrame):
                    fig.add_trace(go.Scatter(x=ohlcv.iloc[tl['UpTrend']['trendline'].index]['DateTime'],y=tl['UpTrend']['trendline']['tl'],marker_color='green'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=ohlcv.iloc[tl['LowTrend']['trendline'].index]['DateTime'],y=tl['LowTrend']['trendline']['tl'],marker_color='red'), row=1, col=1)


        fig.update_yaxes(title_text='Price', row=1, col=1)
        fig.update_xaxes(title_text='Date', row=2, col=1)
        fig.update_layout(title=f"Price {ticker}", autosize=False,
                            xaxis_rangeslider_visible=False,
                            width=1000,
                            height=700)

        fig.show()

    else:

        fig,(ax1) = plt.subplots(1, 1, figsize=(9, 6),sharex=True)
        fig.suptitle('Gráfico '+ticker+' '+str(tf))
        ax1.get_xaxis().set_visible(False)

        if candle:
            # Preparamos los datos para graficar velas
            indice = ohlcv.index
            ohlcv = ohlcv.reset_index(drop=True).reset_index()
            ohlcv['Up'] = ohlcv['Close'] > ohlcv['Open']
            ohlcv['Bottom'] = np.where(ohlcv['Up'], ohlcv['Open'], ohlcv['Close'])
            ohlcv['Bar'] = ohlcv['High'] - ohlcv['Low']
            ohlcv['Body'] = abs(ohlcv['Close'] - ohlcv['Open'])
            ohlcv['Color'] = np.where(ohlcv['Up'], 'g', 'r')
            ax1.yaxis.tick_right()
            ax1.bar(indice, bottom=ohlcv['Low'], height=ohlcv['Bar'], width=0.25, color='#000000')
            ax1.bar(indice, bottom=ohlcv['Bottom'], height=ohlcv['Body'], width=0.5, color=ohlcv['Color'])
        else:
            ax1.plot(ohlcv.index,ohlcv['Close'],color='blue')
