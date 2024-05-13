import numpy as np
import pandas as pd

def Rainbow_Moving_Average(data: pd.Series, length: int = 14, colors: int = 7) -> pd.Series:
    """
    Calculates the Rainbow Moving Average.

    Parameters:
    data (pd.Series): Series containing the data for which Rainbow Moving Average needs to be calculated.
    length (int): The period for the Rainbow Moving Average calculation. Default is 14.
    colors (int): The number of colors to use in the Rainbow Moving Average. Default is 7.

    Returns:
    pd.Series: Series containing the Rainbow Moving Average values.

    Example:
    # Assuming 'data' is a Series containing the data
    rma = Rainbow_Moving_Average(data, length=14, colors=7)
    """

    rm_average = pd.Series(index=data.index, dtype=float)

    for i in range(length, len(data)):
        rm_average.iloc[i] = np.mean(data.iloc[i-length+1:i+1])

    rma = pd.Series(index=data.index, dtype=float)
    for i in range(len(data)):
        if i < length:
            rma.iloc[i] = np.nan
        else:
            values = rm_average[max(0, i - length + 1):i+1]
            rma.iloc[i] = np.average(values, weights=np.arange(1, len(values) + 1))

    return rma