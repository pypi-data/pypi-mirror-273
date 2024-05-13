import pandas as pd

def True_Strength_Index(data: pd.Series, long: int = 25, short: int = 13, signal: int = 13, adjust: bool = True) -> pd.Series:
    """
    Calculates the True Strength Index (TSI) indicator from the given price data.

    The True Strength Index (TSI) is a momentum oscillator that measures the strength of a security's trend over a specified period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    long (int): The number of periods for the long-term EMA calculation.
    short (int): The number of periods for the short-term EMA calculation.
    signal (int): The number of periods for the signal line EMA calculation.
    adjust (bool): Whether to adjust the exponential moving averages.

    Returns:
    pd.DataFrame: A DataFrame containing the True Strength Index (TSI) values and signal line.

    Example:
    # Assuming 'data' is a DataFrame with the price data
    tsi = True_Strength_Index(data, long=25, short=13, signal=13, adjust=True)
    """

    # Calculate Double Smoothed Price (DSP)
    dsp_long = data.ewm(span=long, adjust=adjust).mean()
    dsp_short = dsp_long.ewm(span=short, adjust=adjust).mean()

    # Calculate Price Rate of Change (ROC)
    roc = (data - data.shift(1)).fillna(0)

    # Calculate Double Smoothed ROC (DSROC)
    dsroc_long = roc.ewm(span=long, adjust=adjust).mean()
    dsroc_short = dsroc_long.ewm(span=short, adjust=adjust).mean()

    # Calculate True Strength Index (TSI)
    tsi = 100 * (dsroc_short / dsp_short)

    # Calculate Signal Line (EMA of TSI)
    signal_line = tsi.ewm(span=signal, adjust=adjust).mean()

    return pd.DataFrame({"TSI": tsi, "Signal Line": signal_line})