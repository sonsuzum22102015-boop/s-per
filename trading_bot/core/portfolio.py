# trading_bot/core/portfolio.py

class Portfolio:
    def __init__(self, initial_cash=10000):
        """
        Sanal portföyü başlatır.
        :param initial_cash: Başlangıçtaki sanal nakit miktarı (USD).
        """
        self.cash = initial_cash
        self.holdings = {}  # Örn: {'bitcoin': 0.5}
        self.initial_cash = initial_cash
        print(f"Sanal portföy ${initial_cash} ile oluşturuldu.")

    def buy(self, asset_id, amount, price):
        """
        Sanal bir alım işlemi gerçekleştirir.
        """
        cost = amount * price
        if self.cash >= cost:
            self.cash -= cost
            self.holdings[asset_id] = self.holdings.get(asset_id, 0) + amount
            print(f"ALIM: {amount} {asset_id.capitalize()} @ ${price:.2f} | Maliyet: ${cost:.2f}")
        else:
            print("ALIM BAŞARISIZ: Yetersiz bakiye.")

    def sell(self, asset_id, amount, price):
        """
        Sanal bir satım işlemi gerçekleştirir.
        """
        if self.holdings.get(asset_id, 0) >= amount:
            revenue = amount * price
            self.cash += revenue
            self.holdings[asset_id] -= amount
            if self.holdings[asset_id] == 0:
                del self.holdings[asset_id]
            print(f"SATIM: {amount} {asset_id.capitalize()} @ ${price:.2f} | Gelir: ${revenue:.2f}")
        else:
            print("SATIM BAŞARISIZ: Yetersiz varlık.")

    def get_total_value(self, current_prices):
        """
        Portföyün anlık toplam değerini hesaplar (nakit + varlıklar).
        :param current_prices: {'bitcoin': 12345.67} gibi anlık fiyatları içeren bir sözlük.
        """
        assets_value = 0
        for asset, amount in self.holdings.items():
            assets_value += amount * current_prices.get(asset, 0)

        return self.cash + assets_value

    def display_status(self, current_prices):
        """
        Portföyün mevcut durumunu ekrana yazdırır.
        """
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
