
import time
import requests
import pandas as pd

from data import DataProvider

class Polygon(DataProvider):

    BASE_URL: str = 'https://api.polygon.io'

    def __init__(self,api_key:str='cUlHULSDVdLm9Up1TsKxF3RU2dEKm3nq', 
                 free:bool=False) -> None:

        '''
        Python Wrapper for the Polygon.io API.

        Parameters
        ----------
        api_key: str
            Personal key for the polygon API.
        free: bool
            True to wait between requests not to exceed the free plan limits.
        '''

        self.api_key: str = api_key
        self.free: bool = free

    def _request(self, url:str, params:dict={}) -> (list | dict):

        '''
        Performs the request of type GET.

        Parameters
        ----------
        url: str
            URL to make the request.
        params: dict
            Dictionary containing the request parameters.

        Returns
        -------
        result: list | dict
            Contains the requested data.
        '''

        
        params = {**params, **{'apiKey': self.api_key}}

        self.r: requests.Response = requests.get(url=url, params=params)
        if self.free:
            time.sleep(13)

        r: (list | dict) = self.r.json()
        
        if 'status' not in r:
            result: list = [r]
        else:
            if r['status'] in ['OK', 'DELAYED']:
                result: dict = r
            else:
                raise(ValueError(r))

        if 'next_url' in result:
            self.r: requests.Response = requests.get(url=result['next_url'])
            if 'results' in result:
                result['results'] = result['results'] + self.r.json()['results']
        
        return result
            
    def aggregates(self, symbol:str, multiplier:int, timespan:str, 
                   start:str, end:str, adjusted:bool=False, sort:str='desc',
                   limit:int=5000, version:str='/v2', df:bool=True
                   ) -> (dict | pd.DataFrame):

        '''
        Get a single ticker supported by Polygon.io. 
        This response will have detailed information about the 
        ticker and the company behind it.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock/equity.
        multiplier: int
            Number to multiply the timespan to form the timeframe.
        timespan: str
            Time unit to form the timeframe.
            Options: 'minute','hour','day','week','month','quarter','year'.
        start: str
            Date from which to start getting data. Either a date with 
            the format YYYY-MM-DD or a millisecond timestamp.
        end: str
            Date till which to get data. Either a date with the format 
            YYYY-MM-DD or a millisecond timestamp.
        adjusted: bool
            Whether or not the results are adjusted for splits. By default, 
            results are not adjusted. Set this to true to get results that 
            are adjusted for splits.
        sort: str
            Sort the results by timestamp. 'asc' will return results in 
            ascending order (oldest at the top), 'desc' will return results 
            in descending order (newest at the top). Default is 'asc'.
        limit:int
            Limits the number of base aggregates queried to create the 
            aggregate results. Max 50000 and Default 5000.
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''

        params: dict = {'adjusted': adjusted, 'sort': sort, 'limit': limit}
        url: str = self.BASE_URL+version+f'/aggs/ticker/{symbol}/range/{multiplier}/{timespan}' + \
                                   f'/{start}/{end}'
        
        data: (list | dict) = self._request(url=url, params=params)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            data.rename(columns={'v':'Volume','vw':'VWAP','o':'Open',
                                 'c':'Close','h':'High','l':'Low',
                                 't':'DateTime','n':'Trades'}, inplace=True)
            data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            data.set_index(keys='DateTime', inplace=True)
            data.sort_index(ascending=True, inplace=True)
            #data['Volume'] = data['Volume'].astype(float).astype(int)
            #data['VWAP'] = data['VWAP'].astype(float)
            #data['Open'] = data['Open'].astype(float)
            #data['Close'] = data['Close'].astype(float)
            #data['High'] = data['High'].astype(float)
            #data['Low'] = data['Low'].astype(float)
            #data['Trades'] = data['Trades'].astype(int)

        return data
            
    def groupedBy(self, date:str, adjusted:bool=False, include_otc:bool=True,
                   version:str='/v2', df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get the daily open, high, low, and close (OHLC) for the entire 
        stocks/equities markets.

        Parameters
        ----------
        date: str
            Date till which to get data. Either a date with the format 
            YYYY-MM-DD or a millisecond timestamp.
        adjusted: bool
            Whether or not the results are adjusted for splits. By default, 
            results are not adjusted. Set this to true to get results that 
            are adjusted for splits.
        inclued_otc: bool
            Include OTC securities in the response. Default is True 
            (don't include OTC securities).
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''

        params: dict = {'adjusted': adjusted, 'include_otc': include_otc}
        url: str = self.BASE_URL+version+f'/aggs/grouped/locale/us/market/stocks' + \
                                   f'/{date}'
        
        data: (list | dict) = self._request(url=url, params=params)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            data.rename(columns={'v':'Volume','vw':'VWAP','o':'Open',
                                 'c':'Close','h':'High','l':'Low',
                                 't':'DateTime','n':'Trades','T':'Symbol',
                                 'otc':'OTC'}, inplace=True)
            data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            data.set_index(keys='DateTime', inplace=True)
            data['OTC'].fillna(False, inplace=True)
            #data['Volume'] = data['Volume'].astype(float).astype(int)
            #data['VWAP'] = data['VWAP'].astype(float)
            #data['Open'] = data['Open'].astype(float)
            #data['Close'] = data['Close'].astype(float)
            #data['High'] = data['High'].astype(float)
            #data['Low'] = data['Low'].astype(float)
            #data['Trades'] = data['Trades'].astype(int)
            #data['Symbol'] = data['Symbol'].astype(str)

        return data

    def dailyCandle(self, symbol:str, date:str, adjusted:bool=False,
                   version:str='/v1', df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get the open, high, low, close, premarket close and 
        afterhours close prices of a stock symbol on a certain date.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock/equity.
        date: str
            Date till which to get data. Either a date with the format 
            YYYY-MM-DD or a millisecond timestamp.
        adjusted: bool
            Whether or not the results are adjusted for splits. By default, 
            results are not adjusted. Set this to true to get results that 
            are adjusted for splits.
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''

        params: dict = {'adjusted': adjusted}
        url: str = self.BASE_URL+version+f'/open-close/{symbol}/{date}'
        
        data: (list | dict) = self._request(url=url, params=params)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            data.rename(columns={'afterHours':'AH','close':'Close',
                                 'open':'Open','high':'High','low':'Low',
                                 'from':'DateTime','preMarket':'PM',
                                 'symbol':'Symbol','volume':'Volume'}, inplace=True)
            data['DateTime'] = pd.to_datetime(data['DateTime'])
            data.set_index(keys='DateTime', inplace=True)
        
        return data

    def prevDailyCandle(self, symbol:str, adjusted:bool=False,
                   version:str='/v2', df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get the previous day's open, high, low, and close (OHLC) 
        for the specified stock ticker.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock/equity.
        adjusted: bool
            Whether or not the results are adjusted for splits. By default, 
            results are not adjusted. Set this to true to get results that 
            are adjusted for splits.
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''

        params: dict = {'adjusted': adjusted}
        url: str = self.BASE_URL+version+f'/aggs/ticker/{symbol}/prev'
        
        data: (list | dict) = self._request(url=url, params=params)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            data.rename(columns={'v':'Volume','vw':'VWAP','o':'Open',
                                 'c':'Close','h':'High','l':'Low',
                                 't':'DateTime','n':'Trades','T':'Symbol'}, inplace=True)
            data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            data.set_index(keys='DateTime', inplace=True)
        
        return data

    def trades(self, symbol:str, date:str, order:str='asc', sort:str='timestamp',
                limit:int=5000, version:str='/v3', df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get the trades for the specified stock ticker.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock/equity.
        date: str
            Date for which to get data. Either a date with the format 
            YYYY-MM-DD or a millisecond timestamp.
        order: str
            Sort the results by sort filed. 'asc' will return results in 
            ascending order (oldest at the top), 'desc' will return results 
            in descending order (newest at the top). Default is 'asc'.
        sort:str
            Sort field used for ordering.
        limit:int
            Limits the number of base aggregates queried to create the 
            aggregate results. Max 50000 and Default 5000.
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''
        
        params: dict = {'timestamp': date, 'order': order, 'limit': limit, 'sort': sort}
        url: str = self.BASE_URL+version+f'/trades/{symbol}'
        
        data: (list | dict) = self._request(url=url, params=params)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            data.rename(columns={'exchange':'Exchange','price':'Price',
                                 'DateTime':'sip_timestamp',
                                 'size':'Volume'}, inplace=True)
            if 'DateTime' not in data:
                raise(ValueError)
            data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            data.set_index(keys='DateTime', inplace=True)
        
        return data
    
    def lastTrade(self, symbol:str, version:str='/v2', df:bool=True
                  ) -> (dict | pd.DataFrame):

        '''
        Get the last trade for the specified stock ticker.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock/equity.
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''
        
        url: str = self.BASE_URL+version+f'/last/trade/{symbol}'
        
        data: (list | dict) = self._request(url=url)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            # data.rename(columns={'exchange':'Exchange','price':'Price',
            #                      'DateTime':'sip_timestamp',
            #                      'size':'Volume'}, inplace=True)
            # if 'DateTime' not in data:
            #     raise(ValueError)
            # data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            # data.set_index(keys='DateTime', inplace=True)
        
        return data
    
    def quotes(self, symbol:str, date:str, order:str='asc', sort:str='timestamp',
                limit:int=5000, version:str='/v3', df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get NBBO quotes for a ticker symbol in a given time range.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock/equity.
        date: str
            Date till which to get data. Either a date with the format 
            YYYY-MM-DD or a millisecond timestamp.
        order: str
            Sort the results by sort filed. 'asc' will return results in 
            ascending order (oldest at the top), 'desc' will return results 
            in descending order (newest at the top). Default is 'asc'.
        sort:str
            Sort field used for ordering.
        limit:int
            Limits the number of base aggregates queried to create the 
            aggregate results. Max 50000 and Default 5000.
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''
        
        params: dict = {'timestamp': date, 'order': order, 'limit': limit, 
                        'sort': sort}
        url: str = self.BASE_URL+version+f'/quotes/{symbol}'
        
        data: (list | dict) = self._request(url=url, params=params)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            data.rename(columns={'exchange':'Exchange','price':'Price',
                                 'DateTime':'sip_timestamp',
                                 'size':'Volume'}, inplace=True)
            if 'DateTime' not in data:
                raise(ValueError)
            data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            data.set_index(keys='DateTime', inplace=True)
        
        return data
    
    def snapshot(self, symbol:str, include_otc:bool=True, version:str='/v2', 
                 df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get the most up-to-date market data for several tickers.

        Note: Snapshot data is cleared at 3:30am EST and gets populated as 
        data is received from the exchanges. This can happen as early as 4am 
        EST.

        Parameters
        ----------
        symbol: str
            A comma separated list of tickers to get snapshots for.
        inclued_otc: bool
            Include OTC securities in the response. Default is True 
            (don't include OTC securities).
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''
        
        include_otc: str = 'true' if include_otc else 'false'
        params: dict = {'tickers': symbol, 'include_otc': include_otc}
        url: str = self.BASE_URL+version+f'/snapshot/locale/us/markets/stocks/tickers'
        
        data: (list | dict) = self._request(url=url, params=params)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            # data.rename(columns={'exchange':'Exchange','price':'Price',
            #                      'DateTime':'sip_timestamp',
            #                      'size':'Volume'}, inplace=True)
            # if 'DateTime' not in data:
            #     raise(ValueError)
            # data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            # data.set_index(keys='DateTime', inplace=True)
        
        return data
    
    def gainersLosers(self, direction:str, include_otc:bool=True, version:str='/v2', 
                 df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get the most up-to-date market data for the current top 20 gainers or 
        losers of the day in the stocks/equities markets.

        Top gainers are those tickers whose price has increased by the highest 
        percentage since the previous day's close. Top losers are those tickers 
        whose price has decreased by the highest percentage since the previous 
        day's close.

        Note: Snapshot data is cleared at 3:30am EST and gets populated as data 
        is received from the exchanges.

        Parameters
        ----------
        direction: str
            The direction of the snapshot results to return. 
            Can be gainers or losers.
        inclued_otc: bool
            Include OTC securities in the response. Default is True 
            (don't include OTC securities).
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''
        
        include_otc: str = 'true' if include_otc else 'false'
        params: dict = {'include_otc': include_otc}
        url: str = self.BASE_URL+version+f'/snapshot/locale/us/markets/stocks' + \
                                    f'/{direction}'
        
        data: (list | dict) = self._request(url=url, params=params)
        if df:
            columns: dict = {'o':'Open','h':'High','l':'Low','c':'Close',
                       't':'DateTime', 'av':' Average', 'v': 'Volume',
                       'vw': 'VWAP'}
            if 'tickers' in data:
                temp: list = []
                for d in data['tickers']:
                    tdict: dict = {
                        'ticker': d['ticker'],
                        'todaysChangePerc': d['todaysChangePerc'],
                        'todaysChange': d['todaysChange'],
                        'updated': d['updated'],
                    }
                    print(d)
                    for k in ['day','min','prevDay']:
                        for t in d[k]:
                            tdict[k+columns[t]] = d[k][t]
                    temp.append(tdict)
                data: pd.DataFrame = pd.DataFrame(temp)
                for c in [i for i in data.columns if 'DateTime' in i]:
                    data[c] = pd.to_datetime(data[c], unit='ms')
            else:
                data: pd.DataFrame = pd.DataFrame(data)
        
        return data

    def snapshotTicker(self, symbol:str, version:str='/v2', df:bool=True
                       ) -> (dict | pd.DataFrame):

        '''
        Get the most up-to-date market data for a single traded stock ticker.

        Note: Snapshot data is cleared at 3:30am EST and gets populated as 
        data is received from the exchanges. This can happen as early as 4am 
        EST.

        Parameters
        ----------
        symbol: str
            The ticker symbol of the stock/equity.
        version: str
            Name of the version of the API to call.
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the requested data.
        '''
        
        include_otc: str = 'true' if include_otc else 'false'
        url: str = self.BASE_URL+version+f'/snapshot/locale/us/markets/stocks/tickers' + \
                                    f'/{symbol}'
        
        data: (list | dict) = self._request(url=url)
        
        if df:
            data: pd.DataFrame = pd.DataFrame(data['results']) \
                    if 'results' in data else pd.DataFrame(data)
            # data.rename(columns={'exchange':'Exchange','price':'Price',
            #                      'DateTime':'sip_timestamp',
            #                      'size':'Volume'}, inplace=True)
            # if 'DateTime' not in data:
            #     raise(ValueError)
            # data['DateTime'] = pd.to_datetime(data['DateTime'], unit='ms')
            # data.set_index(keys='DateTime', inplace=True)
        
        return data
    


if __name__ == '__main__':

    pol = Polygon('cUlHULSDVdLm9Up1TsKxF3RU2dEKm3nq')
    data = pol.gainersLosers('gainers')
    print(data)