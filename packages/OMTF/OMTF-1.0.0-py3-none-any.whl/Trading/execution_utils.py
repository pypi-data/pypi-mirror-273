
import os
import copy
import math
import datetime as dt
import pytz
import enum
import numpy as np
import pandas as pd

#from google_sheets.google_sheets import GoogleSheets

import json

class JSON:
    
    def write(self, filename:str, data) -> None:

        filename = filename if '.json' in filename else f'{filename}.json'
        with open(filename, "w") as file:
            json.dump(data, file)

    def read(self, filename:str) -> (list | dict):
        
        filename = filename if '.json' in filename else f'{filename}.json'
        with open(filename, 'r') as file:
            data = json.load(file)

        return data

class TypeOperative(enum.Enum):
    DISCRETE: str = 'discrete'
    CONTINUOUS: str = 'continuous'

def typeToDict(el, class_types:list=[], enum_types:list=[]) -> dict:
        
    # to_dict = lambda e: copy.deepcopy(e.to_dict()) if any([isinstance(e, t) for t in types]) else e
    if isinstance(el, list):
        return [typeToDict(e, class_types, enum_types) for e in el]
    elif isinstance(el, dict):
        return {k: typeToDict(v, class_types, enum_types) for k, v in el.items()}
    elif any([isinstance(el, t) for t in class_types]):
        return copy.deepcopy(el).to_dict()
    elif any([isinstance(el, t) for t in enum_types]):
        return copy.deepcopy(el).value
    elif isinstance(el, dt.datetime) or isinstance(el, pd.Timestamp):
        return copy.deepcopy(el).strftime('%Y-%m-%d %H:%M:%S')
    elif type(el).__module__ == np.__name__:
        return copy.deepcopy(el).item()
    elif isinstance(el, pd.DataFrame):
        return copy.deepcopy(el).to_dict('records')
    elif isinstance(el, pd.Series):
        return copy.deepcopy(el).to_list()
    else:
        return copy.deepcopy(el)

class Frequency(enum.Enum):

    NATURAL: str = 'NATURAL'
    BUSINESSDAY: str = 'BUSINESSDAY'
    DAY: str = 'DAY'
    WEEK: str = 'WEEK'
    MONTH: str = 'MONTH'
    YEAR: str = 'YEAR'

class Transitions:

    BUSINESS_DAYS_IN_WEEK: int = 5
    BUSINESS_DAYS_IN_YEAR: int = 256
    DAYS_IN_WEEK: int = 7
    DAYS_IN_YEAR: float = 365.25
    WEEKS_IN_YEAR: float = 52.25
    MONTHS_IN_YEAR: int = 12
    HOURS_IN_YEAR: float = DAYS_IN_YEAR*24
    MINUTES_IN_YEAR: float = HOURS_IN_YEAR*60
    SECONDS_IN_YEAR: float = MINUTES_IN_YEAR*60

    def businessDaysToYear(self, days:float) -> float: return days/self.BUSINESS_DAYS_IN_YEAR
    def businessDaysToMonth(self, days:float) -> float: 
        return days/self.BUSINESS_DAYS_IN_YEAR*self.MONTHS_IN_YEAR
    def businessDaysToWeek(self, days:float) -> float: return days/self.BUSINESS_DAYS_IN_WEEK
    def daysToYear(self, days:float) -> float: return days/self.DAYS_IN_YEAR
    def daysToMonth(self, days:float) -> float: return days/self.DAYS_IN_YEAR*self.MONTHS_IN_YEAR
    def daysToWeek(self, days:float) -> float: return days/self.DAYS_IN_WEEK
    def weekToMonth(self, weeks:float) -> float: return weeks/self.WEEKS_IN_YEAR*self.MONTHS_IN_YEAR
    def weekToYear(self, weeks:float) -> float: return weeks/self.WEEKS_IN_YEAR
    def monthToYear(self, months:float) -> float: return months/self.MONTHS_IN_YEAR

    def getChange(self, first_frequency:Frequency, second_frequency:Frequency
               ) -> float:
        
        '''
        Obtain ratio to multiply.
        '''
        
        if first_frequency == Frequency.NATURAL:
            raise ValueError('The original Frequency can not be NATURAL. It must be explicit.')
        elif second_frequency == Frequency.NATURAL:
            return 1
        
        if first_frequency == Frequency.DAY:
            if second_frequency == Frequency.DAY:
                return 1
            elif second_frequency == Frequency.BUSINESSDAY:
                return self.BUSINESS_DAYS_IN_WEEK / self.DAYS_IN_WEEK
            elif second_frequency == Frequency.WEEK:
                return 1 / self.DAYS_IN_WEEK
            elif second_frequency == Frequency.MONTH:
                return self.MONTHS_IN_YEAR / self.DAYS_IN_YEAR
            elif second_frequency == Frequency.YEAR:
                return 1 / self.DAYS_IN_YEAR
            
        elif first_frequency == Frequency.BUSINESSDAY:
            if second_frequency == Frequency.DAY:
                return self.DAYS_IN_WEEK / self.BUSINESS_DAYS_IN_WEEK
            elif second_frequency == Frequency.BUSINESSDAY:
                return 1
            elif second_frequency == Frequency.WEEK:
                return 1 / self.BUSINESS_DAYS_IN_WEEK
            elif second_frequency == Frequency.MONTH:
                return self.MONTHS_IN_YEAR / self.BUSINESS_DAYS_IN_YEAR
            elif second_frequency == Frequency.YEAR:
                return 1 / self.BUSINESS_DAYS_IN_YEAR
            
        elif first_frequency == Frequency.WEEK:
            if second_frequency == Frequency.DAY:
                return self.DAYS_IN_WEEK 
            elif second_frequency == Frequency.BUSINESSDAY:
                return self.BUSINESS_DAYS_IN_WEEK
            elif second_frequency == Frequency.WEEK:
                return 1
            elif second_frequency == Frequency.MONTH:
                return self.MONTHS_IN_YEAR / self.WEEKS_IN_YEAR
            elif second_frequency == Frequency.YEAR:
                return 1 / self.WEEKS_IN_YEAR
            
        elif first_frequency == Frequency.MONTH:
            if second_frequency == Frequency.DAY:
                return self.DAYS_IN_YEAR / self.MONTHS_IN_YEAR 
            elif second_frequency == Frequency.BUSINESSDAY:
                return self.BUSINESS_DAYS_IN_YEAR / self.MONTHS_IN_YEAR 
            elif second_frequency == Frequency.WEEK:
                return self.WEEKS_IN_YEAR / self.MONTHS_IN_YEAR 
            elif second_frequency == Frequency.MONTH:
                return 1
            elif second_frequency == Frequency.YEAR:
                return 1 / self.MONTHS_IN_YEAR
            
        elif first_frequency == Frequency.YEAR:
            if second_frequency == Frequency.DAY:
                return self.DAYS_IN_YEAR
            elif second_frequency == Frequency.BUSINESSDAY:
                return self.BUSINESS_DAYS_IN_YEAR
            elif second_frequency == Frequency.WEEK:
                return self.WEEKS_IN_YEAR
            elif second_frequency == Frequency.MONTH:
                return self.MONTHS_IN_YEAR
            elif second_frequency == Frequency.YEAR:
                return 1
            
        raise ValueError(f'Something went wrong with original frequency '+
                         f'beeing {first_frequency} and final frequency {second_frequency}')

class TradeSide(enum.Enum): # Deberia ser igual a Signals.Side
    LONG: str = 'LONG'
    SHORT: str = 'SHORT'

class SignalsSide(enum.Enum):
    ALL: float = 'ALL'
    LONG: float = 'LONG'
    SHORT: float = 'SHORT'

class OrderType(enum.Enum):
    MARKET: str = 'MARKET'
    LIMIT: str = 'LIMIT'
    STOP: str = 'STOP'

class CloseMethod(enum.Enum):
    TIME: str = 'TimeLimit'
    SL: str = 'SL'
    TP: str = 'TP'
    EXIT: str = 'Exit'
    CANCEL: str = 'Cancel'

class DrawDownMitigation:

    class Methods(enum.Enum):
        LINEAR: str = 'LINEAR'
        PARABOLIC: str = 'PARABOLIC'

    def __init__(self, increase_rate:float=2, 
                 decrease_rate:float=2, method:Methods=Methods.PARABOLIC, 
                 ma_period:int=0) -> None:

        '''
        Generates the DrawDown mitigation object for the backtest.

        Parameters
        ----------
        max_risk: float
            Maximum risk available. Must be in per unit.
        min_risk: float
            Minimum risk available. Must be in per unit.
        increase_rate: float
            Rate at which increase the risk.
        decrease_rate: float
            Rate at which decrease the risk.
        method: Methods
            Rate application method. It can be LINEAR or PARABOLIC.
        ma_period: int
            Period of the MA to define if increase or decrease. When 0 the difference 
            between previous drawdown and current one will be used.
        '''

        self.increase_rate: float = increase_rate
        self.decrease_rate: float = decrease_rate
        self.method: self.Methods = method
        self.ma_period: int = ma_period

    def calculateRisk(self, returns:pd.Series, risk:float) -> float:

        temp: pd.DataFrame = pd.DataFrame(returns.copy(), columns=['return'])
        temp['cumret'] = (1 + temp['return']).cumprod(axis=0)
        temp['drawdown'] = temp['cumret'] / temp['cumret'].cummax() - 1
        
        if self.ma_period > 0:
            temp['filter'] = temp['drawdown'] - temp['drawdown'].rolling(self.ma_period).mean()
        else:
            temp['filter'] = temp['drawdown'] - temp['drawdown'].shift(1)

        if self.method.value == self.Methods.LINEAR.value:
            if temp.iloc[-1]['filter'] > 0:
                risk = risk * (1 - temp.iloc[-1]['drawdown'] / self.increase_rate)
            elif temp.iloc[-1]['filter'] < 0:
                risk = risk * (1 - temp.iloc[-1]['drawdown'] * self.decrease_rate)
        elif self.method.value == self.Methods.PARABOLIC.value:
            if temp.iloc[-1]['filter'] > 0:
                risk = risk * (1 - temp.iloc[-1]['drawdown'] ** self.increase_rate)
            elif temp.iloc[-1]['filter'] < 0:
                risk = risk * (1 - temp.iloc[-1]['drawdown'] ** (1/self.decrease_rate))

        return risk
    
    def to_dict(self) -> dict:
        return {k: typeToDict(v, enum_types=[self.Methods]) for k, v in self.__dict__.items()}

class Currency:

    def __init__(self, rate:float, currency:str) -> None:

        '''
        Currency rate to use for changing currencies.

        Parameters
        ----------
        rate: float
            Numeric value of the currency rate.
        currency: str
            Currency 
        '''

        self.rate: float = rate
        self.currency: str = currency

    def to_dict(self) -> dict:
        return {k: typeToDict(v) for k, v in self.__dict__.items()}

class CurrencyChange:
    
    def __init__(self, currency_from:str, currency_to:str, rate:float) -> None:

        '''
        currency_from: float
            Currency of the account.
        currency_to: float
            Currency of the asset.
        '''
        
        self.currency_from: str = currency_from
        self.currency_to: str = currency_to
        self.rate: float = rate

    def changeRate(self, rate:float, currency_from:str=None, currency_to:str=None) -> None:

        self.rate: float = rate
        self.currency_from: str = currency_from if currency_from != None else self.currency_from
        self.currency_to: str = currency_to if currency_to != None else self.currency_to
        
    def change(self, qty:float, currency_from:str=None, currency_to:str=None) -> float:

        rate: float = self.rate
        
        if currency_from != None:
            rate: float = rate if currency_from == self.currency_from else 1/rate
        elif currency_to != None:
            rate: float = rate if currency_to == self.currency_to else 1/rate
        elif currency_from == None and currency_to == None:
            raise ValueError('The original currency or the final currency must be specified')

        return qty * rate
    
    def to_dict(self) -> dict:
        return {k: typeToDict(v) for k, v in self.__dict__.items()}

class Commissions:

    class Type(enum.Enum):
        PERUNIT = 'PERUNIT'
        PERCENTAGE = 'PERCENTAGE'
        PERCONTRACT = 'PERCONTRACT'
        FIXED = 'FIXED'

    def __init__(self, ctype:Type=Type.PERCENTAGE, commission:float=5.0, 
                 cmin:float=1, cmax:float=None, currency:str='EUR') -> None:

        '''
        Generate commissions configuration.

        Parameters
        ----------
        ctype: str
            Type of commissions input. It can be: 'percentage', 'perunit' or 'pershare'.
        commission: float
            Value of the commission. If the type is percentage it will be divided by 100.
        cmin: float
            Minimum value of the commission. Some brokers use minimum a dollar, here 
            it is represented.
        cmax: float
            Maximum value of the commission.
        '''

        self.type: self.Type = self.Type.PERUNIT if ctype.value == self.Type.PERCENTAGE.value else ctype
        self.value: float = commission/100 if ctype.value == self.Type.PERCENTAGE.value else commission
        self.min: float = cmin
        self.max: float = cmax
        self.currency: str = currency
    
    def to_dict(self) -> dict:
        return {k: typeToDict(v, enum_types=[self.Type]) for k, v in self.__dict__.items()}

class Leverage:
     
    class Type(enum.Enum):
        SIZE = 'SIZE'
        PRICE = 'PRICE'

    def __init__(self, type:Type, value:float=1.0) -> None:

        self.type: self.Type = type
        self.value: float = value

    def to_dict(self) -> dict:
        return {k: typeToDict(v, enum_types=[self.Type]) for k, v in self.__dict__.items()}

class RiskCalculation:

    class Type(enum.Enum):
        EQUAL: str = 'EQUAL'
        KELLY: str = 'KELLY'
        OPTIMALF: str = 'OPTIMALF'
        VOLATILITY: str = 'VOLATILITY'

    def __init__(self, returns:pd.Series=pd.Series(dtype='float64'), risk_type:Type=Type.EQUAL, 
                 default_risk:float=0.01, min_risk:float=0.005, max_risk:float=0.1,
                 risk_mult:float=1.0, bounded:bool=False, scale:bool=True,
                 mitigation:list=[], verbose:bool=False) -> None:

        '''
        Generate risk configuration.

        Parameters
        ----------
        risk_type: RiskType
            Type of calculation to use. It can be:
            - equal: to use the same for every trade, the default will be used
            - kelly: to calculate using the kelly criterion
            - optimalf: to calculate using the optimal f iterative method
        default_risk: float
            Risk in per unit to use by default.
        risk_mult: float
            Multiplier for the risk.
        min_risk: float
            Minimum risk to use.
        max_risk: float
            Maximum risk to use.
        bounded: bool
            True to bound returns to the max loss.
        scale: bool
            True to bound risk to the max loss.
        verbose: bool
            True to print errors.
        '''

        self.returns: pd.Series = returns
        self.risk_type: self.Type = risk_type
        self.default_risk: float = default_risk
        self.risk_mult: float = risk_mult
        self.min_risk: float = min_risk
        self.max_risk: float = max_risk
        self.bounded: bool = bounded
        self.scale: bool = scale
        self.mitigation: list = mitigation
        self.verbose: bool = verbose
    
    def _wagerScale(self, risk:float, max_loss:float) -> float:
        return risk if max_loss == 0 else risk/max_loss
    
    def _boundReturns(self, returns:(np.ndarray | pd.Series)) -> (np.ndarray | pd.Series):

        '''
        returns: np.ndarray or pd.Series
            Series with per unit return for the trades to bound.
        '''
        
        return returns / 1e-9 if np.abs(np.min(returns)) == 0 else returns / np.abs(np.min(returns))

    def _kellyRisk(self, returns:pd.Series) -> float:

        if len(returns) == 0 and self.verbose:
            print('There are no returns available for the risk calculation')
            return self.default_risk
        
        wins: pd.Series = returns[returns > 0]
        losses: pd.Series = returns[returns <= 0]
        W: float = len(wins) / len(returns)
        avg_loss: float = np.abs(np.mean(losses))
        if avg_loss == 0:
            if self.verbose:
                print('There average loss in the risk calculation is 0')
            R: float = np.mean(wins)
        else:
            R: float = np.mean(wins) / avg_loss

        if R == 0:
            if self.verbose:
                print('The risk/reward ratio in the risk calculation is 0')
            return self.default_riskm
        risk: float = (W - ( (1 - W) / R )) * self.risk_mult

        return risk

    def _optimalFRisk(self, returns:pd.Series=None, n_curves:int=50, 
                      drawdown_limit:float=20.0, certainty_level:float=10.0
                      ) -> float:

        """
        Calculates ideal fraction to stake on an investment with given return distribution

        Args:
        returns: (array-like) distribution that's representative of future returns
        time_horizon: (integer) the number of returns to sample for each curve
        n_curves: (integer) the number of equity curves to generate on each iteration of f
        drawdown_limit: (real) user-specified value for drawdown which must not be exceeded
        certainty_level: (real) the level of confidence that drawdownlimit will not be exceeded

        Returns:
        'f_curve': calculated drawdown and ghpr value at each value of f
        'optimal_f': the ideal fraction of one's account to stake on an investment
        'max_loss': the maximum loss sustained in the provided returns distribution
        """

        bounded_f: pd.Series = np.cumsum(np.array([0.5]*200))
        f_curve: pd.DataFrame = pd.DataFrame(columns=['ghpr', 'drawdown'])
        for f in bounded_f:

            # Generate n_curves number of random equity curves
            reordered_returns = np.random.choice(f * returns, size= 
                (len(returns), n_curves))
            curves = (1 + reordered_returns).cumprod(axis=0)
            curves_df: pd.DataFrame = pd.DataFrame(curves)

            # Calculate Maximum Drawdown for each equity curve
            drawdown = curves_df / curves_df.cummax() - 1
            abs_drawdown = np.abs(drawdown)
            curves_drawdown = np.max(abs_drawdown) * 100
            
            # Calculate GHPR for each equity curve
            eq_arr: np.ndarray = np.array(curves_df)
            curves_ghpr = eq_arr[-1] / eq_arr[0] ** (1 / len(curves_df)) - 1

            # Calculate drawdown at our certainty level
            drawdown_percentile = np.percentile(curves_drawdown, 
                                                certainty_level)

            # Calculate median ghpr value
            curves_ghpr = np.nan_to_num(curves_ghpr)
            ghpr_median: float = np.median(curves_ghpr)
            f: float = round(f, 1)
            if drawdown_percentile <= drawdown_limit:
                _ghpr: float = ghpr_median
            else:
                _ghpr: float = 0
            f_curve.loc[f, 'ghpr'] = _ghpr
            f_curve.loc[f, 'drawdown'] = drawdown_percentile

        f_curve: pd.DataFrame = f_curve.fillna(0)
        risk: float = f_curve['ghpr'].idxmax() * self.risk_mult

        return risk
    
    def _volatilityTargetRisk(self, returns:pd.Series=pd.Series(dtype='float64'), 
                              n:int=5, m:int=10, annualized:bool=False) -> pd.Series:

        if returns.empty:
            returns = self.returns
        
        std: pd.Series = returns.ewm(span=n).std()
        if annualized:
            std = std * (Transitions().getChange(Frequency.BUSINESSDAY, Frequency.YEAR) ** 0.5)
        volatility = 0.7*std + 0.3*std.rolling(m, min_periods=1).mean()

        return self.default_risk / volatility.iloc[-1] if volatility.iloc[-1] > 0 else self.default_risk
    
    def addMitigation(self, mitigation:DrawDownMitigation) -> None:

        self.mitigation.append(copy.deepcopy(mitigation))

    def calculateRisk(self, returns:pd.Series=None, n:int=20, n_curves:int=50, 
                      drawdown_limit:float=20.0, certainty_level:float=10.0) -> float:

        if returns == None:
            returns = self.returns

        returns = returns.fillna(0)

        self.risk = self.default_risk
        max_loss: float = returns.abs().max()

        if self.risk_type.value != self.Type.EQUAL.value and len(returns) >= n:
            n_returns: pd.Series = returns.tail(n)
            if self.bounded:
                n_returns: pd.Series = self._boundReturns(returns=n_returns)

            if self.risk_type.value == self.Type.KELLY.value:
                self.risk = self._kellyRisk(returns=n_returns)
            elif self.risk_type.value == self.Type.OPTIMALF.value:
                self.risk = self._optimalFRisk(returns=n_returns, n_curves=n_curves, drawdown_limit=drawdown_limit, 
                                               certainty_level=certainty_level)
            elif self.risk_type.value == self.Type.VOLATILITY.value:
                self.risk = self._volatilityTargetRisk()
            max_loss: float = n_returns.abs().max()
            
            
            
        # print(self.risk, max_loss)
        if self.risk != self.risk:
            self.risk = self.min_risk
            
        if self.scale and max_loss == max_loss:
            self.risk = self._wagerScale(risk=self.risk, max_loss=max_loss)
            
        if len(self.mitigation) > 0:
            self.risk = min([mit.calculateRisk(returns, self.risk) for mit in self.mitigation])

        if self.risk > self.max_risk:
            self.risk = self.max_risk
        elif self.risk < self.min_risk:
            self.risk = self.min_risk

        return self.risk
    
    def to_dict(self) -> dict:
        return {k: typeToDict(v, class_types=[DrawDownMitigation], 
                              enum_types=[self.Type]) for k, v in self.__dict__.items() \
                    if k not in ['risk']}

class Execution:
    
    class Type(enum.Enum):
        ENTRY = 'ENTRY'
        EXIT = 'EXIT'

    class Method(enum.Enum):
        MANUAL: str = 'MANUAL'
        LIMIT: str = 'LIMIT'
        STOP: str = 'STOP'
        SL: str = 'SL'
        TP: str = 'TP'
    
    def __init__(self, datetime, price:float, execution_type:Type, size:float, 
                 currency:Currency, balance:float, risk_capital:float, sldist:float=None, 
                 leverage:Leverage=Leverage(type=Leverage.Type.SIZE, value=1),
                 spread:float=0.0, commissions:Commissions=Commissions(),
                 currency_change:CurrencyChange=None, asset_currency:bool=False) -> None:
        
        self.datetime = datetime
        self.price: float = price    
        self.execution_type: self.Type = execution_type
        self.size: float = size
        self.currency: Currency = currency
        self.balance: float = balance
        self.risk_capital: float = risk_capital
        self.sldist: float = sldist
        self.spread: float = spread
        self.leverage: Leverage = copy.deepcopy(leverage)
        self._currency_change: CurrencyChange = currency_change
        if currency_change != None:
            self._currency_change.changeRate(rate=currency.rate, currency_to=currency.currency)
        self.commissions: Commissions = commissions
        self.onecandle: bool = False
        self.asset_currency: bool = asset_currency
    
    @property
    def commission_value(self) -> float:

        currency_from: str = self._currency_change.currency_from
        currency_to: str = self._currency_change.currency_to
        commission: Commissions
        com: float = 0
        for commission in self.commissions:

            value = commission.value
            max_val = commission.max if commission.max != None else None
            min_val = commission.min if commission.min != None else None
            if commission.currency != currency_from and commission.currency != currency_to:
                raise ValueError(f'Commissions currency is {commission.currency} while the rate is from {currency_from} to {currency_to}')
            elif commission.currency != currency_from:
                value = self._currency_change.change(qty=commission.value, currency_to=currency_from)
                max_val = self._currency_change.change(qty=commission.max, currency_to=currency_from) \
                            if commission.max != None else None
                min_val = self._currency_change.change(qty=commission.min, currency_to=currency_from) \
                            if commission.min != None else None

            if commission.type.value == Commissions.Type.PERCONTRACT.value:
                temp: float = self.size * value
            elif commission.type.value == Commissions.Type.FIXED.value:
                temp: float = value
            else:
                temp: float = self.size * value * \
                            self._currency_change.change(qty=self.price, currency_to=currency_from)

            if max_val != None and temp > max_val:
                temp: float = max_val
            elif min_val != None and temp < min_val:
                temp: float = min_val
                
            com += temp

        if self.asset_currency:
            temp: float =  self._currency_change.change(qty=com, 
                                currency_to=currency_to)
            
        return com
    
    def to_dict(self) -> dict:
        
        return {k: typeToDict(v, class_types=[Currency, Commissions, Leverage, CurrencyChange], 
                              enum_types=[Execution.Type, Execution.Method]) \
                for k, v in self.__dict__.items()}

class Order:
        
    class Status(enum.Enum):
        REQUEST = 'REQUEST'
        EXECUTED = 'EXECUTED'
        CANCELED = 'CANCELED'
        
    def __init__(self, datetime, price:float, order_type:OrderType, 
                 execution:Execution=None, status:Status=Status.REQUEST) -> None:
        self.datetime = datetime
        self.price: float = price    
        self.order_type: OrderType = order_type
        self.execution: Execution = execution
        self.status: self.Status = status
        
    def cancel(self) -> None:
        self.status = self.Status.CANCELED
        
    def execute(self) -> None:
        self.status = self.Status.EXECUTED
        
    def to_dict(self) -> dict:
        return {k: typeToDict(v, class_types=[Execution], enum_types=[OrderType, self.Status]) \
            for k, v in self.__dict__.items()}
        
class AssetConfig:

    def __init__(self, id:str=None, name:str=None, account_currency:str='EUR', asset_currency:str='USD',
                 risk:RiskCalculation=RiskCalculation(risk_type='equal', default_risk=0.01),
                 leverage:Leverage=Leverage(Leverage.Type.SIZE, 1.0), fractional_size:bool=False,
                 sl:float=None, tp:float=None, order:OrderType=OrderType.STOP, min_size:float=1.0, 
                 max_size:float=10000.0, commissions:(list | Commissions)=[], allocation:float=1.0,
                 drawdown:DrawDownMitigation=None) -> None:

        '''
        Generate commissions configuration.

        Parameters
        ----------
        name: str
            Name of the asset.
        leverage: Leverage
            Leverage type applied for the asset.
        currency: str
            String containing the currency code for the asset. Default is USD.
        risk: RiskCalculation
            Risk in per unit for the asset.
        sl: float
            ATR multiplier for the SL. If it's None then SL will be placed at 0 
            but shorts won't be available.
        tp: float
            ATR multiplier for the TP. If it's None then the trade will be 
            closed when a new entry is signaled.
        order: OrderType
            Order type. It can be 'market', 'limit' or 'stop'.
        min_size: float
            Minimum size to trade the asset.
        max_size: float
            Maximum size available to trade the asset.
        commission: list
            List with Commissions objects associated to the asset, it depends on the asset.
        allocation: float
            Fraction of the account to allocate to this asset.
        drawdown: DrawDownMitigation
            DrawDownMitigation object associated to the asset to modify the risk used.
        '''

        self.id: str = id
        self.name: str = name
        self.risk: RiskCalculation = copy.deepcopy(risk)
        self.sl: float = sl
        self.tp: float = tp
        self.order_type: OrderType = order
        self.min_size: float = min_size
        self.max_size: float = max_size
        self.commissions: list = copy.deepcopy(commissions if isinstance(commissions, list) \
                                               else [commissions])
        self.drawdown: DrawDownMitigation = drawdown
        self.leverage: Leverage = copy.deepcopy(leverage)
        self.fractional_size: bool = fractional_size
        self.allocation: float = allocation
        self.currency: str = asset_currency
        self._currency_change: CurrencyChange = CurrencyChange(currency_from=account_currency, 
                                                   currency_to=asset_currency, rate=1.0)
    
    def to_dict(self) -> dict:

        '''
        Generates a dictionary with the config for the asset.

        Returns
        -------
        object: dict
            Contains the config for the asset.
        '''
        
        return {k: typeToDict(v, class_types=[Commissions, RiskCalculation, Leverage, Currency, CurrencyChange],
                              enum_types=[OrderType]) \
                for k, v in self.__dict__.items()}

class StrategyConfig:

    class Type(enum.Enum):
        DISCRETE: str = 'DISCRETE'
        CONTINUOUS: str = 'CONTINUOUS'

    def __init__(self, name:str, assets:dict={}, use_sl:bool=True, use_tp:bool=True, 
                 time_limit:int=50, timeframe:str='H1', filter:str=None, allocation:float=1.0,
                 risk:RiskCalculation=RiskCalculation(risk_type='equal', default_risk=0.01),
                 drawdown:DrawDownMitigation=None, strat_type:Type=Type.DISCRETE) -> None:

        '''
        Generate commissions configuration.

        Parameters
        ----------
        name: str
            Name of the strategy.
        assets: dict[AssetConfig]
            Dictionary with the assets tradeable by the strategy.
        use_sl: float
            True to use SL as exit method. If the asset config has None as SL multiplier 
            attribute the strategy will only be able to long.
        use_tp: float
            True to use TP as exit method.
        time_limit: int
            Number of candles to wait for the trade to exit, after which the trade 
            will be manually closed.
        timeframe: float
            Minimum size to trade the strategy.
        filter: str
            String containing the filter code.
        allocation: float
            Fraction of the account to allocate to this strategy.
        risk: RiskCalculation
            Risk configuration.
        drawdown: DrawDownMitigation
            DrawDownMitigation object associated to the strategy to modify the risk used.
        '''

        self.name: str = name
        self.assets: dict = {}
        for asset in copy.deepcopy(assets):
            assets[asset].allocation = assets[asset].allocation * allocation
            self.assets[asset] = copy.deepcopy(assets[asset])
        self.use_sl: bool = use_sl
        self.use_tp: bool = use_tp
        self.time_limit: int = time_limit
        self.timeframe: str = timeframe
        self.filter: str = filter
        self.risk: RiskCalculation = copy.deepcopy(risk)
        self.drawdown: DrawDownMitigation = drawdown
        self.allocation: float = allocation
        self.strat_type: self.Type = strat_type

    def addAsset(self, name:str, config:AssetConfig) -> None:

        '''
        Adds an asset to the dictionary of traded assets.
        '''

        config.allocation = config.allocation * self.allocation
        self.assets[name] = copy.deepcopy(config)
    
    def to_dict(self) -> dict:

        '''
        Generates a dictionary with the config for the strategy.

        Returns
        -------
        object: dict
            Contains the config for the strategy.
        '''
        
        return {k: typeToDict(v, class_types=[DrawDownMitigation, RiskCalculation, AssetConfig], 
                              enum_types=[self.Type]) for k, v in self.__dict__.items()}

class Trade:
        
    def __init__(self, candle:dict, signal:TradeSide, strategy:StrategyConfig,
                 entry:float, balance:float, risks:(float | list), 
                 allocate:bool=True, verbose:bool=False) -> None:

        '''
        Generates the trade object for the backtest.

        Parameters
        ----------
        candle: dict
            Dictionary with the current candle data.
        signal: TradeSignal
            Direction for the trade. It can be 'long' or 'short'.
        strategy: Signals.Side
            Name of the strategy used to enter the trade.
        entry: float
            Entry price.
        balance: float
            Balance when entering the trade.
        risks: float or dict
            Risk used in the trade.
        verbose: bool
            True to print errors.
        '''

        # comission = asset.commission.value * 100 if 'JPY' in candle['Ticker'] and \
        #             asset.commission.type == 'pershare' else asset.commission.value
        strategy: StrategyConfig = copy.deepcopy(strategy)
        asset: AssetConfig = copy.deepcopy(strategy.assets[candle['Ticker']])

        self.datetime = candle['DateTime']
        self.ticker: str = candle['Ticker']
        self.asset: AssetConfig = asset
        self.strategy: StrategyConfig = strategy
        self.order: OrderType = asset.order_type
        self.signal: TradeSide = signal
        self.balance: float = balance
        self.risk_capital: float = self.asset.allocation * balance if allocate else balance
        self.entry: float = entry
        sldist: float = self.asset.sl * candle['SLdist']
        tpdist: float = self.asset.tp * candle['SLdist']
        self.sldist: float = sldist
        self.sl: float = entry - sldist if signal.value == TradeSide.LONG.value else entry + sldist
        self.tp: float = entry + tpdist if signal.value == TradeSide.LONG.value else entry - tpdist
        self.returns: float = 0
        self.commissions: list = copy.deepcopy(asset.commissions)
        self.risks: list = copy.deepcopy(risks)
        self.risk: float = self.calculateRisk(risks=copy.deepcopy(risks))
        self.allocate: bool = allocate
        self.result: float = 0
        self.order_candles: list = []
        self.execution_candles: list = []
        self.onecandle: bool = False
        self.method: str = None # clossing method
        self.leverage: Leverage = copy.deepcopy(asset.leverage)
        self.closed: bool = False
        self.verbose: bool = verbose
        
        self.executions: list = []
        self.orders: list = [
            Order(
                datetime=candle['DateTime'],
                price=entry,
                order_type=asset.order_type,
                execution=None
            )
        ]
        
    @property
    def open_orders(self) -> list:
        return [o for o in self.orders if o.status.value == Order.Status.REQUEST.value]
        
    @property
    def entries(self) -> list:
        return [exe for exe in self.executions if exe.execution_type.value == Execution.Type.ENTRY.value]
    
    @property
    def exits(self) -> list:
        return [exe for exe in self.executions if exe.execution_type.value == Execution.Type.EXIT.value]
    
    @property
    def entries_size(self) -> float:
        return sum([exe.size for exe in self.entries])
    
    @property
    def exits_size(self) -> float:
        return sum([exe.size for exe in self.exits])
    
    @property
    def current_size(self) -> float:
        return (self.entries_size - self.exits_size) if len(self.executions) > 0 else 0

    @property
    def entry_price(self) -> float:
        if self.has_executions:
            if self.entries_size == 0:
                return None
            return sum([exe.size * exe.price for exe in self.entries]) / self.entries_size
        else:
            return None
    
    @property
    def exit_price(self) -> float:
        if self.has_executions:
            return sum([exe.size * exe.price for exe in self.exits]) / self.exits_size \
                if self.exits_size != 0 else self.execution_candles[-1]['Close']
        else:
            return None
    
    @property
    def current_sl(self) -> float:
        if self.has_executions:
            return (self.entry_price - self.entries[-1].sldist) if self.signal.value == TradeSide.LONG.value else \
                (self.entry_price + self.entries[-1].sldist)
        else:
            return self.sl
    
    @property
    def current_tp(self) -> float:
        if self.has_executions:
            return (self.entry_price + self.entries[-1].sldist) if self.signal.value == TradeSide.LONG.value else \
                (self.entry_price - self.entries[-1].sldist)
        else:
            return self.tp
    
    @property
    def spread(self) -> float:
        if self.has_executions:
            return sum([exe.size * exe.spread for exe in self.executions]) / \
                (self.entries_size + self.exits_size)
        elif self.has_orders and len(self.order_candles) > 0:
            return self.order_candles[-1]['Spread']
        else: 
            return None
    
    @property
    def currency(self) -> float:
        if self.has_executions:
            return sum([exe.currency.rate * exe.size for exe in self.executions]) / \
                (self.entries_size + self.exits_size)
        else:
            return self.order_candles[-1]['CurrencyMult'] if self.has_orders else None
        
    @property
    def commissions_value(self) -> float:

        '''
        Calculates the commission applied to the trade.

        Returns
        -------
        commission: float
            Commission currently charged for the trade.
        '''
        
        if self.has_executions:
            return sum([exe.commission_value for exe in self.executions]) \
                if len(self.executions) > 0 else 0
        else:
            return 0
    
    @property
    def position(self) -> float:
        if self.has_executions:
            return self.current_size * \
                self.asset._currency_change.change(qty=self.entry_price, currency_from=self.asset.currency)
        else:
            return 0
        
    @property
    def floating_result(self) -> float:
        if self.has_executions:
            temp: float = ((self.exit_price - self.entry_price) if self.signal.value == TradeSide.LONG.value \
                    else (self.entry_price - self.exit_price)) * self.current_size
            return self.asset._currency_change.change(qty=temp, currency_from=self.asset.currency)
        else:
            return 0
        
    @property
    def gross_result(self) -> float:
        if self.has_executions:
            temp: float = ((self.exit_price - self.entry_price) if self.signal.value == TradeSide.LONG.value \
                    else (self.entry_price - self.exit_price)) * (self.exits_size) 
            return self.asset._currency_change.change(qty=temp, currency_from=self.asset.currency)
        else:
            return 0
    
    @property
    def net_result(self) -> float:
        return self.gross_result - self.commissions_value
    
    @property
    def net_return(self) -> float:
        return self.net_result / self.balance
     
    @property
    def has_orders(self) -> bool:
        return len(self.orders) > 0
    
    @property
    def has_executions(self) -> bool:
        return len([e for e in self.executions if e.size != 0]) > 0

    def addCandle(self, candle: dict) -> None:

        new_candle: dict = {'DateTime':candle['DateTime'] ,'Open':candle['Open'], 
                        'High':candle['High'], 'Low':candle['Low'], 
                        'Close':candle['Close'], 'Volume': candle['Volume'],
                        'Spread':candle['Spread'], 'CurrencyMult':candle['CurrencyMult'],
                        f'{self.strategy.name}Entry': candle[f'{self.strategy.name}Entry']}
        if f'{self.strategy.name}Exit' in candle:
            new_candle[f'{self.strategy.name}Exit'] = candle[f'{self.strategy.name}Exit']
        if len(self.executions) > 0:
            self.execution_candles.append(new_candle)
        else:
            self.order_candles.append(new_candle)

    def calculateRisk(self, risks:(float | list)=None) -> float:

        '''
        Calculates the risk of the trade.

        Returns
        -------
        risk: float
            Risk of the trade.
        '''
        
        if risks == None:
            risks = copy.deepcopy(self.risks)
        self.risk = min([(risk if isinstance(risk, float) else risk.calculateRisk()) \
                         for risk in copy.deepcopy(risks) if risk == risk]) \
                    if isinstance(risks, list) else risks

        return self.risk

    def changeCurrency(self, qty:float, currency:Currency=None) -> float:

        currency_change: CurrencyChange = copy.deepcopy(self.asset._currency_change)
        if currency != None:
            currency_change.changeRate(rate=currency.rate, currency_to=currency.currency)
        return currency_change.change(qty, 
                    currency_to=currency_change.currency_to if currency == None \
                    else currency.currency)
        
    def calculateSize(self, price:float, balance:float=None, 
                      sldist:float=None, currency:Currency=None) -> float:

        ## CALCULATE SIZE DEPENDING ON CURRENT SIZE AND RISK FOR NEXT EXECUTIONS ------------------------------------

        '''
        Calculates the size of the trade.

        Returns
        -------
        size: float
            Size of the trade.
        '''

        if balance != None:
            self.risk_capital: float = self.asset.allocation * balance if self.allocate else balance
        self.risk_capital = self.changeCurrency(self.risk_capital, currency=currency)
        if sldist != None:
            self.sldist: float = sldist

        leverage: Leverage = self.asset.leverage
        
        # print(self.risk, self.risk_capital, self.sldist)
        size = self.risk * self.risk_capital / self.sldist if self.sldist != 0 else self.asset.max_size
        if leverage.type.value == Leverage.Type.SIZE.value:
            size = size * leverage.value
        elif leverage.type.value == Leverage.Type.PRICE.value:
            size = size / leverage.value
        else:
            raise ValueError('Not a valid Type of leverage')
        
        if size > self.asset.max_size:
            size = self.asset.max_size
        elif size < self.asset.min_size:
            size = self.asset.min_size

        if leverage.type.value == Leverage.Type.SIZE.value and size * price > self.risk_capital * leverage.value:
            size = self.risk_capital * leverage.value / price
        elif leverage.type.value == Leverage.Type.PRICE.value and size * price > self.risk_capital / leverage.value:
            size = self.risk_capital / (price * leverage.value)

        if self.risk_capital <= 0:
            size = 0.0

        if size != size:
            print('Size calculated for this execution is NaN')
            size = 0.0
            
        return size if self.asset.fractional_size else math.floor(size)
    
    def recalculateSL(self, balance:float, currency:Currency=None) -> None:

        if balance != None:
            self.risk_capital: float = self.asset.allocation * balance if self.allocate else balance
        self.risk_capital = self.changeCurrency(self.risk_capital, currency=currency)
        
        sldist: float = self.risk_capital * self.calculateRisk()/(self.current_size if self.current_size != 0 else 1)
        if self.signal.value == TradeSide.LONG.value:
            self.sl = self.entry_price - sldist
        elif self.signal.value == TradeSide.SHORT.value:
            self.sl = self.entry_price + sldist
        
        return sldist

    def addOrder(self, price:float, candle:dict, balance:float, order_type:OrderType, 
                 with_execution:bool=True, execution_type:Execution.Type=Execution.Type.ENTRY, 
                 size:float=None, status:Order.Status=Order.Status.REQUEST) -> None:
        
        if with_execution:
            if execution_type.value == Execution.Type.EXIT.value:
                size: float = self.current_size if size == None or size > self.current_size else size
                execution = Execution(
                    datetime=candle['DateTime'],
                    price=price,
                    execution_type=execution_type,
                    size=size,
                    currency=Currency(rate=candle['CurrencyMult'], currency=self.asset.currency),
                    balance=None,
                    risk_capital=None,
                    sldist=None,
                    spread=candle['Spread'],
                    commissions=copy.deepcopy(self.asset.commissions),
                    currency_change=self.asset._currency_change
                )
            else:
                sldist: float = self.asset.sl * candle['SLdist']
                currency: Currency = Currency(rate=candle['CurrencyMult'], currency=self.asset.currency)
                size: float = self.calculateSize(price=price, balance=balance, 
                                                sldist=sldist, currency=currency)
                execution = Execution(
                    datetime=candle['DateTime'],
                    price=price,
                    execution_type=execution_type,
                    size=size,
                    currency=currency,
                    balance=balance,
                    risk_capital=self.asset.allocation * balance if self.allocate else balance,
                    sldist=candle['SLdist'],
                    spread=candle['Spread'],
                    commissions=copy.deepcopy(self.asset.commissions),
                    currency_change=self.asset._currency_change
                )
        else:
            execution = None
        order = Order(datetime=candle['DateTime'], price=price, order_type=order_type, 
                      execution=execution, status=status)
        self.orders.append(order)
    
    def addExecution(self, price:float, candle:dict, signal:TradeSide, balance:float, 
                     execution:Execution=None) -> None:
        
        sldist: float = self.asset.sl * candle['SLdist']
        tpdist: float = self.asset.tp * candle['SLdist']
        if execution == None:
            execution = Execution(
                datetime=candle['DateTime'],
                price=price,
                execution_type=Execution.Type.ENTRY,
                size=0,
                currency=Currency(rate=candle['CurrencyMult'], currency=self.asset.currency),
                balance=balance,
                risk_capital=self.asset.allocation * balance if self.allocate else balance,
                sldist=candle['SLdist'],
                spread=candle['Spread'],
                commissions=copy.deepcopy(self.asset.commissions),
                currency_change=self.asset._currency_change
            )
        else:
            execution = copy.deepcopy(execution)
            execution.price = price
        if execution.execution_type.value != Execution.Type.EXIT.value:
            execution.size = self.calculateSize(price=price, balance=balance, 
                                                sldist=sldist, currency=execution.currency)
        self.executions.append(execution)
        if len(self.executions) > 1:
            sldist = self.recalculateSL(balance=balance)
        self.tp = price + tpdist if signal.value == TradeSide.LONG.value else price - tpdist
    
    def reduceExecution(self, size:float, price:float, candle:dict, method:CloseMethod=None) -> None:

        if size >= self.current_size:
            if size > self.current_size:
                if self.verbose:
                    print(f'Trying to close {size} contracts while having {self.current_size}')
                size = self.current_size
            if len(self.execution_candles) <= 1:
                self.onecandle = True
            self.method = CloseMethod.EXIT if method == None else method
            self.closed = True

        self.executions.append(
            Execution(
                datetime=candle['DateTime'],
                price=price,
                execution_type=Execution.Type.EXIT,
                size=size,
                currency=Currency(rate=candle['CurrencyMult'], currency=self.asset.currency),
                balance=None,
                risk_capital=None,
                sldist=None,
                spread=candle['Spread'],
                commissions=copy.deepcopy(self.asset.commissions),
                currency_change=self.asset._currency_change
            )
        )

        result = (price - self.entry_price if self.signal.value == TradeSide.LONG.value else self.entry_price - price) * size
        result = self.asset._currency_change.change(qty=result, currency_from=self.asset.currency)
        
        return result
              
    def closeTrade(self, candle:dict=None, price:float=None, method:CloseMethod=CloseMethod.CANCEL,
                   order_type:OrderType=OrderType.MARKET) -> None:
        
        if self.has_executions and self.current_size == 0:
            if self.verbose:
                print([copy.deepcopy(e).to_dict() for e in self.executions])
            if self.method.value in [CloseMethod.CANCEL.value, CloseMethod.EXIT.value, 
                                     CloseMethod.SL.value, CloseMethod.TP.value, 
                                     CloseMethod.TIME.value]:
                return None
            raise ValueError('Trying to close a trade that is already closed.')
        
        o: Order
        for o in self.open_orders:
            o.cancel()
        
        if self.has_executions:
            
            if isinstance(candle, type(None)):
                raise ValueError('You must pass the current candle as an argument')
            
            price: float = price if price != None else candle['Close']
            self.addOrder(price, candle, balance=None, 
                          order_type=order_type, with_execution=False,
                          execution_type=Execution.Type.EXIT,
                          status=Order.Status.EXECUTED)
            self.reduceExecution(self.current_size, price, candle, method=method)
            self.closed = True
        else:
            self.method = CloseMethod.CANCEL
            self.closed = True
    
    def executeOrder(self, candle:dict, balance:float) -> bool:
        
        order: Order
        price: float = 0
        for order in [o for o in self.orders if o.status.value == Order.Status.REQUEST.value]:
            
            execution: Execution = None
            if isinstance(order.execution, Execution):
                execution = copy.deepcopy(order.execution)

            if order.order_type.value == OrderType.STOP.value: # STOP orders
            
                if self.signal.value == TradeSide.LONG.value and self.entry <= candle['High'] + candle['Spread']:
                    price: float = order.price if candle['Open'] < order.price else candle['Open']

                if self.signal.value == TradeSide.SHORT.value and self.entry >= candle['Low']:
                    price: float = order.price
                        
            elif order.order_type.value == OrderType.LIMIT.value: # LIMIT orders

                if self.signal.value == TradeSide.LONG.value and self.entry > candle['Low'] + candle['Spread']:
                    price: float = order.price if candle['Open'] > order.price else candle['Open']

                if self.signal.value == TradeSide.SHORT.value and self.entry < candle['High']:
                    price: float = order.price if candle['Open'] < order.price else candle['Open']
            
            elif order.order_type.value == OrderType.MARKET.value:
                price: float = order.price
                
            if price != 0:
                self.addExecution(price, candle, self.signal, balance, execution=execution)
                order.execute()
                if self.current_size == 0:
                    self.closed = True
    
    def checkSL(self, candle:dict) -> bool:

        if not self.strategy.use_sl:
            return False

        price: float = 0
        
        if self.signal.value == TradeSide.SHORT.value and candle['High'] + candle['Spread'] >= self.current_sl: # High
            price: float = self.current_sl if candle['Open'] < self.current_sl else candle['Open']
            if len(self.execution_candles) <= 1 and candle['Low'] + candle['Spread'] <= self.current_tp and \
                candle['High'] + candle['Spread'] >= self.current_sl:
                self.onecandle = True

        if self.signal.value == TradeSide.LONG.value and candle['Low'] <= self.current_sl: # Low
            price: float = self.current_sl if candle['Open'] > self.current_sl else candle['Open']
            if len(self.execution_candles) <= 1 and candle['High'] >= self.current_tp and \
                candle['Low'] <= self.current_sl:
                self.onecandle = True

        if price != 0:
            self.closeTrade(candle=candle, price=price, method=CloseMethod.SL, 
                            order_type=OrderType.STOP)
            return True
                    
        return False
        
    def checkTP(self, candle:dict) -> bool:

        if not self.strategy.use_tp:
            return False

        price: float = 0
        
        if self.signal.value == TradeSide.SHORT.value and candle['Low'] + candle['Spread'] <= self.current_tp: # High
            price: float = self.current_tp if candle['Open'] > self.tp else candle['Open']
            if len(self.execution_candles) <= 1 and candle['Low'] + candle['Spread'] <= self.current_tp and \
                candle['High'] + candle['Spread'] >= self.current_sl:
                self.onecandle = True

        if self.signal.value == TradeSide.LONG.value and candle['High'] >= self.current_tp: # Low
            price: float = self.current_tp if candle['Open'] < self.current_tp else candle['Open']
            if len(self.execution_candles) <= 1 and candle['High'] >= self.current_tp and \
                candle['Low'] <= self.current_sl:
                self.onecandle = True

        if price != 0:
            self.closeTrade(candle=candle, price=price, method=CloseMethod.TP, 
                            order_type=OrderType.STOP)
            return True
                    
        return False
    
    def checkTimeLimit(self, candle:dict) -> bool:
        
        if self.strategy.time_limit > 0 and \
            len(self.execution_candles) >= self.strategy.time_limit:
            self.closeTrade(candle=candle, method=CloseMethod.TIME)
            return True
                    
        return False
        
    def to_dict(self):

        '''
        Generates a dictionary with the trade data.

        Returns
        -------
        object: dict
            Contains the data.
        '''

        signal: str = self.signal.name if isinstance(self.signal, TradeSide) else self.signal
        method: str = self.method.name if isinstance(self.method, CloseMethod) else self.method
        strategy: dict = self.strategy.to_dict() if isinstance(self.strategy, StrategyConfig) \
                         else self.strategy
        commissions: list = [(copy.deepcopy(r).to_dict() if isinstance(r, Commissions) else r) \
                                  for r in self.commissions]
        # self.size = self.calculateSize()
        self.high = max([c['High'] for c in self.execution_candles]) if len(self.execution_candles) > 0 else None
        self.low = min([c['Low'] for c in self.execution_candles]) if len(self.execution_candles) > 0 else None
        asset: dict = self.asset.to_dict() if isinstance(self.asset, AssetConfig) else self.asset
        risks = [(copy.deepcopy(r).to_dict() if isinstance(r, RiskCalculation) else r) for r in self.risks]
        executions = [(copy.deepcopy(r).to_dict() if isinstance(r, Execution) else r) for r in self.executions]
        orders = [(copy.deepcopy(r).to_dict() if isinstance(r, Order) else r) for r in self.orders]
        order: str = self.order.name if isinstance(self.order, OrderType) else self.order
        execution_candles: list = [typeToDict(copy.deepcopy(c)) for c in self.execution_candles]
        order_candles: list = [typeToDict(copy.deepcopy(c)) for c in self.order_candles]

        return {
            'OrderTime': copy.deepcopy(self.datetime).strftime('%Y-%m-%d %H:%M:%S'),
            'Executions': executions,
            'ExecQty': len(executions),
            'Orders': orders,
            'ExitTime': copy.deepcopy(self.executions[-1].datetime).strftime('%Y-%m-%d %H:%M:%S') \
                    if len(self.executions) > 0 else None,
            'Ticker': self.ticker,
            'Strategy': strategy,
            'Order': order,
            'Signal': signal,
            'Entry': self.entry_price,
            'Exit': self.exit_price,
            'SL': self.current_sl,
            'TP': self.current_tp,
            'Risk': self.risk,
            'Size': self.entries_size,
            'Position': self.position,
            'RisksStruct': risks,
            'SLdist': self.sldist,
            'High': self.high,
            'Low': self.low,
            
            'Return': self.returns,
            'PctRet': 0 if self.risk_capital == 0 else self.returns/self.risk_capital,
            'GrossResult': self.gross_result,
            'NetResult': self.net_result,
            'Balance': self.balance,
            'Spread': self.spread,
            'Commission': self.commissions_value,
            'ComOverRet': self.commissions_value/abs(self.gross_result) \
                            if abs(self.gross_result) > 0 else None,
            'CommissionStruc': commissions,
            'Method': method,
            'OneCandle': self.onecandle,
            'Asset': asset,
            'OrderCandles': order_candles,
            'ExecutionCandles': execution_candles,
        }

class KPIs:

    def __init__(self, df:pd.DataFrame) -> None:

        if not isinstance(df, pd.DataFrame):
            raise ValueError('No DataFrame was passed.')
        
        df = df.copy()
        date_tag: str = 'DateTime'
        if 'DateTime' not in df:
            if 'EntryTime' in df:
                date_tag = 'EntryTime'
            elif 'OrderTime' in df:
                date_tag = 'OrderTime'
            elif 'ExitTime' in df:
                date_tag = 'ExitTime'

        self.days: int = np.busday_count(df[date_tag].tolist()[0].date(), df[date_tag].tolist()[-1].date())
        self.frequency: float = len(df)/self.days * 100//1/100
            
        temp: pd.DataFrame = df.copy()        
        temp['Ret'] = temp['Result']/(temp['SLdist']*temp['Size']) * temp['Risk']
        temp['CumRet'] = (1+temp['Ret']).cumprod()

        # Backtest analysis
        self.winrate: float = len(temp['Return'][temp['Return'] > 0.0])/len(temp['Return'])
        self.avg_win: float = temp['Ret'][temp['Ret'] > 0].mean()
        self.avg_loss: float = temp['Ret'][temp['Ret'] < 0].mean()
        self.expectancy: float = (self.winrate * self.avg_win - (1-self.winrate)*abs(self.avg_loss))
        self.kelly: float = self.expectancy/self.avg_win
        self.avg_risk: float = temp['Risk'].mean()
        self.balance: float = temp['Balance'].iloc[-1]
        self.max_dd: float = temp['AccountDD'].max()
        self.n_trades: int = len(temp)
        self.ulcer_index: float = np.sqrt(np.mean(temp['AccountDD']**2)) * 100
        
    def to_dict(self) -> dict:

        return self.__dict__
    
class Metrics:

    transition: Transitions = Transitions()
    
    def __init__(self, trades:pd.DataFrame, from_frequency:Frequency=Frequency.DAY, 
                 to_frequency:Frequency=Frequency.NATURAL, compound:bool=True, 
                 exact_norm:bool=True) -> None:
        
        self.from_frequency: Frequency = from_frequency
        self.to_frequency: Frequency = to_frequency
        self.compound: bool = compound
        if 'RetPct' not in trades:
            raise ValueError('There is no column named "RetPct".')
        self.returns: pd.Series = trades['RetPct'].copy()
        self.cumret: pd.Series = self._cumReturns(returns=self.returns)
        self.transition: float = 1/Transitions().getChange(first_frequency=self.from_frequency, 
                                    second_frequency=self.to_frequency)
        self.exact_norm: bool = exact_norm
        if 'Trades' not in trades:
            raise ValueError('There is no column named "Trades".')
        self.trades: pd.Series = trades['Trades'].copy()
        # self.annualized_ret: pd.Series = self._changeReturnsFrequency(returns=returns, frequency=Frequency.YEAR)
    
    def _changeReturnsFrequency(self, returns:pd.Series, frequency:Frequency=Frequency.NATURAL
                                ) -> pd.Series:
    
        if frequency == Frequency.NATURAL:
            return returns
        else:
            at_frequency_str_dict: dict = {Frequency.YEAR: "Y", Frequency.WEEK: "7D", 
                                    Frequency.MONTH: "1M", Frequency.DAY: "1D"}
            at_frequency_str: str = at_frequency_str_dict[frequency]
            if self.compound:
                cumret = lambda x: ((1+x).cumprod() - 1).iloc[-1]
                return returns.resample(at_frequency_str).apply(cumret)
            else:
                return returns.resample(at_frequency_str).sum()
        
    def _cumReturns(self, returns:pd.Series=pd.Series(dtype='float64')) -> pd.Series:

        if returns.empty:
            returns = self.returns.copy()
            
        if self.compound:
            self.cumret = (1 + returns).cumprod() - 1
        else:
            self.cumret = returns.cumsum()

        return self.cumret
        
    def _removeZeros(self, inplace:bool=False) -> pd.Series:
        
        temp = self.returns.copy()
        temp[temp == 0] = float('nan')
        if inplace:
            self.returns = temp
            
        return temp
    
    def _demean(self, returns:pd.Series=pd.Series(dtype='float64')) -> pd.Series:
        
        if returns.empty:
            returns = self.returns.copy()
            
        return returns - returns.mean()
    
    def _tailRatio(self, quantiles:list=[], quantile_1:float=None, quantile_2:float=None
                   ) -> float:
        
        if quantile_1 != None and quantile_2 != None:
            quantiles = [quantile_1, quantile_2]

        if len(quantiles) >= 2:
            q_extreme: float = [q for q in quantiles if abs(0.5-q) == \
                                max([abs(0.5-q) for q in quantiles])][0]
            q_std: float = [q for q in quantiles if abs(0.5-q) == \
                                min([abs(0.5-q) for q in quantiles])][0]
            
        demean: pd.Series = self._demean(returns=self._removeZeros(inplace=False))
        pr: float = demean.quantile(q_extreme) / demean.quantile(q_std)

        norm_dist_ratio: float = 4.43
        if self.exact_norm:
            from scipy.stats import norm
            norm_dist_ratio: float = norm.ppf(q_extreme) / norm.ppf(q_std)

        return pr / norm_dist_ratio

    @property
    def drawdownSeries(self) -> pd.Series:
        cumret: pd.Series = self.cumret + 1
        return 1 - cumret/cumret.cummax()
    
    @property
    def rateOfReturn(self) -> float:
        
        rate = self.transition * len(self.returns)

        if self.compound:
            return (self.cumret.iloc[-1] + 1) ** (1/rate) - 1
        else:
            return self.cumret.iloc[-1] / rate
    
    @property
    def averageReturn(self) -> float:

        if self.compound:
            return (1 + self.returns.mean()) ** self.transition - 1
        else:
            return self.returns.mean() * self.transition

    @property
    def averageWin(self) -> float:
        
        avg_win = self.returns[self.returns > 0].mean()
        
        if self.compound:
            return (1 + avg_win) ** self.transition - 1
        else:
            return avg_win * self.transition
    
    @property
    def averageLoss(self) -> float:
        
        avg_loss = self.returns[self.returns < 0].mean()
        
        if self.compound:
            return (1 + avg_loss) ** self.transition - 1
        else:
            return avg_loss * self.transition
    
    @property
    def winrate(self) -> float:
        return len(self.returns[self.returns > 0])/len(self.returns)

    @property
    def profitRatio(self) -> float:
        return self.averageWin/abs(self.averageLoss)
    
    @property
    def expectancy(self) -> float:
        return self.averageWin * self.winrate - \
                    (1-self.winrate) * abs(self.averageLoss)
    
    @property
    def kelly(self) -> float:
        return self.winrate - (1 - self.winrate)/self.profitRatio
    
    @property
    def skew(self) -> float:
        return self.returns.skew() * 1/self.transition**(1/2)
    
    @property
    def standardDeviation(self) -> float:
        return self.returns.std() * (self.transition ** (1/2))
    
    @property
    def sharpeRatio(self) -> float:
        return self.averageReturn if self.standardDeviation == 0 else self.averageReturn/self.standardDeviation
    
    @property
    def lowerTailRatio(self) -> float:
        return self._tailRatio(quantile_1=0.01, quantile_2=0.3)
    
    @property
    def upperTailRatio(self) -> float:
        return self._tailRatio(quantile_1=0.7, quantile_2=0.99)
    
    @property
    def averageDrawdown(self) -> float:
        return self.drawdownSeries.mean()
    
    @ property
    def maxDrawdown(self) -> float:
        return self.drawdownSeries.max()
    
    @property
    def totalTrades(self) -> int:
        return len(self.returns)

    @property
    def days(self) -> float:
        if isinstance(self.returns.index[0], str):
            init: dt.datetime = dt.datetime.strptime(self.returns.index[0], '%Y-%m-%d %H:%M:%S').date()
            end: dt.datetime = dt.datetime.strptime(self.returns.index[-1], '%Y-%m-%d %H:%M:%S').date()
            days: int = np.busday_count(init, end)
        # elif isinstance(self.returns.index[0], int):
        #     days: int = self.returns.index[-1] * Transitions().getChange(Frequency.DAY, Frequency.BUSINESSDAY)
        else:
            init = self.returns.index[0] if isinstance(self.returns.index[0], dt.date) else self.returns.index[0].date()
            end = self.returns.index[-1] if isinstance(self.returns.index[0], dt.date) else self.returns.index[-1].date()
            days: int = np.busday_count(init, end)
        
        return days
    
    @property
    def months(self) -> float:
        return Transitions().businessDaysToMonth(self.days)
    
    @property
    def years(self) -> float:
        return Transitions().businessDaysToYear(self.days)

    @property
    def tradingFrequency(self) -> float:
        return len(self.returns) if self.days == 0 else len(self.returns)/self.days
    
    @property
    def ulcerIndex(self) -> float:
        return np.sqrt(np.mean(self.drawdownSeries**2)) * 100

    def _maximum_favorable_excursion(self, method:str='mean') -> float:

        trade: Trade
        data: list = []
        for trade in self.trades:
            if len(trade.execution_candles) <= 0:
                continue
            max_favorable_excursion: float = None;  max_favorable_time: str = None
            max_averse_excursion: float = None;  max_averse_time: str = None
            for candle in trade.execution_candles:
                
                if trade.signal.value == TradeSide.LONG.value:

                    if max_favorable_excursion == None:
                        max_favorable_excursion: float = candle['High']
                        max_favorable_time = candle['DateTime']
                    if max_averse_excursion == None:
                        max_averse_excursion: float = candle['Low']
                        max_averse_time = candle['DateTime']

                    if candle['High'] > max_favorable_excursion or max_favorable_excursion == None:
                        max_favorable_excursion: float = candle['High']
                        max_favorable_time = candle['DateTime']
                    if candle['Low'] < max_averse_excursion or max_averse_excursion == None:
                        max_averse_excursion: float = candle['Low']
                        max_averse_time = candle['DateTime']

                elif trade.signal.value == TradeSide.SHORT.value:

                    if max_averse_excursion == None:
                        max_averse_excursion: float = candle['High']
                        max_averse_time = candle['DateTime']
                    if max_favorable_time == None:
                        max_favorable_time: float = candle['Low']
                        max_favorable_time = candle['DateTime']
                        
                    if candle['High'] > max_favorable_excursion or max_favorable_excursion == None:
                        max_averse_excursion: float = candle['High']
                        max_averse_time = candle['DateTime']
                    if candle['Low'] < max_averse_excursion or max_averse_excursion == None:
                        max_favorable_excursion: float = candle['Low']
                        max_favorable_time = candle['DateTime']
            
            data.append({
                'mfe': abs(max_favorable_excursion - trade.entry),
                'mft': abs(max_favorable_time - trade.datetime),
                'mae': abs(max_averse_excursion - trade.entry),
                'mat': abs(max_averse_time - trade.datetime),
            })
        
        data: pd.DataFrame = pd.DataFrame(data)

        if method == 'mean':
            return {'MFE': data['mfe'].mean(), 'MFT': data['mft'].mean(), 
                    'MAE': data['mae'].mean(), 'MAT': data['mat'].mean()}
        elif method == 'mode':
            return {'MFE': data['mfe'].mode(), 'MFT': data['mft'].mode(), 
                    'MAE': data['mae'].mode(), 'MAT': data['mat'].mode()}
        else:
            raise ValueError('The method for calculating the MAE, MFE, etc must be "mean" or "sum".')
    
    maximum_favorable_excursion = property(_maximum_favorable_excursion)

    def calculateMetrics(self, indicators:list=['expectancy', 'sharpeRatio', 
                        'maxDrawdown']) -> float:
        
        return {ind: self.__getattribute__(ind) for ind in indicators}
            
    def to_dict(self) -> dict:
        
        return {k: (v._value_ if isinstance(v, Frequency) else v) \
                for k, v in self.__dict__.items() \
            if k not in ['returns', 'drawdown', 'compound', 'frequency', 
                         'cumret', 'transition', 'orig_frequency']}

class CorrelationUtils:
    
    def __init__(self, data:(dict | pd.DataFrame)) -> None:
        
        '''
        data: (dict or pd.DataFrame)
            Must be a dictionary with a dataframe containing a 'Close' column for each asset.
            Or a DataFrame containing a column for each asset's price.
        '''
        
        if isinstance(data, dict):
            data = pd.DataFrame({k: v['Close'] for k, v in data})
        
        self.data: pd.DataFrame = data
        
    def getCorrelationMatrix(self):
        
        self.corr_matrix: pd.DataFrame = self.data.corr()
        np.fill_diagonal(self.corr_matrix.values, np.nan)
        
        return self.corr_matrix
    
    def getCorrelationSum(self) -> dict:
        
        return {c: self.corr_matrix[c].sum(skipna=True) for c in self.corr_matrix.columns}
    
    def getCorrelationMean(self) -> dict:
        
        return {c: self.corr_matrix[c].mean(skipna=True) for c in self.corr_matrix.columns}
        

class Correlations(CorrelationUtils):
    
    def __init__(self, trades:list, data:pd.DataFrame) -> None:

        self.trades: dict = {}
        trade: Trade
        for trade in trades:
            if trade.ticker not in self.data:
                self.trades[trade.ticker] = []
            self.trades[trade.ticker].append(copy.deepcopy(trade))

        for c in ['DateTime', 'Ticker', 'Close']:
            if c not in data.columns:
                raise ValueError(f'There is no {c} column.')
        
        self.data: pd.DataFrame = data.pivot_table(index='DateTime', columns='Ticker', values='Close')
        self.data.columns.name = None
        self.data.fillna(0, method='ffill', inplace=True)
        print(self.data)

    

    