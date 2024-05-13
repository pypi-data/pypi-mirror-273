import pandas as pd

def Triple_Exponential_Moving_Average(data: pd.Series, period: int = 9, adjust: bool = True) -> pd.Series:
        """
        Calculates the Triple Exponential Moving Average (TEMA) of a given data series. TEMA is designed to
        address the lag problem of traditional moving averages by applying a triple smoothing of the data,
        which makes it more responsive to recent market changes. This makes TEMA useful for volatile stock data,
        where quick reaction to price changes is crucial.

        Parameters:
        data (pd.DataFrame): DataFrame containing the price data.
        period (int): The number of periods over which the TEMA is calculated.
        adjust (bool): Boolean to decide if the EMA calculation should be adjusted.

        Returns:
        pd.Series: A pandas Series containing the Triple Exponential Moving Average of the data.

        Example:
        # Assuming 'data' is a DataFrame and you want to calculate the TEMA for the 'close' column
        data['TEMA'] = Triple_Exponential_Moving_Average(data['close'], period=9)
        """
        # First EMA
        ema1 = data.ewm(span=period, adjust=adjust).mean()
        # Second EMA of the first EMA
        ema2 = ema1.ewm(span=period, adjust=adjust).mean()
        # Third EMA of the second EMA
        ema3 = ema2.ewm(span=period, adjust=adjust).mean()

        # Triple EMA calculation
        tema = 3 * (ema1 - ema2) + ema3

        return tema