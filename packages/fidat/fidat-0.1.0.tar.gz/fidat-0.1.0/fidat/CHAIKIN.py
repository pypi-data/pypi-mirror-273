import pandas as pd

def Chaikin_Oscillator(close: pd.Series, high: pd.Series, low: pd.Series, volume: pd.Series, adjust: bool = True) -> pd.Series:
    """
    Calculates the Chaikin Oscillator from the given price and volume data.

    The Chaikin Oscillator is a momentum indicator that combines price and volume data to determine bullish or bearish trends.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    adjust (bool): Whether to adjust the exponential moving averages.

    Returns:
    pd.Series: A Series containing the Chaikin Oscillator values.

    Example:
    # Assuming 'close', 'high', 'low', and 'volume' are DataFrames with the close, high, low, and volume data
    chaikin_oscillator = Chaikin_Oscillator(close, high, low, volume, adjust=True)
    """

    # Calculate Money Flow Multiplier (MF Multiplier)
    mf_multiplier = ((close - low) - (high - close)) / (high - low)
    
    # Calculate Money Flow Volume (MF Volume)
    mf_volume = mf_multiplier * volume
    
    # Calculate Accumulation/Distribution Line (ADL)
    adl = mf_volume.cumsum()
    
    # Calculate Chaikin Oscillator as the difference between 3-day and 10-day EMA of ADL
    ema_3 = adl.ewm(span=3, adjust=adjust).mean()
    ema_10 = adl.ewm(span=10, adjust=adjust).mean()
    chaikin_oscillator = ema_3 - ema_10
    
    return chaikin_oscillator