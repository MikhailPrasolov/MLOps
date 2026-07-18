"""CLI entry-point: парсит Telegram-экспорт вакансий в CSV.

Запуск:
    python notebooks/parse_run.py --in <in_dir> --out <out.csv> [--limit N] [--log <log.txt>]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Добавляем src/ в PYTHONPATH, чтобы работали относительные импорты
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
sys.path.insert(0, str(_ROOT))

from src.pipeline import run


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Парсер Telegram web export → vacancies.csv (только вакансии)",
    )
    parser.add_argument(
        "--in", dest="in_dir", required=True,
        help="Папка с messages*.html (Telegram web export)",
    )
    parser.add_argument(
        "--out", dest="out_csv", required=True,
        help="Путь к выходному CSV (например data/processed/vacancies.csv)",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Обработать только первые N файлов (для разработки/тестов)",
    )
    parser.add_argument(
        "--log", dest="log_path", default=None,
        help="Путь к файлу лога (WARNING+); stderr пишется всегда",
    )

    args = parser.parse_args()

    stats = run(
        in_dir=args.in_dir,
        out_csv=args.out_csv,
        limit=args.limit,
        log_path=args.log_path,
    )

    return 0 if stats.files_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())