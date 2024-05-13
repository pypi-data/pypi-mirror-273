import pandas as pd

def Volume_Flow_Indicator(close: pd.Series, high: pd.Series, low: pd.Series, volume: pd.Series, long_period: int = 10,
                          smoothing_factor: int = 3, factor: float = 0.2, vfactor: float = 2.5, adjust: bool = True) -> pd.Series:
    """
    Calculates the Volume Flow Indicator (VFI) from the given close, high, low, and volume data.

    The Volume Flow Indicator (VFI) attempts to measure the strength of price movement by comparing the relationship between price change and volume.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    period (int): The period used in the calculation. Default is 130.
    smoothing_factor (int): The smoothing factor used in the calculation. Default is 3.
    factor (float): The factor used to adjust the volume. Default is 0.2.
    vfactor (float): The volume factor used in the calculation. Default is 2.5.
    adjust (bool): Whether to adjust the indicator. Default is True.

    Returns:
    pd.Series: A Series containing the Volume Flow Indicator (VFI) values.

    Example:
    # Assuming 'close', 'high', 'low', and 'volume' are DataFrames with the required data
    vfi = Volume_Flow_Indicator(close, high, low, volume, period=130, smoothing_factor=3, factor=0.2, vfactor=2.5, adjust=True)
    """

    # Calculate the typical price
    typical_price = (high + low + close) / 3

    # Calculate the volume force
    volume_force = volume * (typical_price - typical_price.shift(1))

    # Apply smoothing
    volume_flow_indicator = volume_force.rolling(window=long_period).sum() / volume.rolling(window=long_period).sum()

    # Adjust the indicator
    if adjust:
        volume_flow_indicator *= factor / vfactor
        volume_flow_indicator = volume_flow_indicator.ewm(span=smoothing_factor, adjust=adjust).mean()

    return volume_flow_indicator