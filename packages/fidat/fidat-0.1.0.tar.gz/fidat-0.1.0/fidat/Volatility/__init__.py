"""
Volatility Indicators
---------------------

Volatility indicators are tools used in technical analysis to measure the extent of price fluctuations over a given period of time. Unlike trend or momentum indicators, volatility indicators do not provide information about the direction of price movements but focus on the rate of change in prices, indicating how dramatically prices are varying.

Definition and Purpose
• Definition: Volatility indicators quantify the rate of price changes, regardless of direction, helping traders to understand the level of risk and potential price movement range in the market.
• Purpose: These indicators are crucial for assessing market sentiment and potential breakouts or contractions in price action. They help traders adjust their trading strategies to the level of market volatility, optimizing trade sizing and setting appropriate stop-loss orders.

Application and Importance
• Application: Volatility indicators are particularly useful in options trading, where volatility is a major factor in pricing. They are also important for risk management, helping traders to adjust their positions and trading strategies according to expected volatility.
• Importance: Understanding volatility is crucial for traders to ensure that they are not entering or exiting trades at inopportune times. High volatility can mean greater risk, but also the potential for higher rewards. Conversely, low volatility might indicate less risk but also fewer opportunities for significant gains.

Volatility indicators thus play a vital role in financial markets by providing insights that help traders make informed decisions about market entries, exits, and potential price movements.
"""

from ..APZ import Adaptive_Price_Zone as APZ
from ..ATR import Average_True_Range as ATR
from ..BB import Bollinger_Bands as BB
from ..BBWIDTH import Bollinger_Bands_Width as BBWIDTH
from ..CHANDELIER import Chandelier_Exit as CHANDELIER
from ..KC import Keltner_Channels as KC
from ..MOBO import Modified_Bollinger_Bands as MOBO
from ..MSD import Moving_Standard_Deviation as MSD
from ..PERCENT_B import Percentage_B as PERCENT_B
from ..SDC import Standard_Deviation_Channel as SDC
from ..VBM import Volatility_Based_Momentum as VBM

from ..TR import True_Range as TR
from ..VC import Value_chart as VC

ALL = [APZ, ATR, BB, BBWIDTH, CHANDELIER, KC, MOBO, MSD, PERCENT_B, SDC, VBM, TR, VC]