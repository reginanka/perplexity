#!/usr/bin/env python3
"""
Приклад 2: Telegram бот з Perplexity API

Вимоги:
    pip install aiogram openai python-dotenv

Налаштування (.env):
    PERPLEXITY_API_KEY=pplx-xxxxxxxxxx
    TELEGRAM_BOT_TOKEN=your_bot_token
"""

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher()

# Асинхронний клієнт для aiogram
perplexity = AsyncOpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)

# Зберігання контексту розмов
conversations: dict[int, list] = {}


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привіт! Я AI-асистент на базі Perplexity.\n"
        "Задавай будь-які питання — я шукаю відповіді в реальному часі!"
    )


@dp.message(Command("clear"))
async def clear_handler(message: types.Message):
    conversations.pop(message.from_user.id, None)
    await message.answer("🗑 Контекст розмови очищено")


@dp.message()
async def message_handler(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text
    
    # Ініціалізація контексту
    if user_id not in conversations:
        conversations[user_id] = [{
            "role": "system",
            "content": "Ти корисний AI-асистент. Відповідай коротко і по суті. Мова: українська."
        }]
    
    conversations[user_id].append({
        "role": "user",
        "content": user_text
    })
    
    # Показуємо typing індикатор
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        response = await perplexity.chat.completions.create(
            model="sonar",
            messages=conversations[user_id],
            return_citations=True
        )
        
        answer = response.choices[0].message.content
        citations = getattr(response, "citations", [])
        
        # Додаємо відповідь до контексту
        conversations[user_id].append({
            "role": "assistant",
            "content": answer
        })
        
        # Обмеження контексту (останні 10 повідомлень + system)
        if len(conversations[user_id]) > 21:
            conversations[user_id] = (
                conversations[user_id][:1] +  # system
                conversations[user_id][-20:]   # останні 20
            )
        
        # Формуємо відповідь
        reply = answer
        if citations:
            reply += "\n\n📚 Джерела:\n"
            for i, url in enumerate(citations[:3], 1):  # максимум 3 джерела
                reply += f"{i}. {url}\n"
        
        await message.reply(reply)
    
    except Exception as e:
        await message.reply(f"❌ Помилка: {str(e)}")


async def main():
    print("🤖 Бот запущено")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
