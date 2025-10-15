# trading_bot/main.py
import time
from core.data_fetcher import get_crypto_price, get_historical_data
from strategies.simple_strategy import simple_moving_average_strategy
from core.portfolio import Portfolio

def trading_cycle(portfolio, coin_id='bitcoin', currency='usd', short_window=10, long_window=30):
    """
    Botun tek bir alım-satım kontrol döngüsünü çalıştırır.
    """
    try:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Yeni kontrol döngüsü...")

        # 1. Veri Çekme
        print("Canlı ve tarihsel veriler çekiliyor...")
        current_price = get_crypto_price(coin_id, currency)
        historical_prices = get_historical_data(coin_id, currency, days=long_window + 1)

        if current_price is None or historical_prices is None:
            print("Veri çekilemedi, bu döngü atlanıyor.")
            return

        # 2. Stratejiyi Çalıştırma
        all_prices = historical_prices + [current_price]
        decision = simple_moving_average_strategy(all_prices, short_window, long_window)
        print(f"Strateji kararı: {decision.upper()}")

        # 3. İşlem Yapma (sadece 0.001 BTC'lik sabit miktar ile)
        trade_amount = 0.001
        if decision == 'buy':
            portfolio.buy(coin_id, trade_amount, current_price)
        elif decision == 'sell':
            portfolio.sell(coin_id, trade_amount, current_price)
        else:
            print("TUT sinyali, işlem yapılmıyor.")

        # 4. Güncel Portföy Durumunu Gösterme
        current_prices_dict = {coin_id: current_price}
        portfolio.display_status(current_prices_dict)

    except Exception as e:
        print(f"Döngü sırasında bir hata oluştu: {e}")


def main():
    """
    Ana fonksiyon - Canlı Paper Trading botunu başlatır.
    """
    best_short_window = 10
    best_long_window = 30

    # Döngü sıklığı (saniye cinsinden)
    # Gerçek kullanımda bu 3600 (1 saat) gibi daha uzun bir süre olabilir.
    cycle_interval = 3600 # 1 saat

    my_portfolio = Portfolio(initial_cash=10000)

    print("--- Canlı Paper Trading Botu Başlatıldı ---")
    print(f"Strateji: SMA ({best_short_window}/{best_long_window})")
    print(f"Kontrol Sıklığı: {cycle_interval} saniye")

    while True:
        trading_cycle(
            portfolio=my_portfolio,
            short_window=best_short_window,
            long_window=best_long_window
        )
        print(f"\nSonraki kontrol için {cycle_interval} saniye bekleniyor...")
        time.sleep(cycle_interval)

if __name__ == "__main__":
    main()
