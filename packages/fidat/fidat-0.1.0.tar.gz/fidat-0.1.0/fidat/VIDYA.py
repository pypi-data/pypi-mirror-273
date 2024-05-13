import pandas as pd
import numpy as np

def Variable_Index_Dynamic_Average(close: pd.Series, period: int = 9, smoothing_period: int = 12) -> pd.Series:
    """
    Calculate the Variable Index Dynamic Average (VIDYA) indicator using the closing prices.

    Parameters:
    - data (pd.Series): Prefer Close. A Series containing the closing prices.
    - period (int): The period for the used to determine volatility.
    - smoothing_period (int): The period for smoothing the VIDYA calculation, used as the span in EMA calculation.

    Returns:
    - pd.Series: A Series containing the VIDYA values.
    """

    # Calculate the Chande Momentum Oscillator (CMO)
    delta = close.diff()
    up = delta.where(delta > 0, 0)
    down = -delta.where(delta < 0, 0)
    sum_up = up.rolling(window=period).sum()
    sum_down = down.rolling(window=period).sum()
    cmo = (sum_up - sum_down) / (sum_up + sum_down).replace(0, np.nan) * 100
    
    # Using the absolute value of the CMO as alpha
    alpha = abs(cmo / 100)
    
    # Calculate the exponential moving average with dynamic smoothing
    # Adjusted alpha for each point
    smoothed_alpha = alpha / smoothing_period
    
    # Initialize VIDYA Series with NaNs
    VIDYA = pd.Series(index=close.index, dtype=float)
    
    # Start calculating VIDYA using the formula with dynamic alpha
    for i in range(len(close)):
        if i == 0:
            VIDYA.iloc[i] = close.iloc[i]  # Starting point for the EMA
        else:
            VIDYA.iloc[i] = (smoothed_alpha.iloc[i] * close.iloc[i]) + ((1 - smoothed_alpha.iloc[i]) * VIDYA.iloc[i - 1])
    
    return VIDYA
