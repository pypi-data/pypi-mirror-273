import pandas as pd
import pytest

from fidat import (ADX, ALMA, CHANDELIER, CHAIKIN, DEMA, DMI, EIS, EMA, EMV, EVSTC, FRAMA, FVE, GHA, GMMA, HMA, ICHIMOKU, JMA, KAMA, KEI, KST, LWMA, MACD, MAMA, MI, PSAR, RMA, SAR, SMA, SMM, SSMA, STC, TEMA, TRIMA, TSI, VAMA, VIDYA, VORTEX, VPT, WMA, WTO, ZLEMA, SMMA, TP, WF, PAI)

from .utils.data import get_ohlcv_data

            
@pytest.mark.trends
def test_Trend_Strength_Indicator(get_ohlcv_data: pd.DataFrame):
    # Testing Trend Strength Indicator
    results = ADX(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[27] == 10.700505023667997
    assert results.iloc[99] == 13.772935249202968

    results = ADX(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[19] == 18.54161787640777
    assert results.iloc[99] == 18.75739025785043
            
@pytest.mark.trends
def test_Arnaud_Legoux_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Arnaud Legoux Moving Average
    results = ALMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[8] == 48.1355063983651
    assert results.iloc[99] == 45.56412668899954

    results = ALMA(get_ohlcv_data['close'], period=10, sigma=True, offset=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 48.703971253876624
    assert results.iloc[99] == 44.046988296329886

@pytest.mark.trends
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
            
@pytest.mark.trends
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
            
@pytest.mark.trends
def test_Double_Exponential_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Double Exponential Moving Average
    results = DEMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 42.671129173684655

    results = DEMA(get_ohlcv_data['close'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 42.72129591301064

@pytest.mark.trends
def test_Directional_Movement_Indicator(get_ohlcv_data: pd.DataFrame):
    results = DMI(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['+DI'].iloc[14] == 28.784773707886934
    assert results['+DI'].iloc[99] == 13.541910462032309
    assert results['-DI'].iloc[14] == 50.57283439719282
    assert results['-DI'].iloc[99] == 21.632459212589033
    assert results['DX'].iloc[14] == 27.4555410748465
    assert results['DX'].iloc[99] == 23.001261502047996

    results = DMI(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10, adjust=True)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['+DI'].iloc[10] == 8.438379853535
    assert results['+DI'].iloc[99] == 12.702775973094734
    assert results['-DI'].iloc[10] == 31.339199368847503
    assert results['-DI'].iloc[99] == 19.964665350774798
    assert results['DX'].iloc[10] == 57.572180014480146
    assert results['DX'].iloc[99] == 22.229746449024542
            
@pytest.mark.trends
def test_Elders_Impulse_System(get_ohlcv_data: pd.DataFrame):
    # Testing Elders Impulse System
    results = EIS(get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0
    assert results.iloc[99] == -1

    results = EIS(get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0
    assert results.iloc[99] == -1
            
@pytest.mark.trends
def test_Exponential_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Exponential Moving Average
    results = EMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 44.0700841485178

    results = EMA(get_ohlcv_data['close'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 44.242596250811374
            
@pytest.mark.trends
def test_Ease_of_Movement(get_ohlcv_data: pd.DataFrame):
    # Testing Ease of Movement
    results = EMV(get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 0.004900843638771172
    assert results.iloc[99] == 0.029993299097620035

    results = EMV(get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[1] == 0.004900843638771172
    assert results.iloc[99] == 0.00549975017299078
            
@pytest.mark.trends
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
            
@pytest.mark.trends
def test_Fractal_Adaptive_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Fractal Adaptive Moving Average
    results = FRAMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[16] == 41.33990264425568
    assert pd.notna(results.iloc[99]) == False

    results = FRAMA(get_ohlcv_data['close'], period=10, batch=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 51.44132536745886
    assert pd.notna(results.iloc[99]) == False
            
@pytest.mark.trends
def test_Finite_Volume_Elements(get_ohlcv_data: pd.DataFrame):
    # Testing Finite Volume Elements
    results = FVE(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[22] == 4090.2939135582674
    assert results.iloc[99] == 46.52219165675559

    results = FVE(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['volume'], period=10, factor=0.25)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 1886.6426476477936
    assert results.iloc[99] == 21.732835588940734
            
@pytest.mark.trends
def test_Gann_HiLo_Activator(get_ohlcv_data: pd.DataFrame):
    # Testing Gann HiLo Activator
    results = GHA(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 48.338620042021375
    assert results.iloc[99] == 45.040027476337734

    results = GHA(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 48.338620042021375
    assert results.iloc[99] == 45.040027476337734

@pytest.mark.trends
def test_Guppy_Multiple_Moving_Average(get_ohlcv_data: pd.DataFrame):
    results = GMMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Short Moving Avg'].iloc[2] == 48.9046324134566
    assert results['Short Moving Avg'].iloc[99] == 42.010953800411095
    assert pd.notna(results['Long Moving Avg'].iloc[2]) == False
    assert results['Long Moving Avg'].iloc[99] == 41.97289025672808

    results = GMMA(get_ohlcv_data['close'], short_period=10, long_period=20)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Short Moving Avg'].iloc[9] == 48.81743086848605
    assert results['Short Moving Avg'].iloc[99] == 43.88907126163223
    assert pd.notna(results['Long Moving Avg'].iloc[9]) == False
    assert results['Long Moving Avg'].iloc[99] == 46.66342282030748
            
@pytest.mark.trends
def test_Hull_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Hull Moving Average
    results = HMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[18] == 47.20028747159862
    assert results.iloc[99] == 39.904971207231114

    results = HMA(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[11] == 51.09929339798172
    assert results.iloc[99] == 39.746450099894616

@pytest.mark.trends
def test_Ichimoku_Cloud(get_ohlcv_data: pd.DataFrame):
    results = ICHIMOKU(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Tenkan-sen'].iloc[8] == 48.338620042021375
    assert results['Tenkan-sen'].iloc[99] == 45.040027476337734
    assert pd.notna(results['Kijun-sen'].iloc[8]) == False
    assert results['Kijun-sen'].iloc[99] == 45.9218048407776
    assert pd.notna(results['Senkou Span A'].iloc[8]) == False
    assert results['Senkou Span A'].iloc[99] == 48.713165014768386
    assert pd.notna(results['Senkou Span B'].iloc[8]) == False
    assert pd.notna(results['Senkou Span B'].iloc[99]) == False
    assert results['Chikou Span'].iloc[8] == 46.892002702152425
    assert pd.notna(results['Chikou Span'].iloc[99]) == False

    results = ICHIMOKU(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], tenkan_period=10, kijun_period=20, senkou_period=30, chikou_period=20)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Tenkan-sen'].iloc[9] == 48.338620042021375
    assert results['Tenkan-sen'].iloc[99] == 45.040027476337734
    assert pd.notna(results['Kijun-sen'].iloc[9]) == False
    assert results['Kijun-sen'].iloc[99] == 45.9218048407776
    assert pd.notna(results['Senkou Span A'].iloc[9]) == False
    assert results['Senkou Span A'].iloc[99] == 48.0973055900617
    assert pd.notna(results['Senkou Span B'].iloc[9]) == False
    assert results['Senkou Span B'].iloc[99] == 47.925201415443894
    assert results['Chikou Span'].iloc[9] == 48.418715033261705
    assert pd.notna(results['Chikou Span'].iloc[99]) == False
            
@pytest.mark.trends
def test_Jurik_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Jurik Moving Average
    results = JMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 8.938318068161724e-06

    results = JMA(get_ohlcv_data['close'], length=10, power=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 0.006904946908351663
            
@pytest.mark.trends
def test_Kaufman_Adaptive_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Kaufman Adaptive Moving Average
    results = KAMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[20] == 44.73207637760049
    assert results.iloc[99] == 46.46621120196576

    results = KAMA(get_ohlcv_data['close'], er_period=20, ema_fast=10, ema_slow=30, period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 51.44132536745886
    assert pd.notna(results.iloc[99]) == False
            
@pytest.mark.trends
def test_Kaufman_Efficiency_Indicator(get_ohlcv_data: pd.DataFrame):
    # Testing Kaufman Efficiency Indicator
    results = KEI(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 0.07359433294381504
    assert results.iloc[99] == 0.08150628943414509

    results = KEI(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[10] == 0.07359433294381504
    assert results.iloc[99] == 0.08150628943414509
            
@pytest.mark.trends
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
            
@pytest.mark.trends
def test_Linear_Weighted_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Linear Weighted Moving Average
    results = LWMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[13] == 48.44758947396452
    assert results.iloc[99] == 44.36163147359928

    results = LWMA(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 49.22936944897578
    assert results.iloc[99] == 43.13852979990859

@pytest.mark.trends
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
            
@pytest.mark.trends
def test_MESA_Adaptive_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing MESA Adaptive Moving Average
    results = MAMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert pd.notna(results.iloc[99]) == False

    results = MAMA(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert pd.notna(results.iloc[99]) == False
            
@pytest.mark.trends
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
            
@pytest.mark.trends
def test_Parabolic_Stop_and_Reversal(get_ohlcv_data: pd.DataFrame):
    # Testing Parabolic Stop and Reversal
    results = PSAR(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 53.068367583095565
    assert results.iloc[99] == 50.78837949699794

    results = PSAR(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'], iaf=True, maxaf=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 53.068367583095565
    assert results.iloc[99] == 50.46949241754382
            
@pytest.mark.trends
def test_Rainbow_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Rainbow Moving Average
    results = RMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[27] == 48.92364955878169
    assert results.iloc[99] == 47.4486447457792

    results = RMA(get_ohlcv_data['close'], length=10, colors=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[19] == 48.71724110376433
    assert results.iloc[99] == 46.551160522791626
            
@pytest.mark.trends
def test_Stop_and_Reversal(get_ohlcv_data: pd.DataFrame):
    # Testing Stop and Reversal
    results = SAR(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 50.78958308775094
    assert results.iloc[99] == 50.78837949699794

    results = SAR(get_ohlcv_data['high'], get_ohlcv_data['low'], af=True, amax=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 50.78958308775094
    assert results.iloc[99] == 50.46949241754382
            
@pytest.mark.trends
def test_Simple_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Simple Moving Average
    results = SMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[4] == 48.16100599731664
    assert results.iloc[99] == 41.97289025672808

    results = SMA(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 48.81743086848605
    assert results.iloc[99] == 43.88907126163223
            
@pytest.mark.trends
def test_Simple_Moving_Median(get_ohlcv_data: pd.DataFrame):
    # Testing Simple Moving Median
    results = SMM(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[8] == 48.207649487022884
    assert results.iloc[99] == 45.57650636451864

    results = SMM(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 48.228107443353444
    assert results.iloc[99] == 45.32384965139101
            
@pytest.mark.trends
def test_Smoothed_Simple_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Smoothed Simple Moving Average
    results = SSMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 45.14932960852692

    results = SSMA(get_ohlcv_data['close'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 45.32168700737358
            
@pytest.mark.trends
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
            
@pytest.mark.trends
def test_Triple_Exponential_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Triple Exponential Moving Average
    results = TEMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 42.60679285635747

    results = TEMA(get_ohlcv_data['close'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 48.207649487022884
    assert results.iloc[99] == 42.36521898391176
            
@pytest.mark.trends
def test_Triangular_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Triangular Moving Average
    results = TRIMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[12] == 48.79726009482008
    assert pd.notna(results.iloc[99]) == False

    results = TRIMA(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[6] == 49.01646315215263
    assert pd.notna(results.iloc[99]) == False

@pytest.mark.trends
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
            
@pytest.mark.trends
def test_Volume_Adjusted_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Volume Adjusted Moving Average
    results = VAMA(get_ohlcv_data['close'], get_ohlcv_data['volume'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[7] == 48.924418363394985
    assert results.iloc[99] == 43.49300429110027

    results = VAMA(get_ohlcv_data['close'], get_ohlcv_data['volume'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 48.79591611162177
    assert results.iloc[99] == 43.96957510449508
            
@pytest.mark.trends
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

@pytest.mark.trends
def test_Vortex_Oscillator(get_ohlcv_data: pd.DataFrame):
    results = VORTEX(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Vortex+'].iloc[13] == 4.36632360566966
    assert pd.notna(results['Vortex+'].iloc[99]) == False
    assert results['Vortex-'].iloc[13] == -25.777876893214223
    assert results['Vortex-'].iloc[99] == 7.9993084059904245

    results = VORTEX(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['Vortex+'].iloc[9] == -3.4531539744962405
    assert pd.notna(results['Vortex+'].iloc[99]) == False
    assert results['Vortex-'].iloc[9] == 2.8746154795725505
    assert results['Vortex-'].iloc[99] == 3.0920145033641755
            
@pytest.mark.trends
def test_Volume_Price_Trend(get_ohlcv_data: pd.DataFrame):
    results = VPT(get_ohlcv_data['open'], get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == -0.052675479365854816
            
@pytest.mark.trends
def test_Weighted_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Weighted Moving Average
    results = WMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[8] == 49.13630146152378
    assert results.iloc[99] == 42.97174280841444

    results = WMA(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[9] == 49.22936944897578
    assert results.iloc[99] == 43.13852979990859

@pytest.mark.trends
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
            
@pytest.mark.trends
def test_Zero_Lag_Exponential_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Zero Lag Exponential Moving Average
    results = ZLEMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[12] == 41.68601066430063
    assert results.iloc[99] == 44.05349050127013

    results = ZLEMA(get_ohlcv_data['close'], period=10, adjust=True)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[4] == 48.86327072858672
    assert results.iloc[99] == 41.47253617834666
            
@pytest.mark.trends
def test_Smoothed_Moving_Average(get_ohlcv_data: pd.DataFrame):
    # Testing Smoothed Moving Average
    results = SMMA(get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == 47.16015619428521

    results = SMMA(get_ohlcv_data['close'], period=10)
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 0.0
    assert results.iloc[99] == 45.32176755188475
            
@pytest.mark.trends
def test_Typical_Price(get_ohlcv_data: pd.DataFrame):
    results = TP(get_ohlcv_data['close'], get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 50.68853338595647
    assert results.iloc[99] == 48.21648936542325

@pytest.mark.trends
def test_Williams_Fractal(get_ohlcv_data: pd.DataFrame):
    results = WF(get_ohlcv_data['high'], get_ohlcv_data['low'])
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['BearishFractal'].iloc[3] == True
    assert results['BearishFractal'].iloc[99] == False
    assert results['BullishFractal'].iloc[3] == False
    assert results['BullishFractal'].iloc[99] == False

    results = WF(get_ohlcv_data['high'], get_ohlcv_data['low'], period=10)
    assert isinstance(results, pd.DataFrame), "Expected the results to be a pandas DataFrame"
    assert results['BearishFractal'].iloc[26] == True
    assert results['BearishFractal'].iloc[99] == False
    assert results['BullishFractal'].iloc[26] == False
    assert results['BullishFractal'].iloc[99] == False
            
@pytest.mark.trends
def test_Price_Action_Indicator(get_ohlcv_data: pd.DataFrame):
    results = PAI(get_ohlcv_data['open'], get_ohlcv_data['high'], get_ohlcv_data['low'], get_ohlcv_data['close'])
    assert isinstance(results, pd.Series), "Expected the results to be a pandas Series"
    assert results.iloc[0] == 1.7044839981915567
    assert results.iloc[99] == -0.10972711707059374
