![Python](https://img.shields.io/badge/Python-3.11-blue)
![AI](https://img.shields.io/badge/AI-integrations-purple)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-26A5E4)


# BTC GPT Signal Bot

This project is an automated BTC/USDT signal bot that combines:

- live market data from Binance,
- classic technical indicators and price patterns,
- and OpenAI GPT analysis,

to generate human-readable trading ideas and send them to Telegram channels.

---

## Features

- Fetches BTC/USDT candles from Binance on multiple timeframes (1m, 15m, 1h, 1d, 1w, 1M).
- Calculates key indicators:
  - EMA 50 / EMA 200
  - RSI
  - MACD (line, signal, histogram)
- Detects basic price patterns:
  - bullish and bearish engulfing
  - volume spikes
- Rule-based filters for:
  - **swing entries** (multi-timeframe confirmation: W1, D1, H1)
  - **scalping entries** (trend + M1 patterns and volume)
- Builds a structured prompt with hints for GPT (trend, context, risk, SL/TP).
- Uses OpenAI Chat Completions API to generate a clear signal text:
  - entry idea,
  - SL/TP levels,
  - confidence,
  - comments.
- Sends formatted HTML messages to Telegram channels (separate chats for swing and scalping).
- Simple retry logic for OpenAI API errors.
- Can run once (single analysis) or in a loop as a “signal watcher”.

---

## Project structure

<details>
  <summary>Click to expand</summary>

  <br>

  Main files and folders:

  - `main.py` — one-shot run: fetch candles → build prompt → ask GPT → send signal to Telegram.
  - `signal_watcher.py` — long-running process that:
    - periodically fetches data,
    - checks swing entry conditions,
    - calls GPT only when rules are satisfied,
    - sends signals to Telegram.

  - `utils/`:
    - `config.py` — API keys and Telegram settings.
    - `multi_tf_fetcher.py` — fetches candles from Binance on multiple timeframes and normalizes them.
    - `indicators.py` — calculates EMA, RSI, MACD and returns the latest values.
    - `patterns.py` — simple pattern detection (engulfing, volume spike).
    - `rule_filter_swing.py` — swing entry filter using W1, D1, H1 indicators and patterns.
    - `rule_filter_scalp.py` — scalping entry filter using H1, M15, M1.
    - `prompt_builder_multi_tf.py` — builds a multi-timeframe prompt for GPT.
    - `prompt_builder_scalp.py` — builds a scalping-oriented prompt for GPT.

  - `gpt_analysis/`:
    - `analyze.py` — wrapper around OpenAI client with retries and simple error handling.

  - `telegram_bot/`:
    - `send_signal.py` — cleans up GPT output (keeps safe HTML) and sends messages to Telegram.

  - `binance_api/`:
    - `fetch_data.py` — helper for loading historical OHLCV data from Binance.

  - `Dockerfile` — minimal Docker image to run the bot.
  - `docker-compose.yml` — simple service definition.
  - `requirements.txt` — Python dependencies.
</details>

## Requirements

<details>
  <summary>Click to expand</summary>

  - Python **3.11** (recommended, as used in Dockerfile)
  - A Binance API key and secret
  - An OpenAI API key
  - A Telegram bot token and chat IDs

  Python packages (also listed in `requirements.txt`):

  - `openai>=1.0.0`
  - `python-binance`
  - `python-telegram-bot==13.15`
  - `pandas`
  - `numpy`
  - `requests`
  - `ta`
  - `urllib3==1.26.15`
</details>


# BTC GPT Signal Bot

Этот проект — автоматический бот сигналов по паре BTC/USDT, который сочетает:

- онлайн-данные с биржи Binance,
- классические технические индикаторы и ценовые паттерны,
- анализ с помощью OpenAI GPT,

чтобы генерировать понятные трейдинговые идеи и отправлять сигналы в Telegram-каналы.

---

## Возможности

- Загружает свечи BTC/USDT с Binance на нескольких таймфреймах (1m, 15m, 1h, 1d, 1w, 1M).
- Считает ключевые индикаторы:
  - EMA 50 / EMA 200
  - RSI
  - MACD (линия, сигнал, гистограмма)
- Определяет базовые ценовые паттерны:
  - бычье и медвежье поглощение (engulfing)
  - всплески объёма
- Правила и фильтры для:
  - **свинг-входа** (мульти-таймфрейм W1, D1, H1),
  - **скальп-входа** (тренд + паттерны и объём на M1).
- Собирает структурированный промпт с подсказками для GPT (тренд, контекст, риск, SL/TP).
- Использует OpenAI Chat Completions API, чтобы сформировать читаемый текст сигнала:
  - идея входа,
  - уровни SL/TP,
  - уверенность,
  - комментарии.
- Отправляет отформатированные HTML-сообщения в Telegram-каналы (отдельные чаты для свинга и скальпа).
- Простая логика повторных попыток при ошибках OpenAI API.
- Может запускаться один раз (разовый анализ) или в режиме «наблюдателя» (цикл).

---

## Структура проекта

<details>
  <summary>Показать структуру</summary>

  <br>

  Основные файлы и папки:

  - `main.py` — однократный запуск: забрать свечи → собрать промпт → спросить GPT → отправить сигнал в Telegram.
  - `signal_watcher.py` — длительно работающий процесс, который:
    - периодически забирает данные,
    - проверяет условия свинг-входа,
    - вызывает GPT только при выполнении правил,
    - отправляет сигналы в Telegram.

  - `utils/`:
    - `config.py` — настройки API-ключей и Telegram.
    - `multi_tf_fetcher.py` — загрузка свечей с Binance на нескольких таймфреймах и приведение к единому виду.
    - `indicators.py` — расчёт EMA, RSI, MACD и возврат последних значений.
    - `patterns.py` — простое определение паттернов (поглощения, всплеск объёма).
    - `rule_filter_swing.py` — фильтр свинг-входа на основе индикаторов и паттернов W1, D1, H1.
    - `rule_filter_scalp.py` — фильтр скальп-входа, использующий H1, M15, M1.
    - `prompt_builder_multi_tf.py` — построение мульти-таймфреймного промпта для GPT.
    - `prompt_builder_scalp.py` — построение промпта для скальпинга.

  - `gpt_analysis/`:
    - `analyze.py` — обёртка над клиентом OpenAI с повторами и простой обработкой ошибок.

  - `telegram_bot/`:
    - `send_signal.py` — чистит вывод GPT (оставляет безопасный HTML) и отправляет сообщения в Telegram.

  - `binance_api/`:
    - `fetch_data.py` — помощник для загрузки исторических OHLCV-данных с Binance.

  - `Dockerfile` — минимальный образ Docker для запуска бота.
  - `docker-compose.yml` — простое описание сервиса.
  - `requirements.txt` — зависимости Python.
</details>

---

<img width="646" height="958" alt="изображение" src="https://github.com/user-attachments/assets/ac97e769-1fa2-4c1f-8ec3-588ea6ab2509" />


## Требования

<details>
  <summary>Показать требования</summary>

  <br>

  - Python **3.11** (рекомендуется, как в Dockerfile)
  - API-ключ и секрет Binance
  - API-ключ OpenAI
  - Токен Telegram-бота и ID чатов

  Пакеты Python (также в `requirements.txt`):

  - `openai>=1.0.0`
  - `python-binance`
  - `python-telegram-bot==13.15`
  - `pandas`
  - `numpy`
  - `requests`
  - `ta`
  - `urllib3==1.26.15`
</details>

---

## Пример конфигурации

<details>
  <summary>Показать пример <code>utils/config.py</code></summary>

  <br>

  ```python
  # utils/config.py

  BINANCE_API_KEY = "your-binance-api-key"
  BINANCE_API_SECRET = "your-binance-api-secret"

  OPENAI_API_KEY = "your-openai-api-key"

  TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
  TELEGRAM_CHAT_ID = "your-main-chat-id"
  TELEGRAM_SCALPING_CHAT_ID = "your-scalping-chat-id"
