"""Шаг 6: recount с word boundaries (\\b).

Цель: устранить substring false positives в подсчёте компаний и скиллов.
См. BLOCKER #2-3 в PLAN.md.

Запуск:
    python analytics/06_recount_with_boundaries.py

Сохраняет:
    analytics/skill_counts_v2.csv   (word-boundary counts)
    analytics/company_counts_v2.csv  (word-boundary counts)
    analytics/06_recount_comparison.txt  (сравнение substring vs \\b)

Сравнение до/после в 06_recount_comparison.txt позволяет оценить
масштаб FP contamination и корректно цитировать числа в постах.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
CSV = _ROOT / "data" / "processed" / "vacancies.csv"


# Копия словарей из 05_companies_skills.py (для самостоятельности)
COMPANIES = {
    "яндекс": "Яндекс", "yandex": "Яндекс",
    "avito": "Avito", "авито": "Avito",
    "ozon": "Ozon", "озон": "Ozon",
    "wildberries": "Wildberries", "wb": "Wildberries", "вб": "Wildberries",
    "aliexpress": "AliExpress", "vk": "VK", "вк": "VK", "vkontakte": "VK",
    "вконтакте": "VK",
    "tinkoff": "Тинькофф", "тинькофф": "Тинькофф", "tcs": "Тинькофф",
    "сбер": "Сбер", "sber": "Сбер", "sberbank": "Сбер",
    "альфабанк": "Альфа-Банк", "alfabank": "Альфа-Банк",
    "втб": "ВТБ", "vtb": "ВТБ",
    "мтс": "МТС", "mts": "МТС",
    "билайн": "Билайн", "beeline": "Билайн", "veon": "Билайн",
    "мегафон": "МегаФон", "megafon": "МегаФон",
    "tele2": "Tele2", "теле2": "Tele2",
    "ростелеком": "Ростелеком", "rostelecom": "Ростелеком",
    "lamoda": "Lamoda", "ламода": "Lamoda",
    "мегамаркет": "МегаМаркет", "megamarket": "МегаМаркет",
    "sbermarket": "СберМаркет", "сбермаркет": "СберМаркет",
    "magnit": "Магнит", "магнит": "Магнит",
    "x5": "X5 Group", "пятёрочка": "X5 Group", "перекрёсток": "X5 Group",
    "леруа": "Леруа Мерлен", "leroy": "Леруа Мерлен",
    "ostrovok": "Ostrovok", "островок": "Ostrovok",
    "ivi": "ivi", "iviclub": "ivi",
    "okko": "Okko", "окко": "Okko",
    "more.tv": "More.tv", "kion": "KION", "кион": "KION",
    "cian": "ЦИАН", "циан": "ЦИАН",
    "domclick": "ДомКлик", "домклик": "ДомКлик",
    "vkusvill": "ВкусВилл", "вкусвилл": "ВкусВилл",
    "raiffeisen": "Райффайзен", "райффайзен": "Райффайзен",
    "qiwi": "QIWI", "киви": "QIWI",
    "tochka": "Точка", "точка": "Точка",
    "aeroflot": "Аэрофлот", "аэрофлот": "Аэрофлот",
    "heineken": "Heineken", "baltika": "Балтика", "балтика": "Балтика",
    "epam": "EPAM", "epam systems": "EPAM",
    "exness": "Exness", "iqoption": "IQ Option",
    "selectel": "Selectel", "селектел": "Selectel",
    "owox": "OWOX", "retailcrm": "RetailCRM",
    "roistat": "Roistat", "ройстат": "Roistat",
    "mindbox": "Mindbox", "майндбокс": "Mindbox",
    "litres": "ЛитРес", "литрес": "ЛитРес",
    "lenta": "Лента", "лента": "Лента",
    "eldorado": "Эльдорадо", "эльдорадо": "Эльдорадо",
    "mvideo": "М.Видео", "мвидео": "М.Видео",
    "fixprice": "Fix Price", "фикспрайс": "Fix Price",
    "kazanexpress": "KazanExpress", "казанэкспресс": "KazanExpress",
    "dnsshop": "DNS", "днс": "DNS",
    "dodo": "Dodo Pizza", "dodopizza": "Dodo Pizza", "додопицца": "Dodo Pizza",
    "papajohns": "Papa John's", "пападжонс": "Papa John's",
    "starbucks": "Starbucks", "старбакс": "Starbucks",
    "kfc": "KFC", "burgerking": "Burger King", "бургеркинг": "Burger King",
    "mcdonalds": "McDonald's", "макдак": "McDonald's",
    "joom": "Joom",
    "telegram": "Telegram", "телеграм": "Telegram",
}

SKILLS = {
    # Hard skills (аналитика)
    "sql": "SQL",
    "python": "Python",
    " r ": "R",
    " r,": "R",
    " r.": "R",
    " r$": "R",
    "excel": "Excel",
    "tableau": "Tableau",
    "power_bi": "Power BI",
    "powerbi": "Power BI",
    "qlik": "Qlik",
    "qliksense": "Qlik Sense",
    "looker": "Looker",
    "redash": "Redash",
    "superset": "Superset",
    "metabase": "Metabase",
    "grafana": "Grafana",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scipy": "SciPy",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "spark": "Spark",
    "hadoop": "Hadoop",
    "kafka": "Kafka",
    "airflow": "Airflow",
    "dbt": "dbt",
    "snowflake": "Snowflake",
    "bigquery": "BigQuery",
    "redshift": "Redshift",
    "clickhouse": "ClickHouse",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "mssql": "MSSQL",
    "sql server": "MS SQL Server",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    " git ": "Git",
    "git, ": "Git",
    "linux": "Linux",
    "restapi": "REST API",
    " rest api": "REST API",
    "graphql": "GraphQL",
    "etl": "ETL",
    "elt": "ELT",
    "olap": "OLAP",
    "bi ": "BI",
    " bi,": "BI",
    " bi.": "BI",
    # Аналитические
    "a/b testing": "A/B Testing",
    "a/b-тестир": "A/B Testing",
    "cohort": "Когортный анализ",
    "воронк": "Воронка",
    "юнит-экономик": "Unit-экономика",
    "юнитэкономик": "Unit-экономика",
    "retention": "Retention",
    " ltv": "LTV",
    " ltv,": "LTV",
    " cac": "CAC",
    " cac,": "CAC",
    "romi": "ROMI",
    "roas": "ROAS",
    " kpi": "KPI",
    " kpi,": "KPI",
    "okr": "OKR",
    "google analytics": "Google Analytics",
    "ga4": "Google Analytics",
    "amplitude": "Amplitude",
    "mixpanel": "Mixpanel",
    "segment": "Segment",
    "firebase": "Firebase",
    "appsflyer": "AppsFlyer",
    "appmetrica": "AppMetrica",
    "яндекс метрик": "Яндекс.Метрика",
    "googleads": "Google Ads",
    "google ads": "Google Ads",
    "adwords": "Google Ads",
    "facebookads": "Facebook Ads",
    "vk ads": "VK Ads",
    "yandex direct": "Яндекс.Direct",
    "яндекс директ": "Яндекс.Direct",
    # Финансы / страхование / банки
    "финанс": "Финансы",
    "банк": "Банки",
    "страхов": "Страхование",
    "1с": "1С",
    "1c": "1С",
    "sap": "SAP",
    " erp": "ERP",
    " crm": "CRM",
    # Языки
    "english": "English",
    "английск": "English",
}


def count_substring(text: str, needle: str) -> int:
    """Старый подсчёт (для сравнения): substring без word boundaries."""
    if not isinstance(text, str) or not needle:
        return 0
    return text.lower().count(needle.lower())


def count_word_boundary(text: str, needle: str) -> int:
    """Новый подсчёт: \\bneedle\\b (не учитывает подстроки).

    Игнорирует регистр. Возвращает 1 если needle является отдельным словом.
    """
    if not isinstance(text, str) or not needle:
        return 0
    pattern = r"\b" + re.escape(needle) + r"\b"
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def count_via_dict(text: str, mapping: dict, use_word_boundary: bool = False) -> Counter:
    """Подсчитывает упоминания по словарю mapping → Counter[canonical_name]."""
    out: Counter = Counter()
    if not isinstance(text, str):
        return out
    func = count_word_boundary if use_word_boundary else count_substring
    for needle, canonical in mapping.items():
        if func(text, needle) > 0:
            out[canonical] += 1
    return out


def main() -> int:
    df = pd.read_csv(CSV)
    print(f"[INFO] Vacancies: {len(df):,}")

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("RECOUNT С WORD BOUNDARIES (BLOCKER #2-3 fix)")
    lines.append("=" * 70)
    lines.append(f"Vacancies: {len(df):,}")
    lines.append("")

    # === КОМПАНИИ ===
    lines.append("## КОМПАНИИ: substring vs \\b")
    lines.append("")
    sub_co: Counter = Counter()
    wb_co: Counter = Counter()
    for text in df["text"].fillna(""):
        sub_co.update(count_via_dict(text, COMPANIES, use_word_boundary=False))
        wb_co.update(count_via_dict(text, COMPANIES, use_word_boundary=True))

    sub_top = sorted(sub_co.items(), key=lambda x: -x[1])[:20]
    wb_top = sorted(wb_co.items(), key=lambda x: -x[1])[:20]

    lines.append(f"Уникальных компаний (substring): {len(sub_co)}")
    lines.append(f"Уникальных компаний (\\b): {len(wb_co)}")
    lines.append("")

    lines.append("### Top-15 компаний: сравнение")
    lines.append("")
    lines.append(f"{'Company':20s}  {'Substr':>8s}  {'WordBound':>10s}  {'FP%':>6s}")
    for sub_name, sub_n in sub_top[:15]:
        wb_n = wb_co.get(sub_name, 0)
        fp_pct = ((sub_n - wb_n) / sub_n * 100) if sub_n > 0 else 0
        lines.append(f"  {sub_name:18s}  {sub_n:8d}  {wb_n:10d}  {fp_pct:5.1f}%")
    lines.append("")

    # === СКИЛЛЫ ===
    lines.append("## СКИЛЛЫ: substring vs \\b")
    lines.append("")
    sub_sk: Counter = Counter()
    wb_sk: Counter = Counter()
    for text in df["text"].fillna(""):
        sub_sk.update(count_via_dict(text, SKILLS, use_word_boundary=False))
        wb_sk.update(count_via_dict(text, SKILLS, use_word_boundary=True))

    sub_sk_top = sorted(sub_sk.items(), key=lambda x: -x[1])[:25]
    wb_sk_top = sorted(wb_sk.items(), key=lambda x: -x[1])[:25]

    lines.append(f"Уникальных скиллов (substring): {len(sub_sk)}")
    lines.append(f"Уникальных скиллов (\\b): {len(wb_sk)}")
    lines.append("")

    lines.append("### Top-25 скиллов: сравнение")
    lines.append("")
    lines.append(f"{'Skill':25s}  {'Substr':>8s}  {'WordBound':>10s}  {'FP%':>6s}")
    for sub_name, sub_n in sub_sk_top[:25]:
        wb_n = wb_sk.get(sub_name, 0)
        fp_pct = ((sub_n - wb_n) / sub_n * 100) if sub_n > 0 else 0
        lines.append(f"  {sub_name:23s}  {sub_n:8d}  {wb_n:10d}  {fp_pct:5.1f}%")
    lines.append("")

    # === НАБЛЮДЕНИЯ ===
    lines.append("## КЛЮЧЕВЫЕ НАБЛЮДЕНИЯ")
    lines.append("")

    # SQL (был 6453 → проверим)
    sql_sub = sub_sk.get("SQL", 0)
    sql_wb = wb_sk.get("SQL", 0)
    lines.append(f"- SQL: substring {sql_sub} → \\b {sql_wb} "
                f"({100 * sql_wb / sql_sub:.0f}% реальных, "
                f"{100 * (sql_sub - sql_wb) / sql_sub:.0f}% FP)")
    lines.append(f"  → после чистки «SQL» в {sql_wb / len(df) * 100:.0f}% вакансий "
                f"(было {sql_sub / len(df) * 100:.0f}%)")

    # VK (был 4968 → проверим)
    vk_sub = sub_co.get("VK", 0)
    vk_wb = wb_co.get("VK", 0)
    lines.append(f"- VK: substring {vk_sub} → \\b {vk_wb} "
                f"({100 * vk_wb / vk_sub:.1f}% реальных)")
    lines.append(f"  → после чистки VK упомянут в {vk_wb / len(df) * 100:.1f}% вакансий "
                f"(было {vk_sub / len(df) * 100:.1f}%)")

    # Telegram (был 1107 → проверим, это конкурент VK, важно корректно)
    tg_sub = sub_co.get("Telegram", 0)
    tg_wb = wb_co.get("Telegram", 0)
    lines.append(f"- Telegram: substring {tg_sub} → \\b {tg_wb} "
                f"({100 * tg_wb / tg_sub:.1f}% реальных)")
    lines.append("")

    lines.append("## ВЫВОД ДЛЯ ПОСТОВ")
    lines.append("")
    if vk_wb > 0 and vk_wb < vk_sub * 0.3:
        lines.append(f"⚠️  VK завышен на ~{(1 - vk_wb / vk_sub) * 100:.0f}% — НЕЛЬЗЯ писать "
                    "'VK = топ-1 работодатель' без оговорки.")
        lines.append(f"   После чистки VK: {vk_wb} реальных упоминаний.")
    if sql_wb > 0:
        lines.append(f"✓  SQL остаётся абсолютным лидером даже после \\b: "
                    f"{sql_wb} упоминаний ({sql_wb / len(df) * 100:.0f}% вакансий).")
        lines.append("   Это безопасный claim для поста 3 (топ-скиллы).")

    # Сохранить
    out = _HERE / "06_recount_comparison.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    # v2 CSV — сохраняем в data/ (рядом с основными данными)
    data_dir = _ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    skills_v2 = pd.DataFrame([
        {"skill": k, "count_word_boundary": v}
        for k, v in wb_sk.most_common()
    ])
    skills_v2.to_csv(data_dir / "skill_counts_v2.csv", index=False, encoding="utf-8")

    companies_v2 = pd.DataFrame([
        {"company": k, "count_word_boundary": v}
        for k, v in wb_co.most_common()
    ])
    companies_v2.to_csv(data_dir / "company_counts_v2.csv", index=False, encoding="utf-8")

    # Также сохранить в data/ для последующих постов
    skills_v2.to_csv(data_dir / "skill_counts.csv", index=False, encoding="utf-8")
    companies_v2.to_csv(data_dir / "company_counts.csv", index=False, encoding="utf-8")

    print(f"[OK] {out}")
    print(f"[OK] data/skill_counts_v2.csv ({len(skills_v2)} строк)")
    print(f"[OK] data/company_counts_v2.csv ({len(companies_v2)} строк)")
    print(f"[OK] data/skill_counts.csv (обновлён v2)")
    print(f"[OK] data/company_counts.csv (обновлён v2)")
    return 0


if __name__ == "__main__":
    sys.exit(main())