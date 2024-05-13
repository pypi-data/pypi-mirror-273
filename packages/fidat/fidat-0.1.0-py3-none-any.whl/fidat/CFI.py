import pandas as pd

def Cumulative_Force_Index(data: pd.Series, volume: pd.Series, adjust: bool = True) -> pd.Series:
    """
    Calculates the Cumulative Force Index (CFI) indicator from the given price and volume data.

    The Cumulative Force Index (CFI) is a variation of the Force Index that accumulates the Force Index values over time.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    adjust (bool): Whether to adjust the exponential moving averages.

    Returns:
    pd.Series: A Series containing the Cumulative Force Index (CFI) values.

    Example:
    # Assuming 'data' is a DataFrame with the price data and 'volume' is a DataFrame with the volume data
    cfi = Cumulative_Force_Index(data, volume, adjust=True)
    """

    # Calculate Price Change
    price_change = data.diff()

    # Calculate Force Index
    force_index = price_change * volume

    # Calculate Cumulative Force Index (CFI)
    cfi = force_index.cumsum()

    return cfi