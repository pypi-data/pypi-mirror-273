
import datetime as dt
import os
import random
import string

import numpy as np
import pandas as pd


class GeometricBrownianMotionAssetSimulator:
    """
    This callable class will generate a daily
    open-high-low-close-volume (OHLCV) based DataFrame to simulate
    asset pricing paths with Geometric Brownian Motion for pricing
    and a Pareto distribution for volume.

    It will output the results to a CSV with a randomly generated
    ticker smbol.

    For now the tool is hardcoded to generate business day daily
    data between two dates, inclusive.

    Note that the pricing and volume data is completely uncorrelated,
    which is not likely to be the case in real asset paths.

    Parameters
    ----------
    start_date : `str`
        The starting date in YYYY-MM-DD format.
    end_date : `str`
        The ending date in YYYY-MM-DD format.
    output_dir : `str`
        The full path to the output directory for the CSV.
    symbol_length : `int`
        The length of the ticker symbol to use.
    init_price : `float`
        The initial price of the asset.
    mu : `float`
        The mean 'drift' of the asset.
    sigma : `float`
        The 'volatility' of the asset.
    pareto_shape : `float`
        The parameter used to govern the Pareto distribution
        shape for the generation of volume data.
    """

    def __init__(self, start_date=None, end_date=None, periods:int=100,
        output_dir:str='random_data', symbol_length:int=4, init_price:float=10.0,
        mu:float=0.1, sigma:float=0.3, pareto_shape:float=1.5, freq:str='B',
        remove_files:bool=True ) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.periods = periods
        self.output_dir = output_dir
        self.symbol_length = symbol_length
        self.init_price = init_price
        self.mu = mu
        self.sigma = sigma
        self.pareto_shape = pareto_shape
        self.freq = freq
        self.remove_files = remove_files

    def _generate_random_symbol(self) -> str:
        """
        Generates a random ticker symbol string composed of
        uppercase ASCII characters to use in the CSV output filename.

        Returns
        -------
        `str`
            The random ticker string composed of uppercase letters.
        """
        return ''.join(
            random.choices(
                string.ascii_uppercase,
                k=self.symbol_length
            )
        )

    def _create_empty_frame(self, start_date=None, end_date=None, 
                            periods:int=None, freq:str='B') -> pd.DataFrame:
        """
        Creates the empty Pandas DataFrame with a date column using
        business days between two dates. Each of the price/volume
        columns are set to zero.

        Returns
        -------
        `pd.DataFrame`
            The empty OHLCV DataFrame for subsequent population.
        """
        if start_date == None:
            start_date = self.start_date
        if end_date == None:
            end_date = self.end_date
        if periods == None:
            periods = self.periods

        if start_date != None and end_date != None:
            if end_date < start_date:
                if end_date == self.end_date:
                    end_date = None
                elif start_date == self.start_date:
                    start_date = None
            else:
                periods = None
        if start_date == None and end_date == None:
            end_date = dt.datetime.today()
            if periods == None:
                periods = 100

        date_range = pd.date_range(
            start=start_date if isinstance(start_date, str) or start_date == None \
                            else start_date.strftime('%Y-%m-%d'),
            end=end_date if isinstance(end_date, str) or end_date == None \
                        else end_date.strftime('%Y-%m-%d'),
            periods=periods,
            freq=freq
        )

        zeros = pd.Series(np.zeros(len(date_range)))

        return pd.DataFrame(
            {
                'date': date_range,
                'open': zeros,
                'high': zeros,
                'low': zeros,
                'close': zeros,
                'volume': zeros
            }
        )

    def _create_geometric_brownian_motion(self, data:pd.DataFrame, 
                                        init_price:float=None) -> np.ndarray:
        """
        Calculates an asset price path using the analytical solution
        to the Geometric Brownian Motion stochastic differential
        equation (SDE).

        This divides the usual timestep by four so that the pricing
        series is four times as long, to account for the need to have
        an open, high, low and close price for each day. These prices
        are subsequently correctly bounded in a further method.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame needed to calculate length of the time series.

        Returns
        -------
        return: np.ndarray
            The asset price path (four times as long to include OHLC).
        """
        
        if init_price != None:
            self.init_price = init_price

        n = len(data)
        T = n / 252.0  # Business days in a year
        dt = T / (4.0 * n)  # 4.0 is needed as four prices per day are required
        
        # Vectorised implementation of asset path generation
        # including four prices per day, used to create OHLC
        asset_path = np.exp(
            (self.mu - self.sigma**2 / 2) * dt +
            self.sigma * np.random.normal(0, np.sqrt(dt), size=(4 * n))
        )
        
        return self.init_price * asset_path.cumprod()

    def _create_geometric_resized_brownian_motion(self, data:pd.DataFrame, 
                                                  init_price:float=None
                                                  ) -> pd.DataFrame:
        """
        Calculates an asset price path using the analytical solution
        to the Geometric Brownian Motion stochastic differential
        equation (SDE).

        This divides the usual timestep by four so that the pricing
        series is four times as long, to account for the need to have
        an open, high, low and close price for each day. These prices
        are subsequently correctly bounded in a further method.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame needed to calculate length of the time series.
        init_price: float
            Price from where to start the data.

        Returns
        -------
        df: pd.DataFrame
            The asset price path (four times as long to include OHLC).
        """

        if init_price != None:
            self.init_price = init_price

        n = len(data)
        T = n / (60*24*365.0) # Business days in a year
        dt = T / (n)  # 4.0 is needed as four prices per day are required
        
        # Vectorised implementation of asset path generation
        # including four prices per day, used to create OHLC
        asset = np.exp(
            (self.mu - self.sigma**2 / 2) * dt +
            self.sigma * np.random.normal(0, np.sqrt(dt), size=(n))
        )
        price = self.init_price * asset.cumprod()
        price = pd.Series(price, index=data['date'], name=None)
        
        df = price.resample(self.freq).ohlc()
        #df.index = df['date']

        return df

    def _append_path_to_data(self, data:pd.DataFrame, path:np.ndarray) -> None:
        """
        Correctly accounts for the max/min calculations required
        to generate a correct high and low price for a particular
        day's pricing.

        The open price takes every fourth value, while the close
        price takes every fourth value offset by 3 (last value in
        every block of four).

        The high and low prices are calculated by taking the max
        (resp. min) of all four prices within a day and then
        adjusting these values as necessary.

        This is all carried out in place so the frame is not returned
        via the method.

        Parameters
        ----------
        data : pd.DataFrame
            The price/volume DataFrame to modify in place.
        path : np.ndarray
            The original NumPy array of the asset price path.
        """
        data['open'] = path[0::4]
        data['close'] = path[3::4]

        data['high'] = np.maximum(
            np.maximum(path[0::4], path[1::4]),
            np.maximum(path[2::4], path[3::4])
        )

        data['low'] = np.minimum(
            np.minimum(path[0::4], path[1::4]),
            np.minimum(path[2::4], path[3::4])
        )
        data.index = data['date']

    def _append_volume_to_data(self, data:pd.DataFrame) -> None:
        """
        Utilises a Pareto distribution to simulate non-negative
        volume data. Note that this is not correlated to the
        underlying asset price, as would likely be the case for
        real data, but it is a reasonably effective approximation.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame to append volume data to, in place.
        """
        data['volume'] = np.array(
            list(
                map(
                    int,
                    np.random.pareto(
                        self.pareto_shape,
                        size=len(data)
                    ) * 1000000.0
                )
            )
        )

    def _output_frame_to_dir(self, symbol:str, data:pd.DataFrame) -> None:
        """
        Output the fully-populated DataFrame to disk into the
        desired output directory, ensuring to trim all pricing
        values to two decimal places.

        Parameters
        ----------
        symbol : str
            The ticker symbol to name the file with.
        data : pd.DataFrame
            The DataFrame containing the generated OHLCV data.
        """
        if self.remove_files:
            for f in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, f))

        output_file = os.path.join(self.output_dir, f'{symbol}.csv')
        data.to_csv(output_file, index=True, float_format='%.4f')

    def generateGBM(self, symbol:str=None, save:bool=True) -> pd.DataFrame:
        """
        The entrypoint for generating the asset OHLCV frame. Firstly this
        generates a symbol and an empty frame. It then populates this
        frame with some simulated GBM data. The asset volume is then appended
        to this data and finally it is saved to disk as a CSV.
        """
        if symbol == None:
            symbol = self._generate_random_symbol()

        if False:
            data = self._create_empty_frame(freq=self.freq)
            path = self._create_geometric_brownian_motion(data)
            self._append_path_to_data(data, path)
        else:
            data = self._create_empty_frame(freq='T')
            data = self._create_geometric_resized_brownian_motion(data)
            
        self._append_volume_to_data(data)
        if save:
            self._output_frame_to_dir(symbol, data)

        return data

    def addGBM(self, data:pd.DataFrame, periods:int=60*24, freq:str='B', symbol:str=None, 
               save:bool=True) -> pd.DataFrame:
        
        self.init_price = data['close'].iloc[-1]
        self.freq = freq
        data.reset_index(drop=False, inplace=True)
        data['date'] = pd.to_datetime(data['date'])
        self.start_date = data['date'].iloc[-1] + dt.timedelta(days=1)
        self.periods = 1
        new_data = self._create_empty_frame(start_date=self.start_date, periods=periods, freq='T')
        new_data = self._create_geometric_resized_brownian_motion(new_data)
        new_data['date'] = new_data.index
        self._append_volume_to_data(new_data)
        data = pd.concat([data, new_data])
        data.reset_index(drop=True, inplace=True)

        if save:
            if symbol == None:
                symbol = self._generate_random_symbol()
            self._output_frame_to_dir(symbol, data)
        
        return data



if False:
    def randomwalk(initial_price:float=10.0,periods:int=100, start:dt.datetime=None, 
                end:dt.datetime=None, freq:str='B', tz:str=None, normalize:bool=False, 
                name=None, closed=None, tick=1, **kwargs):
        """Returns random up/down pandas Series.

        Usage:
            ```
            import datetime
            randomwalk(100)  # Returns +-1up/down 100days from now.
            randomwalk(100, freq='H')  # Returns +-1up/down 100hours from now.
            randomwalk(100, ,tick=0.1 freq='S')  # Returns +-0.1up/down 100seconds from now.
            randomwalk(100, start=datetime.datetime.today())  # Returns +-1up/down 100days from now.
            randomwalk(100, end=datetime.datetime.today())
                # Returns +-1up/down back to 100 days from now.
            randomwalk(start=datetime.datetime(2000,1,1), end=datetime.datetime.today())
                # Returns +-1up/down from 2000-1-1 to now.
            randomwalk(100, freq='H').resample('D').ohlc()  # random OHLC data
            ```

        Args:
            periods: int
            start: start time (default datetime.now())
            end: end time
            freq: ('M','W','D','B','H','T','S') (default 'B')
            tz: time zone
            tick: up/down unit size (default 1)

        Returns:
            pandas Series with datetime index
        """
        if not start and not end:
            start = dt.datetime.today().date()  # default arg of `start`

        index = pd.date_range(start=start, end=end, periods=periods, freq=freq, tz=tz,
                                normalize=normalize, name=name, closed=closed, **kwargs)
        if True:
            mu = 0.1
            sigma = 0.3
            # calc each time step
            dt = (index[-1]-index[0]).days/365/periods
            # simulation using numpy arrays
            St = np.exp(
                (mu - sigma ** 2 / 2) * dt
                + sigma * np.random.normal(0, np.sqrt(dt), size=(1,periods)).T
            )
            # include array of 1's
            #St = np.vstack([np.ones(M), St])
            # multiply through by S0 and return the cumulative product of elements along a given simulation path (axis=0). 
            price = pd.Series(initial_price * np.array([i[0] for i in St]).cumprod(),
                                index=index, name=name, **kwargs)
        elif True:
            bullbear = pd.Series([tick * random.gauss(0,1) for i in index],
                                index=index, name=name, **kwargs)
            price = bullbear.cumsum() + 12
        else:
            #np.random.seed(1)
            bullbear = pd.Series(tick * np.random.randint(-1, 2, len(index)),
                                index=index, name=name, **kwargs)
            price = bullbear.cumsum() + 12

        return price

    rw = randomwalk(periods=60*24*365*1, freq='T', end=dt.datetime.today(), tick=1.2)
    df = rw.resample('H').ohlc()


if __name__ == '__main__':

    for i in range(10):
        gbmas = GeometricBrownianMotionAssetSimulator(periods=60*24*365*10, remove_files=False)
        data = gbmas.generateGBM(save=False)
        data = gbmas.addGBM(data)

    files = [f for f in os.listdir('random_data') if '.csv' in f]

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    for f in files:
        df = pd.read_csv(os.path.join('random_data',f))
        df.index = df['date']
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
        fig.add_trace(go.Candlestick(x=df.index, open=df['open'], high=df['high'], 
                            low=df['low'], close=df['close'], name='Price'), row=1, col=1)
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_layout(
            title_text=f'Price',
            autosize=False,
            width=900,
            height=600,
            margin=dict(l=20, r=20, t=40, b=20),
        )

        fig.show()
