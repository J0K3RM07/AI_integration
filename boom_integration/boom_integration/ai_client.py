from typing import Protocol, Any, Coroutine


class AIClient(Protocol):
    def ask(self, question: str, context: list[str]) -> str: ...


class OpenAIClient:
    """Пример реализации AI-клиента (заглушка)."""

    def ask(self, question: str, context: list[str]) -> str:
        # Здесь должна быть логика обращения к реальному AI сервису
        return f"Ответ на: {question}"
