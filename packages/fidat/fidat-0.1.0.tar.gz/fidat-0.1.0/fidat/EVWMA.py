import pandas as pd

def Exponential_Volume_Weighted_Moving_Average(close: pd.Series, volume: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculate the Exponential Volume Weighted Moving Average (eVWMA), 
    using separate Series for closing prices and trading volumes.

    Parameters:
    - close (pd.Series): A Series containing the closing prices.
    - volume (pd.Series): A Series containing the trading volumes.
    - period (int): The period over which to calculate the eVWMA.

    Returns:
    - pd.Series: A Series containing the eVWMA values.
    """
    # Calculate the volume times close price
    vol_price = volume * close
    
    # Exponential moving sum of volume times price
    vol_price_sum = vol_price.ewm(span=period, adjust=False).mean()
    
    # Exponential moving sum of volume
    volume_sum = volume.ewm(span=period, adjust=False).mean()
    
    # eVWMA calculation
    evwma = vol_price_sum / volume_sum

    return evwma