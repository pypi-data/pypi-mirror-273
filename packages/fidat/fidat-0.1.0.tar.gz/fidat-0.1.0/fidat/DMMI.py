import pandas as pd

def Dynamic_Momentum_Index(close: pd.Series, adjust: bool = True) -> pd.Series:
    """
    Calculate the Dynamic Momentum Index (DMI) for a given series of closing prices.

    Parameters:
        close (pd.Series): Series of closing prices.
        adjust (bool): Whether to adjust the data for splits, dividends, etc. (default is True).

    Returns:
        pd.Series: Series containing the Dynamic Momentum Index (DMI) values.
    """
    price_change = close.diff(1)
    volatility = price_change.abs().rolling(window=14, min_periods=1).mean()
    volatility_sum = volatility.rolling(window=14, min_periods=1).sum()
    velocity = price_change / volatility_sum
    dmi = velocity.rolling(window=14, min_periods=1).sum()
    
    if adjust:
        dmi = dmi / close
        
    return dmi