
import os
import datetime as dt

import numpy as np
import pandas as pd

import json as JSON

import certifi
import urllib3
from bs4 import BeautifulSoup

from data import DataProvider


class CoinMarketCap(DataProvider):

    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/108.0.0.0 Safari/537.36',
    }
    BASE_URL: str = 'https://coinmarketcap.com'

    def _request(self, url:str, headers:dict={}, params:dict=None, json:bool=True):

        headers = {**headers, **self._random_header()}

        self.r = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where()) \
                        .urlopen('GET', url, headers=headers)
        
        if json:
            html: BeautifulSoup = BeautifulSoup(self.r.data, 'html.parser')
            data: dict = JSON.loads(html.find_all('script', {'id':"__NEXT_DATA__"})[0].get_text())
        
            return data
        
        return self.r


    def historicalMarketCap(self, first_date:str='20130429', df:bool=True) -> (list | pd.DataFrame):
        
        # Initialize needed data
        data: dict = {
            'props':{'pageProps': {'nextWeek':first_date}}
        }
        global_data: list = []
        cap_data: list = []

        # Loop for each week
        while 'nextWeek' in data['props']['pageProps']:

            # Get HTML
            url: str = f"{self.BASE_URL}/historical/{data['props']['pageProps']['nextWeek']}/"
            data: dict = self._request(url=url)
            
            # Store the desired data
            global_data.append(data['props']['pageProps']['globalMetrics'])
            cap_data = cap_data + JSON.loads(data['props']['initialState'])['cryptocurrency']['listingHistorical']['data']
            
        return pd.DataFrame(cap_data) if df else cap_data
    
    def getSpotlight(self, df:bool=True) -> dict:

        # Get HTML
        url: str = f'{self.BASE_URL}/best-cryptos/'
        data: dict = self._request(url=url)

        # Store the desired data
        best_cryptos: dict = JSON.loads(data['props']['initialState'])['cryptocurrency']['spotlight']['data']
        
        return {k: pd.DataFrame(best_cryptos[k]) if df else best_cryptos[k] for k in best_cryptos}

    def getGainersLosers(self, df:bool=True) -> dict:

        # Get HTML
        url: str = f'{self.BASE_URL}/gainers-losers/'
        data: dict = self._request(url=url)

        # Store the desired data
        best_cryptos: dict = JSON.loads(data['props']['initialState'])['cryptocurrency']['gainersLosers']
        
        return {k: pd.DataFrame(best_cryptos[k]) if df else best_cryptos[k] for k in best_cryptos}
    

if __name__ == '__main__':

    api = CoinMarketCap()
    market_cap = api.historicalMarketCap(first_date='20230101', df=True)
    spotlight = api.getSpotlight(df=True)
    gl = api.getGainersLosers(df=True)
