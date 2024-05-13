import pandas as pd

def Negative_Volume_Index(data: pd.Series, volume: pd.Series) -> pd.Series:
    """
    Negative Volume Index (NVI)
    """
    nvi = pd.Series(index=data.index, dtype='float64')
    nvi.iloc[0] = 1000

    for i in range(1, len(data)):
        if volume.iloc[i] < volume.iloc[i - 1]:
            nvi.iloc[i] = nvi.iloc[i - 1] * (1 + (data.iloc[i] - data.iloc[i - 1]) / data.iloc[i - 1])
        else:
            nvi.iloc[i] = nvi.iloc[i - 1]

    return nvi