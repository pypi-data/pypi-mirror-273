import pandas as pd

def Positive_Volume_Index(data: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Positive Volume Index (PVI)
    """
    pvi = pd.Series(index=data.index, dtype='float64')
    pvi.iloc[0] = 1000

    for i in range(1, len(data)):
        if volume.iloc[i] > volume.iloc[i - 1]:
            pvi.iloc[i] = pvi.iloc[i - 1] * (1 + (data.iloc[i] - data.iloc[i - 1]) / data.iloc[i - 1])
        else:
            pvi.iloc[i] = pvi.iloc[i - 1]

    return pvi