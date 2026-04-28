← [Назад до головної](../README.md)
# 🤖 Perplexity API у Telegram боті

> Як підключити Perplexity API до Telegram-бота на Python і отримати AI-пошук прямо у месенджері.

---

## Що ти отримаєш

- Бот, що відповідає на запитання з посиланнями на джерела
- Реальний веб-пошук через Sonar модель
- Стрімінг відповідей (друкується поступово)
- Мінімальний код — до 50 рядків

---

## Передумови

- Python 3.10+
- Бібліотека `aiogram` або `python-telegram-bot`
- API ключ Perplexity → [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
- Telegram Bot Token від [@BotFather](https://t.me/BotFather)

```bash
pip install aiogram openai python-dotenv
```

---

## Базова реалізація (aiogram 3.x)

```python
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

client = AsyncOpenAI(
    api_key=os.getenv("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

@dp.message(F.text)
async def handle_message(message: Message):
    thinking = await message.answer("🔍 Шукаю...")
    
    response = await client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {
                "role": "system",
                "content": "Ти корисний асистент. Відповідай українською мовою."
            },
            {
                "role": "user",
                "content": message.text
            }
        ]
    )
    
    answer = response.choices[0].message.content
    citations = response.citations if hasattr(response, 'citations') else []
    
    # Додаємо джерела до відповіді
    if citations:
        sources = "\n\n📚 **Джерела:**\n" + "\n".join(
            f"{i+1}. {url}" for i, url in enumerate(citations[:3])
        )
        answer += sources
    
    await thinking.delete()
    await message.answer(answer, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Файл .env

```env
TELEGRAM_BOT_TOKEN=your_telegram_token
PERPLEXITY_API_KEY=pplx-your-api-key
```

---

## Стрімінг відповідей

Для довгих відповідей краще використовувати стрімінг — бот оновлює повідомлення в реальному часі:

```python
@dp.message(F.text)
async def handle_stream(message: Message):
    sent = await message.answer("⏳")
    full_text = ""
    
    stream = await client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": message.text}],
        stream=True
    )
    
    async for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        full_text += delta
        
        # Оновлюємо повідомлення кожні ~100 символів
        if len(full_text) % 100 < len(delta):
            try:
                await sent.edit_text(full_text[:4096])
            except Exception:
                pass
    
    await sent.edit_text(full_text[:4096])
```

---

## Вибір моделі залежно від типу запиту

| Тип запиту | Модель | Причина |
|---|---|---|
| Звичайне питання | `sonar` | Швидко і дешево |
| Актуальні новини | `sonar-pro` | Глибший пошук |
| Складний аналіз | `sonar-reasoning` | Думає перед відповіддю |

---

## Обробка помилок

```python
from openai import APIError, RateLimitError

try:
    response = await client.chat.completions.create(...)
except RateLimitError:
    await message.answer("⚠️ Перевищено ліміт запитів. Спробуй через хвилину.")
except APIError as e:
    await message.answer(f"❌ Помилка API: {e.message}")
```

---

## Запуск через Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

```yaml
# docker-compose.yml
services:
  bot:
    build: .
    env_file: .env
    restart: unless-stopped
```

---

## Корисні посилання

- [Perplexity API Docs](https://docs.perplexity.ai)
- [aiogram документація](https://docs.aiogram.dev)
- [Приклади коду у папці `/07-api/python-examples/`](../07-api/python-examples/)
