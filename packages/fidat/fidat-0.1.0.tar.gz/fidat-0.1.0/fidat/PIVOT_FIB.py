import pandas as pd

def Fibonacci_Pivot_Points(high: pd.Series, low: pd.Series) -> pd.Series:
    """
    Calculates the Fibonacci Pivot Points indicator from the given high and low price data.

    Fibonacci pivot point levels are determined by first calculating the classic pivot point,
    then multiplying the previous day’s range with its corresponding Fibonacci level.
    Most traders use the 38.2%, 61.8% and 100% retracements in their calculations.

    Parameters:
    high (pd.DataFrame): DataFrame containing the high price data.
    low (pd.DataFrame): DataFrame containing the low price data.

    Returns:
    pd.DataFrame: A DataFrame containing the Fibonacci Pivot Points levels.

    Example:
    # Assuming 'high' and 'low' are DataFrames with the high and low price data
    fibonacci_pivot_points = Pivot_Point_Fibonacci(high, low)
    """

    # Calculate Classic Pivot Points
    pivot_points = (high.shift(1) + low.shift(1) + high.shift(1)) / 3

    # Calculate Pivot Range
    pivot_range = high.shift(1) - low.shift(1)

    # Calculate Fibonacci Pivot Points
    fib_levels = [0, 0.382, 0.618, 1.0]  # Fibonacci levels
    fibonacci_pivot_points = pd.DataFrame(index=pivot_points.index, columns=['R1', 'R2', 'R3', 'R4', 'S1', 'S2', 'S3', 'S4'])
    for idx, level in enumerate(fib_levels):
        fibonacci_pivot_points[f'R{idx+1}'] = pivot_points + (pivot_range * level)
        fibonacci_pivot_points[f'S{idx+1}'] = pivot_points - (pivot_range * level)

    return fibonacci_pivot_points