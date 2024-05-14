
import os
import copy
import math
import datetime as dt
import numpy as np
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from signals import ContinuousSignals
from indicators import OHLC, Indicators
from backtest_utils import (CapitalType, Commissions, BtConfig, 
    Backtest, ReturnsType)
from execution_utils import (TradeSide, OrderType, CloseMethod, 
    DrawDownMitigation, RiskCalculation, AssetConfig, StrategyConfig,
    Trade, KPIs, Leverage, Metrics, Transitions, SignalsSide, Execution,
    JSON)
#from google_sheets.google_sheets import GoogleSheets

class ContinuousBackTest(Backtest):

    '''
    Class used to carry out the backtest of the strategy.
    '''
    
    config: BtConfig = BtConfig((dt.date.today() - dt.timedelta(days=365*2)).strftime('%Y-%m-%d'), 
                      dt.date.today().strftime('%Y-%m-%d'), capital=10000.0, monthly_add=200, 
                      min_size=1000, max_size=10000000, commission=Commissions(),
                      allocate=False)

    def __init__(self, strategies:dict, config:BtConfig=None) -> None:

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
        '''

        self.strategies: dict = strategies
        self.config = config if config != None else self.config

    def backtest(self, df:pd.DataFrame) -> pd.DataFrame:

        '''
        Carries out the backtest logic.

        Parameters
        ----------
        df: pd.DataFrame
            Contains the complete candle data.

        Returns
        -------
        trades: pd.DataFrame
            Contains the trades carried out during the backtest.
        '''

        # Check if the needed data is in the dataframe
        self.data_df: pd.DataFrame = self._newDf(df, needed_cols=['DateTime', 'Open', 'High', 'Low', 
                                                                  'Close', 'Spread', 'SLdist', 'CurrencyMult'], 
                                   overwrite=True)
        if 'DateTime' not in self.data_df.columns:
            print('ATENTION: There is no DateTime column so there will be no iteration!')
            
        # Initialize variables
        last_date = None
        self.open_trades: list = []
        self.closed_trades: list = []
        self.balance: list = [self.config.capital]
        self.backup_balance: list = []
        prev_candle: dict = {}
        for s in self.strategies:
            for t in self.strategies[s].assets:
                prev_candle[t] = {}
        self.getEntries(self.data_df.columns)
        self.getExits(self.data_df.columns)

        # Group data by DateTime
        for g in self.data_df.groupby('DateTime'):
          
            date_result: float = 0
            current_date = g[0]

            # Iterate for each asset in this DateTime
            for i in g[1].index:

                candle: pd.Series = copy.deepcopy(g[1].loc[i])

                if 'SLdist' in candle:
                    if self.config.use_sl and candle['SLdist'] != candle['SLdist']:
                        continue
                    elif candle['SLdist'] != candle['SLdist']:
                        candle['SLdist'] = copy.deepcopy(candle['Close'])
                else:
                    candle['SLdist'] = copy.deepcopy(candle['Close'])
                
                # Check if we are between the backtest dates
                if candle['DateTime'] < self.config.init_date or candle['DateTime'] > self.config.final_date:
                    continue

                # Add the monthly add if greater than 0 and the month has changed
                if self.config.monthly_add > 0 and last_date != None and \
                    last_date.month != current_date.month:
                    self.balance[-1] = self.balance[-1] + self.config.monthly_add
                    
                # Look for entries
                if len(self.entries) > 0:
                    
                    # Get trades qty
                    raw_qty: (float or dict) = self.openQty(candle, self.open_trades, 
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
                        
                        # print(candle[f'{strat}Entry'])
                        # If there are any orders and didn't reach the trades qty limit
                        if candle[f'{strat}Entry'] != 0 and trades_qty < self.config.max_trades:

                            strategy: StrategyConfig = self.strategies[strat]
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
                                    
                                    current_capital: float = self.currentCapital(self.balance[-1], open_trades=self.open_trades, 
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
                                                date_result += trade.net_result
                                                self.open_trades: list = [trade for trade in self.open_trades if not trade.closed]
                                                if size > current_position.current_size and \
                                                    (side == TradeSide.LONG and self.config.side != SignalsSide.SHORT) or \
                                                    (side == TradeSide.SHORT and self.config.side != SignalsSide.LONG):
                                                    current_capital: float = self.currentCapital(self.balance[-1], open_trades=self.open_trades, 
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
                            current_capital: float = self.currentCapital(self.balance[-1], open_trades=self.open_trades, 
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
                                date_result += trade.net_result
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
                                    date_result += trade.net_result
                                    delete.append(trade)
                    
                    for d in delete:
                        self.open_trades.remove(d)

                last_date = copy.deepcopy(current_date)
                prev_candle[candle['Ticker']] = candle

            self.balance.append(self.balance[-1]+date_result)
            self.backup_balance.append(self.config.capital + sum([trade.net_result for trade in self.closed_trades]))

        # Calculate and store final data
        # self.trades = self.tradesDF(closed_trades)
        self.trades: list = [{**copy.deepcopy(t).to_dict(), **{'Trades':t}} for t in self.closed_trades]
        temp:list = []
        t: Trade
        for t in self.open_trades:
            trade: Trade = copy.deepcopy(t)
            trade.closeTrade(candle=candle, price=candle['Close'], method=CloseMethod.EXIT)
            temp.append(trade)
        self.trades: pd.DataFrame = self.tradesDF(pd.DataFrame(self.trades + \
                [{**copy.deepcopy(t).to_dict(), **{'Trades':t}} for t in temp]))
        if not self.trades.empty:
            self.trades['StratName'] = self.trades['Strategy'].apply(lambda x: x['name'])
        # self.trades['WeekDay'] = self.trades['EntryTime'].dt.day_name()
        self.open_trades: pd.DataFrame = pd.DataFrame(
                    [{**copy.deepcopy(t).to_dict(), **{'Trades':t}} for t in self.open_trades])

        return self.trades.copy()
    
    def calculateBalance(self, trades:list=None, verbose:bool=True) -> pd.DataFrame:

        if not isinstance(trades, list):
            if self.trades.empty:
                print('There are no trades to plot')
                return None
            trades = self.trades['Trades'].copy().to_list()

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

    def saveResult(self, file:str='TradesBacktested.xlsx', sheet:str='CompleteTrades'):

        writer: pd.ExcelWriter = pd.ExcelWriter(file)
        self.trades.to_excel(writer, sheet_name=sheet, index=False)
        self.calculateBalance().to_excel(writer, sheet_name='Balance', index=False)
        writer.save()

    # def resultsToGoogle(self, sheetid:str, sheetrange:str):

    #     google = GoogleSheets(sheetid, secret_path=os.path.join('google_sheets','client_secrets.json'))
    #     google.appendValues(self.trades.values, sheetrange=sheetrange)

    def btKPI(self, df:pd.DataFrame=None, print_stats:bool=False) -> dict:

        if not isinstance(df, pd.DataFrame):
            df: pd.DataFrame = self.trades[(self.trades['Method'] != 'CANCEL') & (self.trades['Entry'] != None)].copy()
            
        # stats: dict = KPIs(df).to_dict()
        date_tag: str = 'DateTime'
        if 'DateTime' not in df:
            if 'EntryTime' in df:
                date_tag = 'EntryTime'
            elif 'OrderTime' in df:
                date_tag = 'OrderTime'
            elif 'ExitTime' in df:
                date_tag = 'ExitTime'
        
        metrics: Metrics = Metrics(returns=df.set_index(date_tag, drop=True)['RetPct'], 
                              compound=True)
        stats: dict = metrics.calculateMetrics(
            indicators=['winrate', 'averageWin', 'averageLoss', 
                        'expectancy', 'tradingFrequency', 'kelly', 'maxDrawdown']
        )

        if print_stats:
            print(f"Winrate: {stats['winrate'] :%}") # With two decimal spaces and commas for the thousands :,.2f
            print(f"Avg. Win: {stats['averageWin'] :%}")
            print(f"Avg. Loss: {stats['averageLoss'] :%}")
            print(f"Expectancy: {stats['expectancy'] :%}")
            print(f"Trading frequency: {stats[strat]['tradingFrequency']}")
            #print(f"Monthly Expectancy: {((1 + expectancy*len(trades)/days)**(20) - 1) :%}")
            #print(f"Anual Expectancy: {((1 + expectancy*len(trades)/days)**(52*5) - 1) :%}")
            print(f"Kelly: {stats[strat]['kelly'] :%}")
            print(f"Backtest Max. DD: {stats[strat]['maxDrawdown'] :%}")
            # print(f'Ulcer Index: {(((trades['AccountDD'] * 100)**2).sum()/len(trades['AccountDD']))**(1/2) * 100//1/100}')

        return stats

    def weekDayKPI(self, trades:pd.DataFrame=None, df:bool=False):

        trades = self.trades if trades == None else trades

        trades['Date'] = pd.to_datetime(trades['EntryTime'], format='%Y-%m-%d %H:%M:%S')
        trades['WeekDay'] = trades['Date'].dt.day_name()
        day_stats: dict = {}
        for g in trades.groupby('WeekDay'):

            day: pd.DataFrame = g[1]
            temp: dict = {}
            temp['winrate'] = len(day['Return'][day['Return'] > 0])/len(day['Return'])
            temp['avg_win'] = day['%ret'][day['%ret'] > 0].mean()
            temp['avg_loss'] = day['%ret'][day['%ret'] < 0].mean()
            temp['expectancy'] = (temp['winrate']*temp['avg_win'] - (1-temp['winrate'])*abs(temp['avg_loss']))
            temp['kelly'] = temp['expectancy']/temp['avg_win']
            day_stats[g[0]] = temp

        return pd.DataFrame(day_stats) if df else day_stats

    def tradesAnalysis(self, trades:pd.DataFrame=None, plot:bool=False):

        trades = self.trades if trades == None else trades

        temp_df:list = []
        patterns: list = []
        for i,t in enumerate(trades.values):
            temp = pd.DataFrame(t[16])
            if len(temp['Close']) > 1:
                temp['ret'] = (1 + temp['Close'].pct_change(1)).cumprod() - 1
            else:
                temp['ret'] = temp['Close']/temp['Open'] - 1
            
            if t[2] == 'Sell':
                temp['ret'] = -1*temp['ret']
                
            temp['cumMax'] = temp['ret'].cummax()
            max_idx = temp['cumMax'].idxmax()
            temp['cumMin'] = temp['ret'].cummin()
            min_idx = temp['cumMin'].idxmin()
            temp_df.append(temp)
            patterns.append({'Max': temp['ret'].max(), 'MaxIdx': temp['ret'].idxmax(),
                            'Min': temp['ret'].min(), 'MinIdx': temp['ret'].idxmin(),
                            'End': temp['ret'].tolist()[-1], 'EndIdx': len(temp['ret'])})

        if plot:
            temp_df: list = []

            fig = make_subplots(rows=1, cols=1)
            for i,t in enumerate(patterns):
                fig.add_trace(go.Scatter(x=[n for n in range(len(t['ret']))], y=t['ret'], name=f'Trade {i}'), row=1, col=1)
                fig.update_yaxes(title_text='Return', row=1, col=1)
                fig.update_xaxes(title_text='Candle since entry', row=1, col=1)
                fig.update_layout(title='Trade evolution', autosize=False,
                                    xaxis_rangeslider_visible=False,
                                    width=1000,
                                    height=700)

            fig.show()

        turn_loss: int = 0; turn_loss_idx: int = 0
        loss: int = 0; loss_idx: int = 0
        turn_win: int = 0; turn_win_idx: int = 0
        win: int = 0; win_idx: int = 0
        real: list = []
        for t in patterns:
            if t['Max'] == t['Max']:
                real.append(t)

                if t['MinIdx'] > t['MaxIdx'] and t['Max'] > 0:
                    turn_loss += 1
                    turn_loss_idx += t['MaxIdx']
                if t['Max'] <= 0:
                    loss += 1
                    loss_idx += t['MaxIdx']
                if t['MaxIdx'] > t['MinIdx'] and t['Min'] < 0:
                    turn_win += 1
                    turn_win_idx += t['MinIdx']
                if t['Min'] >= 0:
                    win += 1
                    win_idx += t['MinIdx']

        print(f'Avg. Index give up win {turn_loss_idx/turn_loss}')
        print(f'Prob. of give up win {turn_loss/len(real)}')
        print(f'Avg. Index straight loss {loss_idx/loss}')
        print(f'Prob of straight loss {loss/len(real)}')
        print(f'Avg. Index turn to win {turn_win_idx/turn_win}')
        print(f'Prob of turn to win {turn_win/len(real)}')
        print(f'Avg. Index straight win {win_idx/win}')
        print(f'Prob of straight win {win/len(real)}')

        return trades

    def btPlot(self, balance:bool=False, buy_hold:bool=True, log:bool=True) -> None:

        if self.trades.empty:
            print('There are no trades to plot')
            return None
        
        if balance:
            balance: pd.DataFrame = self.calculateBalance(verbose=False)
        else:
            balance: pd.DataFrame = self.trades.copy()

        if 'DateTime' not in balance and 'ExitTime' in balance:
            balance['DateTime'] = balance['ExitTime'].copy()

        self.balance = balance.copy()
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
                    print(g[1])
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
            
        # fig.add_trace(go.Histogram(x=trades['%ret'][trades['%ret'] > 0], name='Wins', 
        #                           marker_color='green'), row=3, col=1)
        # fig.add_trace(go.Histogram(x=trades['%ret'][trades['%ret'] <= 0], name='Losses', 
        #                           marker_color='red'), row=3, col=1)

        # if log:
        #     fig.update_yaxes(type="log", row=3, col=1)

        # fig.update_yaxes(title_text='Qty.', row=3, col=1)
        # fig.update_xaxes(title_text='Return (%)', row=3, col=1)

        fig.update_xaxes(title_text='Date', row=2, col=1)
        fig.update_layout(title=f"Account balance {self.config.capital + self.trades[[c for c in self.trades.columns if 'Result' in c][0]].sum()*100//1/100}$", 
                          autosize=False, width=1000, height=700)

        fig.show()
    
    def stats(self, column:str='Ticker', plot:bool=False, 
                    print_stats:bool=False) -> pd.DataFrame:

        self.stats_dict: dict = {}
        pairs: list = []
        trades: pd.DataFrame = copy.deepcopy(self.trades)
        if len(trades) <= 0:
            print('There are no trades')
            return pd.DataFrame()
        
        for g in trades.groupby(column):

            temp: pd.DataFrame = g[1].copy()
            temp = self.tradesDF(trades=temp['Trades'].tolist())

            self.stats_dict[g[0]] = self.btKPI(df=temp, print_stats=print_stats)
            
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






if __name__ == '__main__':

    import yfinance as yf

    from randomWalk import GeometricBrownianMotionAssetSimulator as GBMS
    gbms: GBMS = GBMS(start_date=None, end_date=None, periods=60*24*365*10,
                output_dir='random_data', symbol_length=4, init_price=10.0,
                mu=0.1, sigma=0.3, pareto_shape=1.5, freq='B',
                remove_files=True )

    config: BtConfig = BtConfig(init_date='2010-01-01', final_date=dt.date.today().strftime('%Y-%m-%d'), 
                      capital=5000.0, monthly_add=0, allocate=False,  # (dt.date.today() - dt.timedelta(days=250)).strftime('%Y-%m-%d')
                      min_size=1000, max_size=10000000, commission=Commissions(), 
                      use_sl=False, use_tp=False, time_limit=0, side=SignalsSide.LONG,
                      max_trades=100000, offset_aware=False)

    etf_com = [Commissions(ctype=Commissions.Type.FIXED, commission=1, cmin=1), 
               Commissions(ctype=Commissions.Type.PERCENTAGE, commission=0.25, cmin=0)]
    
    assets: dict = {
        'SPY':AssetConfig(name='SPY', sl=4.0, tp=8.0, order=OrderType.STOP, 
                        leverage=Leverage(Leverage.Type.SIZE, 1),
                        min_size=1, max_size=5000, risk=None, allocation=0.5,
                        account_currency='EUR', asset_currency='USD',
                        commissions=etf_com)
    }

    # bbRsiStrat, stochDip
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
    }
    
    # Prepare data needed for backtest
    signals: ContinuousSignals = ContinuousSignals(backtest=True, side=ContinuousSignals.Side.LONG, errors=False)
    indicators: Indicators = Indicators(errors=False)
    total_data: list = []
    data: dict = {}
    if len(data) <= 0:
        for strat in strategies:

            if strat not in dir(signals):
                print(f'{strat} not between the defined signals.')
                continue
            signal = getattr(signals, strat)

            for t,c in strategies[strat].assets.items():

                if t not in data:
                    temp: pd.DataFrame = yf.Ticker(t).history(period='max',interval='1d') # gbms.generateGBM(symbol=t, save=False) # 
                    temp.columns = [c.capitalize() for c in temp.columns]
                    temp.rename(columns={'Date':'DateTime'}, inplace=True)
                else:
                    temp = data[t].copy()

                temp.loc[:,'distATR'] = indicators.atr(n=20, method='s', dataname='ATR', new_df=temp)['ATR']
                temp.loc[:,'SLdist'] = temp['distATR'] * c.sl
                temp.loc[:,'Ticker'] = t
                temp.loc[:,'Spread'] = 0
                temp.loc[:,'CurrencyMult'] = 1
                temp.loc[:,'Date'] = pd.to_datetime(temp.index)
                if 'DateTime' not in temp.columns and 'Date' in temp.columns:
                    temp.rename(columns={'Date':'DateTime'}, inplace=True)
                
                if 'Volume' not in temp.columns:
                    temp['Volume'] = [0]*len(temp)

                temp = signal(df=temp, strat_name=strat)
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
        df.loc[:,'DateTime'] = pd.to_datetime(df['DateTime'])
    if df['DateTime'].iloc[0].tzinfo != None:
        df['DateTime'] = df['DateTime'].dt.tz_convert(None)
    df['Close'] = df['Close'].ffill()
    df['Spread'] = df['Spread'].ffill()
    df['Open'] = np.where(df['Open'] != df['Open'], df['Close'], df['Open'])
    df['High'] = np.where(df['High'] != df['High'], df['Close'], df['High'])
    df['Low'] = np.where(df['Low'] != df['Low'], df['Close'], df['Low'])

    total_data.append(df)

    # Backtest
    bt: ContinuousBackTest = ContinuousBackTest(strategies=strategies, config=config)
    
    total_data: pd.DataFrame = pd.concat(total_data)
    trades: pd.DataFrame = bt.backtest(df=total_data)

    # bt.btPlot(balance=True, buy_hold=True, log=False)
    stats: pd.DataFrame = bt.stats(column='StratName')
    print(stats)

    bt.trades.to_excel('cont_trades.xlsx')