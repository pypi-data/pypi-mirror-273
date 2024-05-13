import pandas as pd 

def Bull_Power(high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Bull Power indicator from the given high and low price data.

    Bull Power is the difference between the high price and the 13-period exponential moving average of the low price.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the Bull Power values.

    Example:
    # Assuming 'high' is a DataFrame with the high price data and 'low' is a DataFrame with the low price data
    bull_power = Bull_Power(high, low)
    """
    ema_low = low.ewm(span=13, min_periods=13).mean()
    bull_power = high - ema_low
    return bull_power