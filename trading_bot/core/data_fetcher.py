# trading_bot/core/data_fetcher.py
from pycoingecko import CoinGeckoAPI

def get_crypto_price(coin_id, currency='usd'):
    """
    Belirtilen kripto paranın anlık fiyatını çeker.
    """
    try:
        cg = CoinGeckoAPI()
        price_data = cg.get_price(ids=coin_id, vs_currencies=currency)
        return price_data[coin_id][currency]
    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return None

def get_historical_data(coin_id, currency='usd', days=7):
    """
    Belirtilen kripto paranın geçmiş fiyat verilerini çeker.
    """
    try:
        cg = CoinGeckoAPI()
        historical_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=currency, days=days)
        # API'den gelen veri [(timestamp, price), ...] formatındadır.
        # Sadece fiyatları [price1, price2, ...] listesi olarak ayıklayalım.
        prices = [item[1] for item in historical_data['prices']]
        return prices
    except Exception as e:
        print(f"Tarihsel veri çekme hatası: {e}")
        return None
