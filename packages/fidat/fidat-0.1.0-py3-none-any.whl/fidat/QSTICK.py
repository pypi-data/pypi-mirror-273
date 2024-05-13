import pandas as pd

def QStick(open: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """
    QStick indicator shows the dominance of black (down) or white (up) candlesticks, which are red and green in Chart,
    as represented by the average open to close change for each of past N days.

    Parameters:
    ohlc (pd.DataFrame): DataFrame containing open, high, low, and close price data.
    period (int): The number of periods to use in the calculation. Default is 14.

    Returns:
    pd.Series: A Series containing the QStick values.

    Example:
    # Assuming 'ohlc' is a DataFrame with OHLC data
    qstick = QSTICK(ohlc, period=14)
    """

    _close = close.tail(period)
    _open = open.tail(period)

    return (_close - _open) / period