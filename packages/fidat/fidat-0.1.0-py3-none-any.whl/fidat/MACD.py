import pandas as pd

def Moving_Average_Convergence_Divergence(data: pd.Series, period_fast: int = 12, period_slow: int = 26, signal: int = 9, adjust: bool = True) -> pd.Series:
    """
    Calculates the Moving Average Convergence Divergence (MACD) and its signal line from the given price data.

    The MACD is a trend-following momentum indicator that shows the relationship between two moving averages
    of a security’s price. The MACD is calculated by subtracting the 26-period EMA from the 12-period EMA.
    The signal line, which is the 9-period EMA of the MACD, is used to generate buy and sell signals.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period_fast (int): The number of periods for the fast EMA.
    period_slow (int): The number of periods for the slow EMA.
    signal (int): The number of periods for the signal line EMA.
    adjust (bool): Boolean to decide if the EMA calculation should be adjusted.

    Returns:
    pd.DataFrame: A DataFrame containing the MACD, MACD Signal, and MACD Histogram.

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the MACD for
    macd_data = Moving_Average_Convergence_Divergence(data['Close'], period_fast=12, period_slow=26, signal=9)
    """

    # Calculate fast and slow EMAs
    ema_fast = data.ewm(span=period_fast, adjust=adjust).mean()
    ema_slow = data.ewm(span=period_slow, adjust=adjust).mean()

    # Calculate MACD line
    macd_line = ema_fast - ema_slow

    # Calculate signal line
    macd_signal = macd_line.ewm(span=signal, adjust=adjust).mean()

    # Calculate MACD histogram
    macd_histogram = macd_line - macd_signal

    # Create DataFrame to hold MACD data
    macd_data = pd.DataFrame({
        'MACD': macd_line,
        'Signal': macd_signal,
        'Histogram': macd_histogram
    })

    return macd_data
