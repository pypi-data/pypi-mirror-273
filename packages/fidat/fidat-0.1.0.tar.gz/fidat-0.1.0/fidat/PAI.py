import pandas as pd

def Price_Action_Indicator(open: pd.Series, high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """
    Calculate the Price Action Indicator (PAI).

    Parameters:
    open_price (pd.Series): Series containing the opening prices.
    high (pd.Series): Series containing the high prices.
    low (pd.Series): Series containing the low prices.
    close (pd.Series): Series containing the closing prices.

    Returns:
    pd.Series: Series containing the Price Action Indicator (PAI) values.

    Example:
    # Assuming 'open_price', 'high', 'low', and 'close' are Series containing the respective data
    pai_values = price_action_indicator(open_price, high, low, close)
    """

    body_range = close - open
    shadow_range = high - low

    # Calculate PAI as the ratio of body range to shadow range
    pai_values = body_range / shadow_range

    return pai_values