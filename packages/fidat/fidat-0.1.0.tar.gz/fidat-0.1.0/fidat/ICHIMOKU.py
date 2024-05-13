import pandas as pd

def Ichimoku_Cloud(close: pd.Series, high: pd.Series, low: pd.Series, tenkan_period: int = 9, kijun_period: int = 26, senkou_period: int = 52, chikou_period: int = 26) -> pd.Series:
    """
    Calculates the Ichimoku Cloud indicator from the given close, high, and low price data.

    The Ichimoku Cloud, also known as Ichimoku Kinko Hyo, is a versatile indicator that provides information about support and resistance levels, trend direction, and momentum.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    tenkan_period (int): The period used to calculate the Tenkan-sen (Conversion Line). Default is 9.
    kijun_period (int): The period used to calculate the Kijun-sen (Base Line). Default is 26.
    senkou_period (int): The period used to calculate the Senkou Span A and Senkou Span B. Default is 52.
    chikou_period (int): The period used to calculate the Chikou Span (Lagging Span). Default is 26.

    Returns:
    pd.DataFrame: A DataFrame containing the Ichimoku Cloud values.

    Example:
    # Assuming 'close' is a DataFrame with the close price data, 'high' is a DataFrame with the high price data, and 'low' is a DataFrame with the low price data
    ichimoku_cloud = Ichimoku_Cloud(close, high, low, tenkan_period=9, kijun_period=26, senkou_period=52, chikou_period=26)
    """

    # Calculate the Tenkan-sen (Conversion Line)
    tenkan_sen = (high.rolling(window=tenkan_period).max() + low.rolling(window=tenkan_period).min()) / 2

    # Calculate the Kijun-sen (Base Line)
    kijun_sen = (high.rolling(window=kijun_period).max() + low.rolling(window=kijun_period).min()) / 2

    # Calculate the Senkou Span A
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(senkou_period)

    # Calculate the Senkou Span B
    senkou_span_b = ((high.rolling(window=senkou_period).max() + low.rolling(window=senkou_period).min()) / 2).shift(senkou_period)

    # Calculate the Chikou Span (Lagging Span)
    chikou_span = close.shift(-chikou_period)

    # Create a DataFrame to store the Ichimoku Cloud values
    ichimoku_cloud = pd.DataFrame({
        'Tenkan-sen': tenkan_sen,
        'Kijun-sen': kijun_sen,
        'Senkou Span A': senkou_span_a,
        'Senkou Span B': senkou_span_b,
        'Chikou Span': chikou_span
    })

    return ichimoku_cloud