import pandas as pd

def Stochastic_Oscillator_RSI(data: pd.Series, rsi_period: int = 14, stoch_period: int = 14) -> pd.Series:
    """
    Calculates the Stochastic Oscillator RSI (StochRSI) from the given price data.

    StochRSI is an oscillator that measures the level of RSI relative to its high-low range over a set time period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    rsi_period (int): The number of periods for calculating the RSI.
    stoch_period (int): The number of periods for calculating the Stochastic Oscillator RSI.

    Returns:
    pd.Series: A Series containing the Stochastic Oscillator RSI values.

    Example:
    # Assuming 'data' is a DataFrame with the price data
    stoch_rsi = Stochastic_Oscillator_RSI(data, rsi_period=14, stoch_period=14)
    """

    # Calculate RSI
    delta = data.diff()
    gain = delta.where(delta > 0, 0).rolling(window=rsi_period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Calculate StochRSI
    lowest_rsi = rsi.rolling(window=stoch_period).min()
    highest_rsi = rsi.rolling(window=stoch_period).max()
    stoch_rsi = 100 * ((rsi - lowest_rsi) / (highest_rsi - lowest_rsi))

    return stoch_rsi
