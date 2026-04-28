#!/usr/bin/env python3
"""
Приклад 3: Автоматичний новинний дайджест

Функції:
- Збирає новини по темах
- Фільтрує за свіжістю
- Зберігає у JSON
- Може відправляти у Telegram

Вимоги:
    pip install openai python-dotenv requests
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)

# Теми для дайджесту
DIGEST_TOPICS = [
    "штучний інтелект та машинне навчання",
    "технологічні стартапи України",
    "n8n та автоматизація",
]


def get_news_for_topic(topic: str, recency: str = "day") -> dict:
    """Отримує новини по темі."""
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ти новинний редактор. Підсумовуй новини коротко і структуровано. "
                    "Формат: 3-5 пунктів з найважливішим. Мова: українська."
                )
            },
            {
                "role": "user",
                "content": f"Головні новини за сьогодні на тему: {topic}"
            }
        ],
        search_recency_filter=recency,
        return_citations=True,
        web_search_options={"search_context_size": "medium"}
    )
    
    return {
        "topic": topic,
        "summary": response.choices[0].message.content,
        "sources": getattr(response, "citations", [])[:5],
        "tokens": response.usage.total_tokens,
        "timestamp": datetime.now().isoformat()
    }


def create_daily_digest(topics: list = None) -> dict:
    """Створює повний щоденний дайджест."""
    if topics is None:
        topics = DIGEST_TOPICS
    
    digest = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "created_at": datetime.now().isoformat(),
        "topics": [],
        "total_tokens": 0
    }
    
    for topic in topics:
        print(f"⏳ Збираємо новини: {topic}")
        news = get_news_for_topic(topic)
        digest["topics"].append(news)
        digest["total_tokens"] += news["tokens"]
        print(f"✅ Готово ({news['tokens']} токенів)")
    
    return digest


def format_for_telegram(digest: dict) -> str:
    """Форматує дайджест для Telegram."""
    text = f"📰 *Дайджест за {digest['date']}*\n\n"
    
    for item in digest["topics"]:
        text += f"🔹 *{item['topic'].upper()}*\n"
        text += item["summary"] + "\n"
        
        if item["sources"]:
            text += "\n📚 Джерела:\n"
            for i, url in enumerate(item["sources"][:2], 1):
                text += f"{i}. {url}\n"
        
        text += "\n" + "─" * 30 + "\n\n"
    
    text += f"_Токенів використано: {digest['total_tokens']}_"
    return text


def save_digest(digest: dict, filename: str = None):
    """Зберігає дайджест у JSON файл."""
    if filename is None:
        filename = f"digest_{digest['date']}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(digest, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Збережено: {filename}")


if __name__ == "__main__":
    print("🚀 Створення щоденного дайджесту...")
    
    digest = create_daily_digest()
    save_digest(digest)
    
    telegram_text = format_for_telegram(digest)
    print("\n" + "=" * 50)
    print("TELEGRAM PREVIEW:")
    print("=" * 50)
    print(telegram_text[:1000])
    print(f"\n📊 Загальна статистика:")
    print(f"  Тем: {len(digest['topics'])}")
    print(f"  Токенів: {digest['total_tokens']}")
