import pandas as pd

def Bollinger_Bands_Width(data: pd.Series, period: int = 20, MA: pd.Series = None) -> pd.Series:
    """
    Calculates the Bollinger Bands Width (BBWIDTH) indicator from the given price data.

    The Bollinger Bands Width (BBWIDTH) measures the width of the Bollinger Bands on a normalized basis.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods for calculating the moving average.
    MA (pd.Series): Optional pre-calculated moving average. If not provided, it will be calculated from 'data'.

    Returns:
    pd.Series: A Series containing the Bollinger Bands Width (BBWIDTH) values.

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the BBWIDTH for
    bbwidth = BBWIDTH(data['Close'], period=20)
    """

    # Calculate moving average if not provided
    if MA is None:
        MA = data.rolling(window=period).mean()

    # Calculate standard deviation
    std = data.rolling(window=period).std()

    # Calculate Bollinger Bands Width
    bb_width = (2 * std) / MA

    return bb_width

# Example usage:
# Assuming 'data' is a DataFrame with the price data.
# bbwidth = BBWIDTH(data['Close'], period=20)
