import pandas as pd

def Volume_Price_Trend(open: pd.Series, close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Volume Price Trend (VPT) indicator from the given open, close, high, and low price data.

    The Volume Price Trend (VPT) indicator is a cumulative indicator that combines price and volume to show the direction of the trend and strength of buying and selling pressure.

    Parameters:
    open (pd.DataFrame): DataFrame containing the open price data.
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the Volume Price Trend (VPT) values.

    Example:
    # Assuming 'open', 'close', 'high', and 'low' are DataFrames with the required data
    vpt = Volume_Price_Trend(open, close, high, low)
    """

    # Calculate the Volume Price Trend (VPT)
    vpt = pd.Series(0, index=open.index, dtype=float)
    for i in range(1, len(open)):
        close_change = close.iloc[i] - close.iloc[i - 1]
        vpt.iloc[i] = vpt.iloc[i - 1] + (close_change * (high.iloc[i] - low.iloc[i]) / close.iloc[i])

    return vpt