import pandas as pd

def Moving_Standard_Deviation(data: pd.Series, period: int = 21) -> pd.Series:
    """
    Calculates the moving standard deviation of the given data over a specified period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data for which to calculate the moving standard deviation.
    period (int): The period over which to calculate the moving standard deviation. Default is 21.

    Returns:
    pd.Series: A Series containing the moving standard deviation values.

    Example:
    # Assuming 'data' is a DataFrame containing the data
    moving_std = Moving_Standard_Deviation(data, period=21)
    """

    # Calculate the moving standard deviation
    moving_std = data.rolling(window=period).std()

    return moving_std