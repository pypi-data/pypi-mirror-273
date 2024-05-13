import pandas as pd

def Demand_Index(close: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculate the Demand Index for a given series of closing prices and volumes.
    
    Parameters:
        close (pd.Series): Series of closing prices.
        volume (pd.Series): Series of trading volumes.
        
    Returns:
        pd.Series: Series containing the Demand Index values.
    """
    di_values = []

    for i in range(1, len(close)):
        price_change = close.iloc[i] - close.iloc[i - 1]
        di = price_change / close.iloc[i - 1] * volume.iloc[i]
        di_values.append(di)
    
    di_series = pd.Series(di_values, index=close.index[1:])
    return di_series