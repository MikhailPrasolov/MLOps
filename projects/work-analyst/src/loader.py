"""Чтение HTML-файлов Telegram-экспорта.

Telegram web export делит историю на страницы (messages.html, messages2.html, ...).
Внутри каждой страницы — десятки-сотни `<div class="message ...">` блоков.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable, Iterator


_MESSAGES_FILE_RE = re.compile(r"^messages\d*\.html$", re.IGNORECASE)


def list_html_files(in_dir: str | Path) -> list[Path]:
    """Возвращает отсортированный список messages*.html в in_dir.

    Сортировка по имени (числовой лексикографически) даёт правильный порядок:
    messages.html (1), messages2.html, ..., messages10.html, messages100.html.

    >>> from pathlib import Path
    >>> import tempfile, os
    >>> with tempfile.TemporaryDirectory() as d:
    ...     [Path(d, n).write_text("x") for n in ["messages.html", "messages2.html", "messages10.html"]]
    ...     [p.name for p in list_html_files(d)]
    ['messages.html', 'messages2.html', 'messages10.html']
    """
    p = Path(in_dir)
    if not p.is_dir():
        raise FileNotFoundError(f"Input dir not found: {p}")
    files = sorted(
        (f for f in p.iterdir() if f.is_file() and _MESSAGES_FILE_RE.match(f.name)),
        key=lambda f: _natural_sort_key(f.name),
    )
    return files


def _natural_sort_key(name: str) -> tuple:
    """Числовая сортировка: messages2 < messages10 < messages100.

    Возвращает кортеж вида (символ, число, символ, число, ...). Каждый
    символ строки-блока становится отдельным элементом, чтобы кортежи
    были сравнимы поэлементно с самого начала. 'messages.html' →
    ('m','e','s','s','a','g','e','s','.','h','t','m','l'),
    'messages2.html' → ('m','e','s','s','a','g','e','s',2,'.','h','t','m','l').
    Сравнение ('m',..,'s','.','h',...) vs ('m',..,'s',2,'.','h',...): на позиции
    индекса символа после цифр — строковый '.' меньше числового 2 нельзя
    сравнить напрямую, но на индексе самой цифры строковый '.' >
    числовой 2 — нет, в ('m',..,'s','.','h',...) '.' стоит на 8-й позиции,
    а в ('m',..,'s',2,'.','h',...) 2 стоит на 8-й. Python сравнивает:
    строка vs int → TypeError. Поэтому используем другой подход.

    Корректный подход: каждый блок становится (0, "str") или (1, int),
    где 0 < 1. Так Python всегда знает, как сравнить, а порядок внутри
    строкового блока — лексикографический (т.к. (0, 'm') < (0, 's')).

    >>> sorted(['messages.html', 'messages2.html', 'messages10.html'],
    ...        key=_natural_sort_key)
    ['messages.html', 'messages2.html', 'messages10.html']
    """
    parts = re.split(r"(\d+)", name)
    key = []
    for p in parts:
        if not p:
            continue
        if p.isdigit():
            key.append((1, int(p)))
        else:
            # Разбиваем строку на символы, чтобы каждая «буква» была (0, char)
            for ch in p:
                key.append((0, ch))
    return tuple(key)


def read_messages_html(file_path: str | Path) -> str:
    """Читает файл как UTF-8. Бросает UnicodeDecodeError, если кодировка не UTF-8."""
    return Path(file_path).read_text(encoding="utf-8")


def iter_messages_html_from(
    files: list[Path],
) -> Iterator[tuple[Path, str]]:
    """Yields (path, html_text) для уже отфильтрованного списка файлов.

    Это split-вариант iter_messages_html: отдельно получаем список
    (list_html_files), отдельно читаем (read_messages_html). Полезно
    когда нужно логировать размер / количество файлов до чтения.
    """
    for fp in files:
        yield fp, read_messages_html(fp)


def iter_messages_html(
    in_dir: str | Path,
    limit: int | None = None,
) -> Iterator[tuple[Path, str]]:
    """Yields (path, html_text) для первых N (если limit) или всех messages*.html.

    >>> import tempfile, os
    >>> from pathlib import Path
    >>> with tempfile.TemporaryDirectory() as d:
    ...     for n in ["messages.html", "messages2.html"]:
    ...         Path(d, n).write_text("<html>" + n + "</html>", encoding="utf-8")
    ...     paths = [p.name for p, _ in iter_messages_html(d)]
    ...     paths
    ['messages.html', 'messages2.html']
    """
    files = list_html_files(in_dir)
    if limit is not None:
        files = files[:limit]
    for fp in files:
        try:
            yield fp, read_messages_html(fp)
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                e.encoding,
                e.object,
                e.start,
                e.end,
                f"{fp}: {e.reason}",
            ) from e


def total_size(files: Iterable[Path]) -> int:
    """Суммарный размер файлов в байтах (для прогресс-бара)."""
    return sum(f.stat().st_size for f in files)