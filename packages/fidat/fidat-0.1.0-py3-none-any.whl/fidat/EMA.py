import pandas as pd

def Exponential_Moving_Average(data: pd.Series, period: int = 9, adjust: bool = True) -> pd.Series:
    """
    Calculates the Exponential Weighted Moving Average (EMA) of a given data series. EMA is a type of moving average
    that places a greater weight and significance on the most recent data points. It is also referred to as the
    exponentially weighted moving average. EMA reacts more significantly to recent price changes than a simple moving average (SMA),
    which applies an equal weight to all observations in the period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data series.
    period (int): The number of periods over which to calculate the EMA.
    adjust (bool): Boolean to decide whether the EMA calculation is adjusted.

    Returns:
    pd.Series: A pandas Series containing the Exponential Moving Average of the input data series.

    Example:
    # Assuming 'data' is a DataFrame and you want to calculate the EMA for the 'Close' column
    data['EMA'] = Exponential_Moving_Average(data['Close'], period=9)
    """
    return data.ewm(span=period, adjust=adjust).mean()
