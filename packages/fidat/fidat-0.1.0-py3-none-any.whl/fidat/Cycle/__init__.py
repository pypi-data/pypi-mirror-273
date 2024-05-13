"""
Cycle Indicators
----------------

Cycle indicators are tools in technical analysis used to identify and anticipate the timing of significant highs and lows in markets through the analysis of cycles. These indicators are based on the idea that financial markets move in cyclical patterns, reflecting periodic fluctuations in investor sentiment, economic factors, and other market forces. Here’s a detailed look at cycle indicators:

Definition and Purpose
• Definition: Cycle indicators are used to determine the timing of market cycles, helping traders to predict future market movements by analyzing past patterns and durations of bullish and bearish trends.
• Purpose: The main purpose of these indicators is to forecast turning points or continuation points within market cycles. Traders use these indicators to capitalize on the cyclical nature of markets, entering trades at the beginning of a trend and exiting at its likely reversal.

Application and Importance
• Application: Cycle indicators are typically used in conjunction with other forms of analysis to confirm or refute other signals. They are particularly favored in markets known for clear cyclical patterns, such as commodities or forex.
• Importance: Understanding the cyclical nature of markets can significantly enhance a trader's ability to make informed decisions, minimizing risk and maximizing potential returns by timing entries and exits more effectively.

Cycle indicators are especially valuable in identifying the emotional and psychological state of the market, which influences trading behavior. As such, they are a vital part of the toolkit for many technical analysts and traders.
"""

from ..STC import Schaff_Trend_Cycle as STC
from ..EVSTC import Schaff_Trend_Cycle_EVWMA_MACD as EVSTC
from ..COPP import Coppock_Curve as COPP
from ..DPO import Detrended_Price_Oscillator as DPO
from ..KST import Know_Sure_Thing as KST
from ..PSK import Prings_Special_K as PSK
from ..PRSK import Price_Swing_Kaufman as PRSK
from ..WTO import Wave_Trend_Oscillator as WTO
from ..WP import Wave_PM as WP

ALL = [STC, EVSTC, COPP, DPO, KST, PSK, PRSK, WTO, WP]