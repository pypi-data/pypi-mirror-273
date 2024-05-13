import numpy as np
import pandas as pd

def Wave_PM(data: pd.Series, period: int = 14, lookback_period: int = 10) -> pd.Series:
    """
    Calculates the Wave PM (Whistler Active Volatility Energy Price Mass) indicator.

    Parameters:
    data (pd.DataFrame): DataFrame containing the close prices.
    period (int): The period used to calculate the moving average and standard deviation. Default is 14.
    lookback_period (int): The number of periods to look back for calculating the power. Default is 100.

    Returns:
    pd.Series: Series containing the Wave PM indicator values.

    Example:
    # Assuming 'data' is a DataFrame containing the close prices
    wave_pm = Wave_PM(data, period=14, lookback_period=100)
    """

    ma = data.rolling(window=period).mean()
    std = data.rolling(window=period).std(ddof=0)

    dev = 3.2 * std
    power = (dev / ma) ** 2

    def tanh(x):
        return (np.exp(2 * x) - 1) / (np.exp(2 * x) + 1)

    variance = power.rolling(window=lookback_period).sum() / lookback_period
    calc_dev = np.sqrt(variance) * ma
    y = (dev / calc_dev)
    oscLine = tanh(y)

    return oscLine