import pandas as pd
import pytest

from fidat import (AO, ARO, BOP, CCI, CMO, DMMI, EFT, EVW_MACD, FISH, HMAO, HPO, IFT_RSI, MACD, MOM, PPO, PZO, ROC, RSI, STC, STOCH, STOCHRSI, TSI, UO, VBM, VW_MACD, ZCO, QSTICK, SMO, STOCHD, ARSI, ASI, WILLIAMS)

from .utils.data import get_ohlcv_data

            
@pytest.mark.momentum
def test_Awesome_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Awesome Oscillator
    results = AO(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[33] == 2.0037392676818158
    assert results.iloc[99] == -1.1713870957806805

    results = AO(get_ohlcv_data['high'], get_ohlcv_data['low'], slow_period=20, fast_period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[19] == -0.8426375021259176
    assert results.iloc[99] == -0.3755515495979509
            
@pytest.mark.momentum
def test_Aroon_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Aroon Oscillator
    results = ARO(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[14] == -14.285714285714285
    assert results.iloc[99] == -71.42857142857143

    results = ARO(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == -20.0
    assert results.iloc[99] == 20.0
            
@pytest.mark.momentum
def test_Balance_of_Power(get_ohlcv_data: pd.DataFrame):
    results = BOP(get_ohlcv_data['open'], get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 1.7044839981915567
    assert results.iloc[99] == -0.10972711707059374
            
@pytest.mark.momentum
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
            
@pytest.mark.momentum
def test_Chande_Momentum_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Chande Momentum Oscillator
    results = CMO(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == 1.2557086055385167

    results = CMO(get_ohlcv_data['close'], period=10, factor=0.25)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == -0.06735192397682427
            
@pytest.mark.momentum
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
            
@pytest.mark.momentum
def test_Ehlers_Fisher_Transform(get_ohlcv_data: pd.DataFrame):
    # Testing Ehlers Fisher Transform
    results = EFT(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.05142292043204571
    assert pd.notna(results.iloc[99]) == False

    results = EFT(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.05142292043204571
    assert pd.notna(results.iloc[99]) == False

@pytest.mark.momentum
def test_Elastic_Volume_Weighted_MACD(get_ohlcv_data: pd.DataFrame):
    results = EVW_MACD(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Elastic_VW_MACD'].iloc[1] == 0.0005106436077824128
    assert results['Elastic_VW_MACD'].iloc[99] == -0.8324712896717159
    assert results['Elastic_VW_Signal'].iloc[1] == 0.00028369089321245156
    assert results['Elastic_VW_Signal'].iloc[99] == -0.46842772016801487
    assert results['Elastic_VW_Histogram'].iloc[1] == 0.00022695271456996124
    assert results['Elastic_VW_Histogram'].iloc[99] == -0.36404356950370104

    results = EVW_MACD(get_ohlcv_data['close'], get_ohlcv_data['volume'], period_fast=10, period_slow=20, signal=True, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Elastic_VW_MACD'].iloc[1] == 0.0010199787471805166
    assert results['Elastic_VW_MACD'].iloc[99] == -1.0899147797008197
    assert results['Elastic_VW_Signal'].iloc[1] == 0.0010199787471805166
    assert results['Elastic_VW_Signal'].iloc[99] == -1.0899147797008197
    assert results['Elastic_VW_Histogram'].iloc[1] == 0.0
    assert results['Elastic_VW_Histogram'].iloc[99] == 0.0
            
@pytest.mark.momentum
def test_Fisher_Transform(get_ohlcv_data: pd.DataFrame):
    # Testing Fisher Transform
    results = FISH(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 0.1649242650340237
    assert results.iloc[99] == 0.5971987948323685

    results = FISH(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 0.1649242650340237
    assert results.iloc[99] == 0.5971987948323685
            
@pytest.mark.momentum
def test_Hull_Moving_Average_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Hull Moving Average Oscillator
    results = HMAO(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[15] == 49.69
    assert results.iloc[99] == 39.84

    results = HMAO(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[11] == 51.83
    assert results.iloc[99] == 38.69
            
@pytest.mark.momentum
def test_High_Pass_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing High Pass Oscillator
    results = HPO(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == -3.1123865215515636
    assert results.iloc[99] == 2.715203944819862

    results = HPO(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 0.8307445240237641
    assert results.iloc[99] == 4.87023568179724
            
@pytest.mark.momentum
def test_Inverse_Fisher_Transform_RSI(get_ohlcv_data: pd.DataFrame):
    # Testing Inverse Fisher Transform RSI
    results = IFT_RSI(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[12] == 0.02717075172702679
    assert results.iloc[99] == -0.36246996805000886

    results = IFT_RSI(get_ohlcv_data['close'], rsi_period=10, wma_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[28] == 0.054931133713440196
    assert results.iloc[99] == -0.09301043263309205

@pytest.mark.momentum
def test_Moving_Average_Convergence_Divergence(get_ohlcv_data: pd.DataFrame):
    results = MACD(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['MACD'].iloc[1] == 0.000917985219956563
    assert results['MACD'].iloc[99] == -1.2016937776355903
    assert results['Signal'].iloc[1] == 0.0005099917888647573
    assert results['Signal'].iloc[99] == -0.6937222981514408
    assert results['Histogram'].iloc[1] == 0.00040799343109180575
    assert results['Histogram'].iloc[99] == -0.5079714794841494

    results = MACD(get_ohlcv_data['close'], period_fast=10, period_slow=20, signal=True, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['MACD'].iloc[1] == 0.0010228978165258695
    assert results['MACD'].iloc[99] == -1.155479817300261
    assert results['Signal'].iloc[1] == 0.0010228978165258695
    assert results['Signal'].iloc[99] == -1.155479817300261
    assert results['Histogram'].iloc[1] == 0.0
    assert results['Histogram'].iloc[99] == 0.0
            
@pytest.mark.momentum
def test_Market_Momentum(get_ohlcv_data: pd.DataFrame):
    # Testing Market Momentum
    results = MOM(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 3.2336758804359746
    assert results.iloc[99] == -12.190547542690425

    results = MOM(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 3.2336758804359746
    assert results.iloc[99] == -12.190547542690425

@pytest.mark.momentum
def test_Percentage_Price_Oscillator(get_ohlcv_data: pd.DataFrame):
    results = PPO(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['PPO'].iloc[1] == 0.001903392631143629
    assert results['PPO'].iloc[99] == -2.626027559573435
    assert results['Signal'].iloc[1] == 0.0010574403506353493
    assert results['Signal'].iloc[99] == -1.5256946117693007
    assert results['Histogram'].iloc[1] == 0.0008459522805082797
    assert results['Histogram'].iloc[99] == -1.1003329478041342

    results = PPO(get_ohlcv_data['close'], period_fast=10, period_slow=20, signal=True, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['PPO'].iloc[1] == 0.002120912836889141
    assert results['PPO'].iloc[99] == -2.545217589323987
    assert results['Signal'].iloc[1] == 0.002120912836889141
    assert results['Signal'].iloc[99] == -2.545217589323987
    assert results['Histogram'].iloc[1] == 0.0
    assert results['Histogram'].iloc[99] == 0.0
            
@pytest.mark.momentum
def test_Price_Zone_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Price Zone Oscillator
    results = PZO(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == 2.715203944819862

    results = PZO(get_ohlcv_data['close'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == 4.87023568179724
            
@pytest.mark.momentum
def test_Rate_of_Change(get_ohlcv_data: pd.DataFrame):
    # Testing Rate of Change
    results = ROC(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[12] == -6.764112015540014
    assert results.iloc[99] == -6.31928403849813

    results = ROC(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 6.70780657187291
    assert results.iloc[99] == -20.000946098184002
            
@pytest.mark.momentum
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
            
@pytest.mark.momentum
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
            
@pytest.mark.momentum
def test_Stochastic_Oscillator(get_ohlcv_data: pd.DataFrame):
    # Testing Stochastic Oscillator
    results = STOCH(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == 8.056088502327146
    assert results.iloc[99] == -9.966695256234512

    results = STOCH(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == -7.8861207153336474
    assert results.iloc[99] == -11.14254301705343
            
@pytest.mark.momentum
def test_Stochastic_Oscillator_RSI(get_ohlcv_data: pd.DataFrame):
    # Testing Stochastic Oscillator RSI
    results = STOCHRSI(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[26] == 41.332826263506455
    assert results.iloc[99] == 53.05099413415889

    results = STOCHRSI(get_ohlcv_data['close'], rsi_period=10, stoch_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[28] == 71.37284726703584
    assert results.iloc[99] == 0.0

@pytest.mark.momentum
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
            
@pytest.mark.momentum
def test_Ultimate_Oscillator(get_ohlcv_data: pd.DataFrame):
    results = UO(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[46] == -11.821188169180749
    assert results.iloc[99] == -24.254923475924574
            
@pytest.mark.momentum
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

@pytest.mark.momentum
def test_Volume_Weighted_MACD(get_ohlcv_data: pd.DataFrame):
    results = VW_MACD(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['VW_MACD'].iloc[1] == 0.0009158068965788857
    assert results['VW_MACD'].iloc[99] == -1.128970836814581
    assert results['VW_Signal'].iloc[1] == 0.0005087816092104921
    assert results['VW_Signal'].iloc[99] == -0.6485028187292466
    assert results['VW_Histogram'].iloc[1] == 0.0004070252873683936
    assert results['VW_Histogram'].iloc[99] == -0.48046801808533435

    results = VW_MACD(get_ohlcv_data['close'], get_ohlcv_data['volume'], period_fast=10, period_slow=20, signal=True, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['VW_MACD'].iloc[1] == 0.0010199787471805166
    assert results['VW_MACD'].iloc[99] == -1.0899147797008197
    assert results['VW_Signal'].iloc[1] == 0.0010199787471805166
    assert results['VW_Signal'].iloc[99] == -1.0899147797008197
    assert results['VW_Histogram'].iloc[1] == 0.0
    assert results['VW_Histogram'].iloc[99] == 0.0
            
@pytest.mark.momentum
def test_Zero_Cross_Indicator(get_ohlcv_data: pd.DataFrame):
    results = ZCO(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0
    assert results.iloc[98] == 0
            
@pytest.mark.momentum
def test_QStick(get_ohlcv_data: pd.DataFrame):
    # Testing QStick
    results = QSTICK(get_ohlcv_data['open'], get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.8136930571410791
    assert results.iloc[13] == 0.14961259454668863

    results = QSTICK(get_ohlcv_data['open'], get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == -0.015838189298814597
    assert results.iloc[9] == 0.20945763236536408

@pytest.mark.momentum
def test_Squeeze_Momentum_Indicator(get_ohlcv_data: pd.DataFrame):
    results = SMO(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Squeeze Momentum'].iloc[19] == -2.3383703211377664
    assert results['Squeeze Momentum'].iloc[99] == 2.0958841231219907
    assert results['Upper Band'].iloc[19] == 56.22646983472684
    assert results['Upper Band'].iloc[99] == 58.21311517136721
    assert results['Lower Band'].iloc[19] == 40.53924976772889
    assert results['Lower Band'].iloc[99] == 35.113730469247756

    results = SMO(get_ohlcv_data['close'], period=10, MA=None)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Squeeze Momentum'].iloc[9] == 0.8307445240237641
    assert results['Squeeze Momentum'].iloc[99] == 4.87023568179724
    assert results['Upper Band'].iloc[9] == 56.7776974191549
    assert results['Upper Band'].iloc[99] == 51.953994042651175
    assert results['Lower Band'].iloc[9] == 40.8571643178172
    assert results['Lower Band'].iloc[99] == 35.82414848061329
            
@pytest.mark.momentum
def test_Stochastic_Oscillator_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Stochastic Oscillator Moving Average
    results = STOCHD(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[15] == 20.14221565748014
    assert results.iloc[99] == 42.22590190732571

    results = STOCHD(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10, stoch_period=20)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[28] == 65.62894766893062
    assert results.iloc[99] == 41.00267760693152
            
@pytest.mark.momentum
def test_Adaptive_Relative_Strength_Index(get_ohlcv_data: pd.DataFrame):
    # Testing Adaptive Relative Strength Index
    results = ARSI(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == 45.282685647721365
    assert results.iloc[99] == 51.96377826551337

    results = ARSI(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 51.5181160686873
    assert results.iloc[99] == 53.47669782981356
            
@pytest.mark.momentum
def test_Accumulative_Swing_Index(get_ohlcv_data: pd.DataFrame):
    results = ASI(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == -0.24986915030994414
    assert results.iloc[98] == -410.1833389007513
            
@pytest.mark.momentum
def test_Williams_Percent_Range(get_ohlcv_data: pd.DataFrame):
    # Testing Williams Percent Range
    results = WILLIAMS(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == -73.55092679073103
    assert results.iloc[99] == -24.63992432960371

    results = WILLIAMS(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == -39.439602214606914
    assert results.iloc[99] == -15.749116097381519
