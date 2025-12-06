import pandas as pd
from ta.trend import ema_indicator, MACD
from ta.momentum import rsi

def calculate_indicators(df: pd.DataFrame) -> dict:
    df = df.copy()

    # EMA
    df['ema50'] = ema_indicator(df['close'], window=50)
    df['ema200'] = ema_indicator(df['close'], window=200)

    # RSI
    df['rsi'] = rsi(df['close'], window=14)

    # MACD (исправлено)
    macd_indicator = MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd_indicator.macd()
    df['macd_signal'] = macd_indicator.macd_signal()
    df['macd_hist'] = macd_indicator.macd_diff()

    # Возьмём последнюю строку
    latest = df.iloc[-1]
    print("[DEBUG] Индикаторы рассчитаны из", len(df), "свечей")
    print("[DEBUG] EMA50:", df['ema50'].dropna().shape[0], 
            "EMA200:", df['ema200'].dropna().shape[0],
            "MACD:", df['macd'].dropna().shape[0])

    return {
        "price": round(latest["close"], 2),
        "ema50": round(latest["ema50"], 2),
        "ema200": round(latest["ema200"], 2),
        "rsi": round(latest["rsi"], 1),
        "macd": round(latest["macd"], 2),
        "macd_signal": round(latest["macd_signal"], 2),
        "macd_hist": round(latest["macd_hist"], 2),
        "volume": round(float(latest["volume"]), 2)
    }
