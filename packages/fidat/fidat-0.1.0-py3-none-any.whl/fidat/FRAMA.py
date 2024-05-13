import pandas as pd
import numpy as np

def Fractal_Adaptive_Moving_Average(data: pd.Series, period: int = 16, batch: int = 10) -> pd.Series:
    """
    Calculates the Fractal Adaptive Moving Average (FRAMA) of a given price series. The FRAMA indicator
    adapts its sensitivity to price movements based on the fractal dimension of the price series,
    which allows it to better handle varying market conditions compared to traditional moving averages.

    Parameters:
    data (pd.Series): Series containing the price data.
    period (int): The number of periods over which the FRAMA is calculated.
    batch (int): The batch size used to calculate the fractal dimension.

    Returns:
    pd.Series: A pandas Series containing the Fractal Adaptive Moving Average of the data.

    Example:
    # Assuming 'data' is a DataFrame and you want to calculate the FRAMA for the 'Close' column
    data['FRAMA'] = FRAMA(data['Close'], period=16, batch=10)
    """

    assert period % 2 == 0, print("FRAMA period must be even")

    # Calculate the fractal dimension of each batch
    def get_fractal_dimension(data):
        N = len(data)
        L = sum(np.sqrt((data - data.shift(1)) ** 2))
        L1 = sum(np.sqrt((data - data.shift(batch)) ** 2)) / (N/batch)
        return np.log(N) / (np.log(N) + np.log(L/L1))
    
    # Calculate the FRAMA
    N = len(data)
    frama = pd.Series(index=data.index, data=np.nan)
    alpha = pd.Series(index=data.index, data=np.nan)
    
    for i in range(period, N):
        D = get_fractal_dimension(data.iloc[i-period:i])
        alpha.iloc[i] = np.exp(-4.6 * (D - 1))  # Calculate alpha based on the fractal dimension
        if i == period:
            frama.iloc[i] = data.iloc[i]  # Initialize FRAMA
        else:
            frama.iloc[i] = alpha.iloc[i] * data.iloc[i] + (1 - alpha.iloc[i]) * frama.iloc[i-1]

    return frama