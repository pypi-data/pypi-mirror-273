import pandas as pd

def Volume_Adjusted_Moving_Average(close: pd.Series, volume: pd.Series, period: int = 8) -> pd.Series:
    """
    Calculate the Volume Adjusted Moving Average (VAMA) using separate DataFrames for closing prices and volume.

    Parameters:
    - close (pd.DataFrame): A DataFrame containing the closing prices with an appropriate datetime index.
    - volume (pd.DataFrame): A DataFrame containing the trading volumes, aligned with the 'close' DataFrame index.
    - period (int): The period over which to calculate the VAMA.

    Returns:
    - pd.Series: A Series containing the VAMA values.
    """
    # Calculate the volume-weighted prices
    volume_weighted_prices = close.squeeze() * volume.squeeze()
    
    # Sum of volume-weighted prices over the period
    sum_volume_weighted_prices = volume_weighted_prices.rolling(window=period).sum()
    
    # Sum of volumes over the period
    sum_volumes = volume.squeeze().rolling(window=period).sum()
    
    # VAMA is the ratio of these sums
    vama = sum_volume_weighted_prices / sum_volumes
    
    return vama