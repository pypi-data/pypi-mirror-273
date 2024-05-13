import pandas as pd

def Beta_Coefficient(stock_returns: pd.Series, market_returns: pd.Series, window: int = 25) -> float:
    """
    Calculate the Beta Coefficient.

    Parameters:
    stock_returns (pd.Series): Returns of the stock.
    market_returns (pd.Series): Returns of the market.
    window (int): Rolling window size.

    Returns:
    float: Beta coefficient.
    """
    
    covariance = stock_returns.rolling(window=window).cov(market_returns)
    
    variance = market_returns.rolling(window=window).var()
    
    beta = covariance / variance

    return beta