
import enum
import time
import requests
import numpy as np
import pandas as pd

class CoordinatesType(enum.Enum):
    DECIMAL: str = 'DECIMAL'
    DMS: str = 'DMS'

class AEMET:
        
    BASE_URL: str = 'https://opendata.aemet.es/opendata'
    API_KEY: str = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkY2Fyb25tQGdtYWlsLmNvbSIsImp0aSI6ImMzYTgzM2E4LTIxOTctNDZhZi04YjZiLTU3NDk5NDJmNTc1YiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzEwODM4MzAzLCJ1c2VySWQiOiJjM2E4MzNhOC0yMTk3LTQ2YWYtOGI2Yi01NzQ5OTQyZjU3NWIiLCJyb2xlIjoiIn0.fx6e-NSDgDC7FC5ulpt6fmLjHA2o8V7BZZNOdm8yU54'

    def __init__(self, api_key:str=None, wait:bool=True) -> None:

        '''
        Performs the request of type GET.

        Parameters
        ----------
        api_key: str
            Token for the OpenData API.
        wait: bool
            True to wait between calls so that we are not banned.
        '''

        if api_key != None:
            self.API_KEY: str = api_key
        self.wait: bool = wait
            
    def _request(self, url:str, params:dict=None, headers:dict=None):

        '''
        Performs the request of type GET.

        Parameters
        ----------
        url: str
            URL to make the request.
        params: dict
            Dictionary containing the request parameters.
        headers: dict
            Headers to pass in the request.

        Returns
        -------
        result: list | dict
            Contains the requested data.
        '''
        
        if params != None: 
            params: dict = { **params, **{'api_key': self.API_KEY}}
        else: 
            params: dict = {'api_key': self.API_KEY}
        
        self.r: requests.Response = requests.get(url, headers=headers, params=params)
        temp: dict = self.r.json()
        if temp['estado'] != 200:
            raise ValueError(f"{temp['estado']} ERROR: {temp['descripcion']}")
        self.data: requests.Response = requests.get(url=temp['datos'])
        
        if self.wait:
            time.sleep(60/60)
        
        return self.data.json()
    
    @staticmethod
    def dmsToDecimal(coordenada):
        
        # Extraer partes de la coordenada en formato DMS
        grados = float(coordenada[:2])
        minutos = float(coordenada[2:4])
        segundos = float(coordenada[4:6])
        direccion = coordenada[-1]  # 'N' para Norte, 'S' para Sur, 'E' para Este, 'W' para Oeste

        # Calcular el valor decimal
        decimal = grados + (minutos / 60) + (segundos / 3600)

        # Ajustar el signo según la dirección
        if direccion in ['S', 'W']:
            decimal = -decimal

        return decimal
    
    @staticmethod
    def geographicalDistance(lat_asset:float, long_asset:float, lat_station:float, 
                long_station:float) -> float:

        R = 6371 # Earth radius
        # Conversion to radians
        d_lat = np.radians(float(lat_station)-float(lat_asset))
        d_lon = np.radians(float(long_station)-float(long_asset))
        r_lat1 = np.radians(float(lat_asset))
        r_lat2 = np.radians(float(lat_station))
        # Haversine formula
        a = np.sin(d_lat/2.) **2 + \
            np.cos(r_lat1) * np.cos(r_lat2) * np.sin(d_lon/2.)**2
        # Calculate distance between two points
        haversine = 2 * R * np.arcsin(np.sqrt(a))

        return haversine
            
    def getStations(self, coordinates:CoordinatesType=CoordinatesType.DECIMAL, 
                    df:bool=True) -> (list | pd.DataFrame):
            
        url: str = f"{self.BASE_URL}/api/valores/climatologicos/inventarioestaciones/todasestaciones/"

        headers: dict = {
            'cache-control': 'no-cache'
        }

        data = self._request(url, headers=headers)
        
        data: pd.DataFrame = pd.DataFrame(data)
        if coordinates == CoordinatesType.DECIMAL:
            data['latitud'] = data['latitud'].apply(self.dmsToDecimal)
            data['longitud'] = data['longitud'].apply(self.dmsToDecimal)
        
        return data if df else data.to_dict('records')
            
    def getNearestStation(self, lat:float, lon:float, 
                          coordinates:CoordinatesType=CoordinatesType.DECIMAL) -> dict:
            
        stations: pd.DataFrame = self.getStations(coordinates=coordinates, df=True)
        stations['distance'] = stations.apply(lambda x: self.geographicalDistance(lat, lon, x['latitud'], x['longitud']), axis=1)
        
        return stations[stations['distance'].abs() == stations['distance'].abs().min()].to_dict('records')[0]
    
    def _checkDate(self, date:str) -> str:
        
        if isinstance(date, str):
            if 'T' in date and len(date.split(':')) == 3 and len(date.split('-')) == 3:
                return date
            elif 'T' in date and len(date.split('T')[1].split(':')) != 3:
                raise ValueError('The format must be: YYYY-MM-DDTHH:MM:SSUTC')
            elif 'T' not in date and len(date.split('-')) == 3:
                date: str = date+'T00:00:00UTC'
            else:
                raise ValueError('The date must be a string with this format: YYYY-MM-DDTHH:MM:SSUTC')
        else:
            raise ValueError('The date must be a string with this format: YYYY-MM-DDTHH:MM:SSUTC')
        
        return date
        
    def getStationDailyData(self, start:str, end:str, station:str, df:bool=True) -> (list | pd.DataFrame):
        
        start: str = self._checkDate(start)
        end: str = self._checkDate(end)
            
        url: str = f"{self.BASE_URL}/api/valores/climatologicos/diarios/datos/fechaini/{start}/fechafin/{end}/estacion/{station}"

        headers: dict = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        data = self._request(url, headers=headers)
        data: pd.DataFrame = pd.DataFrame(data)
        for c in ['altitud', 'tmed', 'prec', 'tmin', 'tmax', 'dir', 'velmedia', 
                'racha', 'hrMedia', 'presMin', 'presMax', 'hrMax', 'hrMin']:
            if c in data.columns:
                data[c] = pd.to_numeric(data[c].str.replace(',','.'), errors='coerce')
        
        data.fillna(0, inplace=True)
        
        return data if df else data.to_dict('records')
        
    def getStationMonthlyData(self, start:str, end:str, station:str, df:bool=True) -> (list | pd.DataFrame):
            
        url: str = f"{self.BASE_URL}/api/valores/climatologicos/mensualesanuales/datos/anioini/{start}/aniofin/{end}/estacion/{station}"

        headers: dict = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        data = self._request(url, headers=headers)
        data: pd.DataFrame = pd.DataFrame(data)
        for c in ['n_cub', 'hr', 'nw_55', 'tm_min', 'ts_min', 
                'nt_30', 'n_des', 'np_100', 'n_nub', 'nw_91', 'np_001',
                'w_rec', 'e', 'np_300', 'p_mes', 'w_med', 'nt_00', 'ti_max',
                'tm_mes', 'tm_max', 'np_010']:
            if c in data.columns:
                data[c] = pd.to_numeric(data[c].str.replace(',','.'), errors='coerce')
        
        data.fillna(0, inplace=True)
        
        return data if df else data.to_dict('records')


if __name__ == '__main__':
    
    aemet = AEMET()
    station = aemet.getNearestStation(lat=42, lon=2, coordinates=CoordinatesType.DECIMAL)
    
    start = '2019-04-01T00:00:00UTC'
    end = '2023-12-31T23:59:59UTC'
    data = aemet.getStationDailyData(start=start, end=end, station=station['indicativo'])

    summary: list = []
    for g in data.groupby([pd.to_datetime(data['fecha']).dt.year]):
        
        summary.append({
            'station': station,
            'year': g[0][0],
            'temperature' : g[1]['tmed'].mean() if 'tmed' in g[1] else 0,
            'precipitation' : g[1]['prec'].mean() if 'prec' in g[1] else 0,
            'windSpeed' : g[1]['velmedia'].mean() if 'velmedia' in g[1] else 0,
            'humidity' : g[1]['hrMedia'].mean() if 'hrMedia' in g[1] else 0,
            'presion' : (g[1]['presMin'].mean() + g[1]['presMax'].mean()) / 2 if 'presMax' in g[1] and 'presMin' in g[1] else 0
        })