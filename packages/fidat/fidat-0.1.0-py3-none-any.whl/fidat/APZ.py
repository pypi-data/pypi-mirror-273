import pandas as pd

def Adaptive_Price_Zone(close: pd.Series, high: pd.Series, low: pd.Series, period: int = 21, dev_factor: int = 2, MA: pd.Series = None, adjust: bool = True) -> pd.Series:
    """
    Calculates the Adaptive Price Zone (APZ) indicator from the given high and low price data.

    The Adaptive Price Zone (APZ) is a technical indicator developed by Lee Leibfarth.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The period used in the calculation. Default is 21.
    dev_factor (int): The deviation factor used to calculate the upper and lower bands. Default is 2.
    MA (pd.Series): Optional moving average data. If provided, it will be used instead of calculating a new one. Default is None.
    adjust (bool): Whether to adjust the calculation. Default is True.

    Returns:
    pd.DataFrame: A DataFrame containing the Adaptive Price Zone (APZ) values.

    Example:
    # Assuming 'high' is a DataFrame with the high price data and 'low' is a DataFrame with the low price data
    apz = APZ(high, low, period=21, dev_factor=2, MA=None, adjust=True)
    """

    # Calculate the midpoint between high and low prices
    midpoint = (high + low) / 2

    # Calculate the Average True Range (ATR)
    atr = pd.concat([(high - low), (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1).max(axis=1).rolling(window=period).mean()

    # Calculate the upper and lower bands
    upper_band = midpoint + (dev_factor * atr)
    lower_band = midpoint - (dev_factor * atr)

    return pd.DataFrame({'Upper Band': upper_band, 'Lower Band': lower_band})