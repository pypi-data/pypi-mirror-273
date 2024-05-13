import pandas as pd

def Coppock_Curve(data: pd.Series, adjust: bool = True) -> pd.Series:
    """
    Calculates the Coppock Curve indicator from the given data.

    The Coppock Curve is a momentum indicator that signals buying opportunities when the indicator moves from negative territory to positive territory.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.
    adjust (bool): Whether to adjust the exponential moving averages. Default is True.

    Returns:
    pd.Series: A Series containing the Coppock Curve values.

    Example:
    # Assuming 'data' is a DataFrame with the data
    coppock_curve = Coppock_Curve(data, adjust=True)
    """

    # Calculate the rate of change for a given period
    roc = data.pct_change()

    # Define the long period (usually 14 periods)
    long_period = 14

    # Calculate the 14-period rate of change
    roc_14 = roc.rolling(window=long_period).sum()

    # Calculate the short period (usually 11 periods)
    short_period = 11

    # Calculate the 11-period rate of change
    roc_11 = roc.rolling(window=short_period).sum()

    # Calculate the Coppock Curve as the sum of the 14-period and 11-period rate of change
    coppock_curve = roc_11 + roc_14

    return coppock_curve
