import pandas as pd

def Typical_Price(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Typical Price from the given close, high, and low price data.

    The Typical Price is the average of the high, low, and close prices for a given period.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the Typical Price values.

    Example:
    # Assuming 'close', 'high', and 'low' are DataFrames with the close, high, and low price data
    typical_price = Typical_Price(close, high, low)
    """

    # Calculate Typical Price
    typical_price = (high + low + close) / 3

    return typical_price