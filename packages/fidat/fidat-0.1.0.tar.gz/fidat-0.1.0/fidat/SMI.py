import pandas as pd

def CT_Reverse_Stochastic_Momentum_Index(close: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    CT Reverse Stochastic Momentum Index (SMI)
    """
    # Define the typical price
    tp = (high + low + close) / 3
    
    # Calculate the 14-period highest high and lowest low
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    
    # Calculate the raw Stochastic Momentum Index (SMI)
    raw_smi = (tp - (highest_high + lowest_low) / 2) / ((highest_high - lowest_low) / 2)
    
    # Calculate the smoothed SMI
    smoothed_smi = raw_smi.rolling(window=3).mean()
    
    return smoothed_smi