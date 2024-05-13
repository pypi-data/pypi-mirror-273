import pandas as pd

def Market_Momentum(data: pd.Series, period: int = 10) -> pd.Series:
    """
    Calculates the Market Momentum indicator from the given price data.

    Market Momentum measures the difference between the current closing price and the closing price n periods ago.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods for calculating the momentum.

    Returns:
    pd.Series: A Series containing the Market Momentum values.

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the Market Momentum for
    market_momentum = Market_Momentum(data['Close'], period=10)
    """

    # Calculate Market Momentum
    market_momentum = data.diff(periods=period)

    return market_momentum