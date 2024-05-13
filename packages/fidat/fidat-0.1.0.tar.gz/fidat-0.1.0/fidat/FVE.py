import pandas as pd

def Finite_Volume_Elements(close: pd.Series, high: pd.Series, low: pd.Series, volume: pd.Series, period: int = 22, factor: float = 0.3) -> pd.Series:
    """
    Calculates the Finite Volume Elements (FVE) indicator from the given close, high, low, and volume data.

    The Finite Volume Elements (FVE) indicator is a volume-based indicator that helps identify the strength of price trends.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    period (int): The period used in the calculation. Default is 22.
    factor (float): The factor used to calculate the Finite Volume Elements (FVE) values. Default is 0.3.

    Returns:
    pd.Series: A Series containing the Finite Volume Elements (FVE) values.

    Example:
    # Assuming 'close', 'high', 'low', and 'volume' are DataFrames with the required data
    fve = Finite_Volume_Elements(close, high, low, volume, period=22, factor=0.3)
    """

    # Calculate the typical price
    typical_price = (high + low + close) / 3

    # Calculate the volume-based cumulative sum
    volume_sum = volume.cumsum()

    # Calculate the Finite Volume Elements (FVE)
    fve = typical_price * (volume_sum - volume_sum.shift(period)) / (volume_sum.shift(period) * factor)

    return fve