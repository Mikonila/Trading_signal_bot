from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import time
from utils.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_market(prompt: str, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # можно "gpt-4o" если хочешь побольше модель
                messages=[
                    {"role": "system", "content": "Ты профессиональный трейдер и аналитик криптовалют."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
            else:
                return "⚠️ GPT вернул пустой ответ."


        except (APIError, APIConnectionError, RateLimitError) as e:
            print(f"⚠️ GPT ошибка (попытка {attempt + 1} из {retries}): {e}")
            time.sleep(delay)

        except Exception as e:
            print(f"❌ Неизвестная ошибка OpenAI: {e}")
            break

    return "⚠️ GPT не ответил — сервис недоступен."
