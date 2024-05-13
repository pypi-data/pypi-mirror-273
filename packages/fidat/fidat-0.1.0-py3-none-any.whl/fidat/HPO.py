import pandas as pd

def High_Pass_Oscillator(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the High Pass Oscillator.

    Parameters:
    data (pd.DataFrame): DataFrame containing close prices.
    period (int): Period for calculating the oscillator. Default is 14.

    Returns:
    pd.Series: Series with the High Pass Oscillator values.
    """
    high_pass = data - data.rolling(window=period).mean()
    return high_pass