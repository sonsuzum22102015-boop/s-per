# trading_bot/main.py
from core.data_fetcher import get_historical_data
from core.backtester import run_backtest

def main():
    """
    Ana fonksiyon - Backtest modunu çalıştırır.
    """
    coin_id = 'bitcoin'
    days_to_backtest = 365
    initial_cash = 10000

    print(f"Backtest için {coin_id.capitalize()} verisi çekiliyor ({days_to_backtest} gün)...")
    historical_prices = get_historical_data(coin_id, days=days_to_backtest)

    if historical_prices and len(historical_prices) > 0:
        run_backtest(
            historical_prices=historical_prices,
            initial_cash=initial_cash,
            short_window=20, # Kısa vadeli SMA periyodu
            long_window=50   # Uzun vadeli SMA periyodu
        )
    else:
        print("Backtest için yeterli tarihsel veri çekilemedi.")


if __name__ == "__main__":
    main()
