"""
Демонстрация интеграции OutputFilter с Ollama.
LLM генерирует ответ, а OutputFilter фильтрует конфиденциальные данные.
"""

import ollama
from output_filter import OutputFilter


def safe_chat(prompt: str, model: str = 'llama2:7b') -> str:
    """
    Отправляет запрос в LLM и фильтрует ответ через OutputFilter.
    
    :param prompt: запрос пользователя.
    :param model: имя модели Ollama (например, 'llama2:7b').
    :return: безопасный ответ (с заменёнными конфиденциальными данными).
    """
    filter_obj = OutputFilter()
    
    # 1. Отправляем запрос в LLM
    print(f"\n[Запрос к модели {model}]: {prompt}")
    response = ollama.chat(model=model, messages=[
        {'role': 'user', 'content': prompt}
    ])
    raw_answer = response['message']['content']
    
    print("\n=== Сырой ответ LLM ===")
    print(raw_answer)
    
    # 2. Сканируем ответ на конфиденциальные данные
    findings = filter_obj.scan(raw_answer)
    if findings:
        print("\n Обнаружены конфиденциальные данные:")
        for data_type, value in findings:
            print(f"  - {data_type}: {value}")
    else:
        print("\n Конфиденциальных данных не найдено.")
    
    # 3. Фильтруем ответ
    safe_answer = filter_obj.filter(raw_answer)
    
    print("\n=== Безопасный ответ ===")
    print(safe_answer)
    
    return safe_answer


if __name__ == '__main__':
    # Промпт, который может спровоцировать LLM на «утечку» данных
    test_prompts = [
        "Придумай пример письма с email и паролем для теста безопасности.",
        "Напиши пример конфига с API-ключом.",
        "Как дела?",
    ]
    
    for prompt in test_prompts:
        safe_chat(prompt)
        print("\n" + "=" * 60)