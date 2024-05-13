import numpy as np
import pandas as pd

def Standard_Deviation_Channel(data: pd.Series, length: int = 20, period: int = 2) -> pd.DataFrame:
    """
    Calculates the Standard Deviation Channel.

    Parameters:
    data (pd.Series): Series containing the data for which the Standard Deviation Channel needs to be calculated.
    length (int): The period for the Standard Deviation calculation. Default is 20.
    width (int): The number of standard deviations to use for the channel width. Default is 2.

    Returns:
    pd.DataFrame: DataFrame containing the upper and lower bands of the Standard Deviation Channel.

    Example:
    # Assuming 'data' is a Series containing the data
    std_channel = Standard_Deviation_Channel(data, length=20, width=2)
    """

    rolling_std = data.rolling(window=length).std()
    upper_band = data + period * rolling_std
    lower_band = data - period * rolling_std

    std_channel = pd.DataFrame({'Upper Band': upper_band, 'Lower Band': lower_band}, index=data.index)

    return std_channel