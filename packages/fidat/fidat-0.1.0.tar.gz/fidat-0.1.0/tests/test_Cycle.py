import pandas as pd
import pytest

from fidat import (STC, EVSTC, COPP, DPO, KST, PSK, PRSK, WTO, WP)

from .utils.data import get_ohlcv_data

            
@pytest.mark.cycle
def test_Schaff_Trend_Cycle(get_ohlcv_data: pd.DataFrame):
    # Testing Schaff Trend Cycle
    results = STC(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == 63.12811508906577
    assert results.iloc[99] == 2.6905787053964385

    results = STC(get_ohlcv_data['close'], fast_period=10, slow_period=20, k_period=10, d_period=20, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[47] == 43.041160023925194
    assert results.iloc[99] == 56.48297811195012
            
@pytest.mark.cycle
def test_Schaff_Trend_Cycle_EVWMA_MACD(get_ohlcv_data: pd.DataFrame):
    # Testing Schaff Trend Cycle EVWMA MACD
    results = EVSTC(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == 57.50986617906114
    assert results.iloc[99] == 2.1857760474153136

    results = EVSTC(get_ohlcv_data['close'], get_ohlcv_data['volume'], period_fast=10, period_slow=20, k_period=10, d_period=20, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[47] == 41.14524744922375
    assert results.iloc[99] == 56.63847989770943
            
@pytest.mark.cycle
def test_Coppock_Curve(get_ohlcv_data: pd.DataFrame):
    # Testing Coppock Curve
    results = COPP(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[14] == 0.546217621895722
    assert results.iloc[99] == 0.3776282084270345

    results = COPP(get_ohlcv_data['close'], adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[14] == 0.546217621895722
    assert results.iloc[99] == 0.3776282084270345
            
@pytest.mark.cycle
def test_Detrended_Price_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Detrended Price Oscillator
    results = DPO(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[30] == 3.8041214336030507
    assert results.iloc[99] == 2.1261911675847003

    results = DPO(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[15] == -0.5186725521773212
    assert results.iloc[99] == -0.06180876736279828
            
@pytest.mark.cycle
def test_Know_Sure_Thing(get_ohlcv_data: pd.DataFrame):
    # Testing Know Sure Thing
    results = KST(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[35] == 0.5443993116798997
    assert results.iloc[99] == -0.8556889493274726

    results = KST(get_ohlcv_data['close'], r1=5, r2=10, r3=20, r4=30)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[35] == 0.3701390547962935
    assert results.iloc[99] == -0.96871186982012
            
@pytest.mark.cycle
def test_Prings_Special_K(get_ohlcv_data: pd.DataFrame):
    # Testing Prings Special K
    results = PSK(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == -102.62202269604828

    results = PSK(get_ohlcv_data['close'], short_period=10, long_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == -61.646239878963705
            
@pytest.mark.cycle
def test_Price_Swing_Kaufman(get_ohlcv_data: pd.DataFrame):
    # Testing Price Swing Kaufman
    results = PRSK(get_ohlcv_data['open'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == -70.44839981915568
    assert results.iloc[99] == -303.271366119251

    results = PRSK(get_ohlcv_data['open'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['close'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == -70.44839981915568
    assert results.iloc[99] == -303.271366119251

@pytest.mark.cycle
def test_Wave_Trend_Oscillator(get_ohlcv_data: pd.DataFrame):
    results = WTO(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Wave_Trend1'].iloc[1] == -121.21212121212122
    assert results['Wave_Trend1'].iloc[99] == -22.641246928876676
    assert pd.notna(results['Wave_Trend2'].iloc[1]) == False
    assert results['Wave_Trend2'].iloc[99] == -26.006851530875224

    results = WTO(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], channel_length=10, average_length=20, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Wave_Trend1'].iloc[1] == -121.21212121212122
    assert results['Wave_Trend1'].iloc[99] == -22.65466793164888
    assert pd.notna(results['Wave_Trend2'].iloc[1]) == False
    assert results['Wave_Trend2'].iloc[99] == -26.43537539601306
            
@pytest.mark.cycle
def test_Wave_PM(get_ohlcv_data: pd.DataFrame):
    # Testing Wave PM
    results = WP(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[22] == 0.8170009668101688
    assert results.iloc[99] == 0.7994878194271271

    results = WP(get_ohlcv_data['close'], period=10, lookback_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[28] == 0.7703400039668921
    assert results.iloc[99] == 0.6353079529256073
