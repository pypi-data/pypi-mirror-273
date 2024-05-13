import pandas as pd

def Relative_Strength_Index(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Relative Strength Index (RSI) of the given pandas Series.

    RSI compares the magnitude of recent gains to recent losses in an attempt to determine overbought and oversold conditions of an asset.

    Args:
        data (pd.Series): A pandas Series for which the RSI is calculated.
        period (int): The number of periods over which to calculate the RSI. Traditionally, 14 periods are used.

    Returns:
        pd.Series: A pandas Series containing the RSI values.
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    # Calculate the exponential moving averages (EMA) of gains and losses
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Use the EMAs to calculate the Relative Strength (RS)
    RS = avg_gain / avg_loss

    # Calculate the RSI
    RSI = 100 - (100 / (1 + RS))

    return RSI