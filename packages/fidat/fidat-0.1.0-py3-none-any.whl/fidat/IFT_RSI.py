import pandas as pd
import numpy as np

def Inverse_Fisher_Transform_RSI(data: pd.Series, rsi_period: int = 5, wma_period: int = 9) -> pd.Series:
    """
    Calculates the Modified Inverse Fisher Transform applied on Relative Strength Index (RSI) from the given price data.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    rsi_period (int): The number of periods for calculating the RSI.
    wma_period (int): The number of periods for calculating the weighted moving average (WMA) of the RSI.

    Returns:
    pd.Series: A Series containing the Inverse Fisher Transform RSI values.

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the Inverse Fisher Transform RSI for
    ift_rsi = Inverse_Fisher_Transform_RSI(data['Close'], rsi_period=5, wma_period=9)
    """

    # Calculate RSI
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Apply Inverse Fisher Transform
    v1 = 0.1 * (rsi - 50)
    ift_rsi = pd.Series(np.nan, index=v1.index)

    # Calculation using np.tanh for the hyperbolic tangent part of the IFT
    ift_rsi = (np.exp(2 * v1) - 1) / (np.exp(2 * v1) + 1)

    # Calculate WMA of Inverse Fisher Transform RSI
    wma_ift_rsi = ift_rsi.rolling(window=wma_period).mean()

    return wma_ift_rsi