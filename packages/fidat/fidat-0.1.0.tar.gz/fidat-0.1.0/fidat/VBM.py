import pandas as pd

def Volatility_Based_Momentum(close: pd.Series, high: pd.Series, low: pd.Series, roc_period: int = 12, atr_period: int = 26) -> pd.Series:
    """
    Calculates the Volatility-Based Momentum (VBM) indicator from the given price data.

    The Volatility-Based Momentum (VBM) indicator combines the Rate of Change (ROC) and the Average True Range (ATR)
    to provide a measure of momentum adjusted for volatility.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    roc_period (int): The number of periods for calculating the Rate of Change (ROC).
    atr_period (int): The number of periods for calculating the Average True Range (ATR).

    Returns:
    pd.Series: A Series containing the Volatility-Based Momentum (VBM) values.

    Example:
    # Assuming 'close', 'high', and 'low' are DataFrames with corresponding price data
    vbm = Volatility_Based_Momentum(close, high, low, roc_period=12, atr_period=26)
    """

    # Calculate Rate of Change (ROC)
    roc = close.pct_change(periods=roc_period) * 100

    # Calculate Average True Range (ATR)
    high_low_range = high - low
    high_close_range = abs(high - close.shift())
    low_close_range = abs(low - close.shift())
    true_range = pd.concat([high_low_range, high_close_range, low_close_range], axis=1).max(axis=1)
    atr = true_range.rolling(window=atr_period).mean()

    # Calculate Volatility-Based Momentum (VBM)
    vbm = roc / atr

    return vbm