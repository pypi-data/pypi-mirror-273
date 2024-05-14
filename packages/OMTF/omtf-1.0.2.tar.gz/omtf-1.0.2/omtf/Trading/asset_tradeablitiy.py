
import numpy as np
import pandas as pd

from execution_utils import AssetConfig

class AssetTradeable:
    
    def __init__(self, asset:AssetConfig, prices:pd.DataFrame, trades:pd.DataFrame, 
                 asset_column:str='Ticker') -> None:
        self.asset: AssetConfig = asset
        self.prices: pd.DataFrame = prices
        self._columnInDF(asset_column, trades)
        if self._columnInDF(asset_column, trades):
            self.trades: pd.DataFrame = trades[trades[asset_column] == asset].copy()
        
    def _columnInDF(self, column:str, df:pd.DataFrame, errors:bool=True) -> bool:
        
        if column not in df:
            if errors:
                raise ValueError(f"The column {column} is not in the dataframe columns ({','.join(df.columns)})")
            else:
                print(f"The column {column} is not in the dataframe columns ({','.join(df.columns)})")
                return False
        else:
            return True
    
    def liquidationDays(self, window:int=20, vol_fraction:float=0.05, volume_column:str='Volume', 
                        qty_column:str='Size') -> pd.Series:
        
        if self._columnInDF(volume_column, self.prices):
            avg_vol: pd.Series = self.prices[volume_column].rolling(window=window).mean() * vol_fraction
        
        if self._columnInDF(qty_column, self.trades):
            size: pd.Series = self.trades[qty_column]
        
        return size/avg_vol
    
    def commissionErosion(self, com_column:str='Commission', ret_column:str='GrossResult') -> pd.Series:
        
        self._columnInDF(com_column, self.trades)
        self._columnInDF(ret_column, self.trades)
        
        trades: pd.DataFrame = self.trades[self.trades[ret_column] != 0].copy()
        
        return trades[com_column] / trades[ret_column].abs()
    
    def isTradeable(self, liquidation_days:float=1, commission_erosion:float=0.2, 
                    liquidation_vol_window:int=20, liquidation_vol_fraction:float=0.05, 
                    volume_column:str='Volume', qty_column:str='Size', com_column:str='Commission', 
                    ret_column:str='GrossResult') -> bool:
        
        liquidation: pd.Series = self.liquidationDays(window=liquidation_vol_window, 
                                                      vol_fraction=liquidation_vol_fraction, 
                                                      volume_column=volume_column, qty_column=qty_column)
        erosion: pd.Series = self.commissionErosion(com_column=com_column, ret_column=ret_column)
        
        return len(erosion[erosion < commission_erosion]) <= 0 and \
            len(liquidation[liquidation < liquidation_days]) <= 0