import pandas as pd

def Simple_Moving_Median(data: pd.Series, period: int = 9) -> pd.Series:
    """
    Simple moving median, an alternative to moving average. SMA, when used to estimate the underlying trend in a time series,
    is susceptible to rare events such as rapid shocks or other anomalies. A more robust estimate of the trend is the simple moving median over n time periods.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing the data series.
    period (int): The number of periods over which to calculate the moving median.
    
    Returns:
    pd.Series: A series containing the simple moving median of the data series.
    """
    return data.rolling(window=period).median()