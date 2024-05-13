import pandas as pd

def Value_chart(open: pd.Series, close: pd.Series, high: pd.Series, low: pd.Series, period: int = 5) -> pd.Series:
    """
    Calculates the Value Chart indicator.

    Parameters:
    open (pd.DataFrame): DataFrame containing the open prices.
    close (pd.DataFrame): DataFrame containing the close prices.
    high (pd.DataFrame): DataFrame containing the high prices.
    low (pd.DataFrame): DataFrame containing the low prices.
    period (int): The period used to calculate the indicator. Default is 5.

    Returns:
    pd.DataFrame: DataFrame containing the Value Chart indicator values.

    Example:
    # Assuming 'open', 'close', 'high', and 'low' are DataFrames containing the respective prices
    value_chart = Value_chart(open, close, high, low, period=5)
    """

    # Calculate float axis
    float_axis = ((high + low) / 2).rolling(window=period).mean()

    # Calculate volatility unit
    vol_unit = (high - low).rolling(window=period).mean() * 0.2

    # Calculate Value Chart
    value_chart_high = (high - float_axis) / vol_unit
    value_chart_low = (low - float_axis) / vol_unit
    value_chart_close = (close - float_axis) / vol_unit
    value_chart_open = (open - float_axis) / vol_unit

    # Combine results into a DataFrame
    value_chart_df = pd.concat([value_chart_high, value_chart_low, value_chart_close, value_chart_open], axis=1)
    value_chart_df.columns = ["Value Chart High", "Value Chart Low", "Value Chart Close", "Value Chart Open"]

    return value_chart_df