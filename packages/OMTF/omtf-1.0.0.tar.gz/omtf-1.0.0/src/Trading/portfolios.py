
import enum
import itertools

import numpy as np
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

class VolatType(enum.Enum):
    NEGATIVE: str = 'negative'
    POSITIVE: str = 'positive'
    TOTAL: str = 'total'

class PortfolioWeighting:
    
    portfolio_std: float = None

    def __init__(self, portfolio_prices:pd.DataFrame, volat_target:float=0.1,
                 volat_type:VolatType=VolatType.NEGATIVE, fractional:bool=False, 
                 verbose:bool=False) -> None:
        
        '''
        portfolio_prices: pd.DataFrame
            DataFrame with one column for the prices to use for each asset. The column name 
            must be the asset name.
        '''
        
        self.tickers: list = portfolio_prices.columns
        self.prices: pd.DataFrame = portfolio_prices.copy()
        self.returns: pd.DataFrame = portfolio_prices.copy().pct_change()
        self.returns.dropna(axis=1, how='all', inplace=True)
        self.returns.dropna(axis=0, inplace=True)
        self.volat_target: float = volat_target
        self.volat_type: VolatType = volat_type
        self.fractional: bool = fractional
        self.verbose: bool = verbose
        self._correlationMatrix()
        self._volatilities()
        self._returns()
        
    def _covarianceMatrix(self) -> None:
        self.matrix = np.cov(self.returns, rowvar=False)
        
    def _correlationMatrix(self) -> None:
        self.matrix = self.returns.corr()
        
    def _volatilities(self) -> None:
    
        arr: list = []
        for t in self.returns.columns:
            if self.volat_type == VolatType.NEGATIVE:
                series = self.returns[t][self.returns[t] < 0].copy()
            elif self.volat_type == VolatType.POSITIVE:
                series = self.returns[t][self.returns[t] > 0].copy()
            else:
                series = self.returns[t].copy()
            arr.append(series.std(skipna=True) * (252**(1/2)))
            
        self.volatilities: np.ndarray = np.array(arr)
        
    def _returns(self) -> None:
    
        arr: list = []
        for t in self.returns.columns:
            if self.volat_type == VolatType.POSITIVE:
                series = self.returns[t][self.returns[t] < 0].copy()
            elif self.volat_type == VolatType.NEGATIVE:
                series = self.returns[t][self.returns[t] > 0].copy()
            else:
                series = self.returns[t].copy()
            arr.append(series.mean(skipna=True) * 252)
            
        self.exp_returns: np.ndarray = np.array(arr)
    
    def constraint(self) -> None:
        if self.portfolio_std == None:
            if self.verbose:
                print('You should call the optimize method first to get the portfolio std.')
            raise ValueError('The portfolio Std. was not defined') 
        self.diff = self.portfolio_std - self.volat_target
        return self.diff

class CustomPortfolioWeighting(PortfolioWeighting):

    def __init__(self, portfolio_prices:pd.DataFrame, volat_target:float=0.1,
                 volat_type:VolatType=VolatType.NEGATIVE, fractional:bool=False, 
                 verbose:bool=False) -> None:
        
        '''
        portfolio_prices: pd.DataFrame
            DataFrame with one column for the prices to use for each asset. The column name 
            must be the asset name.
        '''
        
        super().__init__(portfolio_prices=portfolio_prices, volat_target=volat_target, 
                         volat_type=volat_type, fractional=fractional, verbose=verbose)
        
    def volatility(self) -> float:
        w_vol: np.ndarray = np.array(list(self.result.values())) * self.volatilities
        self.portfolio_std: float = np.sqrt(np.dot(np.dot(w_vol.T, self.matrix), w_vol)) # * (252**(1/2))
        return self.portfolio_std
    
    def expReturn(self) -> float:
        self.portfolio_ret: float = sum(np.array(list(self.result.values())) * self.exp_returns)
        return self.portfolio_ret
    
    def optimize(self, complete:bool=False, leverage:bool=False) -> None:
        
        assets: int = len(self.prices.keys())
        temp: pd.DataFrame = self.matrix.copy()
        temp['TotAbs'] = temp.abs().sum(axis=0)
        temp['Tot'] = temp.sum(axis=0)
        temp['Rescaled'] = (temp['Tot'] - (1-assets))/(assets - (1-assets))
        temp['Inverse'] = 1 - temp['Rescaled']
        temp['Weights'] = temp['Inverse']/temp['Inverse'].sum()
        temp['Volat'] = self.volatilities
        temp['VolatCorr'] = np.dot(temp['Volat'], self.matrix.copy())
        temp['VolatPond'] = temp['Volat'] * temp['Weights']
        temp['VolTargeted'] = temp['VolatPond'] * self.volat_target/((temp['VolatPond'] ** 2).sum()**(1/2))
        temp['WeightsTargeted'] = temp['Weights'] * temp['VolTargeted']/temp['VolatPond']

        if complete or ( not leverage and temp['WeightsTargeted'].sum() > 1.0):
            temp['WeightsTargeted'] = temp['WeightsTargeted']/sum(temp['WeightsTargeted'])

        self.result: dict = temp['WeightsTargeted'].to_dict()

        return self.result
    
    def getWeights(self) -> dict:
        
        return self.result
    
    def plot(self) -> None:

        # Coeficientes
        u, v, w = self.volatilities
        X, Y = np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100))
        Z = np.sqrt((self.volat_target**2 - (u*X)**2 - (v*Y)**2) / (w**2))

        point: list = list(self.result.values())
        tickers: list = list(self.result.keys())

        # Crear la figura y agregar la superficie
        fig = go.Figure(go.Surface(x=X, y=Y, z=Z))

        fig.add_trace(go.Scatter3d(x=[point[0]], y=[point[1]], z=[point[2]],
                                mode='markers', marker=dict(size=5, color='red'),
                                name='Actual weighting'))

        fig.update_layout(title='Volatility matching Elipsoid',
                        scene=dict(
                            xaxis_title=tickers[0],
                            yaxis_title=tickers[1],
                            zaxis_title=tickers[2]))

        fig.show()
        

class Markowitz(PortfolioWeighting):
    
    def __init__(self, capital:float, portfolio_prices:pd.DataFrame, volat_target:float=0.1,
                 volat_type:VolatType=VolatType.NEGATIVE, fractional:bool=False, 
                 verbose:bool=False) -> None:
        
        '''
        portfolio_prices: pd.DataFrame
            DataFrame with one column for the prices to use for each asset. The column name 
            must be the asset name.
        '''
        
        super().__init__(portfolio_prices=portfolio_prices, volat_target=volat_target, 
                         volat_type=volat_type, fractional=fractional, verbose=verbose)
        self.capital: float = capital
        self._weightsCombinations()
        
    def _weightsCombinations(self, step:float=0.01) -> None:
        
        prices = self.prices.iloc[-1]
        max_size = self.capital/prices if self.fractional else (self.capital//prices)
        step = step if self.fractional else 1
        it = [[mp-i*step for i in range(int(mp//step))] for mp in max_size]
        sizes: np.ndarray = np.array(list(itertools.product(*it)))
        self.combinations: list = [size * prices / self.capital for size in sizes \
                                    if sum(size * prices) <= self.capital]
                
    def equalInitialization(self) -> None:
        n = self.matrix.shape[0]
        self.weights = np.ones(n) / n
        
    def randomInitialization(self) -> None:
        n = self.matrix.shape[0]
        self.weights = np.random.rand(n)
        self.weights /= np.sum(self.weights)
        
    def expectancyInitialization(self) -> None:
        expected_returns = self.returns.mean().values
        self.weights = expected_returns / np.sum(expected_returns)
        
    def volatilityInitialization(self) -> None:
        
        self.weights = 1 / np.array(self.volatilities)
        self.weights /= np.sum(self.weights)
    
    def volatility(self, combination:np.ndarray) -> float:
        w_vol: np.ndarray = combination * self.volatilities
        self.portfolio_std: float = np.sqrt(np.dot(np.dot(w_vol.T, self.matrix), w_vol)) # * (252**(1/2))
        return self.portfolio_std
    
    def expReturn(self, combination:np.ndarray) -> float:
        self.portfolio_ret: float = sum(combination * self.exp_returns)
        return self.portfolio_ret

    def optimize(self, complete:bool=False, leverage:bool=False) -> np.ndarray:
            
        self.result: list = []
        for combination in self.combinations:
            std: float = self.volatility(combination)
            if std <= self.volat_target:
                self.result.append({
                    'weights': combination,
                    'std': std,
                    'ret': self.expReturn(combination),
                    'diff': self.constraint()
                })
            
            if self.verbose:
                print('Weights: ', self.weights, 'Std: ', self.portfolio_std, 
                      'Ret: ', self.portfolio_ret, 'Diff: ', self.diff)
            
        return self.getWeights(complete=complete, leverage=leverage)
    
    def getWeights(self, complete:bool=False, leverage:bool=False) -> dict:
        
        temp: pd.DataFrame = pd.DataFrame(self.result) \
                                .sort_values(by=['diff', 'ret'], ascending=[False, True])['weights'] \
                                .iloc[0].values
        self.weights: dict = {self.tickers[i]: v for i,v in enumerate(temp)}
        
        if complete or ( not leverage and sum(self.weights.values()) > 1.0):
            self.weights: dict = {k: v/sum(self.weights.values()) for k,v in self.weights.items()}

        return self.weights
    
    def plot(self) -> None:
        
        temp: pd.DataFrame = pd.DataFrame(self.result)
        
        fig = make_subplots(rows=1, cols=1)

        fig.add_trace(go.Scatter(x=temp['std'] * 10000//1/100, y=temp['ret'] * 10000//1/100, 
                                 name='Portfolios', mode='markers'), row=1, col=1)

        fig.update_yaxes(title_text='Expected Return (%)', row=1, col=1)
        fig.update_xaxes(title_text='Standard Deviation (%)', row=1, col=1)

        fig.update_layout(title=f"Efficient Frontier", 
                            autosize=False, width=1000, height=700)

        fig.show()
        

    
def markowitzHistoric(data:dict, capital:float=2000, volat_target:float=0.1, window:int=22, 
                    volat_type:str=VolatType.NEGATIVE, complete:bool = False):
                        
    df = pd.concat([data[ticker]['Close'].copy() for ticker in data.keys()], 
                            axis=1, keys=data.keys())
    df.dropna(inplace=True)

    raw_allocations: list = []
    for i in range(len(df)):
        if i % window == 0 and i != 0:
            temp: pd.DataFrame = df.iloc[i-window:i]
            popt: Markowitz = Markowitz(capital, temp, volat_target, volat_type)
            results: list = popt.optimize()
            raw_allocations.append({df.columns[i]: a for i,a in \
                    enumerate(results)})
        else:
            raw_allocations.append({c: float('nan') for c in df.columns})
            
    allocations: pd.DataFrame = pd.DataFrame(raw_allocations)
    allocations.index = df.index
    allocations.ffill(inplace=True)
    allocations.dropna(inplace=True)
    
    return df, allocations

def customHistoric(data:dict, volat_target:float=0.1, window:int=22, 
                    volat_type:str=VolatType.NEGATIVE, ma_filter:bool=False, 
                    complete:bool = False):
                        
    df = pd.concat([data[ticker]['Close'].copy() for ticker in data.keys()], 
                            axis=1, keys=data.keys())
    df.dropna(inplace=True)

    raw_allocations: list = []
    results: list = [0.333, 0.333, 0.333]
    ma_diff: list = []
    volatility: list = []
    for i in range(len(df)):
        if i % window == 0 and i != 0:
            temp: pd.DataFrame = df.iloc[i-window:i]

            if ma_filter and max(ma_diff[-window:]) != min(ma_diff[-window:]):
                ma_diff.append((temp * results).sum(axis=1).iloc[-1] - (temp * results).sum(axis=1).mean())
                final_volat = volat_target * (ma_diff[-1] - min(ma_diff[-window:])) / (max(ma_diff[-window:]) - min(ma_diff[-window:]))
            else:
                final_volat = volat_target
                
            popt: CustomPortfolioWeighting = CustomPortfolioWeighting(portfolio_prices=temp, 
                                                                      volat_target=final_volat, 
                                                                      volat_type=volat_type)
            results: dict = popt.optimize(complete=complete)
            raw_allocations.append(results)
            volatility.append(popt.volatility())
        else:
            raw_allocations.append({c: float('nan') for c in df.columns})
            volatility.append(volatility[-1] if len(volatility) > 0 else 0)
            
    allocations: pd.DataFrame = pd.DataFrame(raw_allocations)
    allocations.index = df.index
    allocations.ffill(inplace=True)
    allocations.dropna(inplace=True)
    
    return df, allocations, volatility


if __name__ == '__main__':

    import datetime as dt
    import yfinance as yf

    tickers: list = ['SPY', 'QQQ', 'BTC-USD']
    complete_data: dict = {}
    for t in tickers:

        temp = yf.Ticker(t).history(period='max', interval='1d')
        temp.index = temp.index.date
        complete_data[t] = temp.copy()
        
    # df_concat, allocations = markowitzHistoric(data, volat_type=VolatType.TOTAL)
    df_concat, allocations, volatility = customHistoric(complete_data, volat_target=0.1, window=22, 
                                            volat_type=VolatType.NEGATIVE, ma_filter=False,
                                            complete=False)

    results = allocations * df_concat.pct_change()
    results = results[results.index > dt.datetime(2021, 8, 1).date()].copy()
    results['Portfolio'] = results.sum(axis=1)
    results = (1 + results).cumprod()
    print('Max. DD: ', (1 - results['Portfolio']/results['Portfolio'].cummax()).max())
    print('Returns: ', (results['Portfolio'].iloc[-1] - 1))
    print('Returns OVer DrawDown: ', (results['Portfolio'].iloc[-1] - 1)/ \
        (1 - results['Portfolio']/results['Portfolio'].cummax()).max())
    print('Std: ', results['Portfolio'].std())
    print(allocations.iloc[-1])


    # Supongamos que temp es tu DataFrame
    allocations['Tot'] = allocations.sum(axis=1)
    temp: pd.DataFrame = pd.concat([allocations['Tot'], results['Portfolio']], axis=1, keys=['Allocated', 'Return'])
    temp.dropna(inplace=True)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.0,
                        row_heights=[3,1],
                        specs=[[{'secondary_y': True}],[{'secondary_y': False}]])

    fig.add_trace(go.Scatter(x=temp.index, y=temp['Return'] * 10000//1/100, name='Balance'), 
                    row=1, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=temp.index, y=(1 - temp['Return']/temp['Return'].cummax()) * 10000//1/100, 
                                fill='tozeroy', name='DrawDown'), row=1, col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=temp.index, y=temp['Return'].cummax() * 10000//1/100, name='MaxBalance'), 
                    row=1, col=1, secondary_y=False)

    fig.update_yaxes(title_text='Return (%)', row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text='DrawDown (%)', row=1, col=1, secondary_y=True)

    for c in allocations:
        fig.add_trace(go.Scatter(x=allocations.index, y=allocations[c], name=c), 
                            row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=allocations.index, y=volatility, name='Volatility'), 
                        row=2, col=1, secondary_y=False)

    fig.update_yaxes(title_text='Allocations (%)', row=2, col=1)

    fig.update_xaxes(title_text='Date', row=2, col=1)
    fig.update_layout(title=f"Account balance {temp['Return'].iloc[-1] * 10000//1/100}%", 
                        autosize=False, width=1000, height=700)

    fig.show()