import pandas as pd

def Price_Swing_Kaufman(open: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame, close: pd.Series, period: int = 10, adjust: bool = True) -> pd.Series:
    """
    Price Swing Kaufman Indicator

    The Price Swing Kaufman Indicator, developed by Perry J. Kaufman, is a technical analysis tool used to measure price swings in a financial instrument over a specified period. It calculates the percentage of the total price movement that is attributed to swings in the price action.

    """
    high_low_diff = high - low
    close_open_diff = close - open
    hl_co_diff = abs(high_low_diff - close_open_diff)
    hl_co_diff_sum = hl_co_diff.rolling(window=period, min_periods=1).sum()
    hl_diff_sum = high_low_diff.rolling(window=period, min_periods=1).sum()
    pswk = 100 * hl_co_diff_sum / hl_diff_sum
    return pswk