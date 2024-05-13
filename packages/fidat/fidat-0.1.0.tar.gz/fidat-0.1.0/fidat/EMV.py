import pandas as pd

def Ease_of_Movement(high: pd.Series, low: pd.Series, volume: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Ease of Movement (EMV) indicator from the given high, low, and volume data.

    Ease of Movement (EMV) measures the relationship between volume and price change to assess the strength of a trend.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    period (int): The number of periods to use in the calculation.

    Returns:
    pd.Series: A Series containing the Ease of Movement (EMV) values.

    Example:
    # Assuming 'high' is a DataFrame with the high price data, 'low' is a DataFrame with the low price data,
    # and 'volume' is a DataFrame with the volume data
    emv = Ease_of_Movement(high, low, volume, period=14)
    """

    # Calculate Box Ratio
    typical_price = (high + low) / 2
    box_ratio = ((high.diff() - low.diff()) / (high - low)).fillna(0)

    # Calculate EMV
    emv = box_ratio * (typical_price.diff() / volume)

    # Smooth EMV with a moving average
    emv_smoothed = emv.rolling(window=period, min_periods=1).mean()

    return emv_smoothed