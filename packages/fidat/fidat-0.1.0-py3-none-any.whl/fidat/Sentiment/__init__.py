"""
Market Sentiment Indicators
---------------------------

Sentiment indicators are tools used in financial markets to gauge the overall attitude of investors towards a particular security or market. These indicators are derived from various sources of data and aim to measure the mood or psychological state of market participants. The sentiment is often considered a contrarian indicator, suggesting that extreme levels of bullishness or bearishness could signal reversals in market trends.

Definition and Purpose
• Definition: Sentiment indicators reflect the collective emotions and behaviors of market participants, including optimism, pessimism, confidence, and fear.
• Purpose: The main purpose of sentiment indicators is to identify potential turning points in the market by assessing whether investors are overly bullish (which might indicate a market top) or overly bearish (which might suggest a market bottom).

Application and Importance
• Application: Sentiment indicators are used by both individual and institutional investors to inform their trading strategies, often in conjunction with other forms of analysis like fundamental and technical analysis.
• Importance: These indicators provide insights into the psychological underpinnings of market movements. When used correctly, they can help predict market tops and bottoms, offering traders opportunities to enter or exit trades at potentially optimal times.

Sentiment indicators are particularly useful in identifying extremes in market conditions, where emotional investing might drive prices away from fundamental values. They are essential for those looking to understand the often irrational behavior of markets and capitalize on the shifts in general mood among investors.

"""

from ..BC import Beta_Coefficient as BC
from ..BEARP import Bear_Power as BEARP
from ..BULLP import Bull_Power as BULLP
from ..BPBP import Power_Indicators as BPBP
from ..ERI import Elder_Ray_Index as ERI
from ..HA import Heikin_Ashi as HA

ALL = [BC, BEARP, BULLP, BPBP, ERI, HA]