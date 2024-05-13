import pandas as pd

def Accumulative_Swing_Index(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculate the Accumulative Swing Index (ASI) for a given series of closing, high, and low prices.
    
    Parameters:
        close (pd.Series): Series of closing prices.
        high (pd.Series): Series of high prices.
        low (pd.Series): Series of low prices.
        
    Returns:
        pd.Series: Series containing the Accumulative Swing Index values.
    """
    si = 0.0
    asi_values = []

    for i in range(1, len(close)):
        move_range = max(high.iloc[i] - close.iloc[i - 1], close.iloc[i - 1] - low.iloc[i])
        rs = (close.iloc[i] - close.iloc[i - 1]) - 0.5 * (close.iloc[i] - close.iloc[i - 1 - 1]) + 0.25 * (close.iloc[i] - close.iloc[i - 1 - 2])
        si += rs * move_range
        asi_values.append(si)
    
    asi_series = pd.Series(asi_values, index=close.index[1:])
    return asi_series