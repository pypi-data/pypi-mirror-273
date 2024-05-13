import pandas as pd

def Vortex_Oscillator(high: pd.Series, low: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculates the Vortex Oscillator from the given high and low price data.

    The Vortex Oscillator is a technical indicator that plots two oscillating lines to identify positive and negative trend movement.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.
    period (int): The number of periods for calculating the Vortex Oscillator.

    Returns:
    pd.DataFrame: A DataFrame containing the Vortex Oscillator values for both positive and negative trends.

    Example:
    # Assuming 'high' and 'low' are DataFrames with the high and low price data
    vortex_oscillator = Vortex_Oscillator(high, low, period=14)
    """

    # Calculate True Range (TR)
    true_range = high - low

    # Calculate Positive and Negative Vortex Movement (VM+ and VM-)
    vm_plus = true_range.rolling(window=1).sum().shift(1)
    vm_minus = true_range[::-1].rolling(window=1).sum().shift(1)

    # Calculate Positive and Negative True Range (TR+ and TR-)
    tr_plus = (high - low.shift(1)).where(high > low.shift(1), 0).rolling(window=period).sum()
    tr_minus = (low.shift(1) - high).where(low.shift(1) > high, 0).rolling(window=period).sum()

    # Calculate Vortex Oscillator (Vortex+ and Vortex-)
    vortex_plus = tr_plus / vm_minus
    vortex_minus = tr_minus / vm_plus

    return pd.DataFrame({'Vortex+': vortex_plus, 'Vortex-': vortex_minus})