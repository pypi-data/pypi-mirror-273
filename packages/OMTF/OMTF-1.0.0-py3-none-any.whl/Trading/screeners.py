
import enum
import numpy as np
import pandas as pd

from portfolios import CustomPortfolioWeighting, Markowitz, VolatType

    
class Frequency(enum.Enum):
    YEARLY: str = 'yearly'
    MONTHLY: str = 'monthly'
    WEEKLY: str = 'weekly'
    DAILY: str = 'daily'
    
class Screener:
    
    def __init__(self, data:pd.DataFrame, filters:list=[], asset_column:str='Ticker', 
                 date_column:str='DateTime', errors:bool=True) -> None:
        
        '''
        data: pd.DataFrame
            DataFrame with the needed data.
        asset_column: str
            Name of the column where the asset names are stored.
        filters: list
            List of column names where the columns used to calculate the score are stored.
        errors: bool
            True to raise errors.
        '''
        
        self.filters: list = []
        for filt in filters:
            if self._columnInDF(filt, data, errors=errors):
                self.filters.append(filt)
        
        self._columnInDF(asset_column, data, errors=errors)
        self._columnInDF(date_column, data, errors=errors)
                
        self.asset_column: str = asset_column
        self.date_column: str = date_column
        self.data: pd.DataFrame = data.copy() #.dropna()
        
    def _columnInDF(self, column:str, df:pd.DataFrame, errors:bool=True) -> bool:
        
        if column not in df:
            if errors:
                raise ValueError(f"The column {column} is not in the dataframe columns ({','.join(df.columns)})")
            else:
                print(f"The column {column} is not in the dataframe columns ({','.join(df.columns)})")
                return False
        else:
            return True
        
    def _dfToDict(self, df:pd.DataFrame) -> dict:
        
        return df.groupby(self.asset_column).last().copy()
    
    def rank(self, data:pd.DataFrame=pd.DataFrame(), sort:list=['score', 'Close'], 
             ascending:list=[False, True], n:int=None) -> pd.DataFrame:
        
        if data.empty:
            data: pd.DataFrame = self.data.copy()

        data: pd.DataFrame = self._dfToDict(data)
        data['score'] = data[self.filters].sum(axis=1)
        data.sort_values(by=sort, ascending=ascending, inplace=True)
        if n != None:
            data = data.head(n=n)

        if self.asset_column not in data.columns:
            data.reset_index(drop=False, inplace=True)
        
        return data
    
    def historicRank(self, data:pd.DataFrame=pd.DataFrame(), n:int=None, 
                     positive:bool=True) -> pd.DataFrame:
        
        if data.empty:
            data: pd.DataFrame = self.data.copy()

        data: pd.DataFrame = data.set_index([self.date_column, self.asset_column])
        data.index = data.index.set_levels(pd.to_datetime(data.index.levels[0]), level=0)
        data = data.groupby(self.asset_column, as_index=True).shift(1)
            
        self.historic_screener: pd.DataFrame = pd.concat(
            [self.rank(g[1].copy().assign(DateTime=g[0]), n=n) \
            for g in data.groupby(self.date_column)]
        )
        
        if self.asset_column not in self.historic_screener.columns:
            self.historic_screener.reset_index(drop=False, inplace=True)
        self.historic_screener: pd.DataFrame = self.historic_screener.set_index(
                                                [self.date_column, self.asset_column])
        self.historic_screener.index = self.historic_screener.index.set_levels(
                        pd.to_datetime(self.historic_screener.index.levels[0]), level=0)
        self.historic_screener.dropna(axis=1, how='all', inplace=True)
        self.historic_screener: pd.DataFrame = self.historic_screener[
                                                ~self.historic_screener['Close'].isna()
                                                ].copy()
            
        return self.historic_screener
    
    def _getDfFreq(self, df:pd.DataFrame) -> int:

        freq = df.index.get_level_values(level=0).freq
        if freq == None:
            freq = pd.infer_freq(df.index.get_level_values(level=0).unique())

        if freq == None:
            print(df.index.get_level_values(0)[-1], df.index.get_level_values(0)[0], 
                  (df.index.get_level_values(0)[-1] - df.index.get_level_values(0)[0]).days,
                  len(df.index.get_level_values(0).unique()))
            if len(df.index.get_level_values(0).unique()) > 0:
                freq: float = (df.index.get_level_values(0)[-1] - df.index.get_level_values(0)[0]).days/ \
                                    len(df.index.get_level_values(0).unique())
            else:
                freq: int = 0
            print(freq)
            return int(freq)
        
        if freq in ['Y', 'YS']:
            return 4
        elif freq in ['M', 'MS']:
            return 3
        elif freq in ['W']:
            return 2
        else:
            return 1
    
    def historicPortfolio(self, volat_target:float=0.1, volat_type:VolatType=VolatType.NEGATIVE, 
                          fractional:bool=False, frequency:Frequency=Frequency.MONTHLY, 
                          screener:pd.DataFrame=pd.DataFrame(), 
                          data:pd.DataFrame=pd.DataFrame()) -> pd.DataFrame:
        
        '''
        screener: pd.DataFrame
            DataFrame obtained through the historicRank or rank functions of the 
            Screener object.
        data: pd.DataFrame
            DataFrame feed to the Screener object to create the screener.
        frequency: Frequency
            Is the rebalancing frequency of the portfolio.
        '''
        
        if data.empty:
            data: pd.DataFrame = self.data.copy()
        if screener.empty:
            screener: pd.DataFrame = self.historic_screener.copy()
        
        data.set_index([self.date_column, self.asset_column], inplace=True)
        data.index = data.index.set_levels(pd.to_datetime(data.index.levels[0]), level=0)

        # Set the return column
        date_filter: list = [data.index.get_level_values(0).year]
        if frequency == Frequency.MONTHLY or frequency == Frequency.DAILY:
            date_filter.append(data.index.get_level_values(0).month)
            if frequency == Frequency.DAILY:
                date_filter.append(data.index.get_level_values(0).day)

        data['Ret'] = data.groupby(date_filter + [data.index.get_level_values(1)])['Close'] \
                            .transform(lambda x: x/x.shift(1) - 1)
        
        # Adapt screener to the rebalancing frequency
        self.freq_screener: pd.DataFrame = screener.copy()
        self.freq_screener.index = pd.MultiIndex.from_tuples([(pd.to_datetime(date), ticker) \
                                                for date, ticker in self.freq_screener.index], 
                                                names=[self.date_column, self.asset_column])
            
        self.freq_screener['Date'] = self.freq_screener.index.get_level_values(0)
        first_day_of_month = self.freq_screener.groupby([self.freq_screener['Date'].dt.year, 
                                                         self.freq_screener['Date'].dt.month])['Date'].first()

        self.freq_screener: pd.DataFrame = self.freq_screener.loc[[i for i in first_day_of_month \
                                                    if i in self.freq_screener.index]]
        self.freq_screener['Ret'] = self.freq_screener['Close']/self.freq_screener['Open'] - 1

        # Calculate weights and to the screener
        raw_weights: dict = []
        for d in self.freq_screener.index.get_level_values(0).unique():
            
            date_tickers: list = self.freq_screener.loc[d].index.tolist()
            temp: pd.DataFrame = data.loc[(data.index.get_level_values(0) <= d) & \
                                (data.index.get_level_values(1).isin(date_tickers))].copy()
            temp: pd.DataFrame = temp.sort_index(level=self.date_column, ascending=True) \
                                    .tail(len(date_tickers) * 22)
            temp: pd.DataFrame = pd.concat([temp.xs(t, level=self.asset_column)['Close'] \
                                            for t in temp.index.get_level_values(1).unique()], 
                                           axis=1, keys=temp.index.get_level_values(1).unique())
            cust_port: CustomPortfolioWeighting = CustomPortfolioWeighting(portfolio_prices=temp, 
                                                                    volat_target=volat_target, 
                                                                    volat_type=volat_type,
                                                                    fractional=fractional)
            cust_results: dict = cust_port.optimize(complete=False)
            raw_weights += [{self.date_column:d, self.asset_column:k, 'Weight':v} \
                            for k,v in cust_results.items()]

        weights: pd.DataFrame = pd.DataFrame(raw_weights).set_index([self.date_column, self.asset_column])
        self.freq_screener['Weight'] = weights

        # Create Date String Format
        date_str: str = '%Y'
        if frequency == Frequency.MONTHLY or frequency == Frequency.DAILY:
            date_str += '-%m'
            if frequency == Frequency.DAILY:
                date_str += '-%d'
        # Change index from first day of month to all days of month
        ticker_per_day: list = [(date, ticker) \
                                for date in screener.index.get_level_values(0).unique() \
                                if date.strftime(date_str) in self.freq_screener.index \
                                for ticker in self.freq_screener.loc[date.strftime(date_str)]\
                                    .index.get_level_values(self.asset_column).unique()]
        portfolio: pd.DataFrame = self.freq_screener.reindex(pd.MultiIndex.from_tuples(ticker_per_day, 
                                                        names=[self.date_column, self.asset_column]))
        portfolio.sort_index(level=0, inplace=True)
        portfolio.update(data[data.index.isin(portfolio.index)])
        
        # Create Dates for groupby in weighting calculation
        date_filter: list = [portfolio.index.get_level_values(0).year]
        if frequency == Frequency.MONTHLY or frequency == Frequency.DAILY:
            date_filter.append(portfolio.index.get_level_values(0).month)
            if frequency == Frequency.DAILY:
                date_filter.append(portfolio.index.get_level_values(0).day)
        # Fill weights with it's evolution through the month
        if self._getDfFreq(self.freq_screener) > self._getDfFreq(data):
            
            portfolio['Weight'] = portfolio.groupby(self.asset_column)['Weight'].ffill()
            for ticker, group in portfolio.groupby(date_filter + [self.asset_column]):
                portfolio.loc[group.index, 'Weight'] = group['Ret'].add(1).cumprod().shift(1) \
                                                                    .mul(group['Weight'].ffill())
            
            portfolio['Weight'] = portfolio.groupby(pd.Grouper(level=self.date_column, freq='D'))['Weight'] \
                                            .transform(lambda x: x / x.sum())
            portfolio.loc[weights.index, 'Weight'] = weights
            
        portfolio['Weight'] = np.where(portfolio['Weight'].isna(), 0, portfolio['Weight'])
        portfolio['Ret'] = np.where(portfolio['Ret'].isna(), 0, portfolio['Ret'])
        
        return portfolio
    
    def minCapital(self, n:int=10, volat_target:float=0.1, volat_type:VolatType=VolatType.NEGATIVE, 
                    fractional:bool=False, data:pd.DataFrame=pd.DataFrame()) -> float:
        
        
        if data.empty:
            data: pd.DataFrame = self.data.copy()

        data: pd.DataFrame = data.set_index([self.date_column, self.asset_column])
        data.index = data.index.set_levels(pd.to_datetime(data.index.levels[0]), level=0)
        data = data.groupby(self.asset_column, as_index=True).shift(1)

        rank = self.rank(data, n=n)

        date_tickers: list = rank[self.asset_column].tolist()
        temp: pd.DataFrame = data.loc[data.index.get_level_values(1).isin(date_tickers)].copy()
        temp: pd.DataFrame = temp.sort_index(level=self.date_column, ascending=True).tail(len(date_tickers) * 22)
        temp: pd.DataFrame = pd.concat([temp.xs(t, level=self.asset_column)['Close'] \
                                        for t in temp.index.get_level_values(1).unique()], 
                                        axis=1, keys=temp.index.get_level_values(1).unique())

        cust_port: CustomPortfolioWeighting = CustomPortfolioWeighting(portfolio_prices=temp, 
                                                                volat_target=volat_target,
                                                                volat_type=volat_type,
                                                                fractional=fractional)
        cust_results: dict = cust_port.optimize(complete=False)

        min_capital = {t: {'weight': cust_results[t], 'price': temp[t].iloc[-1]} for t in cust_results}


if __name__ == '__main__':
    
    import yfinance as yf
    
    def yf_droplevel(batch_download:pd.DataFrame, ticker:str) -> pd.DataFrame:
        
        df: pd.DataFrame = batch_download.iloc[:, batch_download.columns.get_level_values(1)==ticker]
        df.columns = df.columns.droplevel(1)
        df: pd.DataFrame = df.dropna()
        
        return df
    
    def smaRegime(window:int=20, column:str='Close') -> pd.Series:
        
        diff: pd.Series = df[column] - df[column].rolling(window=window).mean()
        
        return (diff - diff.rolling(window=window).min()) / \
            (diff.rolling(window=window).max() - diff.rolling(window=window).min())
    
    def dcRegime(window:int=20, column:str='Close', high_column:str='High', low_column:str='Low') -> pd.Series:
        
        return (df[column] - df[low_column].rolling(window=window).min()) / \
            (df[high_column].rolling(window=window).max() - df[low_column].rolling(window=window).min())

    
    
    website: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    start: str = '2014-12-31'
    end: str = None

    batch_size: int = 20
    show_batch: bool = True

    web_df_cols = ['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']
    regime_cols = ['sma20', 'sma50', 'sma100', 'sma200','dc20', 'dc50', 'dc100', 'dc200']
    symbol_cols = ['Ticker', 'Close', 'DateTime', 'Close']

    last_row_df_cols = symbol_cols+['score']+regime_cols

    # Download stocks and calculate regimes
    web_df: pd.DataFrame = pd.read_html(website)[0]
    tickers_list: list = list(web_df['Symbol'])
    tickers_list: list = tickers_list[:]
    print('tickers_list',len(tickers_list))

    failed: list = []

    complete: list = []
    for t in range(1, int(len(tickers_list) // batch_size) + 2): 
        m: int = (t - 1) * batch_size
        n: int = t * batch_size
        batch_list: list = tickers_list[m:n]
        if show_batch:
            print(batch_list,m,n)
            
        try:
            batch_download: pd.DataFrame = yf.download(tickers=batch_list, start=start, 
                                        end=end, interval="1d", group_by='column', auto_adjust=True, 
                                        prepost=True, threads=True, proxy=None)
            
            for flat, ticker in enumerate(batch_list):
                try:
                    df: pd.DataFrame = yf_droplevel(batch_download, ticker)
                    df['Ret'] = df['Close'].pct_change()
                    df['Ticker'] = ticker
                    df['DateTime'] = df.index
                    df.reset_index(drop=True, inplace=True)
                    df[f'sma20'] = smaRegime(20, 'Close')
                    df[f'sma50'] = smaRegime(50, 'Close')
                    df[f'sma100'] = smaRegime(100, 'Close')
                    df[f'sma200'] = smaRegime(200, 'Close')
                    df[f'dc20'] = dcRegime(20, 'Close')
                    df[f'dc50'] = dcRegime(50, 'Close')
                    df[f'dc100'] = dcRegime(100, 'Close')
                    df[f'dc200'] = dcRegime(200, 'Close')
                    
                    complete.append(df)
                    
                except Exception as e:
                    print(e)
                    failed.append(ticker)
        
        except Exception as e:
            print(e)
            
    print('failed',failed)
    
    complete_df: pd.DataFrame = pd.concat(complete, axis=0)
    complete_df.drop(columns=['Adj Close'], inplace=True)
    complete_df.dropna(inplace=True)
    complete_df.reset_index(drop=True, inplace=True)
    
    screener = Screener(data=complete_df, filters=regime_cols)
    historic = screener.historicRank(n=10)

    if False: # Si 'Ret' no estaba entre las columnas
        ret: list = []
        temp: pd.DataFrame = complete_df.copy()
        temp.set_index(['DateTime', 'Ticker'], inplace=True)
        for i in historic.index:
            ret.append(temp.loc[i, 'Ret'])
        historic['Ret'] = ret

    historic['Weight'] = 100/10/100
    positions = historic.groupby('DateTime').apply(lambda x: (x['Ret'] * x['Weight']).sum()) \
                        .reset_index(name='Positions')
    positions['CumReturn'].plot()
    positions['Positions'].plot()

