import pandas as pd
import numpy as np

def Weighted_Moving_Average(data: pd.Series, period: int = 9) -> pd.Series:
    """
    Calculate the Weighted Moving Average (WMA) of a given series of closing prices.

    Parameters:
    - close (pd.Series): A Series containing the closing prices.
    - period (int): The period over which to calculate the WMA.

    Returns:
    - pd.Series: A Series containing the WMA values.
    """
    # Generate weights increasing from 1 up to the period number
    weights = pd.Series(range(1, period + 1))
    # Calculate the weighted moving average using the rolling window
    def weighted_average(x):
        return np.dot(x, weights) / weights.sum()

    return data.rolling(window=period).apply(weighted_average, raw=True)