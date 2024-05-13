import pandas as pd

def Weighted_On_Balance_Volume(data: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculates the Weighted On Balance Volume (OBV) indicator from the given price data.

    The Weighted On Balance Volume (OBV) is a variation of the traditional OBV that takes into account the price change as well as the volume.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.

    Returns:
    pd.Series: A Series containing the Weighted On Balance Volume (OBV) values.

    Example:
    # Assuming 'data' is a DataFrame with the price data
    obv = Weighted_OBV(data)
    """

# and -1 if it decreased.
    direction = data.diff().apply(lambda x: 1 if x >= 0 else -1)

    # Calculate Weighted On Balance Volume (WOBV)
    weighted_obv = direction * data.diff().abs() * volume
    weighted_obv = weighted_obv.cumsum()

    return weighted_obv