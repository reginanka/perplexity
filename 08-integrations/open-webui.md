← [Назад до головної](../README.md)
# 🖥️ Perplexity + Open WebUI

> Як підключити Perplexity API до Open WebUI і отримати зручний ChatGPT-подібний інтерфейс з доступом до веб-пошуку.

---

## Що таке Open WebUI

[Open WebUI](https://github.com/open-webui/open-webui) — це self-hosted веб-інтерфейс для LLM, який підтримує OpenAI-сумісні API. Оскільки Perplexity повністю сумісний з OpenAI SDK, підключення займає 2 хвилини.

**Переваги використання Perplexity через Open WebUI:**
- Зручний чат-інтерфейс із збереженням історії
- Можливість перемикатися між моделями (Sonar, Claude, GPT)
- Підтримка системних промптів і персонажів
- Кілька користувачів на одному сервері

---

## Варіант 1: Підключення через OpenAI Connection

Це найпростіший спосіб — Open WebUI підтримує кастомні OpenAI-сумісні ендпоінти.

### Кроки

1. Відкрий Open WebUI → **Settings** (іконка шестерні)
2. Перейди в **Admin Panel** → **Settings** → **Connections**
3. У розділі **OpenAI API** натисни **+** (додати підключення)
4. Заповни:
   - **API Base URL:** `https://api.perplexity.ai`
   - **API Key:** `pplx-your-api-key`
5. Натисни **Save** та перевір підключення кнопкою **Verify**

### Вибір моделей

Після підключення у списку моделей з'являться Perplexity моделі. Якщо не з'явились — додай вручну:

1. **Admin Panel** → **Models** → **Add Model**
2. **Model ID:** `sonar-pro` (або інша модель)
3. **Display Name:** `Perplexity Sonar Pro`

---

## Варіант 2: Docker Compose з Perplexity як default

```yaml
# docker-compose.yml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OPENAI_API_BASE_URL=https://api.perplexity.ai
      - OPENAI_API_KEY=pplx-your-api-key
      - WEBUI_SECRET_KEY=your-secret-key
    volumes:
      - open-webui:/app/backend/data
    restart: unless-stopped

volumes:
  open-webui:
```

```bash
docker compose up -d
# Відкрий http://localhost:3000
```

---

## Рекомендовані системні промпти для Perplexity

### Загальний асистент з веб-пошуком
```
Ти корисний асистент з доступом до актуальної інформації з інтернету.
Завжди відповідай українською мовою.
Коли наводиш факти — вказуй на яких джерелах базуєшся.
Будь лаконічним але вичерпним.
```

### Дослідник ринку
```
Ти аналітик ринку з доступом до актуальних даних.
Для кожного запиту: знайди актуальну інформацію, проаналізуй тренди,
надай структурований звіт з посиланнями на джерела.
Відповідай українською.
```

### Технічний консультант
```
Ти старший розробник зі знанням актуальних версій бібліотек і фреймворків.
Шукай документацію та приклади коду. Відповідай з прикладами коду.
Якщо питання про конкретну версію — перевір актуальну документацію.
```

---

## Підключення кількох провайдерів одночасно

Open WebUI дозволяє підключити кілька API провайдерів:

```yaml
environment:
  # Perplexity (веб-пошук)
  - OPENAI_API_BASE_URLS=https://api.perplexity.ai;https://api.openai.com/v1
  - OPENAI_API_KEYS=pplx-your-key;sk-openai-key
```

Тепер у чаті можна перемикатись між `sonar-pro` (Perplexity) та `gpt-4o` (OpenAI).

---

## Порівняння моделей у контексті Open WebUI

| Модель | Сильна сторона | Коли використовувати |
|---|---|---|
| `sonar` | Швидкий пошук | Прості питання, новини |
| `sonar-pro` | Глибокий пошук | Дослідження, аналіз |
| `sonar-reasoning` | Логічний аналіз | Складні задачі, порівняння |
| `sonar-reasoning-pro` | Максимум якості | Критичні рішення |

---

## Використання з Ollama (гібридна схема)

Можна поєднати локальні моделі (Ollama) і Perplexity в одному інтерфейсі:

```yaml
services:
  ollama:
    image: ollama/ollama
    volumes:
      - ollama:/root/.ollama
    ports:
      - "11434:11434"

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - OPENAI_API_BASE_URL=https://api.perplexity.ai
      - OPENAI_API_KEY=pplx-your-key
    ports:
      - "3000:8080"
    depends_on:
      - ollama

volumes:
  ollama:
  open-webui:
```

**Результат:** локальні моделі (llama3, mistral) + Perplexity з веб-пошуком — все в одному інтерфейсі.

---

## Трабл-шутинг

| Проблема | Рішення |
|---|---|
| Моделі не відображаються | Перевір API key та Base URL у Connections |
| Відповідь порожня | Перевір чи модель підтримує chat completions |
| Помилка 401 | API ключ невірний або прострочений |
| Помилка 429 | Перевищено rate limit — зменши частоту запитів |

---

## Корисні посилання

- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
- [Open WebUI документація](https://docs.openwebui.com)
- [Perplexity API моделі](../07-api/sonar-models.md)
- [Швидкий старт з Perplexity API](../07-api/getting-started.md)
