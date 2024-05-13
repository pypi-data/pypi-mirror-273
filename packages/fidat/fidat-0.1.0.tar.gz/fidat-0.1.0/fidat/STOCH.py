import pandas as pd

def Stochastic_Oscillator(high: pd.Series, low: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Stochastic Oscillator (%K) from the given high and low price data.

    The Stochastic Oscillator (%K) is a momentum indicator that compares a security's closing price
    to its price range over a given time period.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods for calculating the Stochastic Oscillator (%K).

    Returns:
    pd.Series: A Series containing the Stochastic Oscillator (%K) values.

    Example:
    # Assuming 'high' and 'low' are DataFrames with the high and low price data
    stochastic_k = Stochastic_Oscillator(high, low, period=14)
    """

    # Calculate %K
    lowest_low = low.rolling(window=period).min()
    highest_high = high.rolling(window=period).max()
    stochastic_k = 100 * ((high - lowest_low) / (highest_high - lowest_low))

    return stochastic_k