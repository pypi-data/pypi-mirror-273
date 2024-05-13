import pandas as pd

def Elder_Ray_Index(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.DataFrame:
    """
    Elder-Ray Index (Elder Ray)
    """
    bull_power = high - pd.Series(close.shift(1).rolling(window=13).max(), index=close.index)
    bear_power = pd.Series(close.shift(1).rolling(window=13).min(), index=close.index) - low

    return pd.DataFrame({'Bull Power': bull_power, 'Bear Power': bear_power})