def is_volume_spike(candles: list, threshold: float = 1.5) -> bool:
    """
    Проверяет, превышает ли объём последней свечи средний объём * threshold
    """
    if len(candles) < 5:
        return False
    volumes = [float(c['volume']) for c in candles[-6:-1]]  # последние 5 (без текущей)
    avg_volume = sum(volumes) / len(volumes)
    current_volume = float(candles[-1]['volume'])
    return current_volume > avg_volume * threshold


def is_bullish_engulfing(candles: list) -> bool:
    """
    Бычье поглощение: красная свеча, затем зелёная, которая закрылась выше открытия предыдущей
    """
    if len(candles) < 2:
        return False
    prev = candles[-2]
    last = candles[-1]
    return (
        float(prev['close']) < float(prev['open']) and  # пред. свеча красная
        float(last['close']) > float(last['open']) and  # текущая зелёная
        float(last['close']) > float(prev['open'])      # закрытие выше откр. предыдущей
    )


def is_bearish_engulfing(candles: list) -> bool:
    """
    Медвежье поглощение: зелёная свеча, затем красная, которая закрылась ниже открытия предыдущей
    """
    if len(candles) < 2:
        return False
    prev = candles[-2]
    last = candles[-1]
    return (
        float(prev['close']) > float(prev['open']) and
        float(last['close']) < float(last['open']) and
        float(last['close']) < float(prev['open'])
    )
