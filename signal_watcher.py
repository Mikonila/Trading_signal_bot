import time
import pandas as pd
from utils.rule_filter_swing import check_swing_entry
from utils.prompt_builder_multi_tf import build_multi_tf_prompt
from utils.indicators import calculate_indicators
from utils.multi_tf_fetcher import fetch_candles
from telegram_bot.send_signal import send_signal as send_swing_signal
from gpt_analysis.analyze import analyze_market


def run_swing_logic():
    candles = fetch_candles("BTCUSDT", limit=300)
    indicators = {
        "H1": calculate_indicators(pd.DataFrame(candles["H1"])),
        "D1": calculate_indicators(pd.DataFrame(candles["D1"])),
        "W1": calculate_indicators(pd.DataFrame(candles["W1"]))
    }
    if check_swing_entry(candles, indicators):
        prompt = build_multi_tf_prompt(candles)
        signal = analyze_market(prompt) 
        # Проверка на "не рекомендуется"
        if signal.strip().startswith("Нет сигнала"):
            print("GPT: вход не рекомендуется, сигнал не отправлен.")
            return
        send_swing_signal(signal)
    else:
        print("[SWING] Условие входа не выполнено.")

if __name__ == "__main__":
    print("Signal watcher запущен. Ожидание точки входа...")

    run_swing_logic()

    last_swing = time.time()

    while True:
        now = time.time()
        try:

            # Свинг каждый час
            if now - last_swing >= 2 * 60 * 60:
                run_swing_logic()
                last_swing = now

        except Exception as e:
            print(f"[ОШИБКА] {e}")

        time.sleep(10)  # Проверяем таймеры каждые 10 секунд