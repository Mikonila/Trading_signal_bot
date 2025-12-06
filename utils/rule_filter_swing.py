from utils.patterns import is_bullish_engulfing, is_bearish_engulfing, is_volume_spike


def check_swing_entry(candles: dict, indicators: dict) -> bool:
    confirmations = 0
    try:
        w1 = indicators['W1']
        d1 = indicators['D1']
        h1 = indicators['H1']
        h1_candles = candles["H1"]

        # 1. EMA на недельке
        if w1['ema50'] > w1['ema200']:
            confirmations += 1

        # 2. RSI в нейтральной зоне на дневке
        if 40 <= d1['rsi'] <= 60:
            confirmations += 1

        # 3. MACD Histogram положительный на 1ч
        if h1['macd_hist'] > 0:
            confirmations += 1

        # 4. Свечной паттерн
        bullish = is_bullish_engulfing(h1_candles)
        bearish = is_bearish_engulfing(h1_candles)
        if bullish or bearish:
            confirmations += 1

        # 5. Объём
        volume_spike = is_volume_spike(h1_candles)
        if volume_spike:
            confirmations += 1

        print("🔍 Проверка условий:")
        print("W1 EMA50:", w1['ema50'], "EMA200:", w1['ema200'])
        print("D1 RSI:", d1['rsi'])
        print("H1 MACD Histogram:", h1['macd_hist'])
        print("Свечной паттерн (bullish):", bullish)
        print("Свечной паттерн (bearish):", bearish)
        print("Спайк объёма:", volume_spike)
        print("Подтверждений:", confirmations)

        return confirmations >= 1

    except KeyError as e:
        print(f"❌ Пропущены данные: {e}")
        return False