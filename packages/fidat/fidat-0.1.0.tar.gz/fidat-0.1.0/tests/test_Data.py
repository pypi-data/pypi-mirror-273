import pytest
from pandas import DataFrame

from .utils.data import get_ohlcv_data, get_large_price_data

@pytest.mark.data
def test_OHLC_Data(get_ohlcv_data: DataFrame):

    assert [get_ohlcv_data.columns[i] for i in range(4)] == ['open', 'high', 'low', 'close']

    assert get_ohlcv_data['open'].iloc[0] == 52.09180119466482
    assert get_ohlcv_data['high'].iloc[0] == 50.78958308775094
    assert get_ohlcv_data['low'].iloc[0] == 53.068367583095565
    assert get_ohlcv_data['close'].iloc[0] == 48.207649487022884

    assert get_ohlcv_data['open'].iloc[99] == 46.66473061977583
    assert get_ohlcv_data['high'].iloc[99] == 38.400601601792204
    assert get_ohlcv_data['low'].iloc[99] == 57.48955955104808
    assert get_ohlcv_data['close'].iloc[99] == 48.75930694342947

@pytest.mark.data
def test_Large_Price_Data(get_large_price_data: DataFrame):

    assert 'price' in get_large_price_data.columns

    assert get_large_price_data['price'].iloc[0] == 52.76344185237336
    assert get_large_price_data['price'].iloc[999] == 67.030161356612
