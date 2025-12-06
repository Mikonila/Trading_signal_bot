from binance.client import Client
from utils.config import BINANCE_API_KEY, BINANCE_API_SECRET
import pandas as pd
import time

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_ohlcv(symbol='BTCUSDT', interval='1h', limit=1000, start_str='5 years ago UTC'):
    klines = client.get_historical_klines(symbol, interval, start_str)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

def get_historical_ohlcv():
    print("Fetching D1 (daily) data...")
    daily = get_ohlcv(interval='1d')
    time.sleep(1)
    print("Fetching W1 (weekly) data...")
    weekly = get_ohlcv(interval='1w')
    time.sleep(1)
    print("Fetching H1 (hourly) data...")
    hourly = get_ohlcv(interval='1h')
    return {
        "daily": daily,
        "weekly": weekly,
        "hourly": hourly
    }
