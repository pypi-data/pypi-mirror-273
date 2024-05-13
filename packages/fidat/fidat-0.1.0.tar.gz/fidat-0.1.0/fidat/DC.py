import pandas as pd

def Donchian_Channels(high: pd.DataFrame, low: pd.DataFrame, upper_period: int = 20, lower_period: int = 5) -> pd.DataFrame:
    """
    Calculates the Donchian Channels.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high prices.
    low (pd.DataFrame): DataFrame containing the low prices.
    upper_period (int): The period for the upper channel. Default is 20.
    lower_period (int): The period for the lower channel. Default is 5.

    Returns:
    pd.DataFrame: DataFrame containing the upper and lower Donchian Channels.

    Example:
    # Assuming 'high' and 'low' are DataFrames containing high and low prices
    donchian_channels = Donchian_Channels(high, low, upper_period=20, lower_period=5)
    """

    upper_channel = high.rolling(window=upper_period).max()
    lower_channel = low.rolling(window=lower_period).min()

    return pd.concat([upper_channel, lower_channel], axis=1, keys=['Upper Channel', 'Lower Channel'])
