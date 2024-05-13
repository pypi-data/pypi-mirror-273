import pandas as pd

def High_Low_Index(close: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame, period: int = 10) -> pd.DataFrame:
    """
    Calculates the High-Low Index.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close prices.
    high (pd.DataFrame): DataFrame containing the high prices.
    low (pd.DataFrame): DataFrame containing the low prices.
    period (int): The period used to calculate the high-low range. Default is 10.

    Returns:
    pd.DataFrame: DataFrame containing the High-Low Index values.

    Example:
    # Assuming 'close', 'high', and 'low' are DataFrames containing the close, high, and low prices respectively
    high_low_index = High_Low_Index(close, high, low, period=10)
    """

    high_low_range = high - low
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    normalized_range = (high_low_range / (highest_high - lowest_low)) * 100
    high_low_index = (close - lowest_low) / (highest_high - lowest_low)

    return high_low_index