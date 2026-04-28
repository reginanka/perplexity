← [Назад до головної](../README.md)
# 💰 Ціни, токени та оптимізація витрат

> Як не переплачувати за Perplexity API.

---

## Структура ціноутворення

Perplexity API використовує **pay-as-you-go** модель:
- Оплата за **вхідні токени** (твій запит + контекст)
- Оплата за **вихідні токени** (відповідь)
- Додатково: **search units** за кожен веб-пошук

---

## Актуальні ціни (2025)

### Sonar моделі

| Модель | Input ($/1M) | Output ($/1M) | Search unit |
|--------|-------------|--------------|-------------|
| `sonar` | $1 | $1 | $5 / 1000 req |
| `sonar-pro` | $3 | $15 | $5 / 1000 req |
| `sonar-reasoning` | $5 | $8 | $5 / 1000 req |
| `sonar-reasoning-pro` | $8 | $16 | $5 / 1000 req |
| `sonar-deep-research` | $2 | $8 | included |

> 📌 Перевіряй актуальні ціни на [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)

---

## Що таке токени?

**Приблизні орієнтири:**
- 1 слово ≈ 1.3 токени
- 1 000 слів ≈ 1 300 токени
- Одна сторінка A4 ≈ 500-700 токенів

```python
# Перевірка використання токенів
response = client.chat.completions.create(...)

usage = response.usage
print(f"Вхідні: {usage.prompt_tokens}")
print(f"Вихідні: {usage.completion_tokens}")
print(f"Всього: {usage.total_tokens}")
```

---

## Стратегії оптимізації

### 1. Вибирай правильну модель
```python
# ❌ Дорого для простих задач
model = "sonar-reasoning-pro"  # для FAQ бота

# ✅ Правильний вибір
model = "sonar"  # для FAQ бота
model = "sonar-pro"  # для аналізу
```

### 2. Обмежуй довжину відповіді
```python
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[...],
    max_tokens=500  # обмеж вихідні токени
)
```

### 3. Оптимізуй system prompt
```python
# ❌ Довгий загальний system prompt
system = """Ти дуже корисний AI асистент з глибокими знаннями
в усіх сферах. Ти завжди відповідаєш ввічливо і детально..."""

# ✅ Короткий і конкретний
system = "Відповідай коротко. Лише факти. Українською."
```

### 4. Кешуй часті запити
```python
import hashlib
import json
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(question: str) -> str:
    """Кешує відповіді для повторних запитів."""
    response = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content
```

### 5. Контролюй search_context_size
```python
# Для простих питань — мінімальний контекст
web_search_options={"search_context_size": "low"}  # дешевше

# Тільки для складних — великий контекст
web_search_options={"search_context_size": "high"}  # дорожче
```

---

## Підрахунок витрат

```python
class CostTracker:
    """Трекер витрат для моніторингу бюджету."""
    
    PRICES = {
        "sonar": {"input": 1.0, "output": 1.0},
        "sonar-pro": {"input": 3.0, "output": 15.0},
        "sonar-reasoning": {"input": 5.0, "output": 8.0},
    }
    SEARCH_UNIT_COST = 0.005  # $5 per 1000
    
    def __init__(self):
        self.total_cost = 0.0
        self.requests = 0
    
    def track(self, response, model: str):
        prices = self.PRICES.get(model, {"input": 1.0, "output": 1.0})
        input_cost = (response.usage.prompt_tokens / 1_000_000) * prices["input"]
        output_cost = (response.usage.completion_tokens / 1_000_000) * prices["output"]
        search_cost = self.SEARCH_UNIT_COST  # 1 search unit per request
        
        total = input_cost + output_cost + search_cost
        self.total_cost += total
        self.requests += 1
        
        return total
    
    def report(self):
        print(f"Запитів: {self.requests}")
        print(f"Загальна вартість: ${self.total_cost:.4f}")
        print(f"Середня вартість: ${self.total_cost/max(1,self.requests):.4f}")

# Використання
tracker = CostTracker()
# ...
cost = tracker.track(response, "sonar-pro")
tracker.report()
```

---

## Rate Limits

| Тип | Ліміт |
|-----|-------|
| Requests per minute | 50 RPM (стандарт) |
| Requests per day | Без обмежень (за балансом) |
| Max tokens per request | Залежить від моделі |

> Якщо потрібні вищі ліміти — зв'яжись з Perplexity через enterprise форму.

---

## Практичний бюджет

| Сценарій | Модель | Запитів/день | ~Вартість/місяць |
|----------|--------|--------------|------------------|
| Telegram FAQ бот | sonar | 1000 | ~$5-10 |
| Ресерч-інструмент | sonar-pro | 200 | ~$15-25 |
| Автоматизація n8n | sonar | 5000 | ~$20-40 |
| Аналітична платформа | sonar-pro | 1000 | ~$50-80 |
