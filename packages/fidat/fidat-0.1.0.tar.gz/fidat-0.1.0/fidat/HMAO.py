import pandas as pd

def Hull_Moving_Average_Oscillator(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the Hull Moving Average Oscillator.

    Parameters:
    data (pd.DataFrame): DataFrame containing close prices.
    period (int): Period for calculating the Hull Moving Average. Default is 14.

    Returns:
    pd.Series: Series with the Hull Moving Average Oscillator values.
    """
    wma_half_period = int(period / 2)
    wma_half = 2 * data.rolling(window=wma_half_period).mean() - data.rolling(window=period).mean()
    wma_sqrt_period = int(pow(period, 0.5))
    hull_ma = (wma_half.rolling(window=wma_sqrt_period).mean()).round(2)
    return hull_ma