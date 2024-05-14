
import datetime as dt
from random import choice

import numpy as np
import pandas as pd
import requests

from data import DataProvider


class DilutionTracker(DataProvider):

    headers: dict = {
        'Accept': 'application/json',
        'Origin': 'https://dilutiontracker.com',
    }

    cookie: dict = {
        'sid': None
    }

    BASE_URL: str = 'https://api.dilutiontracker.com'

    def __init__(self, ticker:str=None, version:str='v1') -> None:

        self.BASE_URL: str = self.BASE_URL+f'/{version}'
        self.ticker: str = ticker
        self.params: dict = {'ticker': ticker}
    
    def _request(self, url:str, params:str={}) -> requests.Response:

        if self.cookie['sid'] != None:
            self.headers['Cookie'] = f"connect.sid={self.cookie['sid']}"

        r: requests.Response = requests.get(url=url, params=params, 
                         headers=self._random_header())
        
        self.cookies = r.cookies
        self.cookie: dict = {
            'sid': list(r.cookies)[0].value,
            'expiration': dt.datetime.fromtimestamp(list(r.cookies)[0].expires)
        }
        
        return r
    
    def getSid(self) -> None:

        url: str = 'https://m.stripe.com/6'
        r = requests.post(url=url, headers=self._random_header())

        return r
    
    def getTickerCoverage(self) -> requests.Response:

        return self._request(self.BASE_URL+'/getTickerCoverage')
    
    def getPopularTickers(self) -> requests.Response:

        return self._request(self.BASE_URL+'/getPopularTickers').json()
    
    def getReverseSplit(self) -> requests.Response:

        return self._request(self.BASE_URL+'/getReverseSplit')
    
    def getTicker(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getTicker', params=self.params)
    
    def getMarketData(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')
        
        params: dict = {
            'type': 'snapshot', 
            'computeAfterMktChangeRelativeToYesterdayClose': False
        }

        return self._request(self.BASE_URL+f'/getMarketData', 
                             params={**self.params, **params})
    
    def getCompanyProfile(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getCompanyProfile', params=self.params)
    
    def getMarketCap(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getMarketCap', params=self.params)
    
    def getCashPerShare(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getCashPerShare', params=self.params)
    
    def getInstOwn(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getInstOwn', params=self.params)
    
    def getShortInterest(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getInstOwn', params=self.params)
    
    def getSharesOutStanding(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getSharesOS', params=self.params)
    
    def getMovements(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getOurTake', params=self.params)
    
    def getCompletedOfferings(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getCompletedOfferings', params=self.params)
    
    def getCashPosition(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getCashPosition', params=self.params)
    
    def getOhlcvTimeSeriesWithNews(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getOhlcvTimeSeriesWithNews', params=self.params)
    
    def getInstOwn(self, ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')

        return self._request(self.BASE_URL+f'/getInstOwn', params=self.params)
    
    def getSecFilings(self, categories:list=['chronological', 'ownershipFilings', 
                      'disclosureFilings', 'prospectusFilings', 'otherFilings', 
                      'proxyFilings', 'financialFilings'], 
                      ticker:str=None) -> requests.Response:

        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')
        
        if isinstance(categories, str):
            categories: list = [categories]
        data: dict = {}
        for category in categories:
            params: dict = {
                'targetCategory':category,
                'from': 0,
            }
            data[category] = self._request(self.BASE_URL+f'/getSecFilingsByCategoryName', 
                          params={**self.params, **params}).json()

        return data
    
    def getFinancialStatements(self, frequencies:list=['quarter','annual'], 
                               statements:list=['income-statement', 'balance-sheet', 
                                                'cash-flow'],
                               periods:int=28, ticker:str=None) -> requests.Response:
        
        '''
        frequency: str
            From: 'annual' or 'quarterly'.
        statement: str
            From: 'income-statement', 'balance-sheet', 'cash-flow'.
        '''
        if ticker != None:
            self.params['ticker'] = ticker
        if self.params['ticker'] == None:
            raise ValueError('There is no ticker defined!')
        
        if isinstance(frequencies, str):
            frequencies: list = [frequencies]
        if isinstance(statements, str):
            statements: list = [statements]

        data: dict = {}
        for frequency in frequencies:
            data[frequency] = {}
            for statement in statements:
                params: dict = {
                    'frequency': frequency,
                    'numPeriods': periods,
                    'statement': statement
                }
                data[frequency][statement] = self._request(self.BASE_URL+f'/getFinancialStatements', 
                                                params={**self.params, **params}).json()

        return data
        
    

if __name__ == '__main__':

    '''
    https://docs.google.com/document/d/1pP-m3V3vOVj7A8cX1Zl9c4Xs_cg13MIT6Rbqz_udF10/edit#
    '''

    dil = DilutionTracker()
    r = dil.getPopularTickers()