import pandas as pd

def Wave_Trend_Oscillator(close: pd.Series, high: pd.Series, low: pd.Series, channel_length: int = 10, average_length: int = 21, adjust: bool = True) -> pd.Series:
    """
    Calculates the Wave Trend Oscillator (WTO) from the given close, high, and low price data.

    The Wave Trend Oscillator (WTO) is a trend-following indicator that attempts to capture the underlying trend by combining short-term and long-term moving averages with a leading indicator.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    channel_length (int): The length of the channel used in the calculation. Default is 10.
    average_length (int): The length of the moving average used in the calculation. Default is 21.
    adjust (bool): Whether to adjust the calculation for gaps. Default is True.

    Returns:
    pd.DataFrame: A DataFrame containing the Wave Trend Oscillator (WTO) values.

    Example:
    # Assuming 'close' is a DataFrame with the close price data, 'high' is a DataFrame with the high price data, and 'low' is a DataFrame with the low price data
    wto = Wave_Trend_Oscillator(close, high, low, channel_length=10, average_length=21, adjust=True)
    """

    # Calculate True Price
    tp = (high + low + close) / 3

    # Calculate the Exponential Moving Average (ESA)
    esa = tp.ewm(span=average_length, adjust=adjust).mean()

    # Calculate the D component
    d = (tp - esa).abs().ewm(span=channel_length, adjust=adjust).mean()

    # Calculate the Chande Momentum Oscillator (CI)
    ci = (tp - esa) / (0.015 * d)

    # Calculate the Wave Trend Oscillator (WTO)
    wt1 = ci.ewm(span=average_length, adjust=adjust).mean()
    wt2 = wt1.rolling(window=4).mean()

    return pd.DataFrame({'Wave_Trend1': wt1, 'Wave_Trend2': wt2})
