import pandas as pd

def Money_Flow_Index(close: pd.Series, high: pd.Series, low: pd.Series, volume: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Money Flow Index (MFI) from the given price and volume data.

    The Money Flow Index (MFI) is a momentum oscillator that measures the strength of money flowing in and out of a security.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    period (int): The number of periods to use in the calculation.

    Returns:
    pd.Series: A Series containing the Money Flow Index (MFI) values.

    Example:
    # Assuming 'close', 'high', 'low', and 'volume' are DataFrames with the close, high, low, and volume data
    mfi = money_flow_index(close, high, low, volume, period=14)
    """

    # Calculate Typical Price
    typical_price = (high + low + close) / 3

    # Calculate Money Flow
    money_flow = typical_price * volume

    # Calculate Positive Money Flow and Negative Money Flow
    positive_money_flow = money_flow * (typical_price > typical_price.shift(1))
    negative_money_flow = money_flow * (typical_price < typical_price.shift(1))

    # Calculate Money Flow Ratio (MFR)
    positive_money_flow_sum = positive_money_flow.rolling(window=period).sum()
    negative_money_flow_sum = negative_money_flow.rolling(window=period).sum()
    money_flow_ratio = positive_money_flow_sum / negative_money_flow_sum

    # Calculate Money Flow Index (MFI)
    mfi = 100 - (100 / (1 + money_flow_ratio))

    return mfi