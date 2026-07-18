"""Шаг 1: профиль vacancies.csv (типы, пропуски, диапазоны, длины).

Запуск:
    python analytics/01_profile.py

Сохраняет вывод в analytics/profile.txt.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
CSV_PATH = _ROOT / "data" / "processed" / "vacancies.csv"
OUT_PATH = _HERE / "01_profile.txt"


def main() -> int:
    df = pd.read_csv(CSV_PATH)
    lines: list[str] = []

    lines.append("=" * 70)
    lines.append(f"ПРОФИЛЬ VACANCIES.CSV")
    lines.append(f"Файл: {CSV_PATH}")
    lines.append(f"Размер: {CSV_PATH.stat().st_size / 1024 / 1024:.1f} МБ")
    lines.append("=" * 70)
    lines.append("")

    # 1. Общая структура
    lines.append("## 1. Структура (shape, dtypes)")
    lines.append(f"Строк: {len(df):,}")
    lines.append(f"Колонок: {len(df.columns)}")
    lines.append(df.dtypes.to_string())
    lines.append("")

    # 2. Пропуски
    lines.append("## 2. Пропуски (null counts)")
    nulls = df.isna().sum()
    pct = (nulls / len(df) * 100).round(2)
    miss = pd.DataFrame({"nulls": nulls, "%": pct})
    miss = miss[miss["nulls"] > 0]
    if len(miss) > 0:
        lines.append(miss.to_string())
    else:
        lines.append("(нет пропусков в исходном CSV)")
    lines.append("")

    # 3. Уникальные значения для малых cardinality
    lines.append("## 3. Cardinality (количество уникальных значений)")
    for col in df.columns:
        uniq = df[col].nunique(dropna=True)
        lines.append(f"  {col:15s}: {uniq:>7,} unique")
    lines.append("")

    # 4. Дата: диапазон
    lines.append("## 4. Дата — диапазон")
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    n_bad_date = df["date"].isna().sum()
    lines.append(f"  Невалидных date: {n_bad_date}")
    if df["date"].notna().any():
        d_min = df["date"].min()
        d_max = df["date"].max()
        lines.append(f"  Min: {d_min}")
        lines.append(f"  Max: {d_max}")
        lines.append(f"  Span: {(d_max - d_min).days} дней (~{(d_max - d_min).days // 365} лет)")
    lines.append("")

    # 5. Длины текстов (для оценки объёма)
    lines.append("## 5. Длины текстов (chars)")
    if "text" in df.columns:
        text_len = df["text"].fillna("").str.len()
        lines.append(f"  text:    min={text_len.min()}, "
                    f"median={text_len.median():.0f}, "
                    f"mean={text_len.mean():.0f}, "
                    f"p95={text_len.quantile(0.95):.0f}, "
                    f"max={text_len.max()}")
    if "author" in df.columns:
        auth_len = df["author"].fillna("").str.len()
        lines.append(f"  author:  max={auth_len.max()}, "
                    f"unique={df['author'].nunique()}")
    if "tags" in df.columns:
        tags_len = df["tags"].fillna("").str.len()
        lines.append(f"  tags:    max={tags_len.max()}, "
                    f"median empty count={df['tags'].fillna('').eq('').sum()}")
    if "links" in df.columns:
        links_len = df["links"].fillna("").str.len()
        n_with_links = df["links"].fillna("").ne("").sum()
        n_no_links = df["links"].fillna("").eq("").sum()
        lines.append(f"  links:   with_links={n_with_links:,}, "
                    f"empty={n_no_links:,}")
    lines.append("")

    # 6. Топ-10 авторов
    lines.append("## 6. Топ-10 авторов (по числу вакансий)")
    top = df["author"].fillna("(unknown)").value_counts().head(10)
    for author, n in top.items():
        lines.append(f"  {n:5d}  {author}")
    lines.append("")

    # 7. Топ-20 тегов
    lines.append("## 7. Топ-20 тегов")
    tag_counter: dict[str, int] = {}
    for raw in df["tags"].fillna(""):
        for t in raw.split(";"):
            t = t.strip().lower()
            if t:
                tag_counter[t] = tag_counter.get(t, 0) + 1
    top_tags = sorted(tag_counter.items(), key=lambda x: -x[1])[:20]
    for tag, n in top_tags:
        lines.append(f"  {n:6d}  {tag}")
    lines.append("")

    # 8. Топ-15 доменов ссылок
    lines.append("## 8. Топ-15 доменов ссылок")
    from urllib.parse import urlparse
    dom_counter: dict[str, int] = {}
    for raw in df["links"].fillna(""):
        for url in raw.split(";"):
            url = url.strip()
            if not url:
                continue
            try:
                dom = urlparse(url).netloc.lower()
                if not dom:
                    continue
                dom_counter[dom] = dom_counter.get(dom, 0) + 1
            except Exception:
                pass
    top_doms = sorted(dom_counter.items(), key=lambda x: -x[1])[:15]
    for dom, n in top_doms:
        lines.append(f"  {n:6d}  {dom}")
    lines.append("")

    # 9. Уникальных ID и файлов
    lines.append("## 9. Служебные")
    lines.append(f"  unique message_id: {df['message_id'].nunique()}")
    lines.append(f"  unique source_file: {df['source_file'].nunique()}")
    lines.append(f"  total chars in text: {df['text'].fillna('').str.len().sum():,}")

    # Сохранить
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Saved profile → {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())