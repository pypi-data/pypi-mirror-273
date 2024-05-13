import pandas as pd

def Gann_HiLo_Activator(high: pd.DataFrame, low: pd.DataFrame, period: int = 10) -> pd.DataFrame:
    """
    Calculates the Gann HiLo Activator.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high prices.
    low (pd.DataFrame): DataFrame containing the low prices.
    period (int): The period used to calculate the highest high and lowest low. Default is 10.

    Returns:
    pd.DataFrame: DataFrame containing the Gann HiLo Activator values.

    Example:
    # Assuming 'high' and 'low' are DataFrames containing the high and low prices respectively
    gann_hilo_activator = Gann_HiLo_Activator(high, low, period=10)
    """

    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    activator = (highest_high + lowest_low) / 2

    return activator