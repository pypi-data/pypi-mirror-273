import pandas as pd

def Volume_Oscillator(volume: pd.Series, short_period: int = 12, long_period: int = 26) -> pd.Series:
    """
    Calculate the Volume Oscillator.

    Parameters:
    volume (pd.Series): Series containing the volume data.
    short_period (int): Short period for the Volume Oscillator. Default is 12.
    long_period (int): Long period for the Volume Oscillator. Default is 26.

    Returns:
    pd.Series: Series containing the Volume Oscillator values.

    Example:
    # Assuming 'volume' is a Series containing volume data
    volume_oscillator_values = volume_oscillator(volume)
    """

    short_ma = volume.rolling(window=short_period).mean()
    long_ma = volume.rolling(window=long_period).mean()

    volume_oscillator_values = short_ma - long_ma

    return volume_oscillator_values