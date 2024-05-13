import pandas as pd
import numpy as np

def Hull_Moving_Average(data: pd.Series, period: int = 16) -> pd.Series:
    """
    Calculate the Hull Moving Average (HMA) of a given series of closing prices.

    Parameters:
    - data (pd.Series): A Series containing the closing prices.
    - period (int): The period over which to calculate the HMA.

    Returns:
    - pd.Series: A Series containing the HMA values.
    """
    # Calculate the first WMA with half the period
    half_length = int(period / 2)
    sqrt_length = int(np.sqrt(period))

    wma_half = 2 * data.rolling(window=half_length).apply(
        lambda x: np.dot(x, np.arange(1, half_length + 1)) / np.arange(1, half_length + 1).sum(), raw=True)

    # Calculate the second WMA for the full period
    wma_full = data.rolling(window=period).apply(
        lambda x: np.dot(x, np.arange(1, period + 1)) / np.arange(1, period + 1).sum(), raw=True)

    # Calculate the difference of the WMAs
    diff_wma = wma_half - wma_full

    # Calculate the final HMA
    hma = diff_wma.rolling(window=sqrt_length).apply(
        lambda x: np.dot(x, np.arange(1, sqrt_length + 1)) / np.arange(1, sqrt_length + 1).sum(), raw=True)

    return hma