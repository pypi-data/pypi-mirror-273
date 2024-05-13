import pandas as pd

def True_Range(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the True Range (TR) indicator from the given price data.

    The True Range (TR) is the maximum of three price ranges:
    1. The current high minus the current low.
    2. The absolute value of the current high minus the previous close.
    3. The absolute value of the current low minus the previous close.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the True Range (TR) values.

    Example:
    # Assuming 'close', 'high', and 'low' are DataFrames with corresponding price data
    tr = TR(close, high, low)
    """

    # Calculate True Range
    range1 = high - low
    range2 = abs(high - close.shift())
    range3 = abs(low - close.shift())
    tr = pd.concat([range1, range2, range3], axis=1).max(axis=1)

    return tr