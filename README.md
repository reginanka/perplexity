# 🔍 Perplexity AI — Повний гід екосистемою

> **Перший україномовний репозиторій про екосистему Perplexity AI**  
> Описи, порівняння, хаки, інтеграції та практичні приклади коду.

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/reginanka/perplexity?style=for-the-badge&logo=github&color=FFD700)](https://github.com/reginanka/perplexity/stargazers)
[![Last updated](https://img.shields.io/github/last-commit/reginanka/perplexity?style=for-the-badge&color=01696f)](https://github.com/reginanka/perplexity/commits)
[![Ukrainian](https://img.shields.io/badge/мова-українська-blue?style=for-the-badge)](README.md)

</div>



## 🗺️ Навігація по розділах


### 🌐 [01 — Огляд екосистеми](./01-overview/README.md)
Що таке Perplexity, карта продуктів, режими роботи

📄 [Що таке Perplexity?](./01-overview/what-is-perplexity.md) > Повний огляд продукту, чим відрізняється від ChatGPT, Google, Claude. Ключові переваги і обмеження.

📄 [Карта екосистеми](./01-overview/ecosystem-map.md) > Всі продукти Perplexity: Search, Spaces, API, Computer, Labs — де що знаходиться і як пов'язане.

📄 [Порівняння режимів](./01-overview/modes-comparison.md) > Auto / Pro Search / Deep Research / Labs — коли що вмикати і в чому різниця на практиці.


---


### 🔎 [02 — Пошук](./02-search/README.md)
Як шукати ефективно, оператори, Focus-режими, джерела

📄 [Як працює пошук](./02-search/how-search-works.md) > Внутрішня механіка: як Perplexity обирає джерела, ранжує результати і будує відповідь.

📄 [Оператори пошуку](./02-search/search-operators.md) > Спеціальні команди для точного пошуку: site:, filetype:, before:, after: та інші трюки.

📄 [Focus-режими](./02-search/focus-modes.md) > Web, Academic, YouTube, Reddit, Wolfram Alpha, Maps — коли який режим вибирати.

---

### 🤖 [03 — Моделі](./03-models/README.md)

📄 [Всі доступні моделі](./03-models/available-models.md) > Sonar Pro, GPT-4o, Claude 3.5/3.7, Gemini 2.0, Grok — що є в наявності і на яких планах.

📄 [Коли який модель](./03-models/when-to-use-what.md) > Практичний гайд: кодинг → Claude, розмірковування → o1/Sonar Reasoning, контент → GPT-4o.

📄 [Бенчмарк моделей](./03-models/models-benchmark.md) > Реальні порівняння на задачах: аналіз тексту, код, математика, творчі завдання.

---

### 🧪 [04 — Deep Research](./04-deep-research/README.md)

📄 [Що таке Deep Research](./04-deep-research/what-is-deep-research.md) > Як він працює: ітеративний пошук, синтез джерел, формування звіту. Обмеження і сильні сторони.

📄 [Кейси використання](./04-deep-research/use-cases.md) > Аналіз ринку, конкурентна розвідка, наукові огляди, дью-ділідженс — реальні приклади.

📄 [Поради для кращих результатів](./04-deep-research/tips.md) > Як формулювати запити, щоб отримати максимально точний і корисний звіт.


---

### 🗂️ [05 — Spaces](./05-spaces/README.md)

📄 [Що таке Spaces](./05-spaces/what-are-spaces.md) > Огляд функції: завантаження документів, налаштування AI, доступ для команди.

📄 [Швидке налаштування](./05-spaces/setup-guide.md) > Покроковий гайд: від створення Space до першого запиту по документах.

📄 [Spaces як RAG-система](./05-spaces/spaces-as-rag.md) > Порівняння зі звичайним RAG. Коли Spaces достатньо, а коли потрібне кастомне рішення.

---

### 💻 [06 — Computer (AI-агент)](./06-computer/README.md)

📄 [Що таке Computer](./06-computer/what-is-computer.md) > Огляд агентських можливостей: що вміє, як керувати браузером, які задачі вирішує.

📄 [Можливості агента](./06-computer/capabilities.md) > Браузер, файли, код, пошук, sub-агенти — повний список того що вміє Computer.

📄 [Приклади автоматизації](./06-computer/automation-examples.md) > Реальні юзкейси: збір даних, заповнення форм, дослідження конкурентів.

---

### ⚡ [07 — API](./07-api/README.md)

📄 [Швидкий старт](./07-api/getting-started.md) > API ключ, базовий запит, перша відповідь — запускаємо за 5 хвилин.

📄 [Search API](./07-api/search-api.md) > Endpoint'и, параметри, приклади запитів для інтеграції пошуку у свій проект.

📄 [Agent API](./07-api/agent-api.md) > Автономні задачі через API: як запускати і управляти агентськими воркфлоу.

📄 [Sonar моделі](./07-api/sonar-models.md) > sonar, sonar-pro, sonar-reasoning, sonar-reasoning-pro — різниця і коли що використовувати.

📄 [Ціни та оптимізація](./07-api/pricing.md) > Токени, ціни за запит, поради щодо зниження витрат для production-проектів.

🐍 [Python приклади](./07-api/python-examples/README.md) > Готові приклади коду: базовий запит, streaming, Telegram-бот інтеграція.


---

### 🔗 [08 — Інтеграції](./08-integrations/README.md)


📄 [Telegram бот](./08-integrations/telegram-bot.md) > Покроковий гайд: бот на python-telegram-bot з Perplexity API, деплой на Render.

📄 [n8n автоматизація](./08-integrations/n8n.md) > HTTP Request node, обробка відповіді, готові воркфлоу шаблони для n8n.

📄 [Make.com інтеграція](./08-integrations/make-com.md) > HTTP-модуль у Make.com, сценарії з Perplexity для контент-маркетингу та ресерчу.

📄 [Open WebUI](./08-integrations/open-webui.md) > Підключення Sonar моделей до Open WebUI для локального використання.

---

### ⚖️ [09 — Порівняння](./09-comparisons/README.md)

📄 [Perplexity vs ChatGPT](./09-comparisons/perplexity-vs-chatgpt.md) > Детальне порівняння по 10 критеріям: пошук, якість, ціна, інтеграції, API.

📄 [Perplexity vs Gemini](./09-comparisons/perplexity-vs-gemini.md) > Порівняння з Google Gemini: пошук в реальному часі, мультимодальність, Deep Research.

📄 [Perplexity vs Claude.ai](./09-comparisons/perplexity-vs-claude.md) > Perplexity vs Claude.ai: коли Perplexity виграє, а коли краще використовувати Claude.

📄 [Free vs Pro план](./09-comparisons/free-vs-pro.md) > Що реально дає Pro план: ліміти, моделі, Deep Research, API — чи варто платити.

---

### 🛠️ [10 — Хаки та трюки](./10-hacks/README.md)

📄 [Максимум з безкоштовного плану](./10-hacks/free-tier-tricks.md) > Як обійти ліміти Pro Search, використовувати потужні моделі безкоштовно.

📄 [Трюки з промптами](./10-hacks/prompt-tricks.md) > Специфічні для Perplexity техніки: Focus + промпт, ланцюжки запитів, формат виводу.

📄 [Приховані фічі](./10-hacks/hidden-features.md) > Маловідомі можливості інтерфейсу: Collections, Share, Export, keyboard shortcuts.

📄 [Воркфлоу продуктивності](./10-hacks/productivity-workflows.md) > Щоденні сценарії: ранковий ресерч, моніторинг новин, аналіз статей — готові шаблони.

---

## 🚀 Чому Perplexity?

На відміну від ChatGPT чи Claude, Perplexity — це **пошуковий AI**, що завжди дає відповіді з актуальних джерел з цитатами. Але більшість користувачів використовує лише 10% його можливостей.

| Можливість | Що це | Для кого |
|---|---|---|
| 🔍 **Search** | Дослідницький інструмент з цитатами | Всі |
| 🧪 **Deep Research** | Автоматичні звіти на рівні аналітика | Підприємці, дослідники |
| 🗂️ **Spaces** | База знань без налаштування RAG | Команди, бізнес |
| 💻 **Computer** | AI-агент що виконує задачі | Автоматизатори |
| ⚡ **API** | Інтеграція у власні проекти та боти | Розробники |

---

## 💡 Для кого цей репозиторій

- 👨‍💻 **Розробники** — інтеграція Perplexity API у власні проекти
- ⚙️ **Автоматизатори** — n8n, Make.com воркфлоу
- 📱 **Telegram-бот розробники** — AI-пошук у ботах
- 📊 **Підприємці** — AI для досліджень і контенту
- 💸 **Всі** — максимум з безкоштовного плану

---

<div align="center">

🇺🇦 **Весь контент українською мовою. Регулярно оновлюється.**

[⭐ Поставте зірку якщо корисно](https://github.com/reginanka/perplexity) · [🐛 Повідомити про помилку](https://github.com/reginanka/perplexity/issues) · [💡 Запропонувати тему](https://github.com/reginanka/perplexity/issues/new)

</div>
