← [Назад до головної](../README.md)
# 🚀 Швидкий старт з Perplexity API

> Від реєстрації до першого запиту за 10 хвилин.

---

## 1. Отримання API ключа

1. Зайди на [https://www.perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Натисни **"Generate"** поруч з полем API Key
3. Скопіюй та збережи ключ — він показується лише один раз
4. Поповни баланс (мінімум $5) у розділі **"Billing"**

> ⚠️ Зберігай ключ у `.env` файлі, ніколи не комітуй його у репозиторій!

---

## 2. Базова структура API

Perplexity API сумісний з форматом **OpenAI Chat Completions**, що означає:
- Той самий формат запитів `messages: [{role, content}]`
- Підтримка `system` prompt
- Стрімінг через `stream: true`
- Легка міграція з OpenAI SDK

**Base URL:** `https://api.perplexity.ai`  
**Endpoint:** `POST /chat/completions`

---

## 3. Перший запит (curl)

```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [
      {"role": "user", "content": "Що нового у світі AI сьогодні?"}
    ]
  }'
```

---

## 4. Перший запит (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar",
    messages=[
        {"role": "user", "content": "Що нового у світі AI сьогодні?"}
    ]
)

print(response.choices[0].message.content)
```

> 💡 Використовуй офіційний `openai` пакет — він повністю сумісний з Perplexity API.

---

## 5. Структура відповіді

```json
{
  "id": "abc123",
  "model": "sonar",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Текст відповіді..."
      },
      "finish_reason": "stop"
    }
  ],
  "citations": [
    "https://example.com/article1",
    "https://example.com/article2"
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 200,
    "total_tokens": 215
  }
}
```

**Унікальне для Perplexity:** поле `citations` — масив URL-джерел, на які спирається відповідь.

---

## 6. Налаштування оточення (.env)

```env
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

```python
# Завантаження у Python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")
```

---

## 7. Що далі?

| Файл | Що дізнаєшся |
|------|--------------|
| [search-api.md](search-api.md) | Параметри пошуку, фільтри, домени |
| [sonar-models.md](sonar-models.md) | Яку модель вибрати для свого кейсу |
| [pricing.md](pricing.md) | Скільки коштує і як оптимізувати |
| [python-examples/](python-examples/) | Готові приклади коду |
