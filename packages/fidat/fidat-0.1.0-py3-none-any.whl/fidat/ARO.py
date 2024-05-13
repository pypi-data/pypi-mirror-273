import pandas as pd

def Aroon_Oscillator(high: pd.Series, low: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Aroon Oscillator.

    Parameters:
    high (pd.Series): High prices.
    low (pd.Series): Low prices.
    period (int): Number of periods to consider.

    Returns:
    pd.Series: Aroon Oscillator values.
    """

    # Calculate Aroon Up and Aroon Down
    aroon_up = high.rolling(window=period + 1).apply(lambda x: x.argmax(), raw=True) / period * 100
    aroon_down = low.rolling(window=period + 1).apply(lambda x: x.argmin(), raw=True) / period * 100

    # Calculate Aroon Oscillator
    aroon_oscillator = aroon_up - aroon_down

    return aroon_oscillator