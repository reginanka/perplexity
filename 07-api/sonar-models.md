← [Назад до головної](../README.md)
# 🧠 Sonar моделі Perplexity

> Повний огляд моделей API: коли що обирати.

---

## Лінійка Sonar моделей

Sonar — це власна лінійка моделей Perplexity, оптимізована для **пошуку в реальному часі**. Побудована поверх Llama 3, але доповнена унікальним механізмом живого пошуку.

---

## Таблиця моделей (актуально на 2025)

| Модель | Контекст | Пошук | Швидкість | Ціна (за 1M токенів) | Найкраще для |
|--------|----------|-------|-----------|---------------------|-------------|
| `sonar` | 128K | ✅ Базовий | ⚡⚡⚡ | $1 input / $1 output | Чатботи, FAQ |
| `sonar-pro` | 200K | ✅ Просунутий | ⚡⚡ | $3 input / $15 output | Аналітика, ресерч |
| `sonar-reasoning` | 128K | ✅ + Reasoning | ⚡ | $5 input / $8 output | Логічні задачі |
| `sonar-reasoning-pro` | 128K | ✅ + Deep reasoning | ⚡ | $8 input / $16 output | Складний аналіз |
| `sonar-deep-research` | 128K | ✅ Deep Research | 🐢 (хвилини) | — | Глибокий ресерч |

> ⚠️ Ціни можуть змінюватися. Актуальні дані: [pricing.md](pricing.md)

---

## Детальний опис кожної моделі

### `sonar` — Базова
```
Швидка, дешева, з веб-пошуком.
Ідеальна для: Telegram-бот, FAQ, щоденні запити
НЕ підходить для: глибокий аналіз, складна логіка
```

### `sonar-pro` — Просунута
```
Глибший пошук, більший контекст (200K), кращі відповіді.
Ідеальна для: ресерч, аналіз ринку, довгі документи
НЕ підходить для: high-volume дешеві запити
```

### `sonar-reasoning` — З reasoning
```
Mix: пошук + покрокове мислення (chain-of-thought).
Ідеальна для: порівняння, рішення задач, технічні питання
НЕ підходить для: прості lookups
```

### `sonar-reasoning-pro` — Максимум
```
Найсильніший reasoning з пошуком.
Ідеальна для: складний бізнес-аналіз, due diligence
Висока вартість — використовуй обдумано
```

### `sonar-deep-research` — Deep Research
```
Асинхронна модель для багатокрокового дослідження.
Використовується через Agent API.
Відповідь займає хвилини, але результат — повноцінний звіт.
```

---

## Також доступні сторонні моделі

Через Perplexity API можна звертатися і до:

| Модель | Провайдер | Особливість |
|--------|-----------|-------------|
| `r1-1776` | DeepSeek | Офлайн reasoning (без цензури) |

> Сторонні моделі **не мають веб-пошуку** — тільки static knowledge.

---

## Як обрати модель?

```
Простий чатбот/FAQ?
  → sonar

Аналіз, ресерч?
  → sonar-pro

Логічна задача, порівняння?
  → sonar-reasoning

Комплексний звіт (не терміново)?
  → sonar-deep-research (async)

Maximum quality?
  → sonar-reasoning-pro
```

---

## Приклад перемикання моделей

```python
from enum import Enum

class PerplexityModel(str, Enum):
    FAST = "sonar"
    PRO = "sonar-pro"
    REASONING = "sonar-reasoning"
    REASONING_PRO = "sonar-reasoning-pro"
    DEEP_RESEARCH = "sonar-deep-research"

def smart_query(question: str, depth: str = "normal") -> str:
    model_map = {
        "fast": PerplexityModel.FAST,
        "normal": PerplexityModel.PRO,
        "deep": PerplexityModel.REASONING_PRO
    }
    
    model = model_map.get(depth, PerplexityModel.PRO)
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}]
    )
    
    return response.choices[0].message.content
```
