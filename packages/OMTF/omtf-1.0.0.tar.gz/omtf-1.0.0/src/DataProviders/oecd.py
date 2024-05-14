
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

class OECD:

    headers = {'Content-type': 'application/json'}
    BASE_URL = 'https://stats.oecd.org/'
    DATA = 'SDMX-JSON/data/'

    def _request(self, url:str):

        # Post the data request to the BLS API. Return the resulting JSON structure.

        post = requests.post(url)#, headers=self.headers)
        print(post.text)
        data = json.loads(post.text)
        data_list = data['value']

        return data_list

    def indicators(self, key:str=None, df:bool=True):

        r = requests.get(self.BASE_URL)
        html = BeautifulSoup(r.text,'html.parser')

        data = html.find_all('ul', {'class':'treeview'})[0]
        lines = data.find_all('li')
        data = []
        for line in lines:
            available = line.find_all('a',{'class':'q'})
            if len(available) > 0:
                for a in available:
                    if a.has_attr('dscode'):
                        data.append({
                            'DataSet': a['dscode'],
                            'ID': int(a['qid']),
                            'Name': a.get_text(),
                        })

        return pd.DataFrame(data) if df else data

    def getData(self):

        freq = ['M','Q','S']
        agency_name = 'all'
        start = '2009-M2'
        end = '2011-M4'
        countries = 'all'
        dimensions = 'all'
        filter = countries
        dataset = ''
        query = f'{dataset}/{filter}/{agency_name}?startTime={start}&endTime={end}'
        data = self._request(self.BASE_URL+self.DATA+query)
        data = pd.DataFrame(data)



if __name__ == '__main__':
    
    
    'https://stats.oecd.org/SDMX-JSON/data/KEI/LOLITOAA.AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+NMEC+ARG+BRA+CHN+IND+IDN+RUS+SAU+ZAF.ST.M/all?startTime=2021-10&endTime=2023-01&dimensionAtObservation=allDimensions'
    'https://stats.oecd.org/restsdmx/sdmx.ashx/GetDataStructure/KEI'
    ind = OECD().indicators(df=True)
    ind

    import pandas as pd
    import datetime as dt
    import pandas_datareader.data as web

    start_time = dt.datetime(2000, 1, 1)
    end_time = dt.datetime(2022, 2, 1)
    df = web.DataReader('HISTPOP', 'oecd', start_time, end_time)
    df