# trading_bot/core/backtester.py
from .portfolio import Portfolio
from strategies.simple_strategy import simple_moving_average_strategy

def run_backtest(historical_prices, initial_cash=10000, short_window=20, long_window=50):
    """
    Verilen tarihsel veri üzerinde stratejiyi çalıştırır ve sonuçları raporlar.
    """
    portfolio = Portfolio(initial_cash=initial_cash)
    min_data_points = long_window + 1

    print("\n--- Backtest Başlatılıyor ---")
    print(f"Strateji: SMA Kesişimi (Kısa: {short_window}, Uzun: {long_window})")
    print(f"Test periyodu: {len(historical_prices)} gün")
    print(f"Başlangıç Portföy Değeri: ${initial_cash:.2f}")

    for i in range(len(historical_prices)):
        if i < min_data_points:
            continue

        current_data_slice = historical_prices[:i]
        decision = simple_moving_average_strategy(current_data_slice, short_window, long_window)

        current_price = historical_prices[i]
        asset_to_trade = 0.01

        if decision == 'buy':
            portfolio.buy('bitcoin', asset_to_trade, current_price)
        elif decision == 'sell':
            portfolio.sell('bitcoin', asset_to_trade, current_price)

    print("\n--- Backtest Tamamlandı ---")

    final_price_dict = {'bitcoin': historical_prices[-1]}
    final_value = portfolio.get_total_value(final_price_dict)
    profit_or_loss = final_value - initial_cash
    profit_or_loss_percent = (profit_or_loss / initial_cash) * 100

    print("\n--- PERFORMANS ÖZETİ ---")
    portfolio.display_status(final_price_dict)
    print(f"Başlangıç Değeri: ${initial_cash:.2f}")
    print(f"Bitiş Değeri:     ${final_value:.2f}")
    print(f"Toplam Kar/Zarar: ${profit_or_loss:.2f} ({profit_or_loss_percent:.2f}%)")
    print("--------------------------")

    return final_value
