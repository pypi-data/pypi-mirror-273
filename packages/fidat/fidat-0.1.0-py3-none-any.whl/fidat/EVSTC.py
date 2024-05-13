import pandas as pd

def Schaff_Trend_Cycle_EVWMA_MACD(close: pd.Series, volume: pd.Series, period_fast: int = 12, period_slow: int = 30, k_period: int = 10, d_period: int = 3, adjust: bool = True) -> pd.Series:
    """
    Calculates the modified Schaff Trend Cycle (STC) oscillator using EVWMA MACD from the given data.

    Parameters:
    close (pd.Series): Series containing the closing prices.
    volume (pd.Series): Series containing the volume data.
    period_fast (int): The period of the fast exponential volume-weighted moving average (EVWMA). Default is 12.
    period_slow (int): The period of the slow exponential volume-weighted moving average (EVWMA). Default is 30.
    k_period (int): The period of the %K calculation. Default is 10.
    d_period (int): The period of the %D calculation. Default is 3.
    adjust (bool): Whether to adjust the indicator. Default is True.

    Returns:
    pd.Series: A Series containing the modified Schaff Trend Cycle (STC) values.

    Example:
    # Assuming 'close' and 'volume' are Series containing the data
    stc_evwma_macd = Schaff_Trend_Cycle_EVWMA_MACD(close, volume, period_fast=12, period_slow=30, k_period=10, d_period=3, adjust=True)
    """

    # Calculate the EVWMA MACD
    evwma_fast = (close * volume).ewm(span=period_fast, adjust=adjust).mean() / volume.ewm(span=period_fast, adjust=adjust).mean()
    evwma_slow = (close * volume).ewm(span=period_slow, adjust=adjust).mean() / volume.ewm(span=period_slow, adjust=adjust).mean()
    evwma_macd = evwma_fast - evwma_slow

    # Calculate %K
    stok = ((evwma_macd - evwma_macd.rolling(window=k_period).min()) / (evwma_macd.rolling(window=k_period).max() - evwma_macd.rolling(window=k_period).min())) * 100

    # Calculate %D
    stod = stok.rolling(window=d_period).mean()

    # Calculate "double smoothed" %D
    stod_double_smooth = stod.rolling(window=d_period).mean()

    return stod_double_smooth