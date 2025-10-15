# trading_bot/core/portfolio.py
import json
import csv
import os
import time

class Portfolio:
    def __init__(self, initial_cash=10000, state_file='portfolio.json', trades_file='trades.csv'):
        self.state_file = state_file
        self.trades_file = trades_file
        self.initial_cash = initial_cash

        if os.path.exists(self.state_file):
            self._load_state()
        else:
            self.cash = initial_cash
            self.holdings = {}
            print(f"Yeni sanal portföy ${initial_cash} ile oluşturuldu.")
            self._ensure_trades_file_header()
            self.save_state() # Hata Düzeltmesi: Yeni portföy oluşturulduğunda hemen kaydet

    def _ensure_trades_file_header(self):
        if not os.path.exists(self.trades_file) or os.path.getsize(self.trades_file) == 0:
            with open(self.trades_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'asset_id', 'type', 'amount', 'price', 'total_value'])

    def _log_trade(self, asset_id, trade_type, amount, price):
        with open(self.trades_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime('%Y-%m-%d %H:%M:%S'),
                asset_id,
                trade_type,
                amount,
                price,
                amount * price
            ])

    def save_state(self):
        state = {'cash': self.cash, 'holdings': self.holdings, 'initial_cash': self.initial_cash}
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=4)
        # print("Portföy durumu kaydedildi.")

    def _load_state(self):
        with open(self.state_file, 'r') as f:
            state = json.load(f)
            self.cash = state['cash']
            self.holdings = state['holdings']
            self.initial_cash = state.get('initial_cash', 10000)
        print(f"Mevcut portföy durumu {self.state_file} dosyasından yüklendi.")

    def buy(self, asset_id, amount, price):
        cost = amount * price
        if self.cash >= cost:
            self.cash -= cost
            self.holdings[asset_id] = self.holdings.get(asset_id, 0) + amount
            print(f"ALIM: {amount} {asset_id.capitalize()} @ ${price:.2f} | Maliyet: ${cost:.2f}")
            self._log_trade(asset_id, 'buy', amount, price)
            self.save_state()
        else:
            print("ALIM BAŞARISIZ: Yetersiz bakiye.")

    def sell(self, asset_id, amount, price):
        if self.holdings.get(asset_id, 0) >= amount:
            revenue = amount * price
            self.cash += revenue
            self.holdings[asset_id] -= amount
            if self.holdings[asset_id] == 0:
                del self.holdings[asset_id]
            print(f"SATIM: {amount} {asset_id.capitalize()} @ ${price:.2f} | Gelir: ${revenue:.2f}")
            self._log_trade(asset_id, 'sell', amount, price)
            self.save_state()
        else:
            print("SATIM BAŞARISIZ: Yetersiz varlık.")

    def get_total_value(self, current_prices):
        assets_value = 0
        for asset, amount in self.holdings.items():
            assets_value += amount * current_prices.get(asset, 0)
        return self.cash + assets_value

    def display_status(self, current_prices):
        print("\n--- Portföy Durumu ---")
        print(f"Nakit: ${self.cash:.2f}")
        print("Varlıklar:")
        if not self.holdings:
            print("  (Boş)")
        else:
            for asset, amount in self.holdings.items():
                value = amount * current_prices.get(asset, 0)
                print(f"  - {asset.capitalize()}: {amount} (Değer: ${value:.2f})")

        total_value = self.get_total_value(current_prices)
        profit_or_loss = total_value - self.initial_cash
        print(f"Toplam Değer: ${total_value:.2f}")
        print(f"Kar/Zarar: ${profit_or_loss:.2f}")
        print("----------------------")
