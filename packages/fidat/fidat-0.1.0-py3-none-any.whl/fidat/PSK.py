import pandas as pd

def Prings_Special_K(data: pd.DataFrame, short_period: int = 9, long_period: int = 30) -> pd.Series:
    """
    Pring's Special K indicator.
    
    Parameters:
    - data: DataFrame containing the relevant OHLCV data.
    - short_period: Integer representing the short period for calculation (default: 9).
    - long_period: Integer representing the long period for calculation (default: 30).
    
    Returns:
    - Series containing the Pring's Special K values.
    """
    # Add implementation here

    # Calculate short and long EMA
    ema_short = data.ewm(span=short_period, adjust=False).mean()
    ema_long = data.ewm(span=long_period, adjust=False).mean()
    
    # Calculate the difference between short and long EMA
    diff = ema_short - ema_long
    
    # Calculate the signal line
    signal_line = diff.rolling(window=9, min_periods=1).mean()
    
    # Calculate Pring's Special K
    special_k = (diff - signal_line) * 100
    
    return special_k