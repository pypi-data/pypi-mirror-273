import pandas as pd

def Pivot_Points(high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Pivot Points (PIVOT) indicator from the given high and low price data.

    Pivot Points (PIVOT) are significant support and resistance levels calculated based on the previous day's high, low, and close prices.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.DataFrame: A DataFrame containing the Pivot Points (PIVOT) levels.

    Example:
    # Assuming 'high' and 'low' are DataFrames with the high and low price data
    pivot_points = Pivot_Points(high, low)
    """

    # Calculate Pivot Point (PP)
    pivot_point = (high.shift(1) + low.shift(1) + high.shift(1)) / 3

    # Calculate Support 1 (S1) and Resistance 1 (R1)
    support_1 = (pivot_point * 2) - high.shift(1)
    resistance_1 = (pivot_point * 2) - low.shift(1)

    # Calculate Support 2 (S2) and Resistance 2 (R2)
    support_2 = pivot_point - (high.shift(1) - low.shift(1))
    resistance_2 = pivot_point + (high.shift(1) - low.shift(1))

    # Combine into DataFrame
    pivot_points = pd.concat([pivot_point, support_1, resistance_1, support_2, resistance_2], axis=1)
    pivot_points.columns = ['Pivot Point', 'Support 1', 'Resistance 1', 'Support 2', 'Resistance 2']

    return pivot_points