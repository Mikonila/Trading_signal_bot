from utils.patterns import is_bullish_engulfing, is_bearish_engulfing, is_volume_spike

def check_scalp_entry(candles: dict, indicators: dict) -> bool:
    try:
        h1 = indicators['H1']
        m15 = indicators['M15']
        m1 = indicators['M1']

        confirmations = 0

        # 1. Фильтр тренда: EMA50 > EMA200
        if h1['ema50'] > h1['ema200'] and m15['ema50'] > m15['ema200']:
            confirmations += 1

        # 2. RSI
        if m1['rsi'] < 30 or m1['rsi'] > 70:
            confirmations += 1

        # 3. MACD Histogram направление
        if (m1['rsi'] < 30 and m1['macd_hist'] > 0) or (m1['rsi'] > 70 and m1['macd_hist'] < 0):
            confirmations += 1

        # 4. Паттерн свечи
        m1_candles = candles["M1"]
        if is_bullish_engulfing(m1_candles) or is_bearish_engulfing(m1_candles):
            confirmations += 1

        # 5. Объём
        if is_volume_spike(m1_candles):
            confirmations += 1

        return confirmations >= 2

    except KeyError:
        return False
