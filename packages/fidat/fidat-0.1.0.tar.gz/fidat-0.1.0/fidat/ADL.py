import pandas as pd

def Accumulation_Distribution_Line(close: pd.Series, high: pd.Series, low: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculates the Accumulation/Distribution Line from the given price and volume data.

    The Accumulation/Distribution Line is a cumulative indicator that measures the flow of money into or out of a security.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    volume (pd.DataFrame): DataFrame containing the volume data.

    Returns:
    pd.Series: A Series containing the Accumulation/Distribution Line values.

    Example:
    # Assuming 'close', 'high', 'low', and 'volume' are DataFrames with the close, high, low, and volume data
    adl = Accumulation_Distribution_Line(close, high, low, volume)
    """

    # Calculate Money Flow Multiplier (MF Multiplier)
    mf_multiplier = ((close - low) - (high - close)) / (high - low)
    
    # Calculate Money Flow Volume (MF Volume)
    mf_volume = mf_multiplier * volume
    
    # Calculate Accumulation/Distribution Line (ADL)
    adl = mf_volume.cumsum()
    
    return adl