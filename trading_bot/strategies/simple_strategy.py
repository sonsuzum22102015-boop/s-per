# trading_bot/strategies/simple_strategy.py
import numpy as np

def calculate_sma(prices, period):
    """Basit Hareketli Ortalama (SMA) hesaplar."""
    if len(prices) < period:
        return None
    return np.mean(prices[-period:])

def simple_moving_average_strategy(prices, short_window=10, long_window=30):
    """
    Basit Hareketli Ortalama (SMA) kesişim stratejisi.
    Kısa vadeli SMA, uzun vadeli SMA'yı yukarı keserse 'al', aşağı keserse 'sat' sinyali üretir.
    """
    if prices is None or len(prices) < long_window:
        # Yeterli veri yoksa bir karar verme
        return 'hold'

    short_sma = calculate_sma(prices, short_window)
    long_sma = calculate_sma(prices, long_window)

    if short_sma is None or long_sma is None:
        return 'hold'

    # Al sinyali: Kısa vadeli ortalama, uzun vadeli ortalamanın üzerine çıktığında
    if short_sma > long_sma:
        return 'buy'
    # Sat sinyali: Kısa vadeli ortalama, uzun vadeli ortalamanın altına düştüğünde
    elif short_sma < long_sma:
        return 'sell'
    # Kesişim yoksa bir şey yapma
    else:
        return 'hold'
