import pandas as pd

def Market_Facilitation_Index(high: pd.Series, low: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Calculate the Market Facilitation Index (MFI).

    Parameters:
    high (pd.Series): Series containing the high prices.
    low (pd.Series): Series containing the low prices.
    volume (pd.Series): Series containing the trading volume.

    Returns:
    pd.Series: Series containing the Market Facilitation Index (MFI) values.

    Example:
    # Assuming 'high', 'low', and 'volume' are Series containing the respective data
    mfi_values = market_facilitation_index(high, low, volume)
    """

    typical_price = (high + low) / 2
    raw_mfi = typical_price * volume
    mfi_values = raw_mfi.diff()

    return mfi_values