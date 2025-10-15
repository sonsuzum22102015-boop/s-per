# trading_bot/main.py
import time
from core.data_fetcher import get_crypto_price, get_historical_data
from strategies.simple_strategy import simple_moving_average_strategy
from core.portfolio import Portfolio

def main_loop(portfolio, coin_id='bitcoin', currency='usd'):
    """
    Botun ana çalışma döngüsü.
    """
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Yeni döngü başlıyor...")

    # 1. Veri Çekme
    print("Veriler çekiliyor...")
    current_price = get_crypto_price(coin_id, currency)
    # Strateji için yeterli tarihsel veri (örn: 90 günlük)
    historical_prices = get_historical_data(coin_id, currency, days=90)

    if current_price is None or historical_prices is None:
        print("Veri çekilemedi, döngü atlanıyor.")
        return

    # 2. Stratejiyi Çalıştırma
    print("Strateji analizi yapılıyor...")
    # Karar için tarihsel veriye anlık fiyatı da ekleyelim
    all_prices = historical_prices + [current_price]
    decision = simple_moving_average_strategy(all_prices, short_window=20, long_window=50)
    print(f"Strateji kararı: {decision.upper()}")

    # 3. İşlem Yapma
    asset_to_trade = 0.001 # Her işlemde ne kadar BTC alınacak/satılacak (sabit)

    if decision == 'buy':
        print("Alım sinyali alındı. İşlem yapılıyor...")
        portfolio.buy(coin_id, asset_to_trade, current_price)
    elif decision == 'sell':
        print("Satım sinyali alındı. İşlem yapılıyor...")
        portfolio.sell(coin_id, asset_to_trade, current_price)
    else: # hold
        print("Tutma sinyali alındı. İşlem yapılmıyor.")

    # 4. Portföy Durumunu Gösterme
    current_prices_dict = {coin_id: current_price}
    portfolio.display_status(current_prices_dict)


def main():
    # Sanal portföyü başlat
    my_portfolio = Portfolio(initial_cash=10000)

    # Ana döngüyü şimdilik bir kez çalıştırarak entegrasyonu test edelim
    main_loop(my_portfolio, coin_id='bitcoin')

if __name__ == "__main__":
    main()
