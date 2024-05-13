import pandas as pd

def Volume_Weighted_Average_Price(close: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculate the Volume Weighted Average Price (VWAP) from intraday trading data.

    Parameters:
    - data (pd.DataFrame): A DataFrame with columns 'close', 'volume', and 'date' or 'timestamp'.

    Returns:
    - pd.Series: A Series containing the VWAP values for each unique date or timestamp in the data.
    """

    # Calculate direction of price movement
    direction = close.diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)

    # Calculate Weighted On Balance Volume
    weighted_obv = direction * close * volume
    weighted_obv = weighted_obv.cumsum()

    return weighted_obv