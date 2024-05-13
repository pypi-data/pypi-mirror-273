import pandas as pd

from .BASP import Buying_and_Selling_Pressure


def Normalized_BASP(close: pd.Series, high: pd.Series, low: pd.Series, volume: pd.Series, period: int = 40, adjust: bool = True) -> pd.Series:
    """
    Calculates the Normalized Buying and Selling Pressure (BASP) indicators from the given close, high, low, and volume data.

    Normalized BASP scales the Buying Pressure and Selling Pressure indicators to be between 0 and 1.

    Parameters:
    close (pd.DataFrame): DataFrame containing the close price data.
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    volume (pd.DataFrame): DataFrame containing the volume data.
    period (int): The number of periods to use in the calculation. Default is 40.
    adjust (bool): Whether to adjust the exponential moving averages. Default is True.

    Returns:
    pd.DataFrame: A DataFrame containing the Normalized Buying Pressure and Normalized Selling Pressure columns.

    Example:
    # Assuming 'close' is a DataFrame with the close price data, 'high' is a DataFrame with the high price data,
    # 'low' is a DataFrame with the low price data, and 'volume' is a DataFrame with the volume data
    normalized_basp = Normalized_BASP(close, high, low, volume, period=40, adjust=True)
    """

    # Calculate Buying Pressure and Selling Pressure
    buying_pressure = Buying_and_Selling_Pressure(close, high, low, volume, period)['Buying Pressure']
    selling_pressure = Buying_and_Selling_Pressure(close, high, low, volume, period)['Selling Pressure']

    # Normalize Buying Pressure and Selling Pressure
    min_basp = min(buying_pressure.min(), selling_pressure.min())
    max_basp = max(buying_pressure.max(), selling_pressure.max())

    normalized_buying_pressure = (buying_pressure - min_basp) / (max_basp - min_basp)
    normalized_selling_pressure = (selling_pressure - min_basp) / (max_basp - min_basp)

    # Combine Normalized Buying Pressure and Normalized Selling Pressure into a DataFrame
    normalized_basp = pd.DataFrame({'Normalized Buying Pressure': normalized_buying_pressure, 'Normalized Selling Pressure': normalized_selling_pressure})

    return normalized_basp