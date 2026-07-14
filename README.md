# Исследование защиты от prompt injection: CaMeL + Inspect AI

## Описание проекта

Реализация и тестирование защиты **CaMeL** (от библиотеки `camel-prompt-injection`) от атак prompt injection на LLM-агентов, интегрированной в фреймворк **Inspect AI** с использованием бенчмарка **AgentDojo**.

## Что сделано

- **Интеграция CaMeL с Inspect AI** — создан `defences.py` с кастомным solver, который оборачивает пайплайн CaMeL как Inspect solver и конвертирует сообщения между форматами AgentDojo и Inspect AI.
- **Написание тестового скрипта** — `test.py` запускает оценку на бенчмарке AgentDojo (workspace, selected user/injection tasks) с моделью `google/gemini-3.1-flash-lite`, используя CaMeL defense.
- **Утилита конвертации** — `analyse_tools.py` реализует двустороннюю конвертацию сообщений (`agent_dojo_to_inspect_ai`, `inspect_ai_to_agent_dojo`) и поддержку моделей Google/OpenAI/Anthropic.

## Структура

```
test.py              — точка входа, запуск eval
defences.py          — CaMeL solver для Inspect AI
analyse_tools.py     — конвертер сообщений между AgentDojo и Inspect AI
camel-prompt-injection/ — библиотека CaMeL (внешняя зависимость)
```

## Запуск

```bash
source .venv/bin/activate
python test.py
```

Модель задаётся переменной `model` в `test.py`. Результаты логируются в `./logs`.
