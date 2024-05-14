
import datetime as dt

import certifi
import pandas as pd
import urllib3
from bs4 import BeautifulSoup

from data import DataProvider


class FloatChecker(DataProvider):

    # Urls and device to connect
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/58.0.3029.110 Safari/537.36 '
    }
    BASE_URL: str = 'https://www.floatchecker.com/'

    def filterTicker(self,ticker:str) -> dict:

        url: str = self.BASE_URL + f'stock?float={ticker}'
        
        # Nos conectamos y procesamos los datos
        page: urllib3.PoolManager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where()) \
                                    .urlopen('GET',url,headers=self._random_header())
        soup: BeautifulSoup = BeautifulSoup(page.data,'html.parser')
        tabl: set = soup.find_all('div',{"class":"fctab__content"})

        data: dict = {
            'Float':{},
            'Short':{},
            'Outstanding':{}
        }
        for t in tabl:

            # Store data
            head: list = ['Date'] + [i.find_all('img')[0]['alt'].replace(' Icon','') for i in t.find_all('th') 
                                if len(i.find_all('img')) > 0]
            rows: list = [i.get_text() for i in t.find_all('td')]

            dtype: str = t.find_all('th')[1].find_all('img')[0]['title'].split(head[1]+' ')[1].split(' ')[0]

            data[dtype] = {}
            for col in head:
                data[dtype][col] = []

            # Create DataFrame
            c = -1
            prev_it: float = 0
            for i,value in enumerate(rows):
                c = c+1 if i//len(head) == prev_it else 0
                data[dtype][head[c]].append(value)
                prev_it = i//len(head)
            data[dtype] = pd.DataFrame(data[dtype])

            # Format dates
            data[dtype]['Date'] = data[dtype]['Date'].replace({'Jan.':'January','Feb.':'February',
                                                                'Sept.':'September','Oct.':'October',
                                                                'Nov.':'November','Dec.':'December'}, regex=True)
            dates: list = []
            for d in data[dtype]['Date'].tolist():
                dates.append(dt.datetime.strptime(d,'%B %d %Y'))
            data[dtype]['Date'] = dates
            #data[dtype]['Date'] = pd.to_datetime(data[dtype]['Date'], format='%b %d %Y')

            # Format data
            for c in data[dtype].columns[1:]:
                data[dtype][c] = data[dtype][c].replace({'N/A': '0', '-': '0'})
                data[dtype][c] = data[dtype][c].replace({'K': '*1e3', 'k': '*1e3', 'Mil': '*1e6', 'M': '*1e6', 'B': '*1e9', '%': '*1e-2'}, regex=True).map(pd.eval).astype(float)

        return data



if __name__ == '__main__':

    print(FloatChecker().filterTicker('MULN'))