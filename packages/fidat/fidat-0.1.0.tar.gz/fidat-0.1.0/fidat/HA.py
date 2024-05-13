import pandas as pd

def Heikin_Ashi(open: pd.DataFrame, close: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame) -> pd.Series:
    """
    Calculate Heikin-Ashi candles.

    Parameters:
    open (pd.DataFrame): DataFrame containing open prices.
    close (pd.DataFrame): DataFrame containing close prices.
    high (pd.DataFrame): DataFrame containing high prices.
    low (pd.DataFrame): DataFrame containing low prices.

    Returns:
    pd.Series: Series with Heikin-Ashi candles.
    """
    ha_close = (open + close + high + low) / 4
    ha_open = (ha_close.shift(1) + ha_close.shift(2) + ha_close.shift(3) + ha_close.shift(4)) / 4
    ha_high = pd.concat([ha_open, ha_close, high], axis=1).max(axis=1)
    ha_low = pd.concat([ha_open, ha_close, low], axis=1).min(axis=1)
    return pd.concat([ha_open, ha_high, ha_low, ha_close], axis=1, keys=['HA_Open', 'HA_High', 'HA_Low', 'HA_Close'])
