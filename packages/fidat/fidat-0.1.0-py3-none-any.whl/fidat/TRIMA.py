import pandas as pd

def Triangular_Moving_Average(data: pd.Series, period: int = 18) -> pd.Series:
    """
    Calculate the Triangular Moving Average (TRIMA) of a given DataFrame.

    Parameters:
    - data (pd.DataFrame): A DataFrame with a 'close' column containing the closing prices.
    - period (int): The period over which to calculate the TRIMA.

    Returns:
    - pd.Series: A Series containing the TRIMA values.
    """
    # Ensure the period is an odd number by reducing it if it's even
    if period % 2 == 0:
        period -= 1

    # Calculate the simple moving average (SMA)
    sma = data.rolling(window=period, center=True).mean()

    # Calculate the TRIMA as the SMA of the SMA, using half the initial period (rounded down)
    trima_period = period // 2 + 1
    trima = sma.rolling(window=trima_period, center=True).mean()

    return trima