""" 
Support and Resistance 
----------------------
Support and resistance indicators are tools used in technical analysis to identify price levels on charts where the likelihood of price movements pausing or reversing is higher than usual. These levels act as barriers, preventing the price of an asset from getting pushed in a certain direction beyond a certain point, at least temporarily. Here’s a closer look at each:

Support
• Definition: Support is a price level where a downtrend can be expected to pause due to a concentration of demand. As the price of an asset approaches this level, buyers become more inclined to buy and sellers become less inclined to sell. Essentially, support levels indicate that the price is low enough to attract buyers back into the market to prevent further price falls.
• Behavior: When the price dips close to a support level but then typically rises, it demonstrates that the demand for the asset at this price level is strong enough to overcome the selling pressure.

Resistance
• Definition: Resistance is the opposite of support. It is a price level where a price uptrend can pause or reverse following a price increase, due to a concentration of supply. As the price of an asset approaches resistance, sellers become more likely to sell and buyers become less inclined to buy.
• Behavior: When the price rises close to a resistance level but typically falls, it suggests that the selling pressure at this level is sufficient to overcome buying pressure.

Traders and analysts use these indicators to determine strategic places for transactions to be placed, target prices, or stop losses. The logic behind these indicators is that they highlight historical points where the collective decisions of all market participants have led to noticeable price movements.
"""

from ..CHANDELIER import Chandelier_Exit as CHANDELIER
from ..DC import Donchian_Channels as DC
from ..PIVOT import Pivot_Points as PIVOT
from ..PIVOT_FIB import Fibonacci_Pivot_Points as PIVOT_FIB

ALL = [CHANDELIER, DC, PIVOT, PIVOT_FIB]