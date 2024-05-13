import pandas as pd

def Volume_Profile(close: pd.DataFrame, volume: pd.DataFrame, period: int = 30) -> pd.Series:
    """
    Calculate Volume Profile.

    Parameters:
    close (pd.DataFrame): Close prices.
    volume (pd.DataFrame): Volume data.
    period (int): Number of periods to consider.

    Returns:
    pd.Series: Volume profile data.
    """

    # Combine close prices and volume
    data = pd.concat([close, volume], axis=1)

    # Calculate the range of prices
    price_range = close.max() - close.min()

    # Calculate the price increment
    price_increment = price_range / period

    # Create empty Series for volume profile
    volume_profile = pd.Series(index=close.index, dtype=float)

    # Loop over each period
    for i in range(period):
        # Calculate the lower and upper bounds of the current price range
        lower_bound = close.min() + i * price_increment
        upper_bound = lower_bound + price_increment

        # Filter data within the current price range
        data_within_range = data[(data['close'] >= lower_bound) & (data['close'] < upper_bound)]

        # Calculate total volume within the price range
        total_volume = data_within_range['volume'].sum()

        # Assign the total volume to the volume profile Series
        volume_profile.loc[data_within_range.index] = total_volume

    return volume_profile