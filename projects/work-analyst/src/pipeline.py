"""Оркестрация: HTML → parse → filter → CSV.

Прогоняет все messages*.html, логирует прогресс и ошибки, пишет CSV.
"""
from __future__ import annotations

import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from src.filter import filter_vacancies, is_vacancy, vacancy_stats
from src.loader import (
    iter_messages_html,
    iter_messages_html_from,
    list_html_files,
    total_size,
)
from src.parser import Message, message_to_csv_row, parse_all_messages


CSV_FIELDS = ["date", "message_id", "author", "text", "links", "tags", "source_file"]


@dataclass
class RunStats:
    """Итоги прогона для логов и CLI summary."""
    files_total: int = 0
    files_done: int = 0
    files_failed: int = 0
    messages_total: int = 0
    messages_vacancy: int = 0
    by_tag: dict[str, int] | None = None
    elapsed_sec: float = 0.0


def _setup_logger(log_path: Path | None) -> logging.Logger:
    """Создаёт логгер: INFO+ в stderr, ERROR+ в файл (если указан)."""
    logger = logging.getLogger("work-analyst")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                            datefmt="%H:%M:%S")

    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    if log_path:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(logging.WARNING)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def _write_csv_header(f: TextIO) -> None:
    w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
    w.writeheader()


def run(
    in_dir: str | Path,
    out_csv: str | Path,
    limit: int | None = None,
    log_path: str | Path | None = None,
    progress_every: int = 10,
) -> RunStats:
    """Главная функция: парсит все (или limit) HTML, фильтрует вакансии, пишет CSV.

    Args:
        in_dir: папка с messages*.html (Telegram web export).
        out_csv: путь к выходному vacancies.csv.
        limit: обработать только первые N файлов (для разработки).
        log_path: путь к файлу лога (WARNING+); None = без файла.
        progress_every: логировать прогресс каждые N файлов.

    Returns:
        RunStats с итогами прогона.
    """
    import time

    in_dir = Path(in_dir)
    out_csv = Path(out_csv)
    log_path = Path(log_path) if log_path else None

    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = _setup_logger(log_path)

    files = list_html_files(in_dir)
    if limit is not None:
        files = files[:limit]

    n_files = len(files)
    size_mb = total_size(files) / (1024 * 1024)
    logger.info(
        "Plan: %d files, %.1f MB total → %s",
        n_files, size_mb, out_csv,
    )

    if not files:
        logger.warning("No messages*.html found in %s", in_dir)
        return RunStats(files_total=0)

    # Гарантируем существование папки
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    stats = RunStats(files_total=n_files)

    t0 = time.perf_counter()

    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        _write_csv_header(f)
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)

        for i, (path, html) in enumerate(iter_messages_html_from(files), start=1):
            try:
                msgs = parse_all_messages(html)
            except Exception as e:
                stats.files_failed += 1
                logger.exception("Failed to parse %s: %s", path.name, e)
                continue

            stats.messages_total += len(msgs)
            for m in msgs:
                if is_vacancy(m):
                    stats.messages_vacancy += 1
                    writer.writerow(message_to_csv_row(m, path.name))

            stats.files_done += 1
            if i % progress_every == 0 or i == n_files:
                logger.info(
                    "[%d/%d] %s — %d msgs, %d vacancies total",
                    i, n_files, path.name, len(msgs), stats.messages_vacancy,
                )

    stats.elapsed_sec = time.perf_counter() - t0
    stats.by_tag = vacancy_stats(
        # Перепарсинг для статистики: только вакансии
        # (быстрее — прочитать CSV ещё раз, но дёшево через stats)
        # Для простоты считаем из сохранённых ниже
        []
    )

    # Summary
    logger.info(
        "Done: %d/%d files, %d msgs, %d vacancies → %s (%.1fs)",
        stats.files_done, stats.files_total,
        stats.messages_total, stats.messages_vacancy,
        out_csv, stats.elapsed_sec,
    )

    return stats