import pandas as pd

def Zero_Lag_Exponential_Moving_Average(data: pd.Series, period: int = 26, adjust: bool = True) -> pd.Series:
    """
    Calculate the Zero Lag Exponential Moving Average (ZLEMA).

    Parameters:
    - data (pd.Series): A Series containing the closing prices.
    - period (int): The period over which to calculate the ZLEMA.
    - adjust (bool): Specifies whether the EMA should be calculated using an adjusted smoothing factor.

    Returns:
    - pd.Series: A Series containing the ZLEMA values.
    """

    # Calculate the lag adjustment
    lag = (period - 1) // 2
    # Calculate the adjustment by subtracting the lagged price from the current price
    adjustment = data - data.shift(lag)
    # Create a new series by adding the adjustment to the current price
    adjusted_series = data + adjustment
    # Calculate the EMA on the adjusted series
    zlema = adjusted_series.ewm(span=period, adjust=adjust).mean()

    return zlema