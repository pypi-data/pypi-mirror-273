import pandas as pd
import pytest

from fidat import (APZ, ATR, BB, BBWIDTH, CHANDELIER, KC, MOBO, MSD, PERCENT_B, SDC, VBM, TR, VC)

from .utils.data import get_ohlcv_data


@pytest.mark.volatility
def test_Adaptive_Price_Zone(get_ohlcv_data: pd.DataFrame):
    results = APZ(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[20] == 62.34240914033842
    assert results['Upper Band'].iloc[99] == 65.8031017084293
    assert results['Lower Band'].iloc[20] == 35.70985252735581
    assert results['Lower Band'].iloc[99] == 30.087059444410983

    results = APZ(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], period=10, dev_factor=True, MA=None, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[9] == 55.63631243464686
    assert results['Upper Band'].iloc[99] == 56.71470476304781
    assert results['Lower Band'].iloc[9] == 43.067748368707306
    assert results['Lower Band'].iloc[99] == 39.175456389792465
            
@pytest.mark.volatility
def test_Average_True_Range(get_ohlcv_data: pd.DataFrame):
    results = ATR(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == 5.648835924968135
    assert results.iloc[99] == 8.593916995664609

@pytest.mark.volatility
def test_Bollinger_Bands(get_ohlcv_data: pd.DataFrame):
    results = BB(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[19] == 56.22646983472684
    assert results['Upper Band'].iloc[99] == 58.21311517136721
    assert results['Middle Band'].iloc[19] == 48.382859801227866
    assert results['Middle Band'].iloc[99] == 46.66342282030748
    assert results['Lower Band'].iloc[19] == 40.53924976772889
    assert results['Lower Band'].iloc[99] == 35.113730469247756

    results = BB(get_ohlcv_data['close'], period=10, MA=None, std_multiplier=20)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[9] == 128.42009637517455
    assert results['Upper Band'].iloc[99] == 124.53829907182171
    assert results['Middle Band'].iloc[9] == 48.81743086848605
    assert results['Middle Band'].iloc[99] == 43.88907126163223
    assert results['Lower Band'].iloc[9] == -30.785234638202446
    assert results['Lower Band'].iloc[99] == -36.76015654855724
            
@pytest.mark.volatility
def test_Bollinger_Bands_Width(get_ohlcv_data: pd.DataFrame):
    # Testing Bollinger Bands Width
    results = BBWIDTH(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[19] == 0.16211546952212036
    assert results.iloc[99] == 0.24751061223124446

    results = BBWIDTH(get_ohlcv_data['close'], period=10, MA=None)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 0.16306197210815485
    assert results.iloc[99] == 0.18375697068051863

@pytest.mark.volatility
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

@pytest.mark.volatility
def test_Keltner_Channels(get_ohlcv_data: pd.DataFrame):
    results = KC(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[1] == 48.2933780659319
    assert results['Upper Band'].iloc[99] == 55.38170755325157
    assert results['Middle Band'].iloc[1] == 48.21154624060966
    assert results['Middle Band'].iloc[99] == 45.39820256242657
    assert results['Lower Band'].iloc[1] == 48.12971441528742
    assert results['Lower Band'].iloc[99] == 35.414697571601565

    results = KC(get_ohlcv_data['close'], period=10, atr_period=20, MA=None, kc_mult=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[1] == 48.25600465653147
    assert results['Upper Band'].iloc[99] == 49.781876487100604
    assert results['Middle Band'].iloc[1] == 48.21508874387035
    assert results['Middle Band'].iloc[99] == 44.2425962584538
    assert results['Lower Band'].iloc[1] == 48.17417283120923
    assert results['Lower Band'].iloc[99] == 38.703316029807

@pytest.mark.volatility
def test_Modified_Bollinger_Bands(get_ohlcv_data: pd.DataFrame):
    results = MOBO(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[9] == 52.00153748875359
    assert results['Upper Band'].iloc[99] == 47.11504037403981
    assert results['Middle Band'].iloc[9] == 48.81743086848605
    assert results['Middle Band'].iloc[99] == 43.88907126163223
    assert results['Lower Band'].iloc[9] == 45.63332424821851
    assert results['Lower Band'].iloc[99] == 40.663102149224656

    results = MOBO(get_ohlcv_data['close'], period=10, std_multiplier=20)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[9] == 128.42009637517455
    assert results['Upper Band'].iloc[99] == 124.53829907182171
    assert results['Middle Band'].iloc[9] == 48.81743086848605
    assert results['Middle Band'].iloc[99] == 43.88907126163223
    assert results['Lower Band'].iloc[9] == -30.785234638202446
    assert results['Lower Band'].iloc[99] == -36.76015654855724
            
@pytest.mark.volatility
def test_Moving_Standard_Deviation(get_ohlcv_data: pd.DataFrame):
    # Testing Moving Standard Deviation
    results = MSD(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[20] == 3.9046387776640348
    assert results.iloc[99] == 5.803036329574953

    results = MSD(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 3.980133275334425
    assert results.iloc[99] == 4.032461390509473
            
@pytest.mark.volatility
def test_Percentage_B(get_ohlcv_data: pd.DataFrame):
    # Testing Percentage B
    results = PERCENT_B(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[19] == 0.35093787738357024
    assert results.iloc[99] == 0.5907333312185448

    results = PERCENT_B(get_ohlcv_data['close'], period=10, MA=None)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 0.5521806976397017
    assert results.iloc[99] == 0.8019393870242315

@pytest.mark.volatility
def test_Standard_Deviation_Channel(get_ohlcv_data: pd.DataFrame):
    results = SDC(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[19] == 53.888099513589076
    assert results['Upper Band'].iloc[99] == 60.3089992944892
    assert results['Lower Band'].iloc[19] == 38.200879446591124
    assert results['Lower Band'].iloc[99] == 37.209614592369746

    results = SDC(get_ohlcv_data['close'], length=10, period=10)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Upper Band'].iloc[9] == 89.44950814585405
    assert results['Upper Band'].iloc[99] == 89.0839208485242
    assert results['Lower Band'].iloc[9] == 9.846842639165565
    assert results['Lower Band'].iloc[99] == 8.434693038334736
            
@pytest.mark.volatility
def test_Volatility_Based_Momentum(get_ohlcv_data: pd.DataFrame):
    # Testing Volatility Based Momentum
    results = VBM(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[25] == 1.034250026545512
    assert results.iloc[99] == -0.7364779615369783

    results = VBM(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], roc_period=10, atr_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[19] == -1.0739112661498014
    assert results.iloc[99] == -2.3314061377998745
            
@pytest.mark.volatility
def test_True_Range(get_ohlcv_data: pd.DataFrame):
    results = TR(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == -2.278784495344624
    assert results.iloc[99] == 17.006850291529965

@pytest.mark.volatility
def test_Value_chart(get_ohlcv_data: pd.DataFrame):
    results = VC(get_ohlcv_data['open'], get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Value Chart High'].iloc[4] == 4.724542683457763
    assert results['Value Chart High'].iloc[99] == 12.117220319157038
    assert results['Value Chart Low'].iloc[4] == -5.047584206530301
    assert results['Value Chart Low'].iloc[99] == -17.141401590351915
    assert results['Value Chart Close'].iloc[4] == 1.5029928366313376
    assert results['Value Chart Close'].iloc[99] == -3.7600970215095466
    assert results['Value Chart Open'].iloc[4] == -5.133631339420272
    assert results['Value Chart Open'].iloc[99] == -0.5496327899206188

    results = VC(get_ohlcv_data['open'], get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Value Chart High'].iloc[9] == 53.381615058930414
    assert results['Value Chart High'].iloc[99] == 16.528534103818593
    assert results['Value Chart Low'].iloc[9] == -60.50434754163913
    assert results['Value Chart Low'].iloc[99] == -19.392307538245543
    assert results['Value Chart Close'].iloc[9] == -5.619971787407352
    assert results['Value Chart Close'].iloc[99] == -2.9640655018220627
    assert results['Value Chart Open'].iloc[9] == -103.83567011778061
    assert results['Value Chart Open'].iloc[99] == 0.9774248943109672
