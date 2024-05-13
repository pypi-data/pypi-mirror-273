import pandas as pd

def Smoothed_Moving_Average(data: pd.Series, period: int = 42) -> pd.Series:
    """
    Calculates the Smoothed Moving Average (SMMA) of a given data series. The SMMA is a type of moving average that
    applies a greater smoothing factor over a longer period. This average is useful in reducing the noise in a data
    set and identifying long-term trends more clearly than a simple moving average.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods over which the SMMA is calculated.
    adjust (bool): Boolean to decide if the EMA calculation should be adjusted.

    Returns:
    pd.Series: A pandas Series containing the Smoothed Moving Average of the data.

    Example:
    # Assuming 'data' is a DataFrame and you want to calculate the SMMA for the 'close' column
    data['SMMA'] = Smooth_Moving_Average(data['close'], period=42)
    """
    # Initial SMA calculation for the first 'period' values
    initial_sma = data.iloc[:period].mean()
    
    # SMMA formula uses previous SMMA value and the current period's data point
    smma = pd.Series(data=0, index=data.index, dtype=float)
    smma.iloc[period-1] = initial_sma
    for i in range(period, len(data)):
        smma.iloc[i] = (smma.iloc[i-1] * (period - 1) + data.iloc[i]) / period

    return smma