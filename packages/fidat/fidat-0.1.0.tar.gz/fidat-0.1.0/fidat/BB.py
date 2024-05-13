import pandas as pd

def Bollinger_Bands(data: pd.Series, period: int = 20, MA: pd.Series = None, std_multiplier: float = 2) -> pd.Series:
    """
    Calculates the Bollinger Bands (BBANDS) indicator from the given price data.

    Bollinger Bands consist of three lines:
    1. The middle line (MA): typically a simple moving average (SMA) over a specified period.
    2. The upper band: MA + (standard deviation * std_multiplier)
    3. The lower band: MA - (standard deviation * std_multiplier)

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods for calculating the moving average.
    MA (pd.Series): Optional pre-calculated moving average. If not provided, it will be calculated from 'data'.
    std_multiplier (float): The multiplier for the standard deviation.

    Returns:
    pd.DataFrame: A DataFrame containing the Bollinger Bands (upper band, middle band, lower band).

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the BBANDS for
    bollinger_bands = BBANDS(data['Close'], period=20, std_multiplier=2)
    """

    # Calculate moving average if not provided
    if MA is None:
        MA = data.rolling(window=period).mean()

    # Calculate standard deviation
    std = data.rolling(window=period).std()

    # Calculate upper and lower bands
    upper_band = MA + std * std_multiplier
    lower_band = MA - std * std_multiplier

    # Combine into DataFrame
    bollinger_bands = pd.concat([upper_band, MA, lower_band], axis=1)
    bollinger_bands.columns = ['Upper Band', 'Middle Band', 'Lower Band']

    return bollinger_bands