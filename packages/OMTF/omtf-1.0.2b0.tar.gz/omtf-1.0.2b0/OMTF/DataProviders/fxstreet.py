
import enum
import datetime as dt
import requests
import pandas as pd

from data import DataProvider

class FXStreet(DataProvider):

    class Volatility(enum.Enum):
        NONE: str = 'NONE'
        LOW: str = 'LOW'
        MEDIUM: str = 'MEDIUM'
        HIGH: str = 'HIGH'
    
    class Category(enum.Enum):
        BONDAUCTIONS: str = '8896AA26-A50C-4F8B-AA11-8B3FCCDA1DFD'
        CAPITALFLOWS: str = 'FA6570F6-E494-4563-A363-00D0F2ABEC37'
        CENTRALBANKS: str = 'C94405B5-5F85-4397-AB11-002A481C4B92'
        CONSUMPTION: str = 'E229C890-80FC-40F3-B6F4-B658F3A02635'
        ECONOMICACTIVITY: str = '24127F3B-EDCE-4DC4-AFDF-0B3BD8A964BE'
        ENERGY: str = 'DD332FD3-6996-41BE-8C41-33F277074FA7'
        HOLIDAYS: str = '7DFAEF86-C3FE-4E76-9421-8958CC2F9A0D'
        HOUSINGMARKET: str = '1E06A304-FAC6-440C-9CED-9225A6277A55'
        INFLATION: str = '33303F5E-1E3C-4016-AB2D-AC87E98F57CA'
        INTERESTRATES: str = '9C4A731A-D993-4D55-89F3-DC707CC1D596'
        LABORMARKET: str = '91DA97BD-D94A-4CE8-A02B-B96EE2944E4C'
        POLITICS: str = 'E9E957EC-2927-4A77-AE0C-F5E4B5807C16'

    class Country(enum.Enum):
        UNITEDSTATES = 'US'
        UNITEDKINGDOM = 'UK'
        EUROPEANMONETARYUNION = 'EMU'
        GERMANY = 'DE'
        CHINA = 'CN'
        JAPAN = 'JP'
        CANADA = 'CA'
        AUSTRALIA = 'AU'
        NEWZEALAND = 'NZ'
        SWITZERLAND = 'CH'
        FRANCE = 'FR'
        ITALY = 'IT'
        SPAIN = 'ES'
        UKRAINE = 'UA'
        INDIA = 'IN'
        RUSSIA = 'RU'
        TURKEY = 'TR'
        SOUTHAFRICA = 'ZA'
        BRAZIL = 'BR'
        SOUTHKOREA = 'KR'
        INDONESIA = 'ID'
        SINGAPORE = 'SG'
        MEXICO = 'MX'
        SWEDEN = 'SE'
        NORWAY = 'NO'
        DENMARK = 'DK'
        GREECE = 'GR'
        PORTUGAL = 'PT'
        IRELAND = 'IE'
        AUSTRIA = 'AT'
        BELGIUM = 'BE'
        NETHERLANDS = 'NL'
        FINLAND = 'FI'
        CZECHREPUBLIC = 'CZ'
        POLAND = 'PL'
        HUNGARY = 'HU'
        ROMANIA = 'RO'
        CHILE = 'CL'
        COLOMBIA = 'CO'
        ARGENTINA = 'AR'
        ICELAND = 'IS'
        HONGKONG = 'HK'
        SLOVAKIA = 'SK'
        ISRAEL = 'IL'
        SAUDIARABIA = 'SA'
        VIETNAM = 'VN'
        KUWAIT = 'KW'
        EGYPT = 'EG'
        UNITEDARABEMIRATES = 'AE'
        QATAR = 'QA'
        THAILAND = 'TH'

    class Version(enum.Enum):
        V1: str = 'v1'
        V2: str = 'v2'
        
    class TokenGrant(enum.Enum):
        DOMAIN: str = 'domain'
        CLIENT: str = 'client_credentials'
    
    def __init__(self, culture:str='es', version:Version=Version.V1) -> None:
        
        self.culture: str= culture
        self.version: str = version.value
        self.getToken()
        
    def __post(self, url:str, params:dict=None, headers:dict=None) -> dict:
        
        self.r = requests.post(url=url, data=params, headers=headers)
        return self.r.json()
    
    def __get(self, url:str, params:dict=None, headers:dict=None) -> dict:
        
        self.r = requests.get(url=url, params=params, headers=headers)
        return self.r.json()
        
    def getToken(self, client_id:str=None, client_secret:str=None, 
                 grant_type:TokenGrant=TokenGrant.DOMAIN, version:Version=Version.V2) -> None:
        
        params = {'grant_type': grant_type.value}
        if version == self.Version.V1:
            url: str = 'https://authorization.fxstreet.com/token'
        elif version == self.Version.V2:
            url: str = 'https://authorization.fxstreet.com/v2/token'
            params['scope'] = 'calendar'
            
        if client_id != None:
            params['client_id'] = client_id
        if client_secret != None:
            params['client_secret'] = client_secret
        
        current_time = dt.datetime.now()
        self.token: dict = self.__post(url=url, params=params, 
                                       headers={'Origin':'https://www.fxstreet.es'})
        self.token['creation'] = current_time
        self.authorization: str = self.token['token_type'] + ' ' + self.token['access_token']
        
    def getCategories(self, df:bool=False) -> (list | pd.DataFrame):
        
        '''
        start format: 2024-02-20T07:37:56Z
        end format: 2024-02-22T09:37:56Z
        '''
        
        url: str = f'https://calendar-api.fxstreet.com/{self.culture}/api/{self.version}/categories'
        headers: dict = {
            'Authorization': self.authorization,
            'Accept': 'application/json',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        
        data: dict = self.__get(url=f'{url}', headers=headers)
        
        return pd.DataFrame(data) if df else data
        
    def getCalendar(self, start:str=None, end:str=None, countries:list=None, categories:list=None, 
                    volatilities:list=None, df:bool=False) -> (list | pd.DataFrame):
        
        '''
        start format: 2024-02-20T07:37:56Z
        end format: 2024-02-22T09:37:56Z
        '''
        
        url: str = f'https://calendar-api.fxstreet.com/{self.culture}/api/{self.version}/eventDates/{start}/{end}'
        headers: dict = {
            'Authorization': self.authorization,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        volatilities = '&'.join([f'volatilities={v}' for v in volatilities]) if volatilities != None else ''
        countries = '&'.join([f'countries={v}' for v in countries]) if countries != None else ''
        categories = '&'.join([f'categories={v}' for v in categories]) if categories != None else ''
        filters: str = '&'.join([volatilities, countries, categories])
        
        data: dict = self.__get(url=f'{url}?{filters}', headers=headers)
        
        return pd.DataFrame(data) if df else data
    
    
    
if __name__ == '__main__':
    
    
    fx = FXStreet()
    last_day = (dt.datetime.today() - dt.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    countries: list = FXStreet.Country.__members__.keys()
    categories: list = FXStreet.Category.__members__.keys()
    volatilities: list = FXStreet.Volatility.__members__.keys()
    calendar = fx.getCalendar(start='2010-01-01T00:00:01Z', end=last_day, countries=countries, 
                              categories=categories, volatilities=volatilities)
    
    cal_df = pd.DataFrame(calendar)

    events: list = []
    for event in cal_df.groupby('eventId'):
        events.append(
            {
                'eventId': event[0], 
                'periodType': event[1]['periodType'].iloc[-1],
                'name': event[1]['name'].iloc[-1],
                'countryCode': event[1]['countryCode'].iloc[-1],
                'unit': event[1]['unit'].iloc[-1],
                'potency': event[1]['potency'].iloc[-1],
                'isSpeech': event[1]['isSpeech'].iloc[-1],
                'isAllDay': event[1]['isAllDay'].iloc[-1],
                'isReport': event[1]['isReport'].iloc[-1],
            }
        )
    
    COUNTRY_CODES_FILTER_OPTIONS: dict = {v.value: k for k, v in dict(FXStreet.Country.__members__).items()}
    countries: list = []
    for country in cal_df.groupby('countryCode'):
        countries.append(
            {
                'code': country[0],
                'name': COUNTRY_CODES_FILTER_OPTIONS[country[0]],
            }
        )
        
    currencies: list = []
    for currency in cal_df.groupby('currencyCode'):
        currencies.append(
            {
                'code': currency[0],
                'name': '',
            }
        )
        
    values: list = []
    for value in cal_df.groupby('id'):
        values.append(
            {
                'id': value[0],
                'dateUtc': value[1]['dateUtc'].iloc[-1],
                'periodDateUtc': value[1]['periodDateUtc'].iloc[-1],
                'currencyCode': value[1]['currencyCode'].iloc[-1],
                'actual': value[1]['actual'].iloc[-1],
                'revised': value[1]['revised'].iloc[-1],
                'consensus': value[1]['consensus'].iloc[-1],
                'ratioDeviation': value[1]['ratioDeviation'].iloc[-1],
                'previous': value[1]['previous'].iloc[-1],
                'isBetterThanExpected': value[1]['isBetterThanExpected'].iloc[-1],
                'volatility': value[1]['volatility'].iloc[-1],
                'isTentative': value[1]['isTentative'].iloc[-1],
                'isPreliminary': value[1]['isPreliminary'].iloc[-1],
                'lastUpdated': value[1]['lastUpdated'].iloc[-1],
                'previousIsPreliminary': value[1]['previousIsPreliminary'].iloc[-1],
            }
        )
        