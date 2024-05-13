import pandas as pd

def Percentage_B(data: pd.Series, period: int = 20, MA: pd.Series = None) -> pd.Series:
    """
    Calculates the Percent B (%b) indicator from the given price data.

    Percent B (%b), pronounced 'percent b', measures where the last price is in relation to the Bollinger Bands.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period (int): The number of periods for calculating the moving average.
    MA (pd.Series): Optional pre-calculated moving average. If not provided, it will be calculated from 'data'.

    Returns:
    pd.Series: A Series containing the Percent B (%b) values.

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the Percent B for
    percent_b = PERCENT_B(data['Close'], period=20)
    """

    # Calculate moving average if not provided
    if MA is None:
        MA = data.rolling(window=period).mean()

    # Calculate standard deviation
    std = data.rolling(window=period).std()

    # Calculate upper and lower bands
    upper_band = MA + (2 * std)
    lower_band = MA - (2 * std)

    # Calculate Percent B
    percent_b = (data - lower_band) / (upper_band - lower_band)

    return percent_b

# Example usage:
# Assuming 'data' is a DataFrame with the price data.
# percent_b = PERCENT_B(data['Close'], period=20)
