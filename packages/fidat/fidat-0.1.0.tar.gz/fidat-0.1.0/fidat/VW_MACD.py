import pandas as pd

def Volume_Weighted_MACD(close: pd.Series, volume: pd.Series, period_fast: int = 12, period_slow: int = 26, signal: int = 9, adjust: bool = True) -> pd.Series:
    """
    Calculates the Volume-Weighted Moving Average Convergence Divergence (VW_MACD) and its signal line from the given price data.

    The VW_MACD is similar to the traditional MACD indicator, but it incorporates volume into its calculation.
    It measures the difference between two volume-weighted moving averages of a security’s price and compares it
    with a signal line.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    period_fast (int): The number of periods for the fast EMA.
    period_slow (int): The number of periods for the slow EMA.
    signal (int): The number of periods for the signal line EMA.
    adjust (bool): Boolean to decide if the EMA calculation should be adjusted.

    Returns:
    pd.DataFrame: A DataFrame containing the VW_MACD, VW_MACD Signal, and VW_MACD Histogram.

    Example:
    # Assuming 'close' and 'volume' are DataFrames with close price and volume data
    vw_macd_data = Volume_Weighted_MACD(close, volume, period_fast=12, period_slow=26, signal=9)
    """

    # Calculate the volume-weighted close
    weighted_close = close * volume

    # Calculate fast and slow volume-weighted EMAs
    ema_fast = (weighted_close.ewm(span=period_fast, adjust=adjust).mean() / 
                volume.ewm(span=period_fast, adjust=adjust).mean())
    ema_slow = (weighted_close.ewm(span=period_slow, adjust=adjust).mean() / 
                volume.ewm(span=period_slow, adjust=adjust).mean())

    # Calculate VW_MACD line
    vw_macd_line = ema_fast - ema_slow

    # Calculate signal line
    vw_macd_signal = vw_macd_line.ewm(span=signal, adjust=adjust).mean()

    # Calculate VW_MACD histogram
    vw_macd_histogram = vw_macd_line - vw_macd_signal

    # Create DataFrame to hold VW_MACD data
    vw_macd_data = pd.DataFrame({
        'VW_MACD': vw_macd_line,
        'VW_Signal': vw_macd_signal,
        'VW_Histogram': vw_macd_histogram
    })

    return vw_macd_data

# Example usage:
# Assuming 'close' and 'volume' are DataFrames with close price and volume data.
# vw_macd_data = Volume_Weighted_MACD(close, volume, period_fast=12, period_slow=26, signal=9)
