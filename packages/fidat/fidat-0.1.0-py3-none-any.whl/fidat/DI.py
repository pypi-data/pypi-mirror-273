import pandas as pd

def Disparity_Index(close: pd.DataFrame, period: int = 10) -> pd.Series:
    """
    Calculates the Disparity Index.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close prices.
    period (int): The period for calculating the Disparity Index. Default is 10.

    Returns:
    pd.Series: Series containing the Disparity Index values.

    Example:
    # Assuming 'close' is a DataFrame containing the close prices
    disparity_index = Disparity_Index(close, period=10)
    """

    moving_avg = close.rolling(window=period).mean()
    disparity = (close - moving_avg) / moving_avg * 100

    return disparity