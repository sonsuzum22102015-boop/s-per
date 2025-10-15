# trading_bot/main.py
from core.data_fetcher import get_crypto_price

def display_prices(coins):
    """
    Belirtilen kripto paraların fiyatlarını formatlı bir şekilde ekrana yazdırır.
    """
    print("--- Kripto Para Fiyatları ---")
    for coin in coins:
        price = get_crypto_price(coin)
        if price:
            print(f"- {coin.capitalize()}: ${price}")
        else:
            print(f"- {coin.capitalize()}: Fiyat alınamadı.")
    print("-----------------------------")

def main():
    print("Alım satım botu başlatılıyor...")

    popular_coins = ['bitcoin', 'ethereum', 'dogecoin']
    display_prices(popular_coins)

if __name__ == "__main__":
    main()
