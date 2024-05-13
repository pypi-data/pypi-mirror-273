import pandas as pd

def Guppy_Multiple_Moving_Average(close: pd.DataFrame, short_period: int = 3, long_period: int = 5) -> pd.DataFrame:
    """
    Calculates the Guppy Multiple Moving Average.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close prices.
    short_period (int): The period for the short moving average. Default is 3.
    long_period (int): The period for the long moving average. Default is 5.

    Returns:
    pd.DataFrame: DataFrame containing the Guppy Multiple Moving Average values.

    Example:
    # Assuming 'close' is a DataFrame containing the close prices
    gmma = Guppy_Multiple_Moving_Average(close, short_period=3, long_period=5)
    """

    short_moving_avg = close.rolling(window=short_period).mean()
    long_moving_avg = close.rolling(window=long_period).mean()

    GMMA = pd.DataFrame({
        'Short Moving Avg': short_moving_avg,
        'Long Moving Avg': long_moving_avg,
    })

    return GMMA