import pandas as pd

def Price_Zone_Oscillator(data: pd.Series, period: int = 14, adjust: bool = True) -> pd.Series:
    """
    Calculates the Price Zone Oscillator (PZO) indicator from the given price data.

    The Price Zone Oscillator (PZO) is a momentum oscillator that measures the difference between the closing price and a moving average of the closing price over a specified period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods to use in the calculation.
    adjust (bool): Whether to adjust the exponential moving average.

    Returns:
    pd.Series: A Series containing the Price Zone Oscillator (PZO) values.

    Example:
    # Assuming 'data' is a DataFrame with the price data
    pzo = Price_Zone_Oscillator(data, period=14, adjust=True)
    """

    # Calculate Moving Average of Closing Price
    ma_close = data.rolling(window=period, min_periods=1).mean()

    # Calculate Price Zone Oscillator (PZO)
    pzo = data - ma_close

    return pzo
