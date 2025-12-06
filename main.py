from gpt_analysis.analyze import analyze_market
from telegram_bot.send_signal import send_signal
from utils.multi_tf_fetcher import fetch_candles
from utils.prompt_builder_multi_tf import build_multi_tf_prompt


def main():
    print("Fetching candles from Binance (multi-timeframe)...")
    candles = fetch_candles("BTCUSDT", limit=300)

    print("Building prompt...")
    prompt = build_multi_tf_prompt(candles)

    print("Sending data to OpenAI GPT-4o...")
    analysis = analyze_market(prompt)

    print("Sending signal to Telegram...")
    send_signal(analysis)

    


if __name__ == "__main__":
    main()
