
import copy
import datetime as dt
import os

import pandas as pd


class SP500:

    url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    current: pd.DataFrame = pd.DataFrame()
    changes: pd.DataFrame = pd.DataFrame()
    historical: pd.DataFrame = pd.DataFrame()
    cur_formated: bool = False
    cha_formated: bool = False
    his_formated: bool = False

    def __init__(self, path:str=None) -> None:

        self.path: str = path
        data: list = pd.read_html(self.url)
        self.current: pd.DataFrame = data[0]
        self.changes: pd.DataFrame = data[1]

    def _formatChanges(self) -> None:

        if not self.cha_formated:
        
            self.changes.columns = ['date', 'ticker_added','name_added', 'ticker_removed', 'name_removed', 'reason']
            self.changes['reason'] = self.changes['reason'].apply(lambda x: x.split('.[')[0]+'.')
            # Get additions
            additions: pd.DataFrame = self.changes[~self.changes['ticker_added'].isnull()][['date', 'ticker_added', 'name_added', 'reason']]
            additions.columns = [c.split('_')[0] for c in additions.columns]
            additions['action'] = 'added'
            # Get removements
            removals: pd.DataFrame = self.changes[~self.changes['ticker_removed'].isnull()][['date','ticker_removed','name_removed', 'reason']]
            removals.columns = [c.split('_')[0] for c in removals.columns]
            removals['action'] = 'removed'

            self.changes: pd.DataFrame = pd.concat([additions, removals])
            self.changes.loc[:, 'date'] = pd.to_datetime(self.changes['date'])
            self.changes.sort_values('date', inplace=True)

            self.cha_formated: bool = True

    def _formatCurrent(self) -> None:

        if not self.cur_formated:

            self._formatChanges()

            self.current.columns = ['ticker', 'name', 'sector', 'industry', 'location', 'date', 'cik', 'founded']
            # Fill and formet the data
            mask = self.current['date'].astype(str).str.strip().str.fullmatch('\d{4}-\d{2}-\d{2}')
            mask.loc[mask.isnull()] = False
            self.current.loc[mask == False, 'date'] = min(self.current['date'].astype(str).tolist() + self.changes['date'].astype(str).tolist())
            self.current.loc[:, 'date'] = pd.to_datetime(self.current['date'])
            self.current.loc[:, 'cik'] = self.current['cik'].apply(str).str.zfill(10)

            self.cur_formated: bool = True
    
    def _formatHistorical(self, add_only_removed:bool=False) -> None:
        
        if not self.his_formated:

            self._formatChanges()
            self._formatCurrent()

            # Add ticker which are in current but not in changes and those which have only been removed
            if add_only_removed:
                only_removed: list = []
                for g in self.changes.groupby('name'):
                    if len(g[1]['ticker'].unique()) > 1:
                        print(g[0], g[1])
                        g[1]['ticker'] = g[1]['ticker'].iloc[-1]
                    if g[1].iloc[0]['action'] == 'removed':
                        only_removed.append(g[1].iloc[0])

                missing: pd.DataFrame = pd.concat([self.current[~self.current['ticker'].isin(self.changes['ticker'])].copy(),
                                                pd.DataFrame(only_removed)])
            else:
                missing: pd.DataFrame = self.current[~self.current['ticker'].isin(self.changes['ticker'])].copy()

            missing['action'] = 'added'
            missing['reason'] = None
            missing['date'] = min([self.changes['date'].min(), self.current['date'].min()])
            missing.loc[:, 'cik'] = self.current['cik'].apply(str).str.zfill(10)
            missing: pd.DataFrame = missing[['date', 'ticker', 'name', 'reason', 'action', 'cik']]
            # Merge the additions and removals into one dataframe.
            self.historical: pd.DataFrame = pd.concat([self.changes, missing])
            self.historical['date'] = pd.to_datetime(self.historical['date'])

            self.his_formated: bool = True

    def getCurrent(self) -> pd.DataFrame:
        
        self._formatCurrent()

        return self.current

    def getChanges(self) -> pd.DataFrame:
        
        self._formatChanges()

        return self.changes

    def getHistorical(self) -> pd.DataFrame:
        
        self._formatHistorical()

        return self.historical

    def getTables(self):
        
        self._formatCurrent()
        self._formatHistorical()

        return self.current, self.changes, self.historical
    
    def getComponents(self) -> pd.DataFrame:
        
        historical: pd.DataFrame = self.getHistorical()
        index = pd.date_range(end=dt.datetime.today(), start=historical['date'].min())
        df = pd.DataFrame(index=index)
        df['tickers'] = [[]] * len(df)
        
        return df

    
    def saveTables(self) -> None:
        
        current: pd.DataFrame; changes: pd.DataFrame; historical: pd.DataFrame
        current, changes, historical = self.getTables()

        current.to_csv(os.path.join(self.path, 'current_SP500.csv'), mode='w', index=False)
        changes.to_csv(os.path.join(self.path, 'changes_SP500.csv'), mode='w', index=False)
        historical.to_csv(os.path.join(self.path, 'historical_SP500.csv'), mode='w', index=False)

    def getComponents(self) -> pd.DataFrame:
        
        # Leer el archivo CSV en un DataFrame
        if len([f for f in os.listdir(self.path) if 'current' in f]) > 0:
            current: pd.DataFrame = pd.read_csv(os.path.join(self.path, 'current_SP500.csv'))
        else:
            self._formatCurrent()

        if len([f for f in os.listdir(self.path) if 'historical' in f]) > 0:
            df: pd.DataFrame = pd.read_csv(os.path.join(self.path, 'historical_SP500.csv'))
        else:
            self._formatHistorical()
            
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Crear un diccionario para almacenar las acciones en cada fecha
        acciones_por_fecha: dict = {}
        index: set = set(current['ticker'])

        # Iterar a través de las filas del DataFrame
        for i in reversed(df.index):
            row = df.iloc[i]
            fecha = row['date']
            ticker = row['ticker']
            name = row['name']
            action = row['action']
            # Si la acción se añadió, la agregamos al conjunto de acciones en esa fecha
            if action == 'added':
                if f"{ticker}" in index:
                    index.remove(f"{ticker}")
                acciones_por_fecha[fecha] = copy.deepcopy(index)
            # Si la acción se eliminó, la eliminamos del conjunto de acciones en esa fecha
            elif action == 'removed':
                index.add(f"{ticker}")
                acciones_por_fecha[fecha] = copy.deepcopy(index)

        # Crear un DataFrame final con las fechas como índices y las acciones como columnas
        df_final: pd.DataFrame = pd.DataFrame.from_dict({k: ','.join(acciones_por_fecha[k]) for k in acciones_por_fecha}, orient='index')
        df_final.index.name = 'date'
        df_final.sort_index(inplace=True)
        df_final.columns = ['acciones']

        # Ordenar las columnas alfabéticamente
        df_final: pd.DataFrame = df_final.reindex(sorted(df_final.columns), axis=1)

        # Generamos el dataframe para todos los días
        fecha_inicio = df['date'].min()
        fecha_hoy: dt.datetime = dt.datetime.now().date()
        rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_hoy)
        resultado_df: pd.DataFrame = pd.DataFrame(index=rango_fechas, columns=['acciones'])
        resultado_df.index.name = 'date'
        resultado: pd.DataFrame = resultado_df.combine_first(df_final)
        resultado.ffill(inplace=True)

        return resultado


if __name__ == '__main__':

    download = False
    index : SP500 = SP500(path='utils')

    if download:
        index.saveTables()
        current: pd.DataFrame; changes: pd.DataFrame; historical: pd.DataFrame
        current, changes, historical = index.getTables()

    components = index.getComponents()

    components['tickers'] = components['acciones'].str.split(',')
    tickers = list(dict.fromkeys([i for e in components['tickers'] for i in e]))
    dates = {}
    for ticker in tickers:
        temp = components[components['acciones'].str.contains(ticker)].index
        dates[ticker] = {
            'init': temp.min(),
            'final': temp.max(),
        }

    import yfinance as yf

    temp: list = []
    delisted: list = []
    for ticker in dates:
        try:
            ticker_data: pd.DataFrame = yf.Ticker(ticker).history(interval='1d', start=dates[ticker]['init'].strftime('%Y-%m-%d'), end=dates[ticker]['final'].strftime('%Y-%m-%d'), raise_errors=True)
            ticker_data['Ticker'] = ticker
            temp.append(ticker_data)
        except:
            print(ticker)
            delisted.append(ticker)
    df = pd.concat(temp)

    first_date = df.groupby(df.index).count()
    first_date = first_date[first_date['Open'] > 490].index[0]

    rank_data = df.reset_index(drop=False)
    rank_data = rank_data[rank_data['Date'] > first_date]
    rank_data

    import sqlite3

    conn = sqlite3.connect('sp500.db')
    rank_data.to_sql('price', conn, if_exists='replace', index=False)