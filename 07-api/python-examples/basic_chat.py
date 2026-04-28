#!/usr/bin/env python3
"""
Приклад 1: Базовий чат з Perplexity API

Вимоги:
    pip install openai python-dotenv

Налаштування:
    Створи .env файл з:
    PERPLEXITY_API_KEY=pplx-xxxxxxxxxx
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)


def simple_query(question: str, model: str = "sonar") -> str:
    """Простий одноразовий запит."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


def query_with_citations(question: str) -> dict:
    """Запит з поверненням джерел."""
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {"role": "user", "content": question}
        ],
        return_citations=True
    )
    
    return {
        "answer": response.choices[0].message.content,
        "citations": getattr(response, "citations", []),
        "tokens": response.usage.total_tokens
    }


def multi_turn_chat(messages: list) -> str:
    """Багатоходовий діалог зі збереженням контексту."""
    response = client.chat.completions.create(
        model="sonar",
        messages=messages
    )
    return response.choices[0].message.content


def streaming_response(question: str):
    """Стрімінг відповіді (друкує по мірі генерації)."""
    stream = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": question}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()  # новий рядок в кінці


if __name__ == "__main__":
    # Тест 1: Простий запит
    print("=" * 50)
    print("Тест 1: Простий запит")
    answer = simple_query("Що таке Perplexity AI?")
    print(answer[:300], "...")
    
    # Тест 2: З джерелами
    print("\n" + "=" * 50)
    print("Тест 2: Запит з джерелами")
    result = query_with_citations("Останні новини про AI в Україні")
    print(f"Відповідь: {result['answer'][:200]}...")
    print(f"Джерела: {len(result['citations'])} посилань")
    print(f"Токенів: {result['tokens']}")
    
    # Тест 3: Стрімінг
    print("\n" + "=" * 50)
    print("Тест 3: Стрімінг відповіді")
    streaming_response("Назви 3 цікаві факти про Україну")
