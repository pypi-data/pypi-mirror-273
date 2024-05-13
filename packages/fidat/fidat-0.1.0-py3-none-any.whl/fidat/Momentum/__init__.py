"""

Momentum Indicators
-------------------


Momentum indicators are a category of technical analysis tools used to determine the strength or weakness of a price movement over time. They help traders identify the speed of price changes and gauge whether an asset is overbought or oversold, indicating potential reversal points or the continuation of current trends. Here’s a detailed look at momentum indicators:

Definition and Purpose
• Definition: Momentum indicators measure the rate of change in prices or the velocity of price movements. They are generally displayed as oscillators, which are graphical representations that move above and below a central line or between set levels.
• Purpose: The primary purpose of these indicators is to assess how strong or weak a market move is, helping traders to decide whether to buy or sell an asset. They can signal the potential end of a trend or the continuation of a trend, based on the underlying momentum.

Application and Importance
• Application: Momentum indicators are used for intraday trading, swing trading, and long-term investment analysis. They are often combined with other technical tools like trend indicators and volume measures to confirm signals.
• Importance: These indicators are crucial for understanding market psychology and trader behavior, as they can indicate whether buying or selling pressure is increasing or decreasing. This helps traders make more informed decisions about when to enter or exit trades, particularly in volatile markets.

Overall, momentum indicators are essential tools in the technical analyst's toolkit, providing insights not just into market direction but also into the strength of price movements, helping traders to capitalize on trends or avoid losses from potential reversals.

"""

from ..AO import Awesome_Oscillator as AO
from ..ARO import Aroon_Oscillator as ARO
from ..BOP import Balance_of_Power as BOP
from ..CCI import Commodity_Channel_Index as CCI
from ..CMO import Chande_Momentum_Oscillator as CMO
from ..DMMI import Dynamic_Momentum_Index as DMMI
from ..EFT import Ehlers_Fisher_Transform as EFT
from ..EVW_MACD import Elastic_Volume_Weighted_MACD as EVW_MACD
from ..FISH import Fisher_Transform as FISH
from ..HMAO import Hull_Moving_Average_Oscillator as HMAO
from ..HPO import High_Pass_Oscillator as HPO
from ..IFT_RSI import Inverse_Fisher_Transform_RSI as IFT_RSI
from ..MACD import Moving_Average_Convergence_Divergence as MACD
from ..MOM import Market_Momentum as MOM
from ..PPO import Percentage_Price_Oscillator as PPO
from ..PZO import Price_Zone_Oscillator as PZO
from ..ROC import Rate_of_Change as ROC
from ..RSI import Relative_Strength_Index as RSI
from ..STC import Schaff_Trend_Cycle as STC
from ..STOCH import Stochastic_Oscillator as STOCH
from ..STOCHRSI import Stochastic_Oscillator_RSI as STOCHRSI
from ..TSI import True_Strength_Index as TSI
from ..UO import Ultimate_Oscillator as UO
from ..VBM import Volatility_Based_Momentum as VBM
from ..VW_MACD import Volume_Weighted_MACD as VW_MACD
from ..ZCO import Zero_Cross_Indicator as ZCO

from ..QSTICK import QStick as QSTICK
from ..SMO import Squeeze_Momentum_Indicator as SMO
from ..STOCHD import Stochastic_Oscillator_Moving_Average as STOCHD
from ..ARSI import Adaptive_Relative_Strength_Index as ARSI
from ..ASI import Accumulative_Swing_Index as ASI
from ..WILLIAMS import Williams_Percent_Range as WILLIAMS


ALL = [AO, BOP, CCI, CMO, DMMI, EVW_MACD, FISH, IFT_RSI, MACD, MOM, PPO, PZO, ROC, RSI, STC, STOCH, STOCHRSI, TSI, UO, VBM, VW_MACD, EFT, ARO, HMAO, HPO, ZCO, QSTICK, SMO, STOCHD, ARSI, ASI, WILLIAMS]