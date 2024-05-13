import pandas as pd

def Commodity_Channel_Index(close: pd.Series, high: pd.Series, low: pd.Series, period: int = 20, constant: float = 0.015) -> pd.Series:
    """
    Calculates the Commodity Channel Index (CCI) indicator from the given close, high, and low price data.

    Commodity Channel Index (CCI) measures the deviation of the price from its statistical mean.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods to use in the calculation.
    constant (float): Constant multiplier. Default is 0.015.

    Returns:
    pd.Series: A Series containing the Commodity Channel Index (CCI) values.

    Example:
    # Assuming 'close' is a DataFrame with the close price data, 'high' is a DataFrame with the high price data,
    # and 'low' is a DataFrame with the low price data
    cci = Commodity_Channel_Index(close, high, low, period=20, constant=0.015)
    """

    # Typical Price
    tp = (close + high + low) / 3

    # Mean Deviation
    mean_deviation = tp - tp.rolling(window=period).mean()

    # Mean Absolute Deviation
    mean_abs_deviation = mean_deviation.abs().rolling(window=period).mean()

    # Commodity Channel Index (CCI)
    cci = (tp - tp.rolling(window=period).mean()) / (constant * mean_abs_deviation)

    return cci