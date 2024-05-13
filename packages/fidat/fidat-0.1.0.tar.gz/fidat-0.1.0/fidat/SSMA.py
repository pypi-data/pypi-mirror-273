import pandas as pd

def Smoothed_Simple_Moving_Average(data: pd.Series, period: int = 9, adjust: bool = True) -> pd.Series:
    """
    Calculates the Smoothed Simple Moving Average (SSMA) of a given data series.
    SSMA is a form of exponential smoothing which gives more weight to recent data points
    but does not respond as quickly to price changes as an exponential moving average (EMA).

    Parameters:
    data (pd.Series): Pandas Series containing the data over which the moving average is to be calculated.
    period (int): The number of periods over which to calculate the SSMA.
    adjust (bool): Boolean to decide whether the calculation is adjusted (using exponential decay)
                   or simple (similar to an arithmetic moving average but smoother).

    Returns:
    pd.Series: A pandas Series containing the Smoothed Simple Moving Average of the input data series.

    Example:
    # Assuming 'data' is a DataFrame and you want to calculate the SSMA for the 'Close' column
    prices = data['Close']
    data['SSMA'] = SSMA(prices, period=9, adjust=True)
    """
    if adjust:
        # Using exponential decay formula for adjusted SSMA
        return data.ewm(alpha=1/period, adjust=True).mean()
    else:
        # Implementing a simpler, cumulative moving average formula for unadjusted SSMA
        return data.expanding().mean().where(lambda x: x.index >= period - 1)