import pandas as pd

def Simple_Moving_Average(data: pd.Series, period: int = 5) -> pd.Series:
    """
    Calculates the moving average of the specified data over a given window size.
    
    This method computes the simple moving average (SMA), which is a commonly used indicator
    in financial analysis to smooth out price data by creating a constantly updated average price.
    The SMA is calculated by taking the arithmetic mean of a given set of values over the specified
    number of periods in the window.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data series.
    window (int): The size of the moving window over which the average is computed.

    Returns:
    pd.Series: A series containing the moving average of the data series.
    
    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the moving average for.
    data['MA'] = Moving_Average(data['Close'], window=5)
    """
    return data.rolling(window=period).mean()