
import enum
import requests
import pandas as pd

import pandas as pd

class PoblationStyle(enum.Enum):
    
    SHORT: str = 'SHORT'
    MEDIUM: str = 'MEDIUM'
    LONG: str = 'LONG'
    FULL: str = 'FULL'

class GeoNames:
    
    BASE_URL: str = 'http://api.geonames.org/'
    
    def __init__(self, username:str='onemade') -> None:
        
        self.username: str = username
        
    def _request(self, url:str, params:dict=None, headers:dict=None) -> (list | dict):
        params: dict = {**params, **{'username': 'onemade'}}
        self.r: requests.Response = requests.get(url, params=params, headers=headers)
        return self.r.json()
    
    def getPostalCodeCountries(self, df:bool=True) -> (list | pd.DataFrame):
        
        url: str = f'{self.BASE_URL}postalCodeCountryInfoJSON'
        data = self._request(url)['geonames']
        
        return pd.DataFrame(data) if df else data
    
    def getCountryByLocation(self, latitud:float, longitud:float, radius:float=None) -> dict:
        
        url: str = f'{self.BASE_URL}countrySubdivisionJSON'
        params: dict = {
            'lat': latitud,
            'lng': longitud
        }
        
        return self._request(url, params=params)
                             
    def searchPostalCode(self, postal_code:(int|str), country_code:str='ES', 
                        style:PoblationStyle=PoblationStyle.MEDIUM, df:bool=True) -> (list | pd.DataFrame):
        
        url: str = f'{self.BASE_URL}postalCodeSearchJSON'
        params: dict = {
            'postalcode': postal_code,
        }
        if country_code != None:
            url: str = f'{self.BASE_URL}postalCodeLookupJSON'
            params['country'] = country_code
        if style != None:
            params['style'] = style.value
        
        data = self._request(url, params=params)['postalCodes']
        data: pd.DataFrame = pd.DataFrame(data).sort_values('population', ascending=False)
        
        return data if df else data.to_dict('records')
                             
    def searchNearPopulation(self, latitud:float, longitud:float, radius:float=None, max_rows:int=10, 
                             style:PoblationStyle=PoblationStyle.MEDIUM, local_country:bool=True, 
                             df:bool=True) -> (list | pd.DataFrame):
        
        url: str = f'{self.BASE_URL}findNearbyPlaceNameJSON'
        params: dict = {
            'lat': latitud,
            'lng': longitud,
            'radius': radius,
            'maxRows': max_rows,
            'localCountry': local_country,
        }
            
        if style != None:
            params['style'] = style.value
        
        data = self._request(url, params=params)['geonames']
        
        return pd.DataFrame(data) if df else data
    
    def searchNearWeather(self, latitud:float, longitud:float, radius:float=None, df:bool=True
                          ) -> (list | pd.DataFrame):
        
        url: str = f'{self.BASE_URL}findNearByWeatherJSON'
        params: dict = {
            'lat': latitud,
            'lng': longitud,
            'radius': radius,
        }
        
        data = self._request(url, params=params)['weatherObservation']
        
        return pd.DataFrame(data) if df else data



if __name__ == '__main__':
    
    geo = GeoNames('onemade')
    locations = geo.searchNearPopulation(latitud=40.678000000000004, longitud=-3.6189999999999998)