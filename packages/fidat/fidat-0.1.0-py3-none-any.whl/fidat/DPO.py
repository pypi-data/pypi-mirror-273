import pandas as pd

def Detrended_Price_Oscillator(close: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates the Detrended Price Oscillator (DPO).

    Parameters:
    close (pd.Series): Series containing closing prices.
    period (int): The period for the DPO calculation. Default is 20.

    Returns:
    pd.Series: Series containing the Detrended Price Oscillator values.

    Example:
    # Assuming 'close' is a Series containing closing prices
    dpo = Detrended_Price_Oscillator(close, period=20)
    """

    detrended_close = close - close.rolling(window=period).mean().shift(periods=int(period/2) + 1)
    dpo = detrended_close

    return dpo