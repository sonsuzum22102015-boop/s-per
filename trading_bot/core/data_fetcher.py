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
