
import datetime as dt
import json
from random import choice

import pandas as pd
import requests
from bs4 import BeautifulSoup

from data import DataProvider


class MarketWatch(DataProvider):

    payload: dict = {
        "Step": "P1D",
        "TimeFrame":"P1Y", 
        "StartDate":1650412800000,
        "EndDate":1681948800000,
        "EntitlementToken": "cecc4267a0194af89ca343805a3e57af",
        "IncludeMockTick": True,
        "FilterNullSlots": False,
        "FilterClosedPoints": True,
        "IncludeClosedSlots": False,
        "IncludeOfficialClose": True,
        "InjectOpen": False,
        "ShowPreMarket": False,
        "ShowAfterHours": False,
        "UseExtendedTimeFrame": True,
        "WantPriorClose": False,
        "IncludeCurrentQuotes": False,
        "ResetTodaysAfterHoursPercentChange": False,
        "Series": [
            {
                "Key": "STOCK/US/XNAS/CJJD", # XNYS
                "Dialect":"Charting",
                "Kind":"Ticker",
                "SeriesId":"s1",
                "DataTypes": ["Open","High","Low","Last"],
                "Indicators": [
                    {
                        "Parameters": [],
                        "Kind": "Volume",
                        "SeriesId": "i2"
                    },
                    # {
                    #     "Parameters": [
                    #         {"Name":"Period","Value":"50"}
                    #     ],
                    #     "Kind":"SimpleMovingAverage",
                    # "SeriesId":"i3"
                    # },
                    # {
                    #     "Parameters": [
                    #         {"Name":"EMA1","Value":12},
                    #         {"Name":"EMA2","Value":26},
                    #         {"Name":"SignalLine","Value":9}
                    #     ],
                    #     "Kind": "MovingAverageConvergenceDivergence",
                    #     "SeriesId":"i4"
                    # },
                    {
                        "Parameters": [
                            {"Name":"YearOverYear"}
                        ],
                        "Kind": "EarningsEvents", 
                        "SeriesId":"i5"
                    },
                    {
                        "Parameters": [],
                        "Kind":"DividendEvents",
                        "SeriesId":"i6"
                    },
                    {
                        "Parameters":[],
                        "Kind":"SplitEvents",
                        "SeriesId":"i7"
                    },
                    {
                        "Parameters": [
                            {"Name":"DocTypes","Value":"102"},
                            {"Name":"DocTypes","Value":"103"},
                            {"Name":"DocTypes","Value":"115"},
                            {"Name":"DocTypes","Value":"424"},
                            {"Name":"DocTypes","Value":"425"},
                            {"Name":"DocTypes","Value":"426"},
                            {"Name":"DocTypes","Value":"427"},
                            {"Name":"Significance Flag","Value":"None"}
                        ],
                        "Kind":"NewsDensity",
                        "SeriesId":"i8"
                    }
                ]
            }
        ]
    }

    def _request(self, url:str, headers:dict=None, params:dict=None, json:bool=True
                 ) -> (list | dict | requests.Response):

        if headers != None:
            headers: dict = {**headers, **self._random_header()}
        
        self.r: requests.Response = requests.get(url, headers=headers,params=params)

        return self.r.json() if json else self.r
        
    def getData(self, symbol:str, step:str='P1D', timeframe:str='P1Y',
                start:str=None, end:str=None, premarket:bool=True, afterhours:bool=True,
                ckey:str='cecc4267a0') -> (dict | pd.DataFrame):
        
        payload = self.payload.copy()
        if start != None:
            payload['StartDate'] = dt.datetime.timestamp(dt.datetime.strptime(start))
        if end != None:
            payload['EndDate'] = dt.datetime.timestamp(dt.datetime.strptime(start))

        headers: dict = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
            'Host': 'api-secure.wsj.net',
            'Origin': 'https://www.marketwatch.com',
            'Referer': f'https://www.marketwatch.com/investing/stock/{symbol}',
        }

        url: str = 'https://api-secure.wsj.net/api/michelangelo/timeseries/history'
        
        data = self._request(url=url, headers=headers, 
                             params={'json': json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
                                'ckey': ckey})
        print(data)
        df: pd.DataFrame = pd.DataFrame()
        df['Time'] = data['TimeInfo']['Ticks']
        df['DateTime'] = pd.to_datetime(df['Time'], unit='ms')
        df.set_index(keys='DateTime', inplace=True)
        df: pd.DataFrame = df.tz_localize(tz='UTC')#dt.datetime.now(dt.timezone.utc).astimezone().tzinfo)
        df: pd.DataFrame = df.tz_convert('America/New_York')
        for s in data['Series']:
            df[s['DesiredDataPoints']] = s['DataPoints']
        df.rename(columns={'Last':'Close'}, inplace=True)

        if premarket or afterhours:
            data: dict = {'Total':df}
            if premarket:
                data['PM'] = df.between_time('00:00', '09:30')
            if afterhours:
                data['AH'] = df.between_time('16:00', '23:59')
        else:
            data = df.copy()

        return data


    def getQuote(self, symbols:list):
        
        params: dict = {
            'dialect': 'official',
            'needed': 'CompositeTrading|BluegrassChannels',
            'MaxInstrumentMatches': '1',
            'accept': 'application/json',
            'EntitlementToken': 'cecc4267a0194af89ca343805a3e57af',
            'ckey': 'cecc4267a0',
            'dialects': 'Charting',
            'id': ','.join([f'Stock-US-{s}' for s in symbols])
        }
        
        headers: dict = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'api.wsj.net',
            'Origin': 'https://www.marketwatch.com',
            'Referer': f'https://www.marketwatch.com/investing/stock/{symbols[0]}',
        }

        url: str = 'https://api.wsj.net/api/dylan/quotes/v2/comp/quoteByDialect'
        
        quote = self._request(url=url, headers=headers, params=params)
        
        return quote

    def getPremarket(self) -> dict:

        headers: dict = {
            'Origin': 'https://www.marketwatch.com',
        }
        url: str = 'https://www.marketwatch.com/tools/screener/premarket'

        r: requests.Response = self._request(url=url, headers=headers, json=False)
        html: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')

        tables: set = html.find_all('table' ,{'class':'table table--overflow align--right'})

        dfs: list = []
        for table in tables:
            columns: list = [[c for c in i.contents if c != '\n'][0].get_text() for i in table.find_all('th')]
            data: list = [[cell.get_text().replace('\n', '') for cell in row.find_all('td')] \
                    for row in table.find_all('tr')][1:]
            df: pd.DataFrame = pd.DataFrame(columns=columns, data=data)
            df['Symbol'] = df['Symbol'].apply(lambda x: x[:int(len(x)/2)])
            dfs.append(df)
        dfs: dict = {
            'Gainers': dfs[0],
            'Losers': dfs[1],
            'Active': dfs[2]
        }

        return dfs
    
    

if __name__ == '__main__':

    mw = MarketWatch()
    premarket = mw.getPremarket()