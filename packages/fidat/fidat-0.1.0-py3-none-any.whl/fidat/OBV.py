import pandas as pd
import numpy as np

def On_Balance_Volume(data: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculates the On Balance Volume (OBV) indicator from the given price and volume data.

    The On Balance Volume (OBV) is a cumulative indicator that adds volume on up days and subtracts volume on down days.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    volume (pd.DataFrame): DataFrame containing the volume data.

    Returns:
    pd.Series: A Series containing the On Balance Volume (OBV) values.

    Example:
    # Assuming 'data' is a DataFrame with the price data and 'volume' is a DataFrame with the volume data
    obv = On_Balance_Volume(data, volume)
    """

    # Calculate direction of price movement
    direction = data.diff().fillna(0)
    signs = np.where(direction > 0, 1, np.where(direction < 0, -1, 0))

    # Calculate On Balance Volume (OBV)
    obv = volume * signs
    obv = obv.cumsum()

    return obv