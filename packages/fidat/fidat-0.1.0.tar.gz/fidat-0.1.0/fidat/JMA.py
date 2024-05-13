import numpy as np
import pandas as pd

def Jurik_Moving_Average(data: pd.Series, length: int = 14, power: float = 2.0) -> pd.Series:
    """
    Calculates the Jurik Moving Average (JMA).

    Parameters:
    data (pd.Series): Series containing the data for which JMA needs to be calculated.
    length (int): The period for the JMA calculation. Default is 14.
    power (float): The power parameter for the JMA calculation. Default is 2.0.

    Returns:
    pd.Series: Series containing the Jurik Moving Average values.

    Example:
    # Assuming 'data' is a Series containing the data
    jma = Jurik_Moving_Average(data, length=14, power=2.0)
    """

    # Initialize the JMA series with the same index as data
    jma = pd.Series(index=data.index, dtype=float)

    if len(data) < 2:
        return jma  # Not enough data to calculate JMA

    # Set the first two values of JMA to the first value of data to start the calculation
    jma.iloc[0] = data.iloc[0]
    if len(data) > 1:
        jma.iloc[1] = data.iloc[1]

    # Coefficients for calculation
    w = 0.5 ** (1 / length)
    a = np.exp(-np.pi * power)
    b = 2 * a * np.cos(np.pi * (np.sqrt(power) / length))
    c = a ** 2

    # Calculate JMA for the rest of the series
    for i in range(2, len(data)):
        jma.iloc[i] = (1 - w) * (c * (data.iloc[i] - jma.iloc[i - 1]) + 2 * jma.iloc[i - 1] - (c - b) * jma.iloc[i - 2])

    return jma