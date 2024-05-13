import pandas as pd

def Williams_Fractal(high: pd.Series, low: pd.Series, period: int = 2) -> pd.Series:
    """
    Calculates the Williams Fractal Indicator.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high prices.
    low (pd.DataFrame): DataFrame containing the low prices.
    period (int): How many lower highs/higher lows the extremum value should be preceded and followed. Default is 2.

    Returns:
    pd.DataFrame: DataFrame indicating the presence of Williams Fractals.

    Example:
    # Assuming 'high' and 'low' are DataFrames containing the high and low prices respectively
    fractals = Williams_Fractal(high, low, period=2)
    """

    # Calculate the minimum and maximum prices within the rolling window
    min_low = low.rolling(window=2 * period + 1, center=True).min()
    max_high = high.rolling(window=2 * period + 1, center=True).max()

    # Create boolean masks for bearish and bullish fractals
    bearish_mask = low.shift(-period) == min_low
    bullish_mask = high.shift(-period) == max_high

    # Create DataFrame containing bearish and bullish fractals
    fractals = pd.DataFrame({'BearishFractal': bearish_mask, 'BullishFractal': bullish_mask})

    return fractals