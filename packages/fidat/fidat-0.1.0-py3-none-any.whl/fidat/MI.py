import pandas as pd

def Mass_Index(high: pd.Series, low: pd.Series, period: int = 9, adjust: bool = True) -> pd.Series:
    """
    Calculates the Mass Index from the given high and low price data.

    The Mass Index is a technical indicator used to identify trend reversals based on changes in trading ranges over a specified time period.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods for calculating the Mass Index.
    adjust (bool): Whether to adjust the Mass Index calculation.

    Returns:
    pd.Series: A Series containing the Mass Index values.

    Example:
    # Assuming 'high' and 'low' are DataFrames with the high and low price data
    mass_index = Mass_Index(high, low, period=9, adjust=True)
    """

    # Calculate Single-Period Range and Expanding Sum of the Range
    single_period_range = high - low
    sum_single_period_range = single_period_range.cumsum()

    # Calculate Exponential Moving Average of the Expanding Sum of the Range
    ema_range = sum_single_period_range.ewm(span=period, adjust=adjust).mean()

    # Calculate Mass Index
    mass_index = ema_range / ema_range.shift(1)

    return mass_index
