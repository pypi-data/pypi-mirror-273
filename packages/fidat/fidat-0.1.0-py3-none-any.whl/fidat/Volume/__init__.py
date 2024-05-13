"""
Volume Indicators
-----------------

Volume indicators are tools in technical analysis that use trading volume data to assess the strength of price movements and predict future trends. Volume, which represents the total number of shares or contracts traded over a specific period, is often used in conjunction with price data to confirm trends, reversals, or other market patterns.

Definition and Purpose
• Definition: Volume indicators analyze the amount of trading activity and liquidity in a market to provide insights into the strength of price movements and potential upcoming changes in direction.
• Purpose: They help traders understand the levels of buying and selling pressure behind market moves, indicating whether a price trend is likely to continue or reverse.

Application and Importance
• Application: Volume indicators are crucial in confirming trends identified by price analysis. For instance, if prices are rising and volume is increasing, it suggests a strong upward trend. Conversely, if the price increases but volume decreases, it might indicate a lack of support for the upward move (weakness in the trend).
• Importance: Volume indicators provide a deeper insight into market dynamics and trader sentiment. They are used extensively in market analysis to enhance the reliability of other technical indicators and signals. Understanding volume patterns helps in making more accurate predictions about future market movements.

Overall, volume indicators are essential for traders who rely on technical analysis, providing critical information about the underlying strength or weakness of market trends and potential reversals, which are not always apparent from price movements alone.
"""

from ..ADL import Accumulation_Distribution_Line as ADL
from ..BASP import Buying_and_Selling_Pressure as BASP
from ..CHAIKIN import Chaikin_Oscillator as CHAIKIN
from ..EVWMA import Exponential_Volume_Weighted_Moving_Average as EVWMA
from ..MFI import Money_Flow_Index as MFI
from ..MAFI import Market_Facilitation_Index as MAFI
from ..BASPN import Normalized_BASP as BASPN
from ..NVI import Negative_Volume_Index as NVI
from ..OBV import On_Balance_Volume as OBV
from ..PVI import Positive_Volume_Index as PVI
from ..TMF import Twiggs_Money_Flow as TMF
from ..VFI import Volume_Flow_Indicator as VFI
from ..VP import Volume_Profile as VP
from ..VPT import Volume_Price_Trend as VPT
from ..VWAP import Volume_Weighted_Average_Price as VWAP
from ..VZO import Volume_Zone_Oscillator as VZO
from ..WOBV import Weighted_On_Balance_Volume as WOBV

from ..VO import Volume_Oscillator as VO

ALL = [ADL, BASP, BASPN, CHAIKIN, EVWMA, MFI, MAFI, NVI, OBV, PVI, TMF, VFI, VP, VPT, VWAP, VZO, WOBV, VO]