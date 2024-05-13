import pandas as pd
import numpy as np

def Linear_Weighted_Moving_Average(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Linear Weighted Moving Average (LWMA) for all numeric columns in the given DataFrame.

    Parameters:
    - data (pd.DataFrame): A DataFrame containing numeric columns.
    - period (int): The period over which to calculate the LWMA.

    Returns:
    - pd.DataFrame: A DataFrame containing the LWMA values for each numeric column.
    """

    weights = np.arange(1, period + 1)  # Creates an array of weights [1, 2, ..., period]

    # Apply the LWMA calculation using rolling window and weights
    return data.rolling(window=period).apply(lambda y: np.dot(y, weights) / weights.sum(), raw=True)