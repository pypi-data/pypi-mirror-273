import pandas as pd

def Double_Exponential_Moving_Average(data: pd.Series, period: int = 9, adjust: bool = True) -> pd.Series:
    """
    Calculates the Double Exponential Moving Average (DEMA) of a given data series.
    The DEMA uses two EMAs to eliminate lag, which makes it faster and more responsive
    than traditional single or simple EMAs. DEMA is particularly useful to identify
    trend directions and reversals quickly.

    Parameters:
    cls (type): The class this method is part of, typically used when defining a class method.
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods over which the DEMA is calculated.
    adjust (bool): Boolean to decide if the EMA calculation should be adjusted.

    Returns:
    pd.Series: A pandas Series containing the Double Exponential Moving Average of the data.

    Example:
    # Assuming 'data' is a DataFrame and you want to calculate the DEMA for the 'close' column
    data['DEMA'] = cls.DEMA(data['close'], period=9)
    """
    # First EMA
    ema1 = data.ewm(span=period, adjust=adjust).mean()
    # Second EMA of the first EMA
    ema2 = ema1.ewm(span=period, adjust=adjust).mean()
    # Double EMA calculation
    dema = 2 * ema1 - ema2

    return dema