import pandas as pd

def Chandelier_Exit(high: pd.Series, low: pd.Series, short_period: int = 22, long_period: int = 22, k_period: int = 3) -> pd.Series:
    """
    Calculates the Chandelier Exit indicator from the given high and low price data.

    Chandelier Exit sets a trailing stop-loss based on the highest high or lowest low over a specified period, multiplied by a multiple (k).

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    short_period (int): The number of periods for the short Chandelier Exit. Default is 22.
    long_period (int): The number of periods for the long Chandelier Exit. Default is 22.
    k (int): The multiple to multiply the ATR by. Default is 3.

    Returns:
    pd.DataFrame: A DataFrame containing the short and long Chandelier Exit values.

    Example:
    # Assuming 'high' is a DataFrame with the high price data and 'low' is a DataFrame with the low price data
    chandelier_exit = Chandelier_Exit(high, low, short_period=22, long_period=22, k_period=3)
    """

    # Calculate the ATR for short and long periods
    atr_short = high.rolling(window=short_period).max() - high.rolling(window=short_period).min()
    atr_long = high.rolling(window=long_period).max() - high.rolling(window=long_period).min()

    # Calculate the short and long Chandelier Exit values
    chandelier_exit_short = high.rolling(window=short_period).max() - atr_short * k_period
    chandelier_exit_long = high.rolling(window=long_period).max() - atr_long * k_period

    # Combine the short and long Chandelier Exit values into a DataFrame
    chandelier_exit = pd.DataFrame({'Short Chandelier Exit': chandelier_exit_short, 'Long Chandelier Exit': chandelier_exit_long})

    return chandelier_exit