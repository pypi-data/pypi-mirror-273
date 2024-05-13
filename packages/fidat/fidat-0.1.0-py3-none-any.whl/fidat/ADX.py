import pandas as pd

def Trend_Strength_Indicator(high: pd.Series, low: pd.Series, period: int = 14, adjust: bool = True) -> pd.Series:
    """
    Calculates the Trend Strength Indicator (ADX) from the given high and low price data.

    The Trend Strength Indicator (ADX) measures the strength of a price trend.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods for calculating the ADX.
    adjust (bool): Whether to adjust for splits and dividends.

    Returns:
    pd.Series: A Series containing the Trend Strength Indicator (ADX) values.

    Example:
    # Assuming 'high' and 'low' are DataFrames with the high and low price data
    adx = Trend_Strength_Indicator(high, low, period=14)
    """

    # Calculate True Range (TR)
    tr = pd.DataFrame(index=high.index)
    tr['TR1'] = high - low
    tr['TR2'] = (high - high.shift(1)).abs()
    tr['TR3'] = (low - low.shift(1)).abs()
    tr['TR'] = tr[['TR1', 'TR2', 'TR3']].max(axis=1)

    # Calculate Plus Directional Movement (+DM) and Minus Directional Movement (-DM)
    dm_plus = high.diff()
    dm_minus = -low.diff()
    dm_plus[dm_plus < 0] = 0
    dm_minus[dm_minus < 0] = 0

    # Calculate Smoothed Plus Directional Movement (Smoothed +DM) and Smoothed Minus Directional Movement (Smoothed -DM)
    smooth_dm_plus = dm_plus.rolling(window=period).mean()
    smooth_dm_minus = dm_minus.rolling(window=period).mean()

    # Calculate Positive Directional Index (+DI) and Negative Directional Index (-DI)
    di_plus = (smooth_dm_plus / tr['TR']) * 100
    di_minus = (smooth_dm_minus / tr['TR']) * 100

    # Calculate Directional Movement Index (DX)
    dx = ((di_plus - di_minus).abs() / (di_plus + di_minus)) * 100

    # Calculate ADX (Smoothed Moving Average of DX)
    adx = dx.rolling(window=period).mean()

    return adx