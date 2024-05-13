import pandas as pd

def Power_Indicators(high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Bull Power and Bear Power indicators from the given high and low price data.

    Bull Power is the difference between the high price and the 13-period exponential moving average of the low price.
    Bear Power is the difference between the low price and the 13-period exponential moving average of the high price.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.DataFrame: A DataFrame containing the Bear Power and Bull Power columns.

    Example:
    # Assuming 'high' is a DataFrame with the high price data and 'low' is a DataFrame with the low price data
    power_indicators = Power_Indicators(high, low)
    """
    ema_low = low.ewm(span=13, min_periods=13).mean()
    ema_high = high.ewm(span=13, min_periods=13).mean()
    
    bull_power = high - ema_low
    bear_power = low - ema_high
    
    return pd.DataFrame({'Bull Power': bull_power.squeeze(), 'Bear Power': bear_power.squeeze()})