import pandas as pd

def Zero_Cross_Indicator(data: pd.Series) -> pd.Series:
    """
    Calculates the Zero-Cross Indicator, which identifies points where the
    values of a time series data cross zero. This indicator is useful for
    spotting changes in the direction of a time series, suggesting potential
    buy or sell opportunities based on the direction of the crossing.

    Parameters:
    data (pd.Series): A Pandas Series representing the time series data.

    Returns:
    pd.Series: A Pandas Series containing the indicator signals. It returns `1` for
               a cross above zero (buy signal), `-1` for a cross below zero (sell signal),
               and `0` for no crossing (no signal).

    The function returns a series of the same length as the input minus one,
    as the first data point cannot have a previous point to compare with.
    """
    
    # Initialize an empty list to store the signals
    signals = []

    # Iterate over the data
    for i in range(1, len(data)):
        # If the current value crosses above zero and the previous value was below zero
        if data.iloc[i] > 0 and data.iloc[i - 1] <= 0:
            signals.append(1)  # Buy signal
        # If the current value crosses below zero and the previous value was above zero
        elif data.iloc[i] < 0 and data.iloc[i - 1] >= 0:
            signals.append(-1)  # Sell signal
        else:
            signals.append(0)  # No signal

    return pd.Series(signals, index=data.index[1:])