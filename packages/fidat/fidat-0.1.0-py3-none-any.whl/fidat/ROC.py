import pandas as pd

def Rate_of_Change(data: pd.Series, period: int = 12) -> pd.Series:
    """
    Calculates the Rate of Change (ROC) indicator from the given price data.

    The Rate of Change (ROC) measures the percentage change in price over a specified period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods for calculating the ROC.

    Returns:
    pd.Series: A Series containing the Rate of Change (ROC) values.

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the ROC for
    roc = Rate_Of_Change(data['Close'], period=12)
    """

    # Calculate percentage change over the specified period
    roc = data.pct_change(periods=period) * 100

    return roc