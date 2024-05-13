import pandas as pd

def Balance_of_Power(open: pd.Series, close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Balance of Power (BOP) indicator from the given open, close, high, and low price data.

    The Balance of Power (BOP) indicator measures the strength of buyers versus sellers in the market.

    Parameters:
    open (pd.DataFrame): DataFrame containing the open price data.
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.Series: A Series containing the Balance of Power (BOP) values.

    Example:
    # Assuming 'open', 'close', 'high', and 'low' are DataFrames with the open, close, high, and low price data
    balance_of_power = Balance_of_Power(open, close, high, low)
    """

    # Calculate Balance of Power (BOP)
    bop = (close - open) / (high - low)

    return bop