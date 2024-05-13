import pandas as pd

def Bear_Power(high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Bear Power indicator from the given high and low price data.

    Bear Power is the difference between the low price and the 13-period exponential moving average of the high price.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the Bear Power values.

    Example:
    # Assuming 'high' is a DataFrame with the high price data and 'low' is a DataFrame with the low price data
    bear_power = Bear_Power(high, low)
    """
    ema_high = high.ewm(span=13, min_periods=13).mean()
    bear_power = low - ema_high
    return bear_power