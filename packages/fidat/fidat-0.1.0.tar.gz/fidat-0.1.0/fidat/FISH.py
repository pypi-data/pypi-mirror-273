import pandas as pd
import numpy as np

def Fisher_Transform(high: pd.Series, low: pd.Series, period: int = 10, adjust: bool = True) -> pd.Series:
    """
    Calculates the Fisher Transform indicator from the given high and low price data.

    The Fisher Transform was presented by John Ehlers.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The period used in the calculation. Default is 10.
    adjust (bool): Whether to adjust the calculation. Default is True.

    Returns:
    pd.Series: A Series containing the Fisher Transform values.

    Example:
    # Assuming 'high' is a DataFrame with the high price data and 'low' is a DataFrame with the low price data
    fisher = Fisher_Transform(high, low, period=10, adjust=True)
    """

    # Calculate the typical price
    tp = (high + low) / 2

    # Calculate the highest high and lowest low over the period
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()

    # Calculate the range of the indicator
    range_value = highest_high - lowest_low

    # Calculate the normalized price
    normalized_price = 2 * ((tp - lowest_low) / range_value) - 1

    # Apply the Fisher Transform formula
    fisher = pd.Series(0.5 * np.log((1 + normalized_price) / (1 - normalized_price)))

    return fisher