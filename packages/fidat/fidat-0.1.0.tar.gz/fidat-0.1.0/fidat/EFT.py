import pandas as pd
import numpy as np

def Ehlers_Fisher_Transform(close: pd.Series, period: int = 10) -> pd.Series:
    """
    Calculates Ehler's Fisher Transform.

    Parameters:
    close (pd.Series): Series containing closing prices.
    period (int): The period for the Fisher Transform calculation. Default is 10.

    Returns:
    pd.Series: Series containing the Fisher Transform values.

    Example:
    # Assuming 'close' is a Series containing closing prices
    fisher_transform = Ehlers_Fisher_Transform(close, period=10)
    """

    # Normalize the close prices to be within the range [-1, 1]
    normalized_close = 2 * ((close - close.min()) / (close.max() - close.min())) - 1
    normalized_close = normalized_close.clip(-0.999, 0.999)  # Avoid division by zero or values that make log undefined

    # Calculation of the Fisher Transform
    ratio = (1 + normalized_close) / (1 - normalized_close)
    ratio = np.clip(ratio, a_min=np.finfo(float).tiny, a_max=None)  # Prevent non-positive values
    

    m = np.log(ratio)
    ema_ratio = (m - m.rolling(window=period).mean()) / m.rolling(window=period).std(ddof=0)

    fisher_transform = 0.5 * np.log((1 + ema_ratio) / (1 - ema_ratio))
    # Ensure the argument for the second log is also always positive
    fisher_transform = np.clip(fisher_transform, np.finfo(float).tiny, np.inf)

    return fisher_transform.bfill()