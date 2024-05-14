
import requests
import numpy as np
import pandas as pd


class OpenStreetMap:
    
    BASE_URL: str = 'https://nominatim.openstreetmap.org/'
    
    def getCityByPostalCode(self, postal_code:int, country:str='Spain', 
                            df:bool=True) -> (list | pd.DataFrame):
        
        url: str = f"{self.BASE_URL}search"
        params: dict = {
            'postalcode': postal_code,
            'country': 'Spain',
            'format': 'jsonv2',
            'addressdetails': 1,
        }
        response: requests.Response = requests.get(url, params=params)
        data = response.json()
        
        return pd.DataFrame(data) if df else data
    
    def getCityByCoordinates(self, latitud:float, longitud:float, 
                             df:bool=True) -> (list | pd.DataFrame):
    
        url: str = f'{self.BASE_URL}reverse.php'
        params: dict = {
            'lat': latitud,
            'lon': longitud,
            'zoom': 18,
            'format': 'jsonv2',
            'addressdetails': 1
        }
        response: requests.Response = requests.get(url, params=params)
        data = response.json()
        
        return pd.DataFrame(data) if df else data
    
    def getCityByName(self, city:str, country:str='Spain', df:bool=True) -> (list | pd.DataFrame):
    
        url: str = f'{self.BASE_URL}search'
        params: dict = {
            'city': city,
            'country': country,
            'format': 'jsonv2',
            'addressdetails': 1
        }
        response: requests.Response = requests.get(url, params=params)
        data = response.json()
        
        return pd.DataFrame(data) if df else data
    
if __name__ == '__main__':
    
    postal_code: int = 28294
    
    osm: OpenStreetMap = OpenStreetMap()
    data = osm.getCityByPostalCode(postal_code=postal_code, country='Spain')
    city = osm.getCityByName(city='Madrid')
    