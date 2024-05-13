import pandas as pd

def Schaff_Trend_Cycle(data: pd.Series, fast_period: int = 23, slow_period: int = 50, k_period: int = 10, d_period: int = 3, adjust: bool = True) -> pd.Series:
    """
    Calculates the Schaff Trend Cycle (STC) oscillator from the given data.

    The Schaff Trend Cycle (STC) oscillator is a momentum oscillator that combines the concepts of the stochastic oscillator and the moving average.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data for which to calculate the Schaff Trend Cycle.
    period_fast (int): The period of the fast exponential moving average. Default is 23.
    period_slow (int): The period of the slow exponential moving average. Default is 50.
    k_period (int): The period of the %K calculation. Default is 10.
    d_period (int): The period of the %D calculation. Default is 3.
    adjust (bool): Whether to adjust the indicator. Default is True.

    Returns:
    pd.Series: A Series containing the Schaff Trend Cycle (STC) values.

    Example:
    # Assuming 'data' is a DataFrame containing the data
    stc = Schaff_Trend_Cycle(data, period_fast=23, period_slow=50, k_period=10, d_period=3, adjust=True)
    """

# Calculate the fast and slow exponential moving averages
    ema_fast = data.ewm(span=fast_period, adjust=adjust).mean()
    ema_slow = data.ewm(span=slow_period, adjust=adjust).mean()

    # Calculate the MACD
    macd = ema_fast - ema_slow

    # Calculate %K
    stok = ((macd - macd.rolling(window=k_period).min()) / (macd.rolling(window=k_period).max() - macd.rolling(window=k_period).min())) * 100

    # Calculate %D
    stod = stok.rolling(window=d_period).mean()

    # Calculate "double smoothed" %D
    stod_double_smooth = stod.rolling(window=d_period).mean()

    return stod_double_smooth 
