"""Фильтрация сообщений по тегам-маркерам вакансий."""
from __future__ import annotations

from src.parser import Message


# Главные маркеры вакансий в канале «Работа ищет аналитиков»
VACANCY_TAGS: set[str] = {
    "#vacancy",
    "#вакансия",
    "#vacancies",     # иногда используется
    "#вакансиям",     # редкая форма
    "#естьработа",    # исторический тег (правила чата)
}


def is_vacancy(msg: Message) -> bool:
    """True если у сообщения есть хотя бы один тег-маркер вакансии."""
    return bool(set(msg.tags) & VACANCY_TAGS)


def filter_vacancies(messages: list[Message]) -> list[Message]:
    """Оставляет только вакансии (immutable фильтрация)."""
    return [m for m in messages if is_vacancy(m)]


def vacancy_stats(messages: list[Message]) -> dict[str, int]:
    """Статистика по тегам вакансий: сколько сообщений с каждым тегом.

    Полезно для sanity-check: если #естьработа 0 — старые данные не зацепились.
    """
    stats: dict[str, int] = {tag: 0 for tag in VACANCY_TAGS}
    for m in messages:
        for tag in m.tags:
            if tag in stats:
                stats[tag] += 1
    return stats