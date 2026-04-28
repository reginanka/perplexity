← [Назад до головної](../README.md)
# 🔧 Perplexity + Make.com

> Як інтегрувати Perplexity API у Make.com (колишній Integromat) для no-code автоматизації з AI-пошуком.

---

## Чому Make.com + Perplexity

- Візуальний конструктор сценаріїв без коду
- 1000+ готових інтеграцій (Google, Telegram, Slack, Notion...)
- Perplexity підключається через модуль **HTTP**
- Ідеально для не-розробників

---

## Крок 1: Додати HTTP модуль

Perplexity поки не має офіційного модуля в Make.com, тому використовуємо **HTTP → Make a request**.

### Налаштування

| Поле | Значення |
|---|---|
| **URL** | `https://api.perplexity.ai/chat/completions` |
| **Method** | `POST` |
| **Headers** | `Authorization: Bearer YOUR_KEY` + `Content-Type: application/json` |
| **Body type** | `Raw` |
| **Content type** | `JSON (application/json)` |

### Тіло запиту

```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "system",
      "content": "Відповідай лаконічно українською мовою."
    },
    {
      "role": "user",
      "content": "{{1.text}}"
    }
  ],
  "max_tokens": 800
}
```

> `{{1.text}}` — це дані з попереднього модуля (наприклад, Telegram повідомлення)

---

## Крок 2: Зберігання API ключа

**Варіант A — напряму у Headers (швидко, але небезпечно):**
```
Authorization: Bearer pplx-your-api-key-here
```

**Варіант B — через Data Store (рекомендовано):**
1. Відкрий **Data Store** → Створи новий
2. Додай запис: `key = perplexity_api_key`, `value = pplx-...`
3. У сценарії спочатку зчитуй ключ через **Data Store → Get a record**
4. Використовуй: `{{DataStore.perplexity_api_key}}`

---

## Приклад 1: Telegram бот із пошуком

```
[Telegram → Watch Updates]
    ↓
[HTTP → Perplexity API]
    ↓
[Telegram → Send Message]
```

### Watch Updates (Telegram)
- **Connection:** твій бот
- Фільтр: тільки текстові повідомлення (`{{1.message.text}} exists`)

### HTTP (Perplexity)
- URL та Headers як описано вище
- У `content` вставляємо: `{{1.message.text}}`

### Send Message (Telegram)
- **Chat ID:** `{{1.message.chat.id}}`
- **Text:**
```
{{2.data.choices[].message.content}}
```

> Щоб отримати відповідь: `{{HTTPModule.data.choices[1].message.content}}`

---

## Приклад 2: Автоматичний аналіз нових листів Gmail

```
[Gmail → Watch Emails]
    ↓
[HTTP → Perplexity «Підсумуй лист»]
    ↓
[Notion → Create Page]
```

### HTTP Body для аналізу листа
```json
{
  "model": "sonar",
  "messages": [
    {
      "role": "user",
      "content": "Підсумуй цей email в 3 реченнях і вкажи необхідні дії:\n\n{{1.snippet}}"
    }
  ],
  "max_tokens": 300
}
```

---

## Приклад 3: Моніторинг бренду / ключових слів

```
[Schedule → кожні 6 годин]
    ↓
[HTTP → Perplexity «Новини про {бренд}»]
    ↓
[Filter → лише якщо є нові згадки]
    ↓
[Slack → Send Message]
```

### Запит для моніторингу
```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "Знайди свіжі новини та згадки про 'НазваБренду' за останні 24 години. Перерахуй з посиланнями."
    }
  ]
}
```

---

## Парсинг відповіді Make.com

Make.com автоматично парсить JSON. Шлях до відповіді:

```
# Текст відповіді
{{НазваHTTPМодуля.data.choices[].message.content}}

# Перше джерело
{{НазваHTTPМодуля.data.citations[]}}

# Модель, що використовувалась
{{НазваHTTPМодуля.data.model}}
```

---

## Обробка помилок

1. Клікни правою кнопкою на HTTP модуль → **Add error handler**
2. Вибери **Resume** або **Rollback**
3. Додай **Telegram → Send Message** для сповіщення про помилку:
```
❌ Сценарій Make.com: помилка API
Код: {{error.statusCode}}
Повідомлення: {{error.message}}
```

---

## Ліміти та оптимізація

| Параметр | Рекомендація |
|---|---|
| `max_tokens` | 500-1000 для чатів, 2000 для аналізу |
| Модель | `sonar` для простих, `sonar-pro` для складних запитів |
| Retry | Додай **repeater** при помилці 429 (rate limit) |
| Кешування | Зберігай повторювані відповіді у Data Store |

---

## Корисні посилання

- [Make.com документація HTTP модуля](https://www.make.com/en/help/app/http)
- [Perplexity API Reference](https://docs.perplexity.ai/api-reference)
- [Make.com шаблони](https://www.make.com/en/templates)
