
import json
import requests
import pandas as pd

from bs4 import BeautifulSoup


class WorldPopulation:
    
    BASE_URL: str = 'https://worldpopulationreview.com/'
    
    def getCountries(self, df:bool=True) -> (list | pd.DataFrame):
        
        url: str = f'{self.BASE_URL}countries'
        self.r = requests.get(url)
        html = BeautifulSoup(self.r.content,'html.parser')
                
        temp: str = [e for e in html.find_all('script') if 'self.__next_f.push(' in e.get_text()][-5] \
                .get_text().replace('self.__next_f.push(', '')[:-1]
        
        data: list = json.loads(json.loads(temp)[1][2:])[0][3]['children'][0][3]['children'][0][3]['children'][1][3]['data']
        
        return pd.DataFrame(data) if df else data
    
    def getCountry(self, country:str='spain', df:bool=True):
        
        url: str = f'{self.BASE_URL}countries/cities/{country.lower().replace(' ', '-')}'
        self.r = requests.get(url)
        html = BeautifulSoup(self.r.content,'html.parser')
        
        return html
    
    def getCountryCities(self, country:str='spain', df:bool=True) -> (list | pd.DataFrame):
        
        url: str = f'{self.BASE_URL}countries/{country.lower().replace(' ', '-')}-population'
        self.r = requests.get(url)
        html = BeautifulSoup(self.r.content,'html.parser')

        table = html.find('table', {'class': 'tp-table-body'})
        head = [e.get_text() for e in table.find('thead').find_all('th')]
        rows = [[c.get_text() for c in r.find_all('th')]+[c.get_text() for c in r.find_all('td')] for r in table.find_all('tr')]
        data = pd.DataFrame(rows, columns=head)
        
        return data if df else data.to_dict('records')
    
    def getCountryTopCities(self, country:str='spain', df:bool=True) -> (list | pd.DataFrame):
        
        url: str = f'{self.BASE_URL}countries/{country.lower().replace(' ', '-')}-population'
        self.r = requests.get(url)
        html = BeautifulSoup(self.r.content,'html.parser')

        temp: str = [e for e in html.find_all('script') if 'self.__next_f.push(' in e.get_text()][-2] \
                .get_text().replace('self.__next_f.push(', '')[:-1]
        data: list = json.loads(json.loads(temp)[1][2:])[0][3]['children'][0][3]['children'][0][3]['children'][1][3]['cities']
        
        return pd.DataFrame(data) if df else data
        
