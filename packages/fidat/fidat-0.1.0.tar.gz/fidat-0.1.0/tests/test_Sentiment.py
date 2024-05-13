import pandas as pd
import pytest

from fidat import (BC, BEARP, BULLP, BPBP, ERI, HA)

from .utils.data import get_ohlcv_data

            
@pytest.mark.sentiment
def test_Beta_Coefficient(get_ohlcv_data: pd.DataFrame):
    # Testing Beta Coefficient
    results = BC(get_ohlcv_data['close'], get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[24] == 0.9999999999999868
    assert results.iloc[99] == 1.000000000000013

    results = BC(get_ohlcv_data['close'], get_ohlcv_data['close'], window=30)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[29] == 0.9999999999999881
    assert results.iloc[99] == 1.000000000000019
            
@pytest.mark.sentiment
def test_Bear_Power(get_ohlcv_data: pd.DataFrame):
    results = BEARP(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[12] == 2.5205734717823134
    assert results.iloc[99] == 12.352580049358075
            
@pytest.mark.sentiment
def test_Bull_Power(get_ohlcv_data: pd.DataFrame):
    results = BULLP(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[12] == -1.228170915609219
    assert results.iloc[99] == -10.41205576141708

@pytest.mark.sentiment
def test_Power_Indicators(get_ohlcv_data: pd.DataFrame):
    results = BPBP(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Bull Power'].iloc[12] == -1.228170915609219
    assert results['Bull Power'].iloc[99] == -10.41205576141708
    assert results['Bear Power'].iloc[12] == 2.5205734717823134
    assert results['Bear Power'].iloc[99] == 12.352580049358075

@pytest.mark.sentiment
def test_Elder_Ray_Index(get_ohlcv_data: pd.DataFrame):
    results = ERI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Bull Power'].iloc[13] == -16.032263950744316
    assert results['Bull Power'].iloc[99] == -22.549252884327693
    assert results['Bear Power'].iloc[13] == -4.047336118522807
    assert results['Bear Power'].iloc[99] == -20.698714352762387

@pytest.mark.sentiment
def test_Heikin_Ashi(get_ohlcv_data: pd.DataFrame):
    results = HA(get_ohlcv_data['open'], get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['HA_Open'].iloc[4] == 48.663021533471074
    assert results['HA_Open'].iloc[99] == 43.90012870279844
    assert results['HA_High'].iloc[4] == 50.283059719919336
    assert results['HA_High'].iloc[99] == 47.828549679011395
    assert results['HA_Low'].iloc[4] == 48.663021533471074
    assert results['HA_Low'].iloc[99] == 43.90012870279844
    assert results['HA_Close'].iloc[4] == 50.283059719919336
    assert results['HA_Close'].iloc[99] == 47.828549679011395
