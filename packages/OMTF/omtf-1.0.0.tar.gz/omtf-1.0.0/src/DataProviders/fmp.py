
import requests

from data import DataProvider

class FinancialModellingProp(DataProvider):

    '''
    https://site.financialmodelingprep.com/developer/docs/#Stock-Screener
    '''

    BASE_URL: str = 'https://financialmodelingprep.com/api'

    def __init__(self, api_key:str) -> None:
        
        self.api_key: str = api_key

    def _request(self, url:str, params:dict={}, json:bool=True) -> (list | dict):

        if 'apikey' not in params:
            params['apikey'] = self.api_key

        self.r: requests.Response = requests.get(url, params=params)

        return self.r.json() if json else self.r
    
    def stocksList(self, version:str='v3') -> requests.Response:
        
        url: str = self.BASE_URL+f'/{version}/stock/list'

        return self._request(url)
    
    def stockScreener(self, market_cap_higher:float=None, 
                      market_cap_lower:float=None, price_higher:float=None,
                      price_lower:float=None, volume_higher:float=100000, 
                      volume_lower:float=None, etf:bool=False, active:bool=True,
                      sector:list=None, industry:list=None, country:list=['US'], 
                      exchange:list=['NYSE','NASDAQ','AMEX'], limit:int=None,
                      version:str='v3') -> requests.Response:
        
        url: str = self.BASE_URL+f'/{version}/stock-screener'
        params: dict = {}
        if market_cap_higher != None: params['marketCapMoreThan'] = market_cap_higher
        if market_cap_lower != None: params['marketCapLowerThan'] = market_cap_lower
        if price_higher != None: params['priceMoreThan'] = price_higher
        if price_lower != None: params['priceLowerThan'] = price_lower
        if volume_higher != None: params['volumeMoreThan'] = volume_higher
        if volume_lower != None: params['volumeLowerThan'] = volume_lower
        if etf != None: params['isEtf'] = 'true' if etf else 'false'
        if active != None: params['isActivelyTrading'] = 'true' if active else 'false'
        if sector != None and len(sector) > 0: params['sector'] = ','.join(sector)
        if industry != None and len(industry) > 0: params['industry'] = ','.join(industry)
        if country != None and len(country) > 0: params['country'] = ','.join(country)
        if exchange != None and len(exchange) > 0: params['exchange'] = ','.join(exchange)
        if limit != None: params['limit'] = limit

        return self._request(url, params)




if __name__ == '__main__':

    fmp = FinancialModellingProp(api_key='aba9a750dd340f1afcb8fd2d959706de')
    fmp.stocksList()