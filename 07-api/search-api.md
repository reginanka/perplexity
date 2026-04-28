← [Назад до головної](../README.md)
# 🔍 Perplexity Search API

> Як інтегрувати живий веб-пошук у свій проєкт.

---

## Що таке Search API?

Search API — це серце Perplexity. На відміну від звичайних LLM, він **активно шукає в інтернеті** під час генерації відповіді, а не покладається лише на навчальні дані.

**Ключові переваги:**
- Актуальна інформація (не обмежена датою тренування)
- Посилання на джерела у полі `citations`
- Можливість фільтрувати домени
- Підтримка пошуку в академічних базах

---

## Параметри запиту

```python
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "запит"}],
    
    # --- Специфічні параметри Perplexity ---
    search_domain_filter=["bbc.com", "reuters.com"],  # тільки ці сайти
    search_recency_filter="week",   # month / week / day / hour
    return_citations=True,          # повернути масив citations
    return_images=False,            # включити зображення
    return_related_questions=True,  # пов'язані питання
    web_search_options={"search_context_size": "high"}  # low / medium / high
)
```

---

## search_recency_filter — фільтр свіжості

| Значення | Опис | Коли використовувати |
|----------|------|---------------------|
| `"hour"` | Остання година | Breaking news, крипто |
| `"day"` | Останній день | Щоденні дайджести |
| `"week"` | Тиждень | Поточні події |
| `"month"` | Місяць | Тренди, аналітика |
| (не вказано) | Без обмежень | Загальні знання |

---

## search_domain_filter — фільтр доменів

```python
# Дозволити тільки певні сайти
search_domain_filter=["wikipedia.org", "arxiv.org"]

# Заблокувати сайти (з мінусом)
search_domain_filter=["-reddit.com", "-quora.com"]

# Комбінований варіант
search_domain_filter=["nytimes.com", "-twitter.com"]
```

> ⚠️ Максимум 10 доменів у одному запиті.

---

## web_search_options — глибина пошуку

```python
web_search_options={
    "search_context_size": "high"  # low | medium | high
}
```

| Розмір | Токенів контексту | Вартість | Коли використовувати |
|--------|------------------|----------|---------------------|
| `low` | ~3K | Найдешевше | Прості питання |
| `medium` | ~8K | Середня | Більшість задач |
| `high` | ~20K+ | Дорожче | Складний аналіз |

---

## Робота з citations

```python
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "Останні новини про Україну"}],
    return_citations=True
)

content = response.choices[0].message.content
citations = response.citations  # список URL

print("Відповідь:", content)
print("\nДжерела:")
for i, url in enumerate(citations, 1):
    print(f"[{i}] {url}")
```

---

## Приклад: Новинний дайджест

```python
import os
from openai import OpenAI
from datetime import date

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)

def get_daily_digest(topic: str) -> dict:
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[{
            "role": "system",
            "content": "Ти новинний аналітик. Коротко підсумовуй головні новини."
        }, {
            "role": "user",
            "content": f"Головні новини за сьогодні на тему: {topic}"
        }],
        search_recency_filter="day",
        return_citations=True
    )
    
    return {
        "summary": response.choices[0].message.content,
        "sources": response.citations,
        "tokens_used": response.usage.total_tokens
    }

result = get_daily_digest("штучний інтелект")
print(result["summary"])
```

---

## Пов'язані питання

```python
response = client.chat.completions.create(
    model="sonar",
    messages=[{"role": "user", "content": "Що таке квантові комп'ютери?"}],
    return_related_questions=True
)

# Пов'язані питання для UX
related = response.related_questions
for q in related:
    print("-", q)
```

Використовуй для навігації в чатботі або для розширення теми дослідження.
