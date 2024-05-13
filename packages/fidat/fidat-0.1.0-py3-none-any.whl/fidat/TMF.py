import pandas as pd
import numpy as np

def Twiggs_Money_Flow(close: pd.Series, high: pd.Series, low: pd.Series, period: int = 21) -> pd.Series:
    """
    Calculates the Twiggs Money Flow (TMF) indicator from the given close, high, and low price data.

    Twiggs Money Flow (TMF) improves upon the Chaikin Money Flow (CMF) by incorporating the relationship between the open, high, low, and close prices.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods to use in the calculation. Default is 21.

    Returns:
    pd.Series: A Series containing the Twiggs Money Flow (TMF) values.

    Example:
    # Assuming 'close' is a DataFrame with the close price data, 'high' is a DataFrame with the high price data, and 'low' is a DataFrame with the low price data
    twiggs_money_flow = Twiggs_Money_Flow(close, high, low, period=21)
    """

    # Calculate the typical price
    typical_price = (high + low + close) / 3

    # Calculate the money flow volume
    money_flow_volume = typical_price * close.diff()

    # Calculate the raw money flow
    raw_money_flow = money_flow_volume.rolling(window=period).sum()

    # Calculate the raw money flow multiplier
    # Here we change how we calculate the multiplier by counting the number of positive changes in close
    close_changes = close.diff()
    positive_changes = (close_changes > 0).rolling(window=period).sum()  # This is a count of positive changes

    # Calculate the Twiggs Money Flow (TMF) values
    # Protect against division by zero
    twiggs_money_flow = raw_money_flow / positive_changes.replace(0, np.nan)

    return twiggs_money_flow