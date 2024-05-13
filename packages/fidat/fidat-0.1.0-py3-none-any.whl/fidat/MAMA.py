import numpy as np
import pandas as pd

def MESA_Adaptive_Moving_Average(data: pd.Series, period: int = 16) -> pd.Series:
    """
    Calculates the MESA Adaptive Moving Average (MAMA) based on the cyclic components of the market prices.
    MAMA adapts more quickly to price changes than traditional moving averages by using digital signal processing
    techniques, specifically the Hilbert Transform, to estimate cycles.

    Parameters:
    data (pd.Series): Series containing the price data.
    period (int): The number of periods over which to calculate the MAMA.

    Returns:
    pd.Series: A pandas Series containing the MESA Adaptive Moving Average of the data.

    Example:
    # Assuming 'data' is a DataFrame and you want to calculate the MAMA for the 'Close' column
    data['MAMA'] = MAMA(data['Close'], period=16)
    """
    delta_phase = 0.1
    alpha = 0.5

    # Detrend price
    detrend = data - data.shift(1)

    # Hilbert Transform
    Q1 = detrend.shift(period // 2)
    I1 = detrend.shift(period // 4)

    # Compute InPhase and Quadrature components
    jI = 0.0962 * I1 + 0.5769 * I1.shift(2) - 0.5769 * I1.shift(4) - 0.0962 * I1.shift(6)
    jQ = 0.0962 * Q1 + 0.5769 * Q1.shift(2) - 0.5769 * Q1.shift(4) - 0.0962 * Q1.shift(6)

    # Calculate the phase
    phase = np.arctan(jQ / jI)
    phase = np.where(jI < 0, phase + np.pi, phase)
    phase = np.where((jI > 0) & (jQ < 0), phase + 2 * np.pi, phase)

    # Avoid division by zero
    dphase = np.diff(np.unwrap(phase))
    dphase = np.insert(dphase, 0, 0)  # prepend 0 to maintain array size
    safe_dphase = np.where(dphase != 0, dphase, np.finfo(float).eps)  # use epsilon to avoid zero

    # Calculate the adaptive alpha
    alpha = delta_phase / safe_dphase
    alpha = np.clip(alpha, 0.01, 1.0)

    # Smooth the alpha value
    mama = data.copy()
    for i in range(1, len(data)):
        mama.iloc[i] = alpha[i] * data.iloc[i] + (1 - alpha[i]) * mama.iloc[i - 1]

    return mama