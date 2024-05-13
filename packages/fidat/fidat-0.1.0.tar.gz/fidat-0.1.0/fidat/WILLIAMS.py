import pandas as pd

def Williams_Percent_Range(close: pd.Series, high: pd.Series, low: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Williams Percent Range (%R) from the given close, high, and low price data.

    Williams %R, or just %R, is a technical analysis oscillator.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods for calculating the Williams Percent Range (%R).

    Returns:
    pd.Series: A Series containing the Williams Percent Range (%R) values.

    Example:
    # Assuming 'close', 'high', and 'low' are DataFrames with the close, high, and low price data
    williams_percent_r = Williams_Percent_Range(close, high, low, period=14)
    """

    # Calculate Williams Percent Range (%R)
    lowest_low = low.rolling(window=period).min()
    highest_high = high.rolling(window=period).max()
    williams_percent_r = -100 * ((highest_high - close) / (highest_high - lowest_low))

    return williams_percent_r