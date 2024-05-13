import pandas as pd

def Elders_Impulse_System(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 13) -> pd.Series:

    """
    The Elder's Impulse System, developed by Dr. Alexander Elder, is a trading strategy that combines two indicators to generate trading signals: the Elder-Ray Index and the Simple Moving Average (SMA).
    """

    # Calculate Bull Power and Bear Power
    bull_power = high - close.rolling(window=period).mean()
    bear_power = low - close.rolling(window=period).mean()
    
    # Calculate Elder's Impulse
    buy_signal = (bull_power > 0) & (bull_power.diff() > 0) & (bear_power < 0) & (bear_power.diff() < 0)
    sell_signal = (bull_power < 0) & (bull_power.diff() < 0) & (bear_power > 0) & (bear_power.diff() > 0)
    
    impulse = pd.Series(0, index=close.index)
    impulse[buy_signal] = 1
    impulse[sell_signal] = -1
    
    return impulse