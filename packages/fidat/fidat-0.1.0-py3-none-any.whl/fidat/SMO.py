import pandas as pd

def Squeeze_Momentum_Indicator(data: pd.Series, period: int = 20, MA: pd.Series = None) -> pd.Series:
    """
    Calculates the Squeeze Momentum Indicator from the given data.

    The Squeeze Momentum Indicator helps identify periods of low volatility and high volatility contraction, which are often followed by periods of high volatility expansion.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.
    period (int): The period used in the calculation. Default is 20.
    MA (pd.Series): Optional moving average data. If provided, it will be used instead of calculating a new one. Default is None.

    Returns:
    pd.DataFrame: A DataFrame containing the Squeeze Momentum Indicator values.

    Example:
    # Assuming 'data' is a DataFrame with the required data
    squeeze_momentum = Squeeze_Momentum_Indicator(data, period=20, MA=None)
    """

    # Calculate the Bollinger Bands
    if MA is None:
        middle_band = data.rolling(window=period).mean()
    else:
        middle_band = MA
    upper_band = middle_band + 2 * data.rolling(window=period).std()
    lower_band = middle_band - 2 * data.rolling(window=period).std()

    # Calculate the Squeeze Momentum Indicator
    squeeze_momentum = data - middle_band

    return pd.DataFrame({'Squeeze Momentum': squeeze_momentum, 'Upper Band': upper_band, 'Lower Band': lower_band})