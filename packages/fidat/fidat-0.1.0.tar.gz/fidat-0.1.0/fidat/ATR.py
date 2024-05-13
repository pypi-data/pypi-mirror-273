import pandas as pd

def Average_True_Range(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Average True Range (ATR) indicator from the given price data.

    The Average True Range (ATR) is the moving average of the True Range (TR) over a specified period.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the Average True Range (ATR) values.

    Example:
    # Assuming 'close', 'high', and 'low' are DataFrames with corresponding price data
    atr = Average_True_Range(close, high, low)
    """

    # Calculate True Range (TR)
    range1 = high - low
    range2 = abs(high - close.shift())
    range3 = abs(low - close.shift())
    tr = pd.concat([range1, range2, range3], axis=1).max(axis=1)

    # Calculate Average True Range (ATR)
    atr = tr.rolling(window=14).mean()  # Change the window size if needed

    return atr