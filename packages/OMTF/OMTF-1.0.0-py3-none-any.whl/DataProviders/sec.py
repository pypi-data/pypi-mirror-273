
import os
import requests
import time
import pandas as pd

from data import DataProvider


class SEC(DataProvider):

    BASE_URL: str = 'https://www.sec.gov'
    DATA_URL: str = 'https://data.sec.gov'

    IMPORTANT_FORMS: dict = {
        '10-K': 'Key information of production. It is yearly',
        '10-Q': 'Key information of production. It is quarterly',
        '8-K': 'Major developments that occur between filings of the \
                Form 10-K or Form 10-Q',
        '3': 'Initial filing and discloses insider ownership amounts',
        '4': 'Identifies changes in insider ownership',
        '5': 'Is an annual summary of Form 4',
        'DEF 14A': 'Information on matters that require shareholder approval',
        '13D': 'When a shareholder acquires more than 5 percent of the \
                outstanding shares',
    }

    def __init__(self, email:str='dcaronm@gmail.com') -> None:

        '''
        Defines the requests header and the relations between ticker and CIK.

        Parameters
        ----------
        email: str
            Email for the API header.
        '''

        self.headers: dict = {'User-Agent': email}
        self.tickerCik()

    def _request(self, url:str, json:bool=True) -> (list | dict):

        '''
        Makes the requests.

        Parameters
        ----------
        url: str
            URL to request.
        json: bool
            True to return the result as dictionary.

        Returns
        -------
        r: 
            Contains the URL's data.
        '''

        r = requests.get(url, headers=self.headers)
        time.sleep(.1)

        try:
            return r.json() if json else r
        except:
            raise(ValueError(f'Error with url {url}'))

    def tickerCik(self, df:bool=True) -> (dict | pd.DataFrame):

        '''
        Formats the dictionary containing the relationship between 
        Ticker and CIK.

        Parameters
        ----------
        df: bool
            True to return the result as DataFrame.

        Returns
        -------
        tickers_cik: pd.DataFrame | dict
            Contains the relationship between Ticker and CIK.
        '''

        url: str = f'{self.BASE_URL}/files/company_tickers.json'
        
        self.tickers_cik: pd.DataFrame = pd.json_normalize(
                          pd.json_normalize(self._request(url), 
                                            max_level=0).values[0])
        self.tickers_cik['cik_str'] = self.tickers_cik['cik_str'].astype(str).str.zfill(10)
        self.tickers_cik.set_index('ticker',inplace=True)
        
        return self.tickers_cik if df else self.tickers_cik.to_dict()

    def tickerFilings(self, ticker:str) -> pd.DataFrame:

        '''
        Lists the filings for the specified ticker.

        Parameters
        ----------
        ticker: str
            Ticker to request.

        Returns
        -------
        tickers_cik: pd.DataFrame
            Contains the filings.
        '''

        self.cik: str = self.tickers_cik['cik_str'].loc[ticker]
        url: str = f'{self.DATA_URL}/submissions/CIK{self.cik}.json'
        data: dict = self._request(url)
        data['filings'] = pd.DataFrame(data['filings']['recent'])

        return data

    def filingData(self, ticker:str, filing:str=None, document:str=None):

        '''
        Get content of an specific filing.

        Parameters
        ----------
        ticker: str
            Ticker to request.
        filing: str
            Accession Number of a filing from the EDGAR SEC api.
        document: str
            Document name of the filing.

        Returns
        -------
        data: str
            Contains the HTML code of the filing.
        '''

        self.cik: str = self.tickers_cik['cik_str'].loc[ticker]
        if filing == None or document == None:
            filings: pd.DataFrame = self.tickerFilings(ticker=ticker)['filings']
            filing: str = filings['accessionNumber'].iloc[0].replace('-','')
            document = filings['primaryDocument'].iloc[0]
        url: str = f'{self.BASE_URL}/Archives/edgar/data/{self.cik}/{filing}/{document}'
        data: requests.Response = self._request(url, json=False)

        return data.text

    def tickerData(self, ticker:str) -> (list | dict):

        '''
        Get complete available fundamental data of a ticker and their 
        description.

        Parameters
        ----------
        ticker: str
            Ticker to request.

        Returns
        -------
        data: dict
            Contains the fundamental indicators available for the company.
        '''

        self.cik: str = self.tickers_cik['cik_str'].loc[ticker]
        url: str = f'{self.DATA_URL}/api/xbrl/companyfacts/CIK{self.cik}.json'
        data: (list | dict) = self._request(url)

        return data

    def fundamentalIndicator(self, ticker:str, datatype:str) -> (list | dict):

        '''
        Get data of a fundamental indicator for a ticker. To get available 
        fundamental indicators for the ticker call the specific method.

        Parameters
        ----------
        ticker: str
            Ticker to request.
        datatype: str
            Indicator to request.

        Returns
        -------
        data: dict
            Contains the fundamental indicator data for the company.
        '''

        data: str = 'Assets'
        self.cik: str = self.tickers_cik['cik_str'].loc[ticker]
        url: str = f'{self.DATA_URL}/api/xbrl/companyconcept/CIK{self.cik}/us-gaap/{datatype}.json'
        data: (list | dict) = self._request(url)

        return data

    def fundamentalData(self, ticker:str, df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get all the fundamental indicators data for the company.

        Parameters
        ----------
        ticker: str
            Ticker to request.
        df: bool
            True to return the result as DataFrame.

        Returns
        -------
        data: pd.DataFrame | dict
            Contains the indicators data.
        '''

        data = self.tickerData(ticker)['facts']['us-gaap']
        if df:
            data = {k: pd.DataFrame(data[k]['units'][list(data[k]['units'].keys())[0]]) 
                    for k in data if 'Deprecated' not in str(data[k]['label'])}

        return data

    def fundamentalIndicators(self, ticker:str, df:bool=True) -> (list | pd.DataFrame):

        '''
        Get the list of available indicators for the ticker.

        Parameters
        ----------
        ticker: str
            Ticker to request.
        df: bool
            True to return the result as DataFrame.

        Returns
        -------
        data: pd.DataFrame | dict
            Contains the available indicators.
        '''
        
        data = self.fundamentalData(ticker, df=False)
        fundamental_data = [{'Indicator':k, 'Name':data[k]['label'], 
                            'Description':data[k]['description'], 
                            'Units':list(data[k]['units'].keys())} 
                            for k in data if 'Deprecated' not in str(data[k]['label'])]

        return pd.DataFrame(fundamental_data) if df else fundamental_data
    
    def sharesData(self, ticker:str) -> dict:

        '''
        Get the shares data.

        Parameters
        ----------
        ticker: str
            Ticker to request.

        Returns
        -------
        data: dict
            Dictionary containing the insiders shares data and outstanding 
            shares data.
        '''

        data: dict = self.tickerData(ticker)['facts']['dei']
        shares: dict = {
            'Insiders': pd.DataFrame(data[list(data.keys())[0]]['units']['shares']),
            'Outstanding': pd.DataFrame(data[list(data.keys())[1]]['units']['USD']),
        }

        return shares

    def snapshot(self, datatype:str, period:str='Y2022Q4') -> (list | dict):

        '''
        Get the value of a fundamental indicator for the whole market for the 
        specified period.

        Parameters
        ----------
        ticker: str
            Ticker to request.
        period: str
            Period for the data. Must be a year or a quarter with the next format:
             - Year: YXXXX
             - Quarter: YXXXXQX
            Being the 4 X the year and an X the quarter of the year.

        Returns
        -------
        data: dict
            Dictionary containing the data.
        '''

        url: str = f'{self.DATA_URL}/api/xbrl/frames/us-gaap/{datatype}/USD/C{period}I.json'
        data: (list | dict) = self._request(url)

        return data
    
    
if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
      
    sec = SEC('dcaronm@gmail.com')
    ciks = sec.tickerCik(df=False)['cik_str']
    
    ticker = 'AAPL'
    filings = sec.tickerFilings(ticker)['filings']
    filings[filings['form'].isin(list(sec.IMPORTANT_FORMS.keys()))]


    # Diluted Earnings per Share
    data = sec.fundamentalData(ticker) 
    earnings = data['EarningsPerShareDiluted']
    earnings = earnings[earnings['form'] != '10-K/A']
    earnings.set_index('end', inplace=True)

    earnings[['val']].plot(lw=2, figsize=(14, 6), title='Diluted Earnings per Share')
    plt.xlabel('')
    plt.savefig('diluted eps')

    ind = sec.fundamentalIndicators(ticker)
    ind[ind['Name'].astype('str').str.contains('Shares')]


    # Common Stock Shares Outstanding
    shares = data['CommonStockSharesOutstanding']
    shares = shares[shares['form'] == '10-Q']
    shares.set_index('end', inplace=True)

    shares[['val']].plot(lw=2, figsize=(14, 6), title='Diluted Earnings per Share')
    plt.xlabel('')
    plt.savefig('shares')