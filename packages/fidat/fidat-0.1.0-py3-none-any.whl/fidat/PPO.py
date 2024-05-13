import pandas as pd

def Percentage_Price_Oscillator(data: pd.Series, period_fast: int = 12, period_slow: int = 26, signal: int = 9, adjust: bool = True) -> pd.Series:
    """
    Calculates the Percentage Price Oscillator (PPO) and its signal line from the given price data.

    The PPO is a momentum oscillator that measures the difference between two moving averages of
    a security’s price expressed as a percentage. It is similar to the MACD indicator, but instead
    of displaying the absolute difference between two moving averages, it shows this difference
    as a percentage of the slower moving average.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    period_fast (int): The number of periods for the fast EMA.
    period_slow (int): The number of periods for the slow EMA.
    signal (int): The number of periods for the signal line EMA.
    adjust (bool): Boolean to decide if the EMA calculation should be adjusted.

    Returns:
    pd.DataFrame: A DataFrame containing the PPO, PPO Signal, and PPO Histogram.

    Example:
    # Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the PPO for
    ppo_data = Percentage_Price_Oscillator(data['Close'], period_fast=12, period_slow=26, signal=9)
    """

    # Calculate fast and slow EMAs
    ema_fast = data.ewm(span=period_fast, adjust=adjust).mean()
    ema_slow = data.ewm(span=period_slow, adjust=adjust).mean()

    # Calculate PPO line
    ppo_line = ((ema_fast - ema_slow) / ema_slow) * 100

    # Calculate signal line
    ppo_signal = ppo_line.ewm(span=signal, adjust=adjust).mean()

    # Calculate PPO histogram
    ppo_histogram = ppo_line - ppo_signal

    # Create DataFrame to hold PPO data
    ppo_data = pd.DataFrame({
        'PPO': ppo_line,
        'Signal': ppo_signal,
        'Histogram': ppo_histogram
    })

    return ppo_data

# Example usage:
# Assuming 'data' is a DataFrame with a column 'Close' that you want to calculate the PPO for.
# ppo_data = Percentage_Price_Oscillator(data['Close'], period_fast=12, period_slow=26, signal=9)
