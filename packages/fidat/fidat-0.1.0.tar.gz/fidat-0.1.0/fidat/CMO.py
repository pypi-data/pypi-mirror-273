import pandas as pd

def Chande_Momentum_Oscillator(data: pd.Series, period: int = 9, factor: int = 10) -> pd.Series:
    """
    Calculates the Chande Momentum Oscillator (CMO) indicator from the given data.

    The Chande Momentum Oscillator (CMO) measures the difference between the sum of gains and the sum of losses over a specified period.

    Parameters:
    data (pd.DataFrame): DataFrame containing the data.
    period (int): The number of periods to use in the calculation. Default is 9.
    factor (int): A factor to scale the result by. Default is 100.
    adjust (bool): Whether to adjust the exponential moving averages. Default is True.

    Returns:
    pd.DataFrame: A DataFrame containing the Chande Momentum Oscillator (CMO) values.

    Example:
    # Assuming 'data' is a DataFrame with the data
    cmo = CMO(data, period=9, factor=100, adjust=True)
    """

    # Calculate the difference between the current close price and the previous close price
    diff = data.diff()

    # Calculate the sum of gains and losses over the specified period
    sum_gains = diff.where(diff > 0, 0).rolling(window=period).sum()
    sum_losses = abs(diff.where(diff < 0, 0).rolling(window=period).sum())

    # Calculate the Chande Momentum Oscillator (CMO)
    cmo = ((sum_gains - sum_losses) / (sum_gains + sum_losses)).fillna(0) * factor

    return cmo
