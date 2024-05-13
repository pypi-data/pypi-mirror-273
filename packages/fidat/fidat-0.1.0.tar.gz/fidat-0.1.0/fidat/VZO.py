import pandas as pd

def Volume_Zone_Oscillator(data: pd.Series, volume: pd.Series, period: int = 14, adjust: bool = True) -> pd.Series:
    """
    Calculates the Volume Zone Oscillator (VZO) indicator from the given price and volume data.

    The Volume Zone Oscillator (VZO) is a momentum oscillator that measures the positive and negative volume flows over a specified period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    period (int): The number of periods to use in the calculation.
    adjust (bool): Whether to adjust the exponential moving averages.

    Returns:
    pd.Series: A Series containing the Volume Zone Oscillator (VZO) values.

    Example:
    # Assuming 'data' is a DataFrame with the price data and 'volume' is a DataFrame with the volume data
    vzo = Volume_Zone_Oscillator(data, volume, period=14, adjust=True)
    """

    # Calculate Up and Down Volume
    up_volume = (data.diff() > 0).astype(float) * volume
    down_volume = (data.diff() < 0).astype(float) * volume

    # Calculate Positive and Negative Volume Sum
    positive_volume_sum = up_volume.rolling(window=period, min_periods=1).sum()
    negative_volume_sum = down_volume.rolling(window=period, min_periods=1).sum()

    # Calculate Volume Zone Oscillator (VZO)
    vzo = 100 * (positive_volume_sum - negative_volume_sum) / (positive_volume_sum + negative_volume_sum)

    return vzo