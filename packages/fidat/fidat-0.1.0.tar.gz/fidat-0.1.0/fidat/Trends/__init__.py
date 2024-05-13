"""
Trend Indicators
----------------

Trend indicators are a class of technical analysis tools designed to help traders identify and follow the direction of market trends. These indicators smooth out price data over time, providing a clearer picture of the underlying trend by filtering out short-term fluctuations. The main purpose of trend indicators is to show whether an asset is in an uptrend, downtrend, or sideways movement and to signal potential reversals or continuations of these trends.

Definition and Purpose
• Definition: Trend indicators analyze price movements to establish the direction and strength of a market trend.
• Purpose: They help traders determine the overall market direction and make decisions about entry and exit points based on the continuation or reversal of trends.

Application and Importance
• Application: Trend indicators are utilized in various market conditions, whether the market is moving upward, downward, or sideways. They can be adapted for short-term trading, day trading, or long-term investment strategies.
• Importance: By clearly defining the direction of market trends, these indicators assist traders in making informed decisions about buying and selling, helping to reduce risks associated with potential price volatility and market reversals.

Overall, trend indicators are vital for traders who rely on technical analysis to navigate financial markets. They provide essential information on market trends, aiding in the optimization of trading strategies and the enhancement of potential returns on investments.

"""

from ..ADX import Trend_Strength_Indicator as ADX
from ..ALMA import Arnaud_Legoux_Moving_Average as ALMA
from ..CHANDELIER import Chandelier_Exit as CHANDELIER
from ..CHAIKIN import Chaikin_Oscillator as CHAIKIN
from ..DEMA import Double_Exponential_Moving_Average as DEMA
from ..DMI import Directional_Movement_Indicator as DMI
from ..EIS import Elders_Impulse_System as EIS
from ..EMA import Exponential_Moving_Average as EMA
from ..EMV import Ease_of_Movement as EMV
from ..EVSTC import Schaff_Trend_Cycle_EVWMA_MACD as EVSTC
from ..FRAMA import Fractal_Adaptive_Moving_Average as FRAMA
from ..FVE import Finite_Volume_Elements as FVE
from ..GHA import Gann_HiLo_Activator as GHA
from ..GMMA import Guppy_Multiple_Moving_Average as GMMA
from ..HMA import Hull_Moving_Average as HMA
from ..ICHIMOKU import Ichimoku_Cloud as ICHIMOKU
from ..JMA import Jurik_Moving_Average as JMA
from ..KAMA import Kaufman_Adaptive_Moving_Average as KAMA
from ..KEI import Kaufman_Efficiency_Indicator as KEI
from ..KST import Know_Sure_Thing as KST
from ..LWMA import Linear_Weighted_Moving_Average as LWMA
from ..MACD import Moving_Average_Convergence_Divergence as MACD
from ..MAMA import MESA_Adaptive_Moving_Average as MAMA
from ..MI import Mass_Index as MI
from ..PSAR import Parabolic_Stop_and_Reversal as PSAR
from ..RMA import Rainbow_Moving_Average as RMA
from ..SAR import Stop_and_Reversal as SAR
from ..SMA import Simple_Moving_Average as SMA
from ..SMM import Simple_Moving_Median as SMM
from ..SSMA import Smoothed_Simple_Moving_Average as SSMA
from ..STC import Schaff_Trend_Cycle as STC
from ..TEMA import Triple_Exponential_Moving_Average as TEMA
from ..TRIMA import Triangular_Moving_Average as TRIMA
from ..TSI import True_Strength_Index as TSI
from ..VAMA import Volume_Adjusted_Moving_Average as VAMA
from ..VIDYA import Variable_Index_Dynamic_Average as VIDYA
from ..VORTEX import Vortex_Oscillator as VORTEX
from ..VPT import Volume_Price_Trend as VPT
from ..WMA import Weighted_Moving_Average as WMA
from ..WTO import Wave_Trend_Oscillator as WTO
from ..ZLEMA import Zero_Lag_Exponential_Moving_Average as ZLEMA

from ..SMMA import Smoothed_Moving_Average as SMMA
from ..TP import Typical_Price as TP
from ..WF import Williams_Fractal as WF
from ..PAI import Price_Action_Indicator as PAI

ALL = [ADX, ALMA, CHANDELIER, CHAIKIN, DEMA, DMI, EMA, EMV, EVSTC, FRAMA, FVE, HMA, ICHIMOKU, KAMA, KEI, KST, LWMA, MACD, MAMA, MI, PSAR, SAR, SMA, SMM, SSMA, STC, TEMA, TRIMA, TSI, VAMA, VIDYA, VORTEX, VPT, WMA, WTO, ZLEMA, GHA, JMA, GMMA, RMA, EIS, SMMA, TP, WF, PAI]