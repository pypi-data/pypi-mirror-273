import pandas as pd
import pytest

from fidat import (ADL, BASP, CHAIKIN, EVWMA, MFI, MAFI, BASPN, NVI, OBV, PVI, TMF, VFI, VP, VPT, VWAP, VZO, WOBV, VO)

from .utils.data import get_ohlcv_data

            
@pytest.mark.volume
def test_Accumulation_Distribution_Line(get_ohlcv_data: pd.DataFrame):
    results = ADL(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 158.34468430827695
    assert results.iloc[99] == -7533.460123198871

@pytest.mark.volume
def test_Buying_and_Selling_Pressure(get_ohlcv_data: pd.DataFrame):
    results = BASP(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Buying Pressure'].iloc[39] == 24.62102337718975
    assert results['Buying Pressure'].iloc[99] == 26.621995158529295
    assert results['Selling Pressure'].iloc[39] == 22.934061489735083
    assert results['Selling Pressure'].iloc[99] == 20.715916014579694

    results = BASP(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'], period=10)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Buying Pressure'].iloc[9] == 24.570490654790987
    assert results['Buying Pressure'].iloc[99] == 33.013596663184146
    assert results['Selling Pressure'].iloc[9] == 19.268929781763454
    assert results['Selling Pressure'].iloc[99] == 13.067180958737156
            
@pytest.mark.volume
def test_Chaikin_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Chaikin Oscillator
    results = CHAIKIN(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == -5.588947137058312

    results = CHAIKIN(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'], adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == -5.588947137058312
            
@pytest.mark.volume
def test_Exponential_Volume_Weighted_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Exponential Volume Weighted Moving Average
    results = EVWMA(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 45.41117456399061

    results = EVWMA(get_ohlcv_data['close'], get_ohlcv_data['volume'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 44.321137286264715
            
@pytest.mark.volume
def test_Money_Flow_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Money Flow Index
    results = MFI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == 47.27829249963798
    assert results.iloc[99] == 64.87241656634751

    results = MFI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 56.046568157419074
    assert results.iloc[99] == 71.64288097316981
            
@pytest.mark.volume
def test_Market_Facilitation_Index(get_ohlcv_data: pd.DataFrame):
    results = MAFI(get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == -52.11126924822747
    assert results.iloc[99] == -120.86597839328851

@pytest.mark.volume
def test_Normalized_BASP(get_ohlcv_data: pd.DataFrame):
    results = BASPN(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Normalized Buying Pressure'].iloc[39] == 0.6562019554397518
    assert results['Normalized Buying Pressure'].iloc[99] == 0.9924389583622975
    assert results['Normalized Selling Pressure'].iloc[39] == 0.3727301871859309
    assert results['Normalized Selling Pressure'].iloc[99] == 0.0

    results = BASPN(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'], period=10, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Normalized Buying Pressure'].iloc[9] == 0.548636300343767
    assert results['Normalized Buying Pressure'].iloc[99] == 0.9315611266793951
    assert results['Normalized Selling Pressure'].iloc[9] == 0.3081916968301146
    assert results['Normalized Selling Pressure'].iloc[99] == 0.0269203745615352
            
@pytest.mark.volume
def test_Negative_Volume_Index(get_ohlcv_data: pd.DataFrame):
    results = NVI(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 1000.0
    assert results.iloc[99] == 1779.5312150372247
            
@pytest.mark.volume
def test_On_Balance_Volume(get_ohlcv_data: pd.DataFrame):
    results = OBV(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == 284.41421480209317
            
@pytest.mark.volume
def test_Positive_Volume_Index(get_ohlcv_data: pd.DataFrame):
    results = PVI(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 1000.0
    assert results.iloc[99] == 568.376295285682
            
@pytest.mark.volume
def test_Twiggs_Money_Flow(get_ohlcv_data: pd.DataFrame):
    # Testing Twiggs Money Flow
    results = TMF(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[21] == 58.33318132306988
    assert results.iloc[99] == 0.8397118658663151

    results = TMF(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 32.69508524224989
    assert results.iloc[99] == -99.78508596583013
            
@pytest.mark.volume
def test_Volume_Flow_Indicator(get_ohlcv_data: pd.DataFrame):
    # Testing Volume Flow Indicator
    results = VFI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == -0.031146107186536907
    assert results.iloc[99] == -0.021298767027100922

    results = VFI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'], long_period=20, smoothing_factor=10, factor=0.25, vfactor=3.5, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[20] == -0.011145621779615136
    assert results.iloc[99] == -0.0051108805880760826
            
@pytest.mark.volume
def test_Volume_Profile(get_ohlcv_data: pd.DataFrame):
    # Testing Volume Profile
    results = VP(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 633.6564340816057
    assert results.iloc[99] == 633.6564340816057

    results = VP(get_ohlcv_data['close'], get_ohlcv_data['volume'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 1205.7376033543926
    assert results.iloc[99] == 1205.7376033543926
            
@pytest.mark.volume
def test_Volume_Price_Trend(get_ohlcv_data: pd.DataFrame):
    results = VPT(get_ohlcv_data['open'], get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == -0.052675479365854816
            
@pytest.mark.volume
def test_Volume_Weighted_Average_Price(get_ohlcv_data: pd.DataFrame):
    results = VWAP(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == 27800.16992050397
            
@pytest.mark.volume
def test_Volume_Zone_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Volume Zone Oscillator
    results = VZO(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 100.00000000000001
    assert results.iloc[99] == 2.854509217253091

    results = VZO(get_ohlcv_data['close'], get_ohlcv_data['volume'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 100.00000000000001
    assert results.iloc[99] == 3.405037010570951
            
@pytest.mark.volume
def test_Weighted_On_Balance_Volume(get_ohlcv_data: pd.DataFrame):
    results = WOBV(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 2.0527492137894034
    assert results.iloc[99] == -143.77859286186464
            
@pytest.mark.volume
def test_Volume_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Volume Oscillator
    results = VO(get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[25] == 0.5543660054693618
    assert results.iloc[99] == -0.6652772610665139

    results = VO(get_ohlcv_data['volume'], short_period=10, long_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[19] == -1.6168246420043815
    assert results.iloc[99] == -0.7241453420862101
