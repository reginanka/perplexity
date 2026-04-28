← [Назад до головної](../README.md)
# 🤖 Perplexity Agent API

> Автономне виконання багатокрокових задач.

---

## Що таке Agent API?

Agent API (також відомий як **Async API**) дозволяє запускати **тривалі, багатокрокові задачі**, які не вкладаються у звичайний request-response цикл. Замість чекати на відповідь, ти отримуєш `task_id` і опитуєш статус асинхронно.

**Відмінності від звичайного API:**

| Звичайний API | Agent API |
|---------------|-----------|
| Синхронний | Асинхронний |
| Один крок | Багатокрокові задачі |
| Відповідь одразу | Опитування статусу |
| До ~2 хв | До 30+ хв |
| Простий текст | Структурований звіт |

---

## Коли використовувати Agent API?

- **Deep Research** — глибокий аналіз теми з десятками джерел
- **Competitive Analysis** — збір даних про конкурентів
- **Market Research** — дослідження ринку
- **Report Generation** — створення структурованих звітів
- **Data Aggregation** — збір інформації з багатьох джерел

---

## Запуск задачі

```python
import requests
import os

API_KEY = os.environ["PERPLEXITY_API_KEY"]
BASE_URL = "https://api.perplexity.ai"

def start_research_task(query: str) -> str:
    """Запускає асинхронну дослідницьку задачу."""
    response = requests.post(
        f"{BASE_URL}/research/tasks",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "query": query,
            "type": "deep_research"  # або "search"
        }
    )
    
    data = response.json()
    return data["task_id"]

task_id = start_research_task(
    "Аналіз ринку AI-автоматизації в Україні 2025"
)
print(f"Задача запущена: {task_id}")
```

---

## Перевірка статусу

```python
import time

def get_task_status(task_id: str) -> dict:
    """Перевіряє статус задачі."""
    response = requests.get(
        f"{BASE_URL}/research/tasks/{task_id}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    return response.json()

def wait_for_completion(task_id: str, poll_interval: int = 10) -> dict:
    """Чекає завершення задачі з polling."""
    while True:
        status = get_task_status(task_id)
        
        if status["status"] == "completed":
            print("✅ Задача завершена!")
            return status
        elif status["status"] == "failed":
            raise Exception(f"Задача провалилася: {status.get('error')}")
        else:
            print(f"⏳ Статус: {status['status']}...")
            time.sleep(poll_interval)

# Використання
result = wait_for_completion(task_id)
print(result["output"])
```

---

## Повна картина статусів

```
pending → running → completed
                 ↘ failed
```

| Статус | Опис |
|--------|------|
| `pending` | Задача в черзі |
| `running` | Виконується |
| `completed` | Готово, результат доступний |
| `failed` | Помилка виконання |

---

## Структура результату

```json
{
  "task_id": "task_abc123",
  "status": "completed",
  "output": "Детальний звіт...",
  "citations": ["https://...", "https://..."],
  "created_at": "2025-01-01T10:00:00Z",
  "completed_at": "2025-01-01T10:05:30Z",
  "usage": {
    "total_tokens": 15000
  }
}
```

---

## Webhook (замість polling)

Для production систем краще використовувати webhook:

```python
def start_task_with_webhook(query: str, webhook_url: str) -> str:
    response = requests.post(
        f"{BASE_URL}/research/tasks",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "query": query,
            "type": "deep_research",
            "webhook_url": webhook_url  # Perplexity надішле POST сюди
        }
    )
    return response.json()["task_id"]
```

> 💡 Для локального тестування webhook використовуй [ngrok](https://ngrok.com) або [webhook.site](https://webhook.site).

---

## Інтеграція з n8n / Make.com

Agent API чудово підходить для асинхронних workflow:

1. **Trigger** → HTTP Request (запуск задачі)
2. **Wait** → зберегти `task_id`
3. **Poll** → HTTP Request кожні N секунд
4. **Process** → обробка результату
5. **Notify** → Telegram / Email

Див. приклад: [../08-integrations/n8n.md](../08-integrations/n8n.md)
