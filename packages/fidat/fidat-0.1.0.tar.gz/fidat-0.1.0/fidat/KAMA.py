import pandas as pd

def Kaufman_Adaptive_Moving_Average(data: pd.Series, er_period: int = 10, ema_fast: int = 2, ema_slow: int = 30, period: int = 20) -> pd.Series:
    """
    Calculate Kaufman's Adaptive Moving Average (KAMA).

    Parameters:
    - data (pd.Series): (Prefer close) A Series containing the closing prices.
    - er_period (int): The period to calculate the Efficiency Ratio (ER) which adjusts the smoothing.
    - ema_fast (int): The number of periods for the fast EMA component.
    - ema_slow (int): The number of periods for the slow EMA component.
    - period (int): The initial period over which KAMA is calculated.

    Returns:
    - pd.Series: A Series containing the KAMA values.
    """
    # Calculate the Efficiency Ratio (ER)
    change = data.diff(er_period)
    volatility = data.diff().abs().rolling(er_period).sum()
    er = abs(change) / volatility

    # Calculate the Smoothing Constant (SC)
    sc = (er * (2 / (ema_fast + 1) - 2 / (ema_slow + 1)) + 2 / (ema_slow + 1)) ** 2

    # Initialize KAMA with the first data point after the initial period
    kama = pd.Series(index=data.index, data=float('nan'))
    initial_kama = data.iloc[period]
    kama.iloc[period] = initial_kama

    # Calculate KAMA using the iterative approach
    for i in range(period + 1, len(data)):
        kama.iloc[i] = kama.iloc[i - 1] + sc.iloc[i] * (data.iloc[i] - kama.iloc[i - 1])

    return kama