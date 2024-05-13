import pytest

@pytest.mark.code
def test_All_Code_Included():
    from fidat import (ALL, Barriers, Trends, Cycle, Index, Momentum, Sentiment, Volatility, Volume)
    for method in ALL:
        assert method in Barriers.ALL + Trends.ALL + Cycle.ALL + Index.ALL + Momentum.ALL + Sentiment.ALL + Volatility.ALL + Volume.ALL
    
    