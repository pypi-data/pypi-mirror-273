import pandas as pd

def Kaufman_Efficiency_Indicator(data: pd.Series, period: int = 10) -> pd.Series:
    """
    Calculate the Kaufman Efficiency Ratio (ER) using the closing prices.

    Parameters:
    - data (pd.Series): Prefer close. A Series containing the closing prices.
    - period (int): The period over which to calculate the ER.

    Returns:
    - pd.Series: A Series containing the ER values.
    """
    # Calculate the change from the first to the last price over each period
    change = data.diff(period - 1)

    # Calculate the volatility as the sum of the absolute differences between consecutive prices over the period
    volatility = data.diff().abs().rolling(window=period).sum()

    # Efficiency Ratio is the absolute change divided by the volatility
    er = change.abs() / volatility

    return er