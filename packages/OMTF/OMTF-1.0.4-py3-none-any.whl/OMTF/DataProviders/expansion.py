
import enum
import datetime as dt

import requests
from bs4 import BeautifulSoup

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots
    
import yfinance as yf

class Expansion:

    headers = {
        'Accept': 'text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.expansion.com',
        'If-Modified-Since': 'Sat, 29 Oct 1994 19:43:31 GMT',
        'Pragma': 'no-cache',
        'Referer': 'https://www.expansion.com/mercados/euribor.html?intcmp=MENUHOM24101&s_kw=euribor',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-Requested-By': 'FusionCharts',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    base_url = 'https://www.expansion.com'
    app_url = '/app'
    bolsa_url = '/bolsa'

    def _request(self, url:str, params:dict=None, headers:dict=None):

        headers = self.headers if headers == None else headers
        self.r = requests.get(url, params=params, headers=headers)

        return self.r

    def getSymbol(self, symbol:str='TPMB1A') -> dict:

        '''
        Get symbol summary.

        Parameters
        ----------
        symbol: str
            Symbol identifier for the Expansion API.

        Returns
        -------
        data: dict
            Dictionary with the requested data.
        '''

        params = {
            'cod': symbol,
            'llave': ''
        }
        url = f'{self.base_url}{self.app_url}/bolsa/datos/valor_ficha.html'
        r = self._request(url, params)

        return r.json()
    
    def getChartData(self, symbol:str='TPMB1A', df:bool=True
                     ) -> (dict | pd.DataFrame):

        '''
        Get chart data for a symbol.

        Parameters
        ----------
        symbol: str
            Symbol identifier for the Expansion API.
        df: bool
            True to return a pandas DataFrame.

        Returns
        -------
        data: dict or pd.DataFrame
            Dictionary or pd.DataFrame with the requested data.
        '''

        params = {
            'cod': symbol,
            'tipo': '0',
            'configuracion': 'configuracion_cms',
            'llave': '',
        }
        url = f'{self.base_url}{self.app_url}/graficos/datosFlashMedia.html'
        r = self._request(url, params)

        data = BeautifulSoup(r.content, 'html.parser')
        series = data.find_all('dataset')
        series_dict = {}
        for serie in series:

            series_dict[serie['seriesname']] = {
                'Index': [d['tooltext'].split(' ')[1] \
                          for d in serie.find_all('set')],
                'Value': [float(d['value']) for d in serie.find_all('set')],
            }

        return pd.DataFrame(series_dict) if df else series_dict
    
    def getIndicatorData(self, symbol:str='TPMB1A', init:str='20000101', 
                         df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get chart data for a symbol.

        Parameters
        ----------
        symbol: str
            Symbol identifier for the Expansion API.
        init: str
            Initial date in %Y%m%d format.
        df: bool
            True to return a pandas DataFrame.

        Returns
        -------
        data: dict or pd.DataFrame
            Dictionary or pd.DataFrame with the requested data.
        '''

        params = {
            'cod': symbol,
            'tipo': '0',
            'configuracion': 'configuracion_fichas_cms',
            'llave': '',
            'fecha': init, # Date in %Y%m%d format
        }
        url = f'{self.base_url}{self.app_url}/graficos/datosFlash.html'
        r = self._request(url, params)

        data = BeautifulSoup(r.content, 'html.parser')
        index = data.find('categories').find_all('category')
        series = data.find_all('dataset')
        series_dict = {}
        for serie in series:

            series_dict[serie['seriesname']] = {
                'Index': [d['label'] for d in index if d['showlabel'] == "0"],
                'Value': [float(d['value']) for d in serie.find_all('set')],
            }

        serie = series_dict[list(series_dict.keys())[0]]
        if df:
            serie = pd.DataFrame(data=serie['Value'], index=serie['Index'], 
                                 columns=['Close'])

        return serie

    def getQuote(self, symbol:str='TPMB1A') -> dict:

        '''
        Get quote data for a symbol.

        Parameters
        ----------
        symbol: str
            Symbol identifier for the Expansion API.

        Returns
        -------
        data: dict
            Dictionary with the requested data.
        '''

        params = {
            'cod': symbol,
            'numeroh': '0',
        }
        url = f'{self.base_url}{self.bolsa_url}/datos/historico_valor.html'
        r = self._request(url, params)
        
        return r.json()
    
    def getIndexIntradayData(self, symbol:str='I.SP', df:bool=True
                             ) -> (dict | pd.DataFrame):

        '''
        Get intraday data for a symbol.

        Parameters
        ----------
        symbol: str
            Symbol identifier for the Expansion API.
        df: bool
            True to return a pandas DataFrame.

        Returns
        -------
        data: dict or pd.DataFrame
            Dictionary or pd.DataFrame with the requested data.
        '''

        params = {
            'cod': 'I.SP',
            'tipo': '0',
            'configuracion': 'configuracion_fichas_cms',
            'llave': '',
        }
        url = f'{self.base_url}{self.app_url}/graficos/datosFlashIntradiaXT.html'
        r = self._request(url, params)

        data = BeautifulSoup(r.content, 'html.parser')
        index = data.find('categories').find_all('category')
        series = data.find_all('dataset')
        series_dict = {}
        for serie in series:

            series_dict[serie['seriesname']] = {
                'Index': [d['label'] for d in index \
                          if d['showlabel'] == '0' and 'h' not in d['label']],
                'Value': [float(d['value']) for d in serie.find_all('set')],
            }

        serie = series_dict[list(series_dict.keys())[0]]
        if df:
            serie = pd.DataFrame(data=serie['Value'], index=serie['Index'], 
                                 columns=['Close'])

        return serie

    def getIndexMonth(self, symbol:str='I.SP', year:int=2023, month:int=5, 
                      df:bool=True) -> (dict | pd.DataFrame):

        '''
        Get symbol summary.

        Parameters
        ----------
        symbol: str
            Symbol identifier for the Expansion API.
        df: bool
            True to return a pandas DataFrame.

        Returns
        -------
        data: dict
            Dictionary with the requested data.
        '''

        params = {
            'cod': symbol,
        }
        if year != None and month != None:
            params['anyo'] = year
            params['mes'] = month
        else:
            params['numeroh'] = 20

        url = f'{self.base_url}{self.bolsa_url}/datos/historico_mensual.html'
        r = self._request(url, params)
        
        data = r.json()
        if 'cotizaciones' in data['valor'] and df:
            data['valor']['cotizaciones'] = pd.DataFrame(data['valor']['cotizaciones'])

        return data

class Currencies(enum.Enum):
    EUR: str = 'zona-euro'
    GBP: str = 'uk'
    USD: str = 'usa'
    JPY: str = 'japon'
    AUD: str = 'australia'
    CAD: str = 'canada'
    NZD: str = 'nueva-zelanda'
    CHF: str = 'suiza'
    
class Expansion:
    
    BASE_URL: str = 'https://datosmacro.expansion.com'
    
    def __init__(self) -> None:
        pass
    
    def interestRates(self, currencies:list[Currencies], date_from:(str | dt.datetime)=None):
        
        if date_from != None and not isinstance(date_from, str):
            try:
                date_from: str = date_from.strftime('%Y-%m-%d')
            except:
                raise ValueError('In interestRates() the argument date_from must be either a string or a dt.datetime.')
        
        if not isinstance(currencies, list):
            currencies: list = [currencies]
        
        errors: list = []
        for c in currencies:
            if c not in Currencies.__members__.values():
                errors.append(c)
        if len(errors) > 0:
            raise ValueError(f"Las siguientes divisas no son válidas: {','.join(errors)}")
            
        data: list = []
        for currency in Currencies.__members__.values():
            url: str = f'{self.BASE_URL}/tipo-interes/{currency.value}'
        
            df: pd.DataFrame = pd.DataFrame(pd.read_html(url)[0])
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
            df.set_index('Fecha', inplace=True)
            df.sort_index(inplace=True)
            if date_from != None:
                df: pd.DataFrame = df.loc[date_from:].copy()
            df.columns = [currency.name]
            df[currency.name] = df[currency.name].str.replace(',', '.').str.rstrip('%').astype('float')
            
            data.append(df.copy())
        
        
        
        data: pd.DataFrame = pd.concat(data, axis=1, join='outer')
        data = data.reindex(pd.date_range(start=data.index.min(), end=dt.datetime.today(), freq='D'))
        data.fillna(method='ffill', inplace=True)
        
        return data


    
def getCorrelation(data:pd.DataFrame) -> float:
    
    if 'Diff' not in data:
        raise ValueError(f'Diff column is not in the dataframe given')
    if 'Price' not in data:
        raise ValueError(f'Price column is not in the dataframe given')
    
    correlation = data['Diff'].corr(data['Price'])
    
    return correlation

def plot(df:pd.DataFrame, curr1:str, curr2:str, corr:float) -> None:

    fig = make_subplots(rows=1, cols=1, specs=[[{'secondary_y': True}]])

    fig.add_trace(go.Scatter(x=df.index, y=df['Price'], name=f'{curr1}/{curr2}'), 
                    row=1, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=df.index, y=df['Diff'], name='Interest Rates'), 
                    row=1, col=1, secondary_y=True)

    fig.update_yaxes(title_text='Price ($)', row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text='Interest Rates Difference (%)', row=1, col=1, secondary_y=True)

    fig.update_xaxes(title_text='Date', row=1, col=1)
    fig.update_layout(title=f"Currency Pair vs. Interest Rates Difference (Correlation: {corr})", 
                        autosize=False, width=1000, height=700)

    fig.show()

def getRelation(data:pd.DataFrame, pair:str, show_plot:bool=True) -> float:
    
    curr1: str = pair[:3]
    curr2: str = pair[3:]
    
    if curr1 == curr2:
        return 1
    
    if curr1 not in df_tipos:
        raise ValueError(f'{curr1} is not in the dataframe given')
    if curr2 not in df_tipos:
        raise ValueError(f'{curr2} is not in the dataframe given')
    
    temp: pd.DataFrame = data[[curr1, curr2]].copy()
    temp['Diff'] = df_tipos[curr1] - df_tipos[curr2]
    temp['Price'] = yf.download(f'{pair}=X', start=temp.index.min(), 
                            end=temp.index.max(), progress=False)['Close']
    temp.dropna(inplace=True)
    
    correlation: float = temp['Diff'].corr(temp['Price'])
    
    if show_plot:
        plot(temp, curr1, curr2, correlation)

    return correlation

if __name__ == '__main__':

    import itertools
    import matplotlib.pyplot as plt
    

    exp = Expansion()
    df_tipos = exp.interestRates(currencies=list(Currencies.__members__.values()))


    pairs: list = list(itertools.product(*[Currencies.__members__.keys(), 
                                            Currencies.__members__.keys()]))

    correlations: dict = {}
    for pair in [f'{p[0]}{p[1]}' for p in pairs if p[0] != p[1]]:
        correlations[pair] = getRelation(df_tipos, pair, show_plot=False)
