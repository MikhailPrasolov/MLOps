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


def _natural_sort_key(name: str) -> tuple[int, ...]:
    """Числовая сортировка: messages2 < messages10.

    'messages10.html' → (1, 0), 'messages2.html' → (1, 2),
    но в числовой сортировке (2) < (10).
    """
    parts = re.split(r"(\d+)", name)
    return tuple(int(p) if p.isdigit() else p for p in parts)


def read_messages_html(file_path: str | Path) -> str:
    """Читает файл как UTF-8. Бросает UnicodeDecodeError, если кодировка не UTF-8."""
    return Path(file_path).read_text(encoding="utf-8")


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