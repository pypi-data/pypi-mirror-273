
import os
import copy
import math
import datetime as dt
import pytz
import enum
import numpy as np
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from signals import ContinuousSignals, DiscreteSignals
from indicators import Indicators
from backtest_utils import (Commissions, BtConfig, TradeSide, OrderType, CloseMethod, 
    AssetConfig, StrategyConfig, Trade, SignalsSide)
from execution_utils import (DrawDownMitigation, RiskCalculation,
    KPIs, Leverage, Metrics, Transitions, Execution,
    JSON)
from backtest_utils import Backtest, ReturnsType

#from google_sheets.google_sheets import GoogleSheets

class ExecutionType(enum.Enum):
    BACKTEST: str = 'BACKTEST'
    PAPER: str = 'PAPER'
    REAL: str = 'REAL'

class TradingExecution(Backtest):

    def __init__(self, strategies:dict, config:BtConfig=None, 
                 trading_type:ExecutionType=ExecutionType.BACKTEST, 
                 verbose:bool=False, errors:bool=False) -> None:
        super().__init__(strategies, config, verbose, errors)

        self.trading_type: ExecutionType = trading_type
        self.verbose: bool = verbose
        self.errors: bool = errors

    def prepareData(self, df:pd.DataFrame) -> pd.DataFrame:

        '''
        Prepares the needed data.

        Parameters
        ----------
        df: pd.DataFrame
            Contains the complete candle data.
        '''
        
        # Check if the needed data is in the dataframe
        df.reset_index(drop=False, inplace=True)
        self.data_df: pd.DataFrame = self._newDf(df, needed_cols=['DateTime', 'Open', 'High', 'Low', 
                                                                  'Close', 'Spread', 'SLdist', 'CurrencyMult'], 
                                   overwrite=True)
        if 'DateTime' not in self.data_df.columns and self.verbose:
            print('ATENTION: There is no DateTime column so there will be no iteration!')

        self.open_trades: list = []
        self.closed_trades: list = []
        self.balance: list = []
        self.getEntries(self.data_df.columns)
        self.getExits(self.data_df.columns)

    def checkSLdata(self, candle:dict) -> dict:

        if 'SLdist' in candle:
            if self.config.use_sl and candle['SLdist'] != candle['SLdist']:
                candle['SLdist'] = False
            elif candle['SLdist'] != candle['SLdist']:
                candle['SLdist'] = copy.deepcopy(candle['Close'])
        else:
            candle['SLdist'] = copy.deepcopy(candle['Close'])

        return candle
    
    def _execute(self, candle:dict, prev_candle:dict, balance:float) -> None:
        
        # Look for entries
        exe_result: float = 0
        if len(self.entries) > 0:
            
            # Get trades qty
            raw_qty: (float | dict) = self.openQty(candle, self.open_trades, 
                                                    self.config.filter_ticker, 
                                                    self.config.filter_strat,
                                                    use_size=True)

            for strat in self.entries:

                if self.config.filter_ticker and self.config.filter_strat and \
                    strat in raw_qty[candle['Ticker']]:
                    trades_qty: float = raw_qty[candle['Ticker']][strat]
                elif self.config.filter_ticker:
                    trades_qty: float = raw_qty[candle['Ticker']]
                elif self.config.filter_strat:
                    trades_qty: float = raw_qty[strat]
                else:
                    trades_qty: float = raw_qty
                
                # If there are any orders and didn't reach the trades qty limit
                if candle[f'{strat}Entry'] != 0 and trades_qty < self.config.max_trades:

                    strategy: StrategyConfig = self.strategies[[s for s in self.strategies \
                                                if self.strategies[s].name == strat][0]]
                    asset: AssetConfig = strategy.assets[candle['Ticker']]
                    entry: float = None
                    side: int = None
                    
                    # Long orders
                    if candle[f'{strat}Entry'] > 0:
                        side: TradeSide = TradeSide.LONG # Signals.Side.LONG

                    # Short orders
                    if candle[f'{strat}Entry'] < 0:
                        side: TradeSide = TradeSide.SHORT # Signals.Side.SHORT

                    if side != None:
                    
                        entry: float = self.entryPrice(side=side, asset=asset, candle=candle, 
                                                    prev_candle=prev_candle)
                        
                        # If not entered
                        if not self.isEntered(open_trades=self.open_trades, entry=entry, candle=candle, 
                                            prev_candle=prev_candle):
                            
                            current_capital: float = self.currentCapital(balance, open_trades=self.open_trades, 
                                                                        capital_type=self.config.capital_type)
                            
                            # Reset open orders of that strategy
                            if self.config.reset_orders:
                                for trade in self.getFilteredTrades(self.open_trades, ticker=candle['Ticker'],
                                                                    strategy=strategy.name):
                                    if not trade.has_executions:
                                        trade.closeTrade(candle=candle, method=CloseMethod.CANCEL)
                                        self.closed_trades.append(trade)
                                self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]
                            
                            current_position = self.getFilteredTrades(self.open_trades, ticker=candle['Ticker'],
                                                                    strategy=strategy.name)
                            if len(current_position) == 1:
                                current_position: Trade = current_position[0]
                                if current_position.signal == side:
                                    current_position.addOrder(price=entry, candle=candle, balance=current_capital, 
                                                            order_type=asset.order_type, with_execution=False)
                                else:
                                    tot: float = sum([c[f'{strat}Entry'] for c in current_position.execution_candles])
                                    size = abs(math.floor(current_position.current_size*candle[f'{strat}Entry']/tot) \
                                        if tot != 0 else current_position.current_size)
                                    if size >= current_position.current_size:
                                        trade.closeTrade(candle=candle, method=CloseMethod.EXIT)
                                        self.closed_trades.append(trade)
                                        exe_result += trade.net_result
                                        self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]
                                        if size > current_position.current_size and \
                                            (side == TradeSide.LONG and self.config.side != SignalsSide.SHORT) or \
                                            (side == TradeSide.SHORT and self.config.side != SignalsSide.LONG):
                                            current_capital: float = self.currentCapital(balance, open_trades=self.open_trades, 
                                                                        capital_type=self.config.capital_type)
                                            self.open_trades.append(self.openTrade(candle=candle, strategy=strategy, asset=asset, 
                                                                        side=side, entry=entry, current_capital=current_capital))
                                    else:
                                        current_position.addOrder(price=entry, candle=candle, balance=current_capital, 
                                                                order_type=OrderType.MARKET, with_execution=True, 
                                                                size=size, execution_type=Execution.Type.EXIT)
                                    self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]
                            elif len(current_position) > 1:
                                raise ValueError(f"There is more than one position for {candle['Ticker']} with the continuous strategy: {strategy.name}")
                            elif (side == TradeSide.LONG and self.config.side != SignalsSide.SHORT) or \
                                (side == TradeSide.SHORT and self.config.side != SignalsSide.LONG):
                                self.open_trades.append(self.openTrade(candle=candle, strategy=strategy, asset=asset, 
                                                                        side=side, entry=entry, current_capital=current_capital))

        # Review pending orders execution
        if len(self.open_trades) > 0:

            trade: Trade
            for trade in self.open_trades:

                if trade.ticker == candle['Ticker']:
                    current_capital: float = self.currentCapital(balance, open_trades=self.open_trades, 
                                                                        capital_type=self.config.capital_type)
                    trade.executeOrder(candle=candle, balance=current_capital)
                    # Store trade evolution
                    trade.addCandle(candle)
                
        # Check open trades limits orders
        if len(self.open_trades) > 0 and (self.config.use_sl or self.config.use_tp):
            
            delete: list = []
            for trade in self.open_trades:

                if candle['Ticker'] == trade.ticker:

                    # Check SL, TP and Time Limit
                    if trade.checkSL(candle=candle) or trade.checkTP(candle=candle) \
                        or trade.checkTimeLimit(candle=candle):
                        self.closed_trades.append(trade)
                        exe_result += trade.net_result
                        delete.append(trade)
            
            # Delete open trades if already exited
            for d in delete:
                self.open_trades.remove(d)

        # Check open trades Exits if the strategy has exit conditions
        if len(self.exits) > 0:

            delete: list = []
            for strat in self.entries:

                for trade in self.open_trades:
                    if trade.ticker == candle['Ticker'] and trade.strategy.name == strat:

                        price: float = None
                        # Exit Buy
                        if candle[f'{strat}Exit'] == 1 and trade.signal == TradeSide.LONG:
                            price=candle['Open']
                            
                        # Exit Sell
                        elif candle[f'{strat}Exit'] == -1 and trade.signal == TradeSide.SHORT:
                            price=candle['Open'] + candle['Spread']
                                
                        if price != None:
                            trade.closeTrade(candle=candle, price=price, method=CloseMethod.EXIT)
                            self.closed_trades.append(trade)
                            exe_result += trade.net_result
                            delete.append(trade)
            
            for d in delete:
                self.open_trades.remove(d)

        return exe_result
    
    def _backtest(self, candle:dict, prev_candle:dict, balance:float) -> None:
        
        # Look for entries
        exe_result: float = 0
        if len(self.entries) > 0:
            
            # Get trades qty
            raw_qty: (float | dict) = self.openQty(candle, self.open_trades, 
                                                    self.config.filter_ticker, 
                                                    self.config.filter_strat,
                                                    use_size=True)

            for strat in self.entries:

                if self.config.filter_ticker and self.config.filter_strat and \
                    strat in raw_qty[candle['Ticker']]:
                    trades_qty: float = raw_qty[candle['Ticker']][strat]
                elif self.config.filter_ticker:
                    trades_qty: float = raw_qty[candle['Ticker']]
                elif self.config.filter_strat:
                    trades_qty: float = raw_qty[strat]
                else:
                    trades_qty: float = raw_qty
                
                # If there are any orders and didn't reach the trades qty limit
                if candle[f'{strat}Entry'] != 0 and trades_qty < self.config.max_trades:
                    
                    strategy: StrategyConfig = self.strategies[[s for s in self.strategies \
                                                if self.strategies[s].name == strat][0]]
                    asset: AssetConfig = strategy.assets[candle['Ticker']]
                    entry: float = None
                    side: int = None
                    
                    # Long orders
                    if candle[f'{strat}Entry'] > 0:
                        side: TradeSide = TradeSide.LONG # Signals.Side.LONG

                    # Short orders
                    if candle[f'{strat}Entry'] < 0:
                        side: TradeSide = TradeSide.SHORT # Signals.Side.SHORT

                    if side != None:
                    
                        entry: float = self.entryPrice(side=side, asset=asset, candle=candle, 
                                                    prev_candle=prev_candle)
                        
                        # If not entered
                        if not self.isEntered(open_trades=self.open_trades, entry=entry, candle=candle, 
                                            prev_candle=prev_candle):
                            
                            current_capital: float = self.currentCapital(balance, open_trades=self.open_trades, 
                                                                        capital_type=self.config.capital_type)
                            
                            # Reset open orders of that strategy
                            if self.config.reset_orders:
                                for trade in self.getFilteredTrades(self.open_trades, ticker=candle['Ticker'],
                                                                    strategy=strategy.name):
                                    if not trade.has_executions:
                                        trade.closeTrade(candle=candle, method=CloseMethod.CANCEL)
                                        self.closed_trades.append(trade)
                                self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]
                            
                            current_position = self.getFilteredTrades(self.open_trades, ticker=candle['Ticker'],
                                                                    strategy=strategy.name)
                            if len(current_position) == 1:
                                current_position: Trade = current_position[0]
                                if current_position.signal == side:
                                    current_position.addOrder(price=entry, candle=candle, balance=current_capital, 
                                                            order_type=asset.order_type, with_execution=False)
                                else:
                                    tot: float = sum([c[f'{strat}Entry'] for c in current_position.execution_candles])
                                    size = abs(math.floor(current_position.current_size*candle[f'{strat}Entry']/tot) \
                                        if tot != 0 else current_position.current_size)
                                    if size >= current_position.current_size:
                                        current_position.closeTrade(candle=candle, method=CloseMethod.EXIT)
                                        self.closed_trades.append(copy.deepcopy(current_position))
                                        exe_result += trade.net_result
                                        self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]
                                        if size > current_position.current_size and \
                                            (side == TradeSide.LONG and self.config.side != SignalsSide.SHORT) or \
                                            (side == TradeSide.SHORT and self.config.side != SignalsSide.LONG):
                                            current_capital: float = self.currentCapital(balance, open_trades=self.open_trades, 
                                                                        capital_type=self.config.capital_type)
                                            self.open_trades.append(self.openTrade(candle=candle, strategy=strategy, asset=asset, 
                                                                        side=side, entry=entry, current_capital=current_capital))
                                    else:
                                        current_position.addOrder(price=entry, candle=candle, balance=current_capital, 
                                                                order_type=OrderType.MARKET, with_execution=True, 
                                                                size=size, execution_type=Execution.Type.EXIT)
                                    self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]
                            elif len(current_position) > 1:
                                raise ValueError(f"There is more than one position for {candle['Ticker']} with the continuous strategy: {strategy.name}")
                            elif (side == TradeSide.LONG and self.config.side != SignalsSide.SHORT) or \
                                (side == TradeSide.SHORT and self.config.side != SignalsSide.LONG):
                                self.open_trades.append(self.openTrade(candle=candle, strategy=strategy, asset=asset, 
                                                                        side=side, entry=entry, current_capital=current_capital))

        # Review pending orders execution
        if len(self.open_trades) > 0:

            trade: Trade
            for trade in self.open_trades:

                if trade.ticker == candle['Ticker']:
                    
                    self.trade = copy.deepcopy(trade)
                    current_capital: float = self.currentCapital(balance, open_trades=self.open_trades, 
                                                                        capital_type=self.config.capital_type)
                    trade.executeOrder(candle=candle, balance=current_capital)
                    # Store trade evolution
                    trade.addCandle(candle)
                
        # Check open trades limits orders
        if len(self.open_trades) > 0 and (self.config.use_sl or self.config.use_tp):
            
            for trade in self.open_trades:

                if candle['Ticker'] == trade.ticker:

                    self.trade = trade
                    # Check SL, TP and Time Limit
                    if trade.checkSL(candle=candle) or trade.checkTP(candle=candle) \
                        or trade.checkTimeLimit(candle=candle):
                        
                        self.closed_trades.append(trade)
                        exe_result += trade.net_result
            
            # Delete open trades if already exited
            self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]

        # Check open trades Exits if the strategy has exit conditions
        if len(self.exits) > 0:

            for trade in self.open_trades:
                if trade.ticker == candle['Ticker']:

                    price: float = None
                    # Exit Buy
                    if candle[f'{trade.strategy.name}Exit'] == 1 and \
                        trade.signal.value == TradeSide.LONG.value:
                        price = candle['Open']
                        
                    # Exit Sell
                    elif candle[f'{trade.strategy.name}Exit'] == -1 and \
                        trade.signal.value == TradeSide.SHORT.value:
                        price = candle['Open'] + candle['Spread']
                            
                    if price != None:
                        trade.closeTrade(candle=candle, price=price, method=CloseMethod.EXIT)
                        self.closed_trades.append(trade)
                        exe_result += trade.net_result
            
            # Delete open trades if already exited
            self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]

        return exe_result

    def execute(self, df:pd.DataFrame) -> None:

        self.prepareData(df=df)
        
        if self.trading_type.value == ExecutionType.BACKTEST.value:
        
            # Initialize variables
            last_date = None
            self.balance: list = [self.config.capital]
            self.backup_balance: list = []
            prev_candle: dict = {}
            for s in self.strategies:
                for t in self.strategies[s].assets:
                    prev_candle[t] = {}

            # Group data by DateTime
            for g in self.data_df.groupby('DateTime'):
            
                date_result: float = 0
                current_date = g[0]

                # Iterate for each asset in this DateTime
                for i in g[1].index:

                    candle: pd.Series = self.checkSLdata(copy.deepcopy(g[1].loc[i]))
                    
                    # Check if we are between the backtest dates
                    if candle['DateTime'] < self.config.init_date or candle['DateTime'] > self.config.final_date:
                        continue

                    # Add the monthly add if greater than 0 and the month has changed
                    if self.config.monthly_add > 0 and last_date != None and \
                        last_date.month != current_date.month:
                        self.balance[-1] = self.balance[-1] + self.config.monthly_add

                    date_result += self._backtest(candle=candle, prev_candle=prev_candle, balance=self.balance[-1])
                        
                    last_date = copy.deepcopy(current_date)
                    prev_candle[candle['Ticker']] = candle

                self.balance.append(self.balance[-1]+date_result)
                self.backup_balance.append(self.config.capital + sum([trade.net_result for trade in self.closed_trades]))

            temp:list = []      
            t: Trade
            for t in self.open_trades:
                trade: Trade = copy.deepcopy(t)
                candle = self.data_df[self.data_df['Ticker'] == trade.ticker].iloc[-1]
                trade.closeTrade(candle=candle, price=candle['Close'], method=CloseMethod.EXIT)
                temp.append(trade)
            self.closed_trades: list = self.closed_trades + temp
        
        else:
            g = self.data_df.groupby('DateTime')[-1]
            
            date_result: float = 0
            current_date = g[0]

            # Iterate for each asset in this DateTime
            for i in g[1].index:

                candle: pd.Series = self.checkSLdata(copy.deepcopy(g[1].loc[i]))

                date_result += self._execute(candle=candle, prev_candle=prev_candle, balance=self.balance[-1])
                    
                last_date = copy.deepcopy(current_date)
                prev_candle[candle['Ticker']] = candle

            self.balance.append(self.balance[-1]+date_result)
            self.backup_balance.append(self.config.capital + sum([trade.net_result for trade in self.closed_trades]))

    def getTrades(self) -> pd.DataFrame:
        
        # Calculate and store final data
        # self.trades = self.tradesDF(closed_trades)

        closed_trades: pd.DataFrame = self.tradesDF(pd.DataFrame(
                    [{**copy.deepcopy(t).to_dict(), **{'Trades':t}} for t in self.closed_trades \
                     if t.entries_size != 0]))
        if not closed_trades.empty:
            closed_trades['StratName'] = closed_trades['Strategy'].apply(lambda x: x['name'])
        # closed_trades['WeekDay'] = closed_trades['EntryTime'].dt.day_name()
        open_trades: pd.DataFrame = pd.DataFrame(
                    [{**copy.deepcopy(t).to_dict(), **{'Trades':t}} for t in self.open_trades \
                     if t.entries_size != 0])

        return closed_trades, open_trades
    
    def saveResult(self, file:str='ClosedTrades.xlsx') -> None:

        if '.xlsx' not in file:
            file = f'{file}.xlsx'

        closed_trades, open_trades = self.getTrades()
        writer: pd.ExcelWriter = pd.ExcelWriter(file)
        closed_trades.to_excel(writer, sheet_name='Closed', index=False)
        open_trades.to_excel(writer, sheet_name='Open', index=False)
        self.calculateBalance(verbose=False).to_excel(writer, sheet_name='Balance', index=False)
        writer.close()

    def saveJSON(self, file:str='ClosedTrades.json') -> None:

        if '.json' not in file:
            file = f'{file}.json'

        JSON().write(file, data=[t.to_dict() for t in self.closed_trades])
        
    def metrics(self, df:pd.DataFrame=None, print_stats:bool=False) -> dict:

        if not isinstance(df, pd.DataFrame):
            closed_trades, open_trades = self.getTrades()
            df: pd.DataFrame = closed_trades[(closed_trades['Method'] != 'CANCEL') & (closed_trades['Entry'] != None)].copy()
            
        # stats: dict = KPIs(df).to_dict()
        date_tag: str = 'DateTime'
        if 'DateTime' not in df:
            if 'EntryTime' in df:
                date_tag = 'EntryTime'
            elif 'OrderTime' in df:
                date_tag = 'OrderTime'
            elif 'ExitTime' in df:
                date_tag = 'ExitTime'
        
        metrics: Metrics = Metrics(trades=df.set_index(date_tag, drop=True), 
                              compound=True)
        stats: dict = metrics.calculateMetrics(
            indicators=['winrate', 'averageWin', 'averageLoss', 'totalTrades', 
                        'expectancy', 'tradingFrequency', 'kelly', 'maxDrawdown',
                        'maximum_favorable_excursion']
        )
        stats['comOverRet'] = df['ComOverRet'].mean()
        stats['MaxLeverage'] = self.config.capital / df.groupby('OrderTime')['Position'].sum().max()

        if print_stats:
            for k, v in stats.items():
                print(f"{k}: {v}")
            # print(f"Winrate: {stats['winrate'] :%}") # With two decimal spaces and commas for the thousands :,.2f
            
        return stats
    
    def stats(self, column:str='Ticker', plot:bool=False, 
                    print_stats:bool=False) -> pd.DataFrame:

        self.stats_dict: dict = {}
        pairs: list = []
        closed_trades, open_trades = self.getTrades()
        if len(closed_trades) <= 0:
            if self.verbose:
                print('There are no trades')
            return pd.DataFrame()
        else:
            trades: pd.DataFrame = closed_trades[(closed_trades['Method'] != 'CANCEL') & (closed_trades['Entry'] != None)].copy()
        
        for g in trades.groupby(column):

            temp: pd.DataFrame = g[1].copy()
            temp = self.tradesDF(trades=temp['Trades'].tolist())

            self.stats_dict[g[0]] = self.metrics(df=temp, print_stats=print_stats)
            
            if plot:
                fig = make_subplots(specs=[[{'secondary_y': True}]])
                fig.add_trace(go.Scatter(x=temp['Date'],y=temp['Balance'], name='Balance'), 
                              secondary_y=False)
                fig.add_trace(go.Scatter(x=temp['Date'], y=temp['AccountDD'] * 10000//1/100, 
                                         fill='tozeroy', name='DrawDown'), secondary_y=True)

                fig.update_xaxes(title_text='Date')
                fig.update_yaxes(title_text='Return ($)', secondary_y=False)
                fig.update_yaxes(title_text='DrawDown (%)', secondary_y=True)
                fig.update_layout(title=f"{g[0]} account balance {self.config.capital + temp['Result'].sum()*100//1/100}$", 
                                autosize=False,width=1000,height=700,)
                fig.show()

            pairs.append(g[0])

        # Comparison of pairs and total
        stats_df: pd.DataFrame = pd.DataFrame(self.stats_dict).T
        stats_df.sort_values(by=['kelly'], ascending=False, inplace=True)

        return stats_df

    def plot(self, df:pd.DataFrame=None, daily:bool=False, buy_hold:bool=True, log:bool=True) -> None:

        if df == None:
            closed_trades, open_trades = self.getTrades()
            closed_trades = closed_trades[(closed_trades['Method'] != 'CANCEL') & (closed_trades['Entry'] != None)].copy()
            if len(self.closed_trades) <= 0 and self.verbose:
                print('There are no trades to plot')
                return None
        else:
            closed_trades: pd.DataFrame = df.copy()
        
        if daily:
            balance: pd.DataFrame = self.calculateBalance(verbose=False)
        else:
            balance: pd.DataFrame = closed_trades.copy()

        if 'DateTime' not in balance and 'ExitTime' in balance:
            balance['DateTime'] = balance['ExitTime'].copy()

        # Plot Backtest results
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.0,
                            row_heights=[3,1],
                            specs=[[{'secondary_y': True}],[{'secondary_y': False}]])

        fig.add_trace(go.Scatter(x=balance['DateTime'], y=balance['Balance'], name='Balance'), 
                      row=1, col=1, secondary_y=False)
        fig.add_trace(go.Scatter(x=balance['DateTime'], y=balance['AccountDD'] * 10000//1/100, 
                                 fill='tozeroy', name='DrawDown'), row=1, col=1, secondary_y=True)
        fig.add_trace(go.Scatter(x=balance['DateTime'], y=balance['AccountPeak'], name='MaxBalance'), 
                      row=1, col=1, secondary_y=False)
        
        # Add Buy & Hold comparison
        if buy_hold:
            allocation: dict = {}
            for strat in self.strategies.values():
                for asset in strat.assets.values():
                    if asset.name not in allocation:
                        allocation[asset.name] = asset.allocation
                    else:
                        allocation[asset.name] += asset.allocation

            temp: pd.DataFrame = self.data_df[(self.config.init_date < self.data_df['DateTime']) & \
                                              (self.data_df['DateTime'] < self.config.final_date)]
            bh_df: list = []
            for strategy in self.strategies.values():
                for g in temp.groupby('Ticker'):
                    g[1].set_index('DateTime', inplace=True)
                    g[1][g[0]] = g[1]['Close']
                    bh_df.append(g[1][g[0]] * strategy.assets[g[0]].allocation)
            bh_df: pd.DataFrame = pd.concat(bh_df, axis=1)
            bh_df.fillna(0, inplace=True)
            bh_df['Close'] = bh_df.sum(axis=1)
            fig.add_trace(go.Scatter(x=bh_df.index, 
                            y=bh_df['Close']/bh_df['Close'].iloc[0]*self.config.capital, 
                            name='Buy & Hold'), 
                            row=1, col=1, secondary_y=False)

        fig.update_yaxes(title_text='Return ($)', row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text='DrawDown (%)', row=1, col=1, secondary_y=True)

        if log:
            fig.update_yaxes(type="log", row=1, col=1, secondary_y=False)

        fig.add_trace(go.Scatter(x=balance['DateTime'][balance['RetPct'] > 0.0],
                                 y=balance['RetPct'][balance['RetPct'] > 0.0] * 10000//1/100, 
                                 name='Wins', marker_color='green', mode='markers'), row=2, col=1)
        fig.add_trace(go.Scatter(x=balance['DateTime'][balance['RetPct'] <= 0.0], 
                                 y=balance['RetPct'][balance['RetPct'] <= 0.0] * 10000//1/100, 
                                 name='Losses', marker_color='red', mode='markers'), row=2, col=1)

        fig.update_yaxes(title_text='Return (%)', row=2, col=1)

        fig.update_xaxes(title_text='Date', row=2, col=1)
        fig.update_layout(title=f"Account balance {self.config.capital + sum([t.net_result for t in self.closed_trades])*100//1/100}$", 
                          autosize=False, width=1000, height=700)

        fig.show()

    def calculateSignals(self, data:dict={}) -> pd.DataFrame:

        import yfinance as yf
        
        cont_signals: ContinuousSignals = ContinuousSignals(backtest=self.trading_type == ExecutionType.BACKTEST, 
                                                       side=ContinuousSignals.Side.LONG, errors=False)
        disc_signals: DiscreteSignals = DiscreteSignals(backtest=self.trading_type == ExecutionType.BACKTEST, 
                                                   side=DiscreteSignals.Side.LONG, errors=False)

        for strat in self.strategies:

            if self.strategies[strat].name in dir(cont_signals) and self.strategies[strat].strat_type.value == StrategyConfig.Type.CONTINUOUS.value:
                signal = getattr(cont_signals, self.strategies[strat].name)
            elif self.strategies[strat].name in dir(disc_signals) and self.strategies[strat].strat_type.value == StrategyConfig.Type.DISCRETE.value:
                signal = getattr(disc_signals, self.strategies[strat].name)
            elif self.verbose:
                print(f'{strat} ({self.strategies[strat].name}) not between the defined signals in both, discrete and continuous.')
                continue

            for t,c in self.strategies[strat].assets.items():

                if t not in data:
                    print('Downloading data')
                    temp: pd.DataFrame = yf.Ticker(t).history(period='max',interval='1d') # gbms.generateGBM(symbol=t, save=False) # 
                    temp.columns = [c.capitalize() for c in temp.columns]
                    temp.rename(columns={'Date':'DateTime'}, inplace=True)
                else:
                    temp = data[t].copy()
                    
                temp.loc[:,'Ticker'] = t
                if 'SLdist' not in temp:
                    indicators: Indicators = Indicators(ohlc=temp, errors=False)
                    temp.loc[:,'SLdist'] = indicators.atr(n=20, method='s', dataname='ATR', new_df=temp)['ATR']
                if 'Spread' not in temp:
                    temp.loc[:,'Spread'] = 0
                if 'CurrencyMult' not in temp:
                    temp.loc[:,'CurrencyMult'] = 1
                if 'Date' not in temp.columns:
                    if temp.index.inferred_type == 'datetime64':
                        temp.loc[:,'Date'] = temp.index
                    else:
                        temp.loc[:,'Date'] = pd.to_datetime(temp.index)
                if 'DateTime' not in temp.columns and 'Date' in temp.columns:
                    temp.rename(columns={'Date':'DateTime'}, inplace=True)
                if 'Volume' not in temp.columns:
                    temp['Volume'] = [0]*len(temp)

                temp = signal(df=temp, strat_name=self.strategies[strat].name)
                if t in data:
                    for c in temp:
                        if c not in data[t]:
                            data[t][c] = temp[c]
                else:
                    data[t] = temp.copy()

        # Prepare data
        df: pd.DataFrame = pd.concat([data[t] for t in data], ignore_index=True)
        df.sort_values('DateTime', inplace=True)
        try:
            df.loc[:,'DateTime'] = pd.to_datetime(df['DateTime'], unit='s')
        except:
            df.loc[:,'DateTime'] = pd.to_datetime(df['DateTime'], utc=True)
        if df['DateTime'].iloc[0].tzinfo != None:
            df['DateTime'] = df['DateTime'].dt.tz_convert(None)
        df['Close'] = df['Close'].ffill()
        df['Spread'] = df['Spread'].ffill()
        df['Open'] = np.where(df['Open'] != df['Open'], df['Close'], df['Open'])
        df['High'] = np.where(df['High'] != df['High'], df['Close'], df['High'])
        df['Low'] = np.where(df['Low'] != df['Low'], df['Close'], df['Low'])

        return df



if __name__ == '__main__':


    # from randomWalk import GeometricBrownianMotionAssetSimulator as GBMS
    # gbms: GBMS = GBMS(start_date=None, end_date=None, periods=60*24*365*10,
    #             output_dir='random_data', symbol_length=4, init_price=10.0,
    #             mu=0.1, sigma=0.3, pareto_shape=1.5, freq='B',
    #             remove_files=True)

    config: BtConfig = BtConfig(init_date='2010-01-01', final_date=dt.date.today().strftime('%Y-%m-%d'), 
                      capital=5000.0, monthly_add=0, allocate=False,  # (dt.date.today() - dt.timedelta(days=250)).strftime('%Y-%m-%d')
                      min_size=1000, max_size=10000000, commission=Commissions(), 
                      use_sl=True, use_tp=True, time_limit=0, side=SignalsSide.LONG,
                      max_trades=100000, offset_aware=False)

    etf_com = [Commissions(ctype=Commissions.Type.FIXED, commission=1, cmin=1), 
               Commissions(ctype=Commissions.Type.PERCENTAGE, commission=0.25, cmin=0)]

    strategies: dict = {
        'donchianBreakout': StrategyConfig(name='donchianBreakout', use_sl=True, use_tp=False, time_limit=0, 
                                    timeframe='D1', allocation=1.0, strat_type=StrategyConfig.Type.CONTINUOUS,
                                    assets={
                                        'SPY':AssetConfig(name='SPY', sl=4.0, tp=10.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com)
                                    },
                                    risk=RiskCalculation(risk_type=RiskCalculation.Type.EQUAL, max_risk=1, 
                                                    default_risk=1, bounded=False, scale=True)),
        'atrExt': StrategyConfig(name='atrExt', use_sl=True, use_tp=True, time_limit=100, 
                                     timeframe='D1', allocation=1.0, strat_type=StrategyConfig.Type.DISCRETE, 
                                     assets={
                                        'SPY':AssetConfig(name='SPY', sl=4.0, tp=10.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com)
                                    },
                                     risk=RiskCalculation(risk_type=RiskCalculation.Type.EQUAL, max_risk=0.1, 
                                                      default_risk=0.01, bounded=False, scale=False)),
    }
        
    strategies: dict = {
        'rsiExtreme': StrategyConfig(name='rsiExtreme', use_sl=True, use_tp=True, time_limit=100, 
                                        timeframe='D1', allocation=1.0, strat_type=StrategyConfig.Type.DISCRETE, 
                                        assets={
                                        'SPY':AssetConfig(name='SPY', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'GC=F':AssetConfig(name='GC=F', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'EURUSD=X':AssetConfig(name='EURUSD=X', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'BTC=F':AssetConfig(name='BTC=F', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                    },
                                        risk=RiskCalculation(risk_type=RiskCalculation.Type.EQUAL, max_risk=0.1, 
                                                        default_risk=0.01, bounded=False, scale=False)),
        'deMarker': StrategyConfig(name='deMarker', use_sl=True, use_tp=True, time_limit=100, 
                                        timeframe='D1', allocation=1.0, strat_type=StrategyConfig.Type.DISCRETE, 
                                        assets={
                                        'SPY':AssetConfig(name='SPY', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'GC=F':AssetConfig(name='GC=F', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'EURUSD=X':AssetConfig(name='EURUSD=X', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'BTC=F':AssetConfig(name='BTC=F', sl=6.0, tp=6.0, order=OrderType.LIMIT, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                    },
                                        risk=RiskCalculation(risk_type=RiskCalculation.Type.EQUAL, max_risk=0.1, 
                                                        default_risk=0.01, bounded=False, scale=False)),
        'volatBands': StrategyConfig(name='volatBands', use_sl=True, use_tp=True, time_limit=100, 
                                        timeframe='D1', allocation=1.0, strat_type=StrategyConfig.Type.DISCRETE, 
                                        assets={
                                        'SPY':AssetConfig(name='SPY', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'GC=F':AssetConfig(name='GC=F', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'EURUSD=X':AssetConfig(name='EURUSD=X', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'BTC=F':AssetConfig(name='BTC=F', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                    },
                                        risk=RiskCalculation(risk_type=RiskCalculation.Type.EQUAL, max_risk=0.1, 
                                                        default_risk=0.01, bounded=False, scale=False)),
        'bollingerAggresive': StrategyConfig(name='bollingerAggresive', use_sl=True, use_tp=True, time_limit=100, 
                                        timeframe='D1', allocation=1.0, strat_type=StrategyConfig.Type.DISCRETE, 
                                        assets={
                                        'SPY':AssetConfig(name='SPY', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'GC=F':AssetConfig(name='GC=F', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'EURUSD=X':AssetConfig(name='EURUSD=X', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                        'BTC=F':AssetConfig(name='BTC=F', sl=6.0, tp=6.0, order=OrderType.MARKET, 
                                                        leverage=Leverage(Leverage.Type.SIZE, 1),
                                                        min_size=1, max_size=5000, risk=None, allocation=1.0,
                                                        account_currency='EUR', asset_currency='USD',
                                                        commissions=etf_com),
                                    },
                                        risk=RiskCalculation(risk_type=RiskCalculation.Type.EQUAL, max_risk=0.1, 
                                                        default_risk=0.01, bounded=False, scale=False)),
    }

    # Backtest
    bt: TradingExecution = TradingExecution(strategies=strategies, config=config, 
                                            trading_type=ExecutionType.BACKTEST)
    
    data: dict = {}
    df: pd.DataFrame = bt.calculateSignals(data)
    trades: pd.DataFrame = bt.execute(df=df)

    # bt.btPlot(daily=True, buy_hold=True, log=False)
    stats: pd.DataFrame = bt.stats(column='StratName')
    print(stats)

    bt.saveResult('Backtest_Trades.xlsx')