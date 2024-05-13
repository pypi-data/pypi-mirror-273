import pandas as pd
import pytest

from fidat import (CHANDELIER, DC, PIVOT, PIVOT_FIB)

from .utils.data import get_ohlcv_data


@pytest.mark.barriers
def test_Chandelier_Exit(get_ohlcv_data: pd.DataFrame):
    results = CHANDELIER(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Short Chandelier Exit'].iloc[21] == 9.562661591798822
    assert results['Short Chandelier Exit'].iloc[99] == 10.735710512529522
    assert results['Long Chandelier Exit'].iloc[21] == 9.562661591798822
    assert results['Long Chandelier Exit'].iloc[99] == 10.735710512529522

    results = CHANDELIER(get_ohlcv_data['high'], get_ohlcv_data['low'], short_period=10, long_period=20, k_period=10)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Short Chandelier Exit'].iloc[9] == -79.24660223069148
    assert results['Short Chandelier Exit'].iloc[99] == -70.21941573997233
    assert pd.notna(results['Long Chandelier Exit'].iloc[9]) == False
    assert results['Long Chandelier Exit'].iloc[99] == -86.09140829988986

@pytest.mark.barriers
def test_Donchian_Channels(get_ohlcv_data: pd.DataFrame):
    results = DC(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Channel'].iloc[19] == 56.11692024617297
    assert results['Upper Channel'].iloc[99] == 52.233047146423544
    assert results['Lower Channel'].iloc[19] == 39.31399048768409
    assert results['Lower Channel'].iloc[99] == 39.61056253513165

    results = DC(get_ohlcv_data['high'], get_ohlcv_data['low'], upper_period=20, lower_period=10)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Channel'].iloc[19] == 56.11692024617297
    assert results['Upper Channel'].iloc[99] == 52.233047146423544
    assert results['Lower Channel'].iloc[19] == 39.31399048768409
    assert results['Lower Channel'].iloc[99] == 39.61056253513165

@pytest.mark.barriers
def test_Pivot_Points(get_ohlcv_data: pd.DataFrame):
    results = PIVOT(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Pivot Point'].iloc[1] == 51.549177919532475
    assert results['Pivot Point'].iloc[99] == 47.94899637578991
    assert results['Support 1'].iloc[1] == 52.30877275131401
    assert results['Support 1'].iloc[99] == 45.428500334036
    assert results['Resistance 1'].iloc[1] == 50.029988255969386
    assert results['Resistance 1'].iloc[99] == 52.98998845929771
    assert results['Support 2'].iloc[1] == 53.8279624148771
    assert results['Support 2'].iloc[99] == 40.3875082505282
    assert results['Resistance 2'].iloc[1] == 49.27039342418785
    assert results['Resistance 2'].iloc[99] == 55.51048450105162

@pytest.mark.barriers
def test_Fibonacci_Pivot_Points(get_ohlcv_data: pd.DataFrame):
    results = PIVOT_FIB(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['R1'].iloc[1] == 51.549177919532475
    assert results['R1'].iloc[99] == 47.94899637578991
    assert results['R2'].iloc[1] == 50.67868224231083
    assert results['R2'].iloc[99] == 50.837484839639885
    assert results['R3'].iloc[1] == 50.1408891014095
    assert results['R3'].iloc[99] == 52.62199603720165
    assert results['R4'].iloc[1] == 49.27039342418785
    assert results['R4'].iloc[99] == 55.51048450105162
    assert results['S1'].iloc[1] == 51.549177919532475
    assert results['S1'].iloc[99] == 47.94899637578991
    assert results['S2'].iloc[1] == 52.41967359675412
    assert results['S2'].iloc[99] == 45.060507911939936
    assert results['S3'].iloc[1] == 52.95746673765545
    assert results['S3'].iloc[99] == 43.275996714378174
    assert results['S4'].iloc[1] == 53.8279624148771
    assert results['S4'].iloc[99] == 40.3875082505282
