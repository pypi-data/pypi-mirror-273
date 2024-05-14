
import time
import requests

import pandas as pd

from data import DataProvider

class CoinGecko(DataProvider):

    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/108.0.0.0 Safari/537.36',
    }
    BASE_URL: str = 'https://api.coingecko.com/api/v3'

    def __init__(self, free:bool=True) -> None:
        
        self.free: bool = free

    def _request(self, url:str, headers:dict={}, params:dict=None):

        headers = {**headers, **self._random_header()}

        self.r = requests.get(url, params=params, headers=headers)
        if self.free:
            time.sleep(60/10)

        if self.r.status_code == 200:
            return self.r.json()
        else:
            print('Error al obtener datos de mercado:', self.r.text)
            return None
        
    def getCoinsMarkets(self, cryptos:list=[], currency:str='usd', category:str=[],
                        order:str='market_cap_desc', price:bool=True, price_change:list=[],
                        all:bool=False, df:bool=True) -> (list | pd.DataFrame):

        '''
        Get general data of tickers.

        Parameters
        ----------
        cryptos: list
            List of cryptos to get that from.
        currency: str
            Base currency for the pair.
        category: 
            String with tha category. Check getCategoriesList for the list of 
            categories available.
        order: str
            To sort values. 
            Options: market_cap_asc, market_cap_desc, volume_asc, volume_desc, 
                id_asc, id_desc
        price: bool
            True to include 7 days of price data.
        price_change: list
            List with specific percentage change periods to retrieve.
            Options: 1h, 24h, 7d, 14d, 30d, 200d, 1y
        df: bool
            Return data as DataFrame.

        Returns
        -------
        data: list | pd.DataFrame
            Contains the requested data.
        '''

        url: str = f'{self.BASE_URL}/coins/markets'
        params: dict = {
            'per_page': 250,
            'vs_currency': currency,
            'order': order,
            'category': category,
            'price': price,
            'page': 1
        }
        if len(cryptos) > 0:
            params['ids'] = ','.join(cryptos)
        if len(price_change) > 0:
            params['price_change'] = ','.join(price_change)

        if all:
            data = []
            temp = None
            while temp == None or len(temp) >= params['per_page']: 
                temp = self._request(url, params=params)
                params['page'] += 1
                data += temp
        else:
            data = self._request(url, params=params)

        return pd.DataFrame(data) if df else data


if __name__ == '__main__':

    coin = CoinGecko()
    coin.getCoinsMarkets()