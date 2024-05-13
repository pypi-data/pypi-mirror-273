import pandas as pd

def Stochastic_Oscillator_Moving_Average(high: pd.Series, low: pd.Series, period: int = 3, stoch_period: int = 14) -> pd.Series:
    """
    Calculates the Stochastic Oscillator (%D) from the given high and low price data.

    The Stochastic Oscillator (%D) is a 3 period simple moving average of %K.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods for calculating the simple moving average.
    stoch_period (int): The number of periods for calculating the Stochastic Oscillator (%K).

    Returns:
    pd.Series: A Series containing the Stochastic Oscillator (%D) values.

    Example:
    # Assuming 'high' and 'low' are DataFrames with the high and low price data
    stochastic_d = Stochastic_Oscillator_Moving_Average(high, low, period=3, stoch_period=14)
    """

    # Calculate %K
    lowest_low = low.rolling(window=stoch_period).min()
    highest_high = high.rolling(window=stoch_period).max()
    stochastic_k = 100 * ((high - lowest_low) / (highest_high - lowest_low))

    # Calculate %D (simple moving average of %K)
    stochastic_d = stochastic_k.rolling(window=period).mean()

    return stochastic_d