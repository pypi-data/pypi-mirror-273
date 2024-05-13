import pandas as pd

def Ultimate_Oscillator(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Ultimate Oscillator from the given close, high, and low price data.

    The Ultimate Oscillator is a technical analysis indicator used to measure momentum across three different timeframes.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the Ultimate Oscillator values.

    Example:
    # Assuming 'close', 'high', and 'low' are DataFrames with the close, high, and low price data
    ultimate_oscillator = Ultimate_Oscillator(close, high, low)
    """

    # Calculate True Range (TR)
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Calculate Buying Pressure (BP) and True Range Sum (TR_sum) for each period
    bp = close - low
    tr_sum = true_range.rolling(window=7).sum()

    # Calculate Raw Money Flow (RMF) for each period
    raw_money_flow = bp.rolling(window=7).sum()

    # Calculate Average True Range (ATR) for each period
    atr = true_range.rolling(window=7).mean()

    # Calculate Buying Pressure Divisor (BP_divisor) for each period
    bp_divisor = atr.rolling(window=14).sum()

    # Calculate Ultimate Oscillator (UO)
    uo = 100 * ((4 * raw_money_flow / bp_divisor) + (2 * raw_money_flow.rolling(window=14).sum() / bp_divisor.rolling(window=14).sum()) + (raw_money_flow.rolling(window=28).sum() / bp_divisor.rolling(window=28).sum())) / 7

    return uo