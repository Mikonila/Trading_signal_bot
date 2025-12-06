import re
from telegram import Bot
from utils.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_SCALPING_CHAT_ID


def sanitize_gpt_response(text: str) -> str:
    if not text:
        return ""

    # убрать блоки ```html ... ```
    text = text.replace("```html", "").replace("```", "")

    # разрешённые теги
    allowed_tags = ["b", "i", "u", "s", "a", "code", "pre"]

    # удалить все теги, кроме разрешённых
    text = re.sub(
        r"</?(?!{})(\w+)[^>]*>".format("|".join(allowed_tags)),
        "",
        text,
    )

    # чистим тройные переносы
    text = re.sub(r"\n{3,}", "\n\n", text)

    # фильтруем мусорные невидимые символы
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u0400-\u04FF<>/]", "", text)

    # --- балансировка тегов ---
    for tag in allowed_tags:
        open_count = len(re.findall(f"<{tag}[^>]*>", text))
        close_count = len(re.findall(f"</{tag}>", text))
        if close_count > open_count:
            text = re.sub(f"</{tag}>", "", text, count=(close_count - open_count))
        elif open_count > close_count:
            text += "</{}>".format(tag) * (open_count - close_count)

    # plain-текст без тегов для проверки
    plain = re.sub(r"<[^>]+>", "", text).strip().lower()
    if "нет сигнала" in plain:
        return ""

    return text.strip()


def send_signal(message: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    cleaned = sanitize_gpt_response(message)

    if not cleaned:  # <-- защита от пустого текста
        print("[INFO] Сообщение не отправлено (пустое или 'Нет сигнала').")
        return

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=cleaned, parse_mode="HTML")


def send_scalp_signal(message: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    cleaned = sanitize_gpt_response(message)

    if not cleaned:  # <-- то же самое
        print("[INFO] Сообщение не отправлено (пустое или 'Нет сигнала').")
        return

    bot.send_message(chat_id=TELEGRAM_SCALPING_CHAT_ID, text=cleaned, parse_mode="HTML")
