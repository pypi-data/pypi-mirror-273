
import os
import copy
import datetime as dt
import pytz
import enum
import numpy as np
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from indicators import OHLC

from execution_utils import (typeToDict, Commissions, Trade, OrderType, StrategyConfig, 
    AssetConfig, TradeSide, CloseMethod, SignalsSide)

class ReturnsType(enum.Enum):
    SIMPLE = 'SIMPLE'
    COMPOUND = 'COMPOUND'

class CapitalType(enum.Enum):
    BALANCE: str = 'BALANCE'
    UNINVESTED: str = 'UNINVESTED'
    REALIZED: str = 'REALIZED'
    FLOATING: str = 'FLOATING'

class DiscreteConfig:

    '''
    Class used to create the backtest config.
    '''

    def __init__(self, init_date:str=None, final_date:str=None, capital:float=10000.0, 
                 capital_type:CapitalType=CapitalType.UNINVESTED, monthly_add:float=0, 
                 use_sl:bool=True, use_tp:bool=True, time_limit:int=365, min_size:float=1, 
                 max_size:float=10000000, commission:Commissions=None, max_trades:int=3, 
                 filter_ticker:bool=True, filter_strat:bool=False, reset_orders:bool=True, 
                 continue_onecandle:bool=True, offset_aware:bool=False, allocate:bool=True,
                 base_currency:str='EUR', compound:ReturnsType=ReturnsType.COMPOUND
                 ) -> None:

        '''
        Generates the main config object for the backtest.

        Parameters
        ----------
        init_date: str
            Date to start the backtest. Must be in format: YYYY-MM-DD.
        final_date: str
            Date to end the backtest. Must be in format: YYYY-MM-DD.
        capital: float
            Starting capital for the backtest. Default is 10000.
        capital_type: CapitalType
            Type of capital to use for position sizing. It can be:
            - balance: to use the complete realized balance of the account
            - uninvested: to use the uninvested balance of the account
            - unrealized: to use the complete realized and unrealize equity.
        monthly_add: float
            Quantity to add to the balance every month.
        use_sl: bool
            True to use fixed SL. Default is True.
        use_tp: bool
            True to use fixed TP. Default is True.
        time_limit: int
            Number of maximum candles for an open trade before closing.
        min_size: float
            Minimum contracts for a position.
        max_size: float
            Maximum contracts for a position.
        commission: Commissions
            Commissions object associated to broker. This one will be added 
            and applied to each trade in each asset.
        max_trades: int
            Maximum trades open at the same time.
        filter_ticker: bool
            True to apply the max_trades to each ticker.
        filter_strat: bool
            True to apply the max_trades to each strategy.
        reset_orders: bool
            True to reset pending orders in a ticker if another one
            of the same direction (long or short) appeared.
        continue_onecandle: bool
            OneCandle trades are those where a candle triggered the entry, 
            the SL and the TP. As we don't know the order in which they 
            were triggered we can ignore the exit by setting the input to 
            True. This way the trade will stay open till a future candle 
            triggers another exit signal.
        offset_aware: bool
            True to give a timezone to the dates.
        allocate: bool
            True to apply allocation fractions.
        base_currency: str
            String conatining the code for the account currency.
        compound: ReturnsType
            Compounded or simple returns.
        '''

        if init_date == None:
            init_date: str = (dt.date.today() - dt.timedelta(days=365*2)).strftime('%Y-%m-%d')
        if final_date == None:
            final_date: str = dt.date.today().strftime('%Y-%m-%d')

        self.init_date: dt.datetime = self._dateFormat(init_date, offset_aware)
        self.final_date: dt.datetime = self._dateFormat(final_date, offset_aware)
        self.capital: float = capital
        self.capital_type: CapitalType = capital_type
        self.monthly_add: float = monthly_add
        self.use_sl: bool = use_sl
        self.use_tp: bool = use_tp
        self.time_limit: int = time_limit
        self.min_size: float = min_size
        self.max_size: float = max_size
        self.commission: Commissions = copy.deepcopy(commission)
        self.max_trades: int = max_trades
        self.filter_ticker: bool = filter_ticker
        self.filter_strat: bool = filter_strat
        self.reset_orders: bool = reset_orders
        self.continue_onecandle: bool = continue_onecandle
        self.allocate: bool = allocate
        self.base_currency: str = base_currency
        self.compound: ReturnsType = compound

    def _dateFormat(self, datetime:str, offset:bool=False) -> dt.datetime:

        '''
        Generates a dictionary with the config for the backtest.

        Parameters
        ----------
        datetime: str
            DateTime to start the backtest. Must be in format: YYYY-MM-DD.
        offset: bool
            Make the date offset aware. The offset will be UTC.

        Returns
        -------
        datetime: str | dt.datetime
            Contains the formated date.
        '''
        
        if isinstance(datetime, str):
            datetime: dt.datetime = dt.datetime.strptime(datetime, '%Y-%m-%d')
            if offset:
                datetime: dt.datetime = datetime.replace(tzinfo=pytz.UTC)

        return datetime

    def to_dict(self) -> dict:

        '''
        Generates a dictionary with the config for the backtest.

        Returns
        -------
        object: dict
            Contains the config for the backtest.
        '''

        return self.__dict__

class BtConfig:

    def __init__(self, init_date:str=None, final_date:str=None, capital:float=10000.0, 
                 capital_type:CapitalType=CapitalType.UNINVESTED, monthly_add:float=0, 
                 side=SignalsSide.LONG,
                 use_sl:bool=True, use_tp:bool=True, time_limit:int=365, min_size:float=1, 
                 max_size:float=10000000, commission:Commissions=None, max_trades:int=3, 
                 filter_ticker:bool=True, filter_strat:bool=False, reset_orders:bool=True, 
                 continue_onecandle:bool=True, offset_aware:bool=False, allocate:bool=True,
                 base_currency:str='EUR', compound:ReturnsType=ReturnsType.COMPOUND
                 ) -> None:

        '''
        Generates the main config object for the backtest.

        Parameters
        ----------
        init_date: str
            Date to start the backtest. Must be in format: YYYY-MM-DD.
        final_date: str
            Date to end the backtest. Must be in format: YYYY-MM-DD.
        capital: float
            Starting capital for the backtest. Default is 10000.
        capital_type: CapitalType
            Type of capital to use for position sizing. It can be:
            - balance: to use the complete realized balance of the account
            - uninvested: to use the uninvested balance of the account
            - unrealized: to use the complete realized and unrealize equity.
        monthly_add: float
            Quantity to add to the balance every month.
        use_sl: bool
            True to use fixed SL. Default is True.
        use_tp: bool
            True to use fixed TP. Default is True.
        time_limit: int
            Number of maximum candles for an open trade before closing.
        min_size: float
            Minimum contracts for a position.
        max_size: float
            Maximum contracts for a position.
        commission: Commissions
            Commissions object associated to broker. This one will be added 
            and applied to each trade in each asset.
        max_trades: int
            Maximum trades open at the same time.
        filter_ticker: bool
            True to apply the max_trades to each ticker.
        filter_strat: bool
            True to apply the max_trades to each strategy.
        reset_orders: bool
            True to reset pending orders in a ticker if another one
            of the same direction (long or short) appeared.
        continue_onecandle: bool
            OneCandle trades are those where a candle triggered the entry, 
            the SL and the TP. As we don't know the order in which they 
            were triggered we can ignore the exit by setting the input to 
            True. This way the trade will stay open till a future candle 
            triggers another exit signal.
        offset_aware: bool
            True to give a timezone to the dates.
        allocate: bool
            True to apply allocation fractions.
        base_currency: str
            String conatining the code for the account currency.
        compound: ReturnsType
            Compounded or simple returns.
        '''

        if init_date == None:
            init_date: str = pd.Timestamp.min.strftime('%Y-%m-%d')
        if final_date == None:
            final_date: str = dt.date.today().strftime('%Y-%m-%d')

        self.init_date: dt.datetime = self._dateFormat(init_date, offset_aware)
        self.final_date: dt.datetime = self._dateFormat(final_date, offset_aware)
        self.capital: float = capital
        self.capital_type: CapitalType = capital_type
        self.monthly_add: float = monthly_add
        self.use_sl: bool = use_sl
        self.use_tp: bool = use_tp
        self.time_limit: int = time_limit
        self.min_size: float = min_size
        self.max_size: float = max_size
        self.commission: Commissions = copy.deepcopy(commission)
        self.max_trades: int = max_trades
        self.filter_ticker: bool = filter_ticker
        self.filter_strat: bool = filter_strat
        self.reset_orders: bool = reset_orders
        self.continue_onecandle: bool = continue_onecandle
        self.allocate: bool = allocate
        self.base_currency: str = base_currency
        self.compound: ReturnsType = compound
        self.side: SignalsSide = side
        
    def _dateFormat(self, datetime:str, offset:bool=False) -> dt.datetime:

        '''
        Generates a dictionary with the config for the backtest.

        Parameters
        ----------
        datetime: str
            DateTime to start the backtest. Must be in format: YYYY-MM-DD.
        offset: bool
            Make the date offset aware. The offset will be UTC.

        Returns
        -------
        datetime: str | dt.datetime
            Contains the formated date.
        '''
        
        if isinstance(datetime, str):
            datetime: dt.datetime = dt.datetime.strptime(datetime, '%Y-%m-%d')
            if offset:
                datetime: dt.datetime = datetime.replace(tzinfo=pytz.UTC)

        return datetime

    def to_dict(self) -> dict:

        '''
        Generates a dictionary with the config for the backtest.

        Returns
        -------
        object: dict
            Contains the config for the backtest.
        '''

        return {k: typeToDict(v, class_types=[Commissions], enum_types=[CapitalType, ReturnsType, SignalsSide]) \
                for k, v in self.__dict__.items()}

class Backtest(OHLC):

    def __init__(self, strategies:dict, config:BtConfig=None, 
                 verbose:bool=False, errors:bool=False) -> None:

        '''
        Initialize the Backtesting object.

        Parameters
        ----------
        strategies: dict
            Dictionary with the data for strategies.
            Example:
            ex_dict = {
                'strategy1': StrategyConfig(),
                ...
            }
        assets: dict
            Dictionary with the data for assets.
            Example:
            ex_dict = {
                'asset1': AssetConfig(),
                ...
            }
        config: BtConfig
            BtConfig object with the backtest config.
        verbose: bool
            True to print errors.
        errors: bool
            True to raise errors.
        '''

        self.strategies: dict = strategies
        self.config = config if config != None else self.config
        self.verbose: bool = verbose
        self.errors: bool = errors
    
    def fillHalts(self, df:pd.DataFrame) -> pd.DataFrame:

        '''
        Fills halts.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame containing the candles data.

        Returns
        -------
        df: pd.DataFrame
            Contains all the DataFrame without the previous close value 
            for the halts.
        '''

        df['Close'] = df['Close'].ffill()
        df['Spread'] = df['Spread'].ffill()
        df['Open'] = np.where(df['Open'] != df['Open'], df['Close'], df['Open'])
        df['High'] = np.where(df['High'] != df['High'], df['Close'], df['High'])
        df['Low'] = np.where(df['Low'] != df['Low'], df['Close'], df['Low'])

        return df
    
    def getEntries(self, columns:list) -> None:

        '''
        Gets the column names of the different Entry strategies.

        Parameters
        ----------
        columns: list
            Contains the columns of the DataFrame.
        '''
        
        self.entries: list = [c.replace('Entry','').replace('entry','') for c in columns \
                        if 'entry' in c.lower()]
    
    def getExits(self, columns:list) -> None:

        '''
        Gets the column names of the different Exit strategies.

        Parameters
        ----------
        columns: list
            Contains the columns of the DataFrame.
        '''
        
        self.exits: list = [c.replace('Exit','').replace('exit','') for c in columns \
                        if 'exit' in c.lower()]

    def currentCapital(self, balance:float, open_trades:list, 
                       capital_type:CapitalType) -> float:

        '''
        Calculate current available capital.

        Parameters
        ----------
        balance: float
            Current accoutn balance.
        open_trades: list
            List of currently open trades.

        Returns
        -------
        capital: float
            Available capital to trade.
        '''

        if capital_type == CapitalType.UNINVESTED:
            dif: float = -sum([trade.position for trade in open_trades])
        elif capital_type == CapitalType.REALIZED:
            dif: float = sum([trade.net_result for trade in open_trades])
        elif capital_type == CapitalType.FLOATING:
            dif: float = sum([(trade.net_result + trade.floating_result) for trade in open_trades])

        return balance + dif

    def entryPrice(self, side:TradeSide, asset:AssetConfig, candle:dict, prev_candle:dict) -> float:
        
        if side == TradeSide.LONG:
            
            # Buy order entry price
            if asset.order_type == OrderType.MARKET:
                return candle['Open'] + candle['Spread']
            elif asset.order_type == OrderType.STOP:
                if 'High' in prev_candle[candle['Ticker']] and \
                    prev_candle[candle['Ticker']]['High'] > candle['Open']:
                    return prev_candle[candle['Ticker']]['High']
                else:
                    return candle['Open'] + candle['Spread']
            elif asset.order_type == OrderType.LIMIT:
                if 'Low' in prev_candle[candle['Ticker']] and \
                    prev_candle[candle['Ticker']]['Low'] < candle['Open']:
                    return prev_candle[candle['Ticker']]['Low']
                else:
                    return candle['Open'] + candle['Spread']
        
        if side == TradeSide.SHORT:

            # Sell order entry price
            if asset.order_type == OrderType.MARKET:
                return candle['Open']
            elif asset.order_type == OrderType.STOP:
                if 'Low' in prev_candle[candle['Ticker']] and \
                    prev_candle[candle['Ticker']]['Low'] < candle['Open']:
                    return prev_candle[candle['Ticker']]['Low']
                else:
                    return candle['Open']
            elif asset.order_type == OrderType.LIMIT:
                if 'High' in prev_candle[candle['Ticker']] and \
                    prev_candle[candle['Ticker']]['High'] > candle['Open']:
                    return prev_candle[candle['Ticker']]['High']
                else:
                    return candle['Open']

    def isEntered(self, open_trades:list, entry:float, candle:dict, prev_candle:dict) -> bool:

        '''
        Checks if the trade has been already opened.

        Parameters
        ----------
        open_trades: list
            List of Trade objects containing the currently open trades.
        entry: float
            Entry price for the new trade.
        candle: 
            Current candle.
        prev_candle:
            Previous candle.

        Returns
        -------
        entered: bool
            True if the position is already opened, else False.
        '''

        t: Trade
        for t in open_trades:
            if t.entry == entry or candle['Open'] == prev_candle[candle['Ticker']]['Open']:
                return True
        
        return False

    def getFilteredTrades(self, trades:list, ticker:str=None, strategy:str=None, 
                          side:TradeSide=None) -> list:
        
        return [t for t in trades if (t.ticker == ticker or ticker==None) and 
                (t.strategy.name == strategy or strategy == None) and 
                (t.signal == side or side == None) and 
                t.method != CloseMethod.CANCEL]
        
    def openQty(self, candle:dict, open_trades:list, filter_ticker:bool=True, 
                filter_strat:bool=False, use_size:bool=True
                ) -> (int | float | dict):

        '''
        Gets the quantity of open trades.

        Parameters
        ----------
        candle: 
            Contains the current iteration candle.
        open_trades: list
            List with the dictionary that contains the current open trades.
        filter_ticker: bool
            True to return a dictionary with the open trades for each symbol.
        filter_strat: bool
            True to return a dictionry with the open trades for each strategy.
        use_size: bool
            To calculate quantity in contracts instead of trades.

        Returns
        -------
        qty: int | dict
            Integer with the number of open positions. If there is ticker or
            strategy filters applied it will be a dictionary with the value 
            for each filter.
        '''

        qty: dict = {}
        trade: Trade
        # Filtered by ticker and strat
        if filter_ticker and filter_strat:

            # Store the trade qty for all the open trades
            for trade in open_trades:
                size = trade.current_size if use_size else 1
                # If new ticker
                if trade.ticker not in qty:
                    qty[trade.ticker] = {trade.strategy.name: size}
                # For already added tickers
                elif trade.strategy not in qty[trade.ticker]:
                    qty[trade.ticker][trade.strategy.name] = size
                else:
                    qty[trade.ticker][trade.strategy.name] += size

            # If the current iteration ticker has no open trades add it
            if candle['Ticker'] not in qty:
                qty[candle['Ticker']] = {strat: 0 for strat in self.entries}

            qty[candle['Ticker']] = {**qty[candle['Ticker']], **{strat: 0 for strat in self.entries if strat not in qty[candle['Ticker']]}}

        # Filtered by ticker
        elif filter_ticker:

            # Store the trade qty for all the open trades
            for trade in open_trades:
                size = trade.current_size if use_size else 1
                # If new ticker
                if trade.ticker not in qty:
                    qty[trade.ticker] = size
                # For already added tickers
                else:
                    qty[trade.ticker] += size

            # If the current iteration ticker has no open trades add it
            if candle['Ticker'] not in qty:
                qty[candle['Ticker']] = 0

        # Filtered by strat
        elif filter_strat and not filter_ticker:

            # Store the values for all the open trades
            for trade in open_trades:
                size = trade.current_size if use_size else 1
                if trade.strategy.name not in qty:
                    qty[trade.strategy.name] = size
                else:
                    qty[trade.strategy.name] += size

            # If the current iteration strategies have no open trades add them
            for strat in self.entries:
                if strat not in qty:
                    qty[strat] = 0

        # Not filtered
        else:
            qty: float = sum([trade.current_size for trade in open_trades]) if use_size \
                        else len(open_trades)
        
        return qty

    def tradesDF(self, trades:(list | pd.DataFrame), net_results:bool=True) -> pd.DataFrame:
        
        trades = copy.deepcopy(trades)
        if not isinstance(trades, pd.DataFrame):
            trades: pd.DataFrame = pd.DataFrame([{**t.to_dict(), **{'Trades':t}} for t in trades])

        if not trades.empty:
            results = f"{'Net' if net_results else 'Gross'}Result"
            trades['InitBalance'] = trades['Balance'].copy()
            trades['Balance'] = trades['InitBalance'] + trades[results]
            trades['RetPct'] = trades[results] / trades['InitBalance']
            trades.loc[:,'AccountPeak'] = trades['Balance'].cummax()
            trades.loc[:,'AccountDD'] = 1 - trades['Balance']/trades['AccountPeak']
            trades = trades.fillna(0)

        return trades
    
    def openTrade(self, candle:dict, strategy:StrategyConfig, asset:AssetConfig, side:TradeSide, 
                  entry:float, current_capital:float) -> Trade:

        # Define the new order
        risk: list = []
        filtered_trades: list = self.getFilteredTrades(self.closed_trades, candle['Ticker'], strategy.name)
        filtered_trades: pd.Series = self.tradesDF(filtered_trades)['PctRet'] \
                                if len(filtered_trades) > 0 else pd.Series(dtype='float64')
        
        if asset.risk != None:
            asset.risk.returns = copy.deepcopy(filtered_trades)
            risk.append(copy.deepcopy(asset.risk))
        if strategy.risk != None:
            strategy.risk.returns = copy.deepcopy(filtered_trades)
            risk.append(copy.deepcopy(strategy.risk))

        if len(risk) == 0:
            raise ValueError(f'There is no type of risk defined for the asset ({asset.name}) or the strategy {strategy.name}')
        
        if len(filtered_trades) > 0:
            if strategy.drawdown != None:
                for r in risk:
                    r.addMitigation(mitigation=strategy.drawdown)
            if asset.drawdown != None:
                for r in risk:
                    r.addMitigation(mitigation=strategy.drawdown)

        return Trade(candle, side, strategy, entry, current_capital, risks=risk, 
                            allocate=self.config.allocate)
    
    def calculateBalance(self, trades:list=None, verbose:bool=False) -> pd.DataFrame:

        if not isinstance(trades, list):
            if len(self.closed_trades) <= 0 and self.verbose:
                print('There are no trades to plot')
                return None
            trades = copy.deepcopy(self.closed_trades)

        trades = copy.deepcopy(trades)
        balance: list = []
        trade: Trade
        for t, trade in enumerate([t for t in trades if t.has_executions]):
            result: list = []
            prev_c = trade.execution_candles[0]
            for i in range(len(trade.execution_candles)):
                c = trade.execution_candles[i]
                if len(trade.execution_candles) == 1:
                    val = ((trade.exit_price - trade.entry_price) if trade.signal == TradeSide.LONG \
                        else (trade.entry_price - trade.exit_price)) * trade.entries_size - trade.commissions_value
                elif i == 0:
                    val = ((c['Close'] - trade.entry_price) if trade.signal == TradeSide.LONG \
                        else (trade.entry_price - c['Close'])) * trade.entries_size - trade.commissions_value
                elif i == len(trade.execution_candles)-1:
                    val = ((trade.exit_price - prev_c['Close']) if trade.signal == TradeSide.LONG \
                        else (prev_c['Close'] - trade.exit_price)) * trade.entries_size
                else:
                    val = ((c['Close'] - prev_c['Close']) if trade.signal == TradeSide.LONG \
                        else (prev_c['Close'] - c['Close'])) * trade.entries_size

                balance.append({'DateTime':c['DateTime'], 'DailyBalance': val})
                result.append(balance[-1]['DailyBalance'])
                prev_c = c
            if verbose and sum(result) != trade.net_result:
                print(t)
                print(result, sum(result), trade.net_result)

        balance: pd.DataFrame = pd.DataFrame(balance).groupby('DateTime').agg('sum')
        balance.reset_index(drop=False, inplace=True)
        balance.loc[:,'Added'] = np.where(balance['DateTime'].dt.month != \
                                          balance['DateTime'].shift(1).dt.month, 
                                          self.config.monthly_add, 0)
        balance.loc[:,'Added'] = balance['Added'].cumsum()
        balance.loc[:,'Balance'] = balance['DailyBalance'].cumsum() + self.config.capital
        balance.loc[:,'Balance'] = balance['Balance'] + balance['Added']
        balance.loc[:,'RetPct'] = balance['Balance'] / balance['Balance'].shift(1) - 1
        balance.loc[:,'AccountPeak'] = balance['Balance'].cummax()
        balance.loc[:,'AccountDD'] = 1 - balance['Balance']/balance['AccountPeak']

        return balance