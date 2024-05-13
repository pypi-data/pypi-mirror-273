
import pandas as pd
import numpy as np


def Arnaud_Legoux_Moving_Average(data: pd.Series, period: int = 9, sigma: int = 6, offset: float = 0.85) -> pd.Series:
    """
    Calculates the Arnaud Legoux Moving Average (ALMA) of a given data series. ALMA reduces the noise
    and improves the smoothness of the data series while being more responsive than traditional moving
    averages. The offset and sigma parameters control the localization and width of the Gaussian filter,
    allowing customization to fit different types of data and sensitivity needs.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods over which the ALMA is calculated.
    sigma (int): The standard deviation of the Gaussian kernel, which affects the smoothness.
    offset (float): The offset of the window from the mean, which controls the lag and responsiveness.

    Returns:
    pd.Series: A pandas Series containing the Arnaud Legoux Moving Average of the data.

    Example:
    # Assuming 'data' is a DataFrame and you want to calculate the ALMA for the 'close' column
    data['ALMA'] = ALMA(data['close'], period=9, sigma=6, offset=0.85)
    """
    m = int(offset * (period - 1))
    s = period / sigma

    weights = np.array([np.exp(-0.5 * ((i - m) / s) ** 2) for i in range(period)])
    weights /= weights.sum()

    alma = np.convolve(data.values, weights, mode='valid')

    # To align with the input data index, prepend NaNs
    alma_padded = np.empty(data.shape[0])
    alma_padded[:] = np.nan
    alma_padded[(period-1):] = alma

    return pd.Series(alma_padded, index=data.index)