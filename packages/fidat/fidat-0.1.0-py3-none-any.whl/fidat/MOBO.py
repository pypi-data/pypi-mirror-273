import pandas as pd

def Modified_Bollinger_Bands(data: pd.Series, period: int = 10, std_multiplier: float = 0.8) -> pd.Series:
    """
    Calculates the Modified Bollinger Bands (MOBO) indicator from the given price data.

    MOBO bands are based on a zone of 0.80 standard deviation with a 10-period look-back.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods for calculating the moving average and standard deviation.
    std_multiplier (float): The multiplier for the standard deviation.

    Returns:
    pd.DataFrame: A DataFrame containing the MOBO bands (upper band, middle band, lower band).

    Example:
    # Assuming 'data' is a DataFrame with the price data
    mobo_bands = MOBO(data, period=10, std_multiplier=0.8)
    """

    # Calculate moving average
    ma = data.rolling(window=period).mean()

    # Calculate standard deviation
    std = data.rolling(window=period).std()

    # Calculate upper and lower bands
    upper_band = ma + std * std_multiplier
    lower_band = ma - std * std_multiplier

    # Combine into DataFrame
    mobo_bands = pd.concat([upper_band, ma, lower_band], axis=1)
    mobo_bands.columns = ['Upper Band', 'Middle Band', 'Lower Band']

    return mobo_bands
