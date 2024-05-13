import pandas as pd
import pytest

from fidat import (CCI, CFI, DEI, DI, DMMI, EFI, ERI, HLI, MAFI, MFI, MI, NVI, PVI, RSI, SMI, TSI, VIDYA)

from .utils.data import get_ohlcv_data

            
@pytest.mark.index
def test_Commodity_Channel_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Commodity Channel Index
    results = CCI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[38] == -87.68901341660654
    assert results.iloc[99] == 33.729994813739744

    results = CCI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], period=10, constant=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[18] == -1.216375806978682
    assert results.iloc[99] == 1.0771899466999597
            
@pytest.mark.index
def test_Cumulative_Force_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Cumulative Force Index
    results = CFI(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 2.0527492137894034
    assert results.iloc[99] == -143.77859286186464

    results = CFI(get_ohlcv_data['close'], get_ohlcv_data['volume'], adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 2.0527492137894034
    assert results.iloc[99] == -143.77859286186464
            
@pytest.mark.index
def test_Demand_Index(get_ohlcv_data: pd.DataFrame):
    results = DEI(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.04258140016434502
    assert results.iloc[98] == 10.426436159974312
            
@pytest.mark.index
def test_Disparity_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Disparity Index
    results = DI(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 1.7017374926218183
    assert results.iloc[99] == 11.09669341774109

    results = DI(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 1.7017374926218183
    assert results.iloc[99] == 11.09669341774109
            
@pytest.mark.index
def test_Dynamic_Momentum_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Dynamic Momentum Index
    results = DMMI(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 0.0207260048400641
    assert results.iloc[99] == 0.0002609413272472178

    results = DMMI(get_ohlcv_data['close'], adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 0.0207260048400641
    assert results.iloc[99] == 0.0002609413272472178
            
@pytest.mark.index
def test_Elder_Force_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Elder Force Index
    results = EFI(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == -20.176259961600344
    assert results.iloc[99] == 35.91550205161945

    results = EFI(get_ohlcv_data['close'], get_ohlcv_data['volume'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 26.420105103289167
    assert results.iloc[99] == 53.664834562161154

@pytest.mark.index
def test_Elder_Ray_Index(get_ohlcv_data: pd.DataFrame):
    results = ERI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Bull Power'].iloc[13] == -16.032263950744316
    assert results['Bull Power'].iloc[99] == -22.549252884327693
    assert results['Bear Power'].iloc[13] == -4.047336118522807
    assert results['Bear Power'].iloc[99] == -20.698714352762387
            
@pytest.mark.index
def test_High_Low_Index(get_ohlcv_data: pd.DataFrame):
    # Testing High Low Index
    results = HLI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 0.6056039778539308
    assert results.iloc[99] == 0.8425088390261848

    results = HLI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 0.6056039778539308
    assert results.iloc[99] == 0.8425088390261848
            
@pytest.mark.index
def test_Market_Facilitation_Index(get_ohlcv_data: pd.DataFrame):
    results = MAFI(get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == -52.11126924822747
    assert results.iloc[99] == -120.86597839328851
            
@pytest.mark.index
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
            
@pytest.mark.index
def test_Mass_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Mass Index
    results = MI(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 1.510501765653133
    assert results.iloc[99] == 1.0319888393539578

    results = MI(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 1.5053967479966017
    assert results.iloc[99] == 1.0311850655605137
            
@pytest.mark.index
def test_Negative_Volume_Index(get_ohlcv_data: pd.DataFrame):
    results = NVI(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 1000.0
    assert results.iloc[99] == 1779.5312150372247
            
@pytest.mark.index
def test_Positive_Volume_Index(get_ohlcv_data: pd.DataFrame):
    results = PVI(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 1000.0
    assert results.iloc[99] == 568.376295285682
            
@pytest.mark.index
def test_Relative_Strength_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Relative Strength Index
    results = RSI(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 100.0
    assert results.iloc[99] == 49.86430361554353

    results = RSI(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 100.0
    assert results.iloc[99] == 36.52961520463515
            
@pytest.mark.index
def test_CT_Reverse_Stochastic_Momentum_Index(get_ohlcv_data: pd.DataFrame):
    # Testing CT Reverse Stochastic Momentum Index
    results = SMI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[15] == -0.28704759964471777
    assert results.iloc[99] == 0.005683248984300411

    results = SMI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[11] == 0.057413125423076826
    assert results.iloc[99] == 0.16540570166183077

@pytest.mark.index
def test_True_Strength_Index(get_ohlcv_data: pd.DataFrame):
    results = TSI(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['TSI'].iloc[1] == 0.023759162102173718
    assert results['TSI'].iloc[99] == -0.3607005646871022
    assert results['Signal Line'].iloc[1] == 0.01279339497809354
    assert results['Signal Line'].iloc[99] == -0.14644055841743772

    results = TSI(get_ohlcv_data['close'], long=True, short=True, signal=True, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['TSI'].iloc[1] == 0.08480234038500141
    assert results['TSI'].iloc[99] == 16.97439566463457
    assert results['Signal Line'].iloc[1] == 0.08480234038500141
    assert results['Signal Line'].iloc[99] == 16.97439566463457
            
@pytest.mark.index
def test_Variable_Index_Dynamic_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Variable Index Dynamic Average
    results = VIDYA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert pd.notna(results.iloc[99]) == False

    results = VIDYA(get_ohlcv_data['close'], period=10, smoothing_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert pd.notna(results.iloc[99]) == False
