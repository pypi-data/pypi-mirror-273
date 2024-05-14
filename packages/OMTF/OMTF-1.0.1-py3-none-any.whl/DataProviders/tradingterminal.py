
import numpy as np
import pandas as pd

import requests

from data import DataProvider

url = 'https://api.tradingterminal.com/v1/overview/marketSummary?stock=SPY,QQQ,DIA,IWM&crypto=BTCUSD' # Close data
url = 'https://api.tradingterminal.com/v1/overview/callratio?exchanges=AMEX,NYSE,NASDAQ,CBOE' # Pull/Call ratio

url = 'https://api.tradingterminal.com/v1/fmp/CompanyQuote?ticker=AAPL,CLUSD,BZUSD,NGUSD,GCUSD,SIUSD,PLUSD,HGUSD,LBUSD,EURUSD' # Quote
url = 'https://api.tradingterminal.com/v1/fmp/HolidaysAndTradingHours' # Calendar
url = 'https://api.tradingterminal.com/v1/fmp/EarningsCalendarConfirmed?startDate=2023-04-30&endDate=2023-05-06' # Earnings calendar
url = 'https://api.tradingterminal.com/v1/fmp/DividendsCalendar?startDate=2023-04-30&endDate=2023-05-06' # Dividends calendar
url = 'https://api.tradingterminal.com/v1/fmp/IPOCalendar?startDate=2023-04-30&endDate=2023-05-06' # IPO calendar
url = 'https://api.tradingterminal.com/v1/fmp/EconomicCalendar?startDate=2023-04-23&endDate=2023-04-29' # Economic calendar

url = 'https://api.tradingterminal.com/v1/eod/technical?ticker=AAPL&from=2023-03-01&to=2023-05-01&indicator=atr&period=14' # Get indicator

url = 'https://api.tradingterminal.com/v1/qv/insidertrading/AAPL' # Insider transactions
url = 'https://api.tradingterminal.com/v1/qv/congresstrading/AAPL' # Congress transactions
url = 'https://api.tradingterminal.com/v1/qv/wallstreetbets' # WallStreetbets params={'rank':True}
url = 'https://api.tradingterminal.com/v1/qv/housetrading' 
url = 'https://api.tradingterminal.com/v1/qv/senatetrading'
url = 'https://api.tradingterminal.com/v1/qv/lobbying' # Companies lobby
url = 'https://api.tradingterminal.com/v1/qv/smart-money-tracker?period=1648684800000' # Smart money by sector
url = 'https://api.tradingterminal.com/v1/qv/institutional?owner=BERKSHIRE%20HATHAWAY%20INC' # Institutional investments

url = 'https://api.tradingterminal.com/v1/pg/AggregateAllData?ticker=AAPL&multiplier=1&timespan=day&fromDate=2022-05-01&toDate=2023-05-01&sortOrder=asc' # Candle data

url = 'https://api.tradingterminal.com/v1/tw/important-tweets' # Important tweets

url = 'https://api.tradingterminal.com/v1/stnews/movers' #News movers
url = 'https://api.tradingterminal.com/v1/stnews/newsfeed/' # News feed
url = 'https://api.tradingterminal.com/v1/news/metatags' # Top news

url = 'https://api.tradingterminal.com/v1/finage/TickersSnapshot?tickers=TSLA,AMD,AAPL' # Last trade in the tickers





class TradingTerminal(DataProvider):

    static_url: str = 'https://tt-static-files.s3.us-west-2.amazonaws.com/'
    api_url: str = 'https://api.tradingterminal.com/v1/'

    def _request(self, url:str, headers:dict=None, params:dict=None) -> (list | dict):

        headers = {**self._random_header(), **headers}

        self.r: requests.Response = requests.get(url=url, params=params, headers=headers)

        return self.r.json()

    def getStocks(self, df:bool=True) -> (pd.DataFrame | dict):

        '''
        Get available stocks.

        Parameters
        ----------
        df: bool
            True to return DataFrame.

        Returns
        -------
        return: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.static_url+'/tickers.json.gz'
        data = self._request(url=url)

        return pd.DataFrame(data) if df else data

    def getSymbolsRename(self, df:bool=True) -> (pd.DataFrame | dict):

        '''
        Get stocks symbol rename.

        Parameters
        ----------
        df: bool
            True to return DataFrame.

        Returns
        -------
        return: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.static_url+'/symbol_history.json.gz'
        data = self._request(url=url)

        return pd.DataFrame(data) if df else data

    def getInstitutions(self, df:bool=True) -> (pd.DataFrame | dict):

        '''
        Get available institutions.

        Parameters
        ----------
        df: bool
            True to return DataFrame.

        Returns
        -------
        return: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.static_url+'/funds.json.gz'
        data = self._request(url=url)

        return pd.DataFrame(data) if df else data

    def getCryptos(self, df:bool=True) -> (pd.DataFrame | dict):

        '''
        Get available crypto currencies.

        Parameters
        ----------
        df: bool
            True to return DataFrame.

        Returns
        -------
        return: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.static_url+'/crypto.json.gz'
        data = self._request(url=url)

        return pd.DataFrame(data) if df else data

    def screener(self, screener:str='Gainers', df:bool=True
                 ) -> (pd.DataFrame | dict):

        '''
        Get screener results.

        Parameters
        ----------
        screener: string
            Screener name to retrieve. Choose between:
            - Gainers
            - Losers
            - PremarketVol
            - HighVol
        df: bool
            True to return DataFrame.

        Returns
        -------
        return: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.api_url+'cw/initial/toplist'
        if screener == 'Gainers':
            params: dict = {'id': '62a0f35bb8d9394f6851a571'}
        elif screener == 'Losers':
            params: dict = {'id': '62a0f35bb8d9394f6851a572'}
        elif screener == 'PremarketVol':
            params: dict = {'id': '6266cb20fa16a64d39043ad5'}
        elif screener == 'HighVol':
            params: dict = {'id': '62a0f35bb8d9394f6851a573'}
        data = self._request(url=url, params=params)

        return pd.DataFrame(data) if df else data
        
    def sectorPerformance(self, sectors:list=['XLE','XLU','XLK','XLB','XLP','XLY',
                          'XLI','XLC','XLV','XLF','XLRE'], df:bool=True
                          ) -> (pd.DataFrame | dict):

        '''
        Get sectors performance.

        Parameters
        ----------
        sectors: list
            List with sectors ETFs.
        df: bool
            True to return DataFrame.

        Returns
        -------
        return: dict | pd.DataFrame
            Contains the data.
        '''
      
        url: str = self.api_url+'overview/sectorePerformance'
        params: dict = {'ticker':','.join(sectors)}
        data = self._request(url=url, params=params)

        return pd.DataFrame(data) if df else data
        
    def marketBreadth(self, df:bool=True) -> (pd.DataFrame | dict):

        '''
        Get Market Breadth.

        Parameters
        ----------
        df: bool
            True to return DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the data.
        '''
      
        url: str = self.api_url+'overview/marketbreadth'
        data = self._request(url=url)


        if df:
            data: dict = {d['chartTitle']: pd.DataFrame({'greenData':d['greenData'], 'redData':d['redData']}) \
                for d in data}

        return data

        url = 'https://api.tradingterminal.com/v1/overview/marketSummary?stock=SPY,QQQ,DIA,IWM&crypto=BTCUSD' # Close data
        url = 'https://api.tradingterminal.com/v1/overview/marketSummarySnapshot?stock=AAPL' # Snapshot of one symbol
        url = 'https://api.tradingterminal.com/v1/overview/callratio?exchanges=AMEX,NYSE,NASDAQ,CBOE' # Pull/Call ratio

    def tickerInfo(self, tickers:(list | str), df:bool=True
                   ) -> (pd.DataFrame | dict):

        '''
        Get information about a stocks list.

        Parameters
        ----------
        tickers: list | str
            List of Symbols to get info.
        df: bool
            True to return DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.api_url+'fmp/CompanyProfile' # Ticker description
        params: dict = {'ticker': ','.join(tickers) if isinstance(tickers, list) else tickers}
        data = self._request(url=url, params=params)

        return pd.DataFrame(data) if df else data

    def tickerFundamental(self, ticker:str, df:bool=True
                          ) -> (pd.DataFrame | dict):

        '''
        Get historical fundamentals about a stock.

        Parameters
        ----------
        ticker: str
            Symbol to get fundamentals.
        df: bool
            True to return DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.api_url+'eod/fundamentals' # Fundamental historic data
        params: dict = {'ticker': ticker}
        data = self._request(url=url, params=params)

        return pd.DataFrame(data) if df else data
    
    def tickerNews(self, tickers:(list | str), n:int=50, df:bool=True
                   ) -> (pd.DataFrame | dict):

        '''
        Get historical fundamentals about a stock.

        Parameters
        ----------
        tickers: list or str
            Symbol to get fundamentals.
        n: int
            Number of news to show.
        df: bool
            True to return DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the data.
        '''

        url: str = self.api_url+'fmp/FMPNewsFeed' # Fundamental historic data
        params: dict = {'tickers': ','.join(tickers) if isinstance(tickers, list) else tickers, 
                  'limit':n}
        data = self._request(url=url, params=params)

        return pd.DataFrame(data) if df else data

    def snapshot(self, tickers:(list | str), df:bool=True
                 ) -> (pd.DataFrame | dict):

        '''
        Get snapshot for a list of stocks.

        Parameters
        ----------
        tickers: list or str
            List of symbols for the snapshot.
        df: bool
            True to return DataFrame.

        Returns
        -------
        data: dict | pd.DataFrame
            Contains the data.
        '''
        
        url: str = self.api_url+'overview/marketSummarySnapshot' # Fundamental historic data
        params: dict = {'stock': ','.join(tickers)}

        url: str = self.api_url+'pg/TickersSnapshot' # Fundamental historic data
        params: dict = {'tickers': ','.join(tickers) if isinstance(tickers, list) else tickers}

        data = self._request(url=url, params=params)

        return pd.DataFrame(data) if df else data



if __name__ ==  '__main__':

    import datetime as dt
    
    tt = TradingTerminal()
    scan = tt.screener(screener='Gainers')

    for s in ['Gainers', 'Losers', 'HighVol', 'PremarketVol']:

        scan = tt.screener(screener=s)
        if scan.empty:
            continue
        tickers = scan['symbol'].tolist()
        scan_desc = tt.tickerInfo(tickers)
        news = tt.tickerNews(tickers)

        complete = []
        for t in tickers:

            desc = scan_desc[scan_desc['symbol'] == t].to_dict('records')

            temp = {**scan[scan['symbol'] == t].to_dict('records')[0],
                    **(desc[0] if len(desc) > 0 else {}),
                    **{'news':news[news['symbol'] == t].to_dict('records')}}
            complete.append(temp)

        complete = pd.DataFrame(complete)

        complete.to_excel(f"{s}.xlsx")
        complete.to_csv(f"{s}_{dt.datetime.today().strftime('%Y%m%d')}.csv")