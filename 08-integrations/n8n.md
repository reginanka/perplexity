← [Назад до головної](../README.md)
# ⚙️ Perplexity + n8n автоматизація

> Як підключити Perplexity API до n8n для створення автоматизованих воркфлоу з AI-пошуком.

---

## Що можна автоматизувати

- Щоденний моніторинг новин за темою
- Автоматичні відповіді на запити у Telegram/Slack
- Збір і аналіз інформації з веб для звітів
- Перевірка фактів у вхідних даних
- Генерація контенту на основі актуальних джерел

---

## Метод 1: HTTP Request Node (найпростіший)

n8n має вбудований **HTTP Request** вузол — ним можна викликати Perplexity API без будь-яких плагінів.

### Налаштування вузла

**Method:** `POST`  
**URL:** `https://api.perplexity.ai/chat/completions`

**Headers:**
```
Authorization: Bearer {{ $env.PERPLEXITY_API_KEY }}
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "system",
      "content": "Ти корисний асистент. Відповідай українською."
    },
    {
      "role": "user",
      "content": "{{ $json.query }}"
    }
  ],
  "max_tokens": 1024
}
```

### Отримання відповіді

Відповідь знаходиться в:
```
{{ $json.choices[0].message.content }}
```

Джерела (citations):
```
{{ $json.citations }}
```

---

## Метод 2: OpenAI Node (через сумісність)

Perplexity сумісний з OpenAI SDK. У n8n можна використати стандартний **OpenAI** вузол:

1. Додай **Credentials** → OpenAI API
2. **API Key:** твій `pplx-...` ключ
3. **Base URL:** `https://api.perplexity.ai`
4. Вибери операцію: **Chat Completion**
5. Вкажи модель вручну: `sonar-pro`

> ⚠️ Не всі параметри OpenAI Node підтримуються Perplexity. Використовуй лише базові: `model`, `messages`, `max_tokens`.

---

## Приклад воркфлоу: Щоденний дайджест новин

```
[Schedule Trigger] → [Set Topics] → [HTTP Request Perplexity] → [Format Message] → [Send Telegram]
```

### Schedule Trigger
- Cron: `0 9 * * *` (щодня о 9:00)

### Set Node (теми для моніторингу)
```json
{
  "query": "Останні новини про штучний інтелект за сьогодні. Дай топ-5 подій з джерелами."
}
```

### HTTP Request (Perplexity)
Як описано у Методі 1 вище.

### Format Message (Code Node)
```javascript
const content = $input.first().json.choices[0].message.content;
const citations = $input.first().json.citations || [];

let message = `📰 *AI Дайджест — ${new Date().toLocaleDateString('uk-UA')}*\n\n`;
message += content;

if (citations.length > 0) {
  message += '\n\n📚 *Джерела:*\n';
  citations.slice(0, 5).forEach((url, i) => {
    message += `${i+1}. ${url}\n`;
  });
}

return [{ json: { message } }];
```

### Telegram Node
- **Operation:** Send Message
- **Text:** `{{ $json.message }}`
- **Parse Mode:** Markdown

---

## Зберігання API ключа у n8n

1. Відкрий **Settings** → **Variables** або використай **Credentials**
2. Додай змінну `PERPLEXITY_API_KEY`
3. У вузлах посилайся через `{{ $env.PERPLEXITY_API_KEY }}`

Або через **Credentials → Header Auth:**
- **Name:** `Authorization`
- **Value:** `Bearer pplx-your-key`

---

## Обробка помилок у воркфлоу

Додай **Error Trigger** вузол до воркфлоу:

1. Відкрий налаштування воркфлоу → **Error Workflow**
2. Створи окремий воркфлоу для обробки помилок
3. У ньому відправляй сповіщення в Telegram або на email

```javascript
// Code Node для форматування помилки
const error = $input.first().json;
return [{
  json: {
    message: `❌ Помилка воркфлоу: ${error.workflow.name}\n${error.execution.error.message}`
  }
}];
```

---

## Самохостинг n8n + Perplexity через Docker

```yaml
# docker-compose.yml
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=securepassword
      - PERPLEXITY_API_KEY=pplx-your-key
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped

volumes:
  n8n_data:
```

---

## Корисні шаблони

| Сценарій | Складність | Опис |
|---|---|---|
| Дайджест новин | ⭐ Легко | Schedule → Perplexity → Telegram |
| FAQ бот | ⭐⭐ Середньо | Webhook → Perplexity → Відповідь |
| Аналіз конкурентів | ⭐⭐⭐ Складно | Тригер → Кілька запитів → Звіт у Google Docs |

---

## Корисні посилання

- [n8n документація](https://docs.n8n.io)
- [Perplexity API Reference](https://docs.perplexity.ai/api-reference)
- [n8n Community Templates](https://n8n.io/workflows/)
