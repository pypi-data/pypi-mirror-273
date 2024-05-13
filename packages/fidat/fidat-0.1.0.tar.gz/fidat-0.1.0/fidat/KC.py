import pandas as pd

def Keltner_Channels(data: pd.Series, period: int = 20, atr_period: int = 10, MA: pd.Series = None, kc_mult: float = 2) -> pd.Series:
    """
    Calculates the Keltner Channels (KC) indicator from the given price data.

    Keltner Channels (KC) are volatility-based envelopes set above and below an exponential moving average (EMA).
    The width of the channels is based on the Average True Range (ATR).

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods for calculating the moving average.
    atr_period (int): The number of periods for calculating the Average True Range (ATR).
    MA (pd.Series): Optional pre-calculated moving average. If not provided, it will be calculated from 'data'.
    kc_mult (float): The multiplier for the Average True Range (ATR).

    Returns:
    pd.DataFrame: A DataFrame containing the Keltner Channels (upper band, middle band, lower band).

    Example:
    # Assuming 'data' is a DataFrame with the price data
    keltner_channels = Keltner_Channels(data, period=20, atr_period=10, kc_mult=2)
    """

    # Calculate moving average if not provided
    if MA is None:
        MA = data.ewm(span=period, adjust=False).mean()

    # Calculate Average True Range (ATR)
    atr = data.diff().abs().ewm(span=atr_period, adjust=False).mean()

    # Calculate upper and lower bands
    upper_band = MA + (atr * kc_mult)
    lower_band = MA - (atr * kc_mult)

    # Combine into DataFrame
    keltner_channels = pd.concat([upper_band, MA, lower_band], axis=1)
    keltner_channels.columns = ['Upper Band', 'Middle Band', 'Lower Band']

    return keltner_channels