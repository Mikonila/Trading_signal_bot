
from binance.client import Client
from utils.config import BINANCE_API_KEY, BINANCE_API_SECRET
import pandas as pd

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

TIMEFRAMES = {
    "1m": "M1",
    "15m": "M15",
    "1h": "H1",
    "1d": "D1",
    "1w": "W1",
    "1M": "MN1"
}


def fetch_candles(symbol="BTCUSDT", limit=300):
    data = {}
    for interval, label in TIMEFRAMES.items():
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.astype({'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
        df = df.rename(columns={'timestamp': 'time'})
        df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M' if interval != '1M' else '%Y-%m')

        if len(df) > 1:
            df = df.iloc[:-1]

        data[label] = df.to_dict(orient='records')
        for tf, candles_list in data.items():
            print(f"[DEBUG] {tf}: {len(candles_list)} свечей")

    return data
