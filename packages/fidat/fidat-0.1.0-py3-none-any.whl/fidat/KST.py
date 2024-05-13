import pandas as pd

def Know_Sure_Thing(data: pd.Series, r1: int = 10, r2: int = 15, r3: int = 20, r4: int = 30) -> pd.Series:
    """
    Calculates the Know Sure Thing (KST) indicator from the given price data.

    The Know Sure Thing (KST) indicator is a momentum oscillator that measures the rate of change of four different smoothed price averages.

    Parameters:
    data (pd.DataFrame): DataFrame containing the price data.
    r1 (int): The number of periods for the first ROC calculation.
    r2 (int): The number of periods for the second ROC calculation.
    r3 (int): The number of periods for the third ROC calculation.
    r4 (int): The number of periods for the fourth ROC calculation.

    Returns:
    pd.DataFrame: A DataFrame containing the Know Sure Thing (KST) values.

    Example:
    # Assuming 'data' is a DataFrame with the price data
    kst = Know_Sure_Thing(data, r1=10, r2=15, r3=20, r4=30)
    """

    # Calculate Rate of Change (ROC) for different periods
    roc1 = data.pct_change(r1)
    roc2 = data.pct_change(r2)
    roc3 = data.pct_change(r3)
    roc4 = data.pct_change(r4)

    # Calculate the smoothed moving average of ROC for different periods
    sma_roc1 = roc1.rolling(window=6).mean()
    sma_roc2 = roc2.rolling(window=6).mean()
    sma_roc3 = roc3.rolling(window=6).mean()
    sma_roc4 = roc4.rolling(window=6).mean()

    # Calculate the KST by summing the smoothed moving averages of ROC
    kst = sma_roc1 + 2 * sma_roc2 + 3 * sma_roc3 + 4 * sma_roc4

    return kst