import pandas as pd

def Adaptive_Relative_Strength_Index(close: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Adaptive Relative Strength Index (ARSI).

    Parameters:
    close (pd.Series): Close prices.
    period (int): Number of periods to consider.

    Returns:
    pd.Series: Adaptive Relative Strength Index (ARSI) values.
    """

    # Calculate Price Change
    delta = close.diff()

    # Calculate Gain and Loss
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate Smoothed Gain and Loss
    gain_avg = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss_avg = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    # Calculate Relative Strength
    rs = gain_avg / loss_avg

    # Calculate ARSI
    arsi = 100 - (100 / (1 + rs))

    return arsi