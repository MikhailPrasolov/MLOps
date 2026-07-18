"""Шаг 5: топ-компаний (по тексту/ссылкам) + топ-скиллов (по тегам).

Запуск:
    python analytics/05_companies_skills.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
CSV = _ROOT / "data" / "processed" / "vacancies.csv"
FIG_DIR = _HERE / "figures"
FIG_DIR.mkdir(exist_ok=True)


# Словарь известных компаний → каноническое имя
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
    "wildberries": "Wildberries",
    "мегамаркет": "МегаМаркет", "megamarket": "МегаМаркет",
    "sbermarket": "СберМаркет", "сбермаркет": "СберМаркет",
    "sbercloud": "SberCloud", "sberlogistics": "СберЛогистика",
    "magnit": "Магнит", "магнит": "Магнит",
    "x5": "X5 Group", "пятёрочка": "X5 Group", "перекрёсток": "X5 Group",
    "леруа": "Леруа Мерлен", "leroy": "Леруа Мерлен",
    "ostrovok": "Ostrovok", "островок": "Ostrovok",
    "ivideon": "Ivideon", "ivi": "ivi", "iviclub": "ivi",
    "okko": "Okko", "окко": "Okko",
    "more": "More.tv", "more.tv": "More.tv",
    "kion": "KION", "кион": "KION",
    "cinema": "Cinema Park", "cinemapark": "Cinema Park",
    "carprice": "CarPrice", "карпрайс": "CarPrice",
    "drom": "Drom", "дром": "Drom",
    "auto": "Auto.ru", "autoru": "Auto.ru",
    "cian": "ЦИАН", "циан": "ЦИАН",
    "domclick": "ДомКлик", "домклик": "ДомКлик",
    "skolkovo": "Сколково",
    "joom": "Joom",
    "pikabu": "Pikabu", "пикабу": "Pikabu",
    "vkusvill": "ВкусВилл", "вкусвилл": "ВкусВилл",
    "perekrestok": "Перекрёсток",
    "gazprombank": "Газпромбанк", "газпромбанк": "Газпромбанк",
    "ingosstrakh": "Ингосстрах", "ингосстрах": "Ингосстрах",
    "rgs": "Росгосстрах", "росгосстрах": "Росгосстрах",
    "vtb24": "ВТБ", "raiffeisen": "Райффайзен", "райффайзен": "Райффайзен",
    "tinkoffbank": "Тинькофф",
    "psbank": "Промсвязьбанк", "промсвязьбанк": "Промсвязьбанк",
    "uralsib": "Уралсиб", "уралсиб": "Уралсиб",
    "raiffeisenbank": "Райффайзен",
    "qiwi": "QIWI", "киви": "QIWI",
    "mtsbank": "МТС Банк",
    "modulbank": "Модульбанк", "модульбанк": "Модульбанк",
    "tochka": "Точка", "точка": "Точка",
    "rocketbank": "Рокетбанк", "рокетбанк": "Рокетбанк",
    "tinkoff insurance": "Тинькофф Страхование",
    "rostelecom": "Ростелеком",
    "aeroflot": "Аэрофлот", "аэрофлот": "Аэрофлот",
    "mtsbank": "МТС",
    "х5": "X5 Group",
    "heineken": "Heineken", "baltika": "Балтика", "балтика": "Балтика",
    "epam": "EPAM", "epam systems": "EPAM",
    "exness": "Exness", "iqoption": "IQ Option",
    "selectel": "Selectel", "селектел": "Selectel",
    "owox": "OWOX", "owox-bi": "OWOX",
    "retailcrm": "RetailCRM",
    "roistat": "Roistat", "ройстат": "Roistat",
    "mindbox": "Mindbox", "майндбокс": "Mindbox",
    "gmbox": "Gmbox",
    "litres": "ЛитРес", "литрес": "ЛитРес",
    "lenta": "Лента", "лента": "Лента",
    "magnit": "Магнит",
    "pyaterochka": "Пятёрочка", "пятерочка": "Пятёрочка",
    "eldorado": "Эльдорадо", "эльдорадо": "Эльдорадо",
    "mts": "МТС",
    "megafon": "МегаФон",
    "tele2": "Tele2",
    "rostelecom": "Ростелеком",
    "старбакс": "Starbucks", "starbucks": "Starbucks",
    "kfc": "KFC", "burger": "Burger King",
    "burgerking": "Burger King", "макдак": "McDonald's", "mcdonalds": "McDonald's",
    "lamoda": "Lamoda", "wildberries": "Wildberries",
    "dodo": "Dodo Pizza", "dodopizza": "Dodo Pizza", "додопицца": "Dodo Pizza",
    "papajohns": "Papa John's", "пападжонс": "Papa John's",
    "fixprice": "Fix Price", "фикс прайс": "Fix Price", "фикспрайс": "Fix Price",
    "kazanexpress": "KazanExpress", "казанэкспресс": "KazanExpress",
    "leroymerlin": "Леруа Мерлен",
    "dnsshop": "DNS", "днс": "DNS",
    "eldorado": "Эльдорадо",
    "mvideo": "М.Видео", "мвидео": "М.Видео",
    "eldorado": "Эльдорадо",
    "megafon": "МегаФон",
    "mtsbank": "МТС",
    "joom": "Joom",
    "aliexpress": "AliExpress",
    "telegram": "Telegram", "телеграм": "Telegram",
    "rostelecom": "Ростелеком",
    "wildberries": "Wildberries",
}


SKILLS = {
    # Hard skills (аналитика)
    "sql": "SQL",
    "python": "Python",
    "r ": "R",
    "excel": "Excel",
    "tableau": "Tableau",
    "power_bi": "Power BI",
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
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "mssql": "MSSQL",
    "clickhouse": "ClickHouse",
    "hive": "Hive",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "git": "Git",
    "linux": "Linux",
    "restapi": "REST API",
    "rest": "REST API",
    "graphql": "GraphQL",
    "grpc": "gRPC",
    "kafka": "Kafka",
    "rabbit": "RabbitMQ",
    "etl": "ETL",
    "elt": "ELT",
    "olap": "OLAP",
    "oltp": "OLTP",
    "datavault": "Data Vault",
    "dwh": "DWH",
    "bi ": "BI",
    # Аналитические
    "ab testing": "A/B Testing",
    "abтестир": "A/B Testing",
    "a/b": "A/B Testing",
    "cohort": "Когортный анализ",
    "воронк": "Воронка",
    "юнит-экономик": "Unit-экономика",
    "юнитэкономик": "Unit-экономика",
    "retention": "Retention",
    "ltv": "LTV",
    "cac": "CAC",
    "romi": "ROMI",
    "roas": "ROAS",
    "kpi": "KPI",
    "okr": "OKR",
    "ga": "Google Analytics",
    "google analytics": "Google Analytics",
    "gtm": "GTM",
    "amplitude": "Amplitude",
    "mixpanel": "Mixpanel",
    "segment": "Segment",
    "firebase": "Firebase",
    "appsflyer": "AppsFlyer",
    "appmetrica": "AppMetrica",
    "яндексметрик": "Яндекс.Метрика",
    "googleads": "Google Ads",
    "adwords": "Google Ads",
    "facebookads": "Facebook Ads",
    "facebook ads": "Facebook Ads",
    "vk ads": "VK Ads",
    "mytarget": "myTarget",
    "yandex direct": "Яндекс.Direct",
    "яндексдирект": "Яндекс.Direct",
    # Финансы / страхование / банки
    "финанс": "Финансы",
    "банк": "Банки",
    "страхов": "Страхование",
    "sql server": "MS SQL Server",
    "1с": "1С",
    "1c": "1С",
    "sap": "SAP",
    "erp": "ERP",
    "crm": "CRM",
    # Языки
    "english": "English",
    "английск": "English",
    "немецк": "Немецкий",
}


def _extract_companies(text: str) -> Counter:
    """v2: поиск имён компаний с word boundaries (см. 06_recount)."""
    if not isinstance(text, str):
        return Counter()
    out = Counter()
    for needle, canonical in COMPANIES.items():
        pattern = r"\b" + re.escape(needle) + r"\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            out[canonical] += 1
    return out


def _extract_skills(text: str) -> Counter:
    """v2: поиск скиллов с word boundaries (см. 06_recount)."""
    if not isinstance(text, str):
        return Counter()
    out = Counter()
    for needle, canonical in SKILLS.items():
        pattern = r"\b" + re.escape(needle) + r"\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            out[canonical] += 1
    return out


def main() -> int:
    df = pd.read_csv(CSV)
    print(f"[INFO] Scanning {len(df):,} vacancies for companies + skills...")

    # 1. Компании
    company_counter: Counter = Counter()
    for text in df["text"].fillna(""):
        company_counter.update(_extract_companies(text))

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("ТОП-30 КОМПАНИЙ (v2 — word boundaries)")
    lines.append("=" * 70)
    # Считаем через lambda-функцию с _extract_companies (как в основном цикле)
    has_company_count = df["text"].fillna("").apply(lambda t: bool(_extract_companies(t))).sum()
    lines.append(f"Вакансий с хотя бы одной упомянутой компанией (\\b): {has_company_count:,} "
                 f"({100 * has_company_count / len(df):.1f}%)")
    lines.append("Сравнение v1 (substring) vs v2 (\\b): см. 06_recount_comparison.txt")
    lines.append("")
    for company, n in company_counter.most_common(30):
        bar = "#" * min(n // 3, 60)
        lines.append(f"  {n:4d}  {company:30s}  {bar}")
    lines.append("")

    # 2. Скиллы
    skill_counter: Counter = Counter()
    for text in df["text"].fillna(""):
        skill_counter.update(_extract_skills(text))

    lines.append("## ТОП-40 СКИЛЛОВ (v2 — word boundaries)")
    lines.append("")
    for skill, n in skill_counter.most_common(40):
        bar = "#" * min(n // 10, 60)
        lines.append(f"  {n:5d}  {skill:30s}  {bar}")
    lines.append("")

    # Сохранить
    out = _HERE / "05_companies_skills.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    # Сохранить CSV
    skills_df = pd.DataFrame([
        {"skill": k, "count": v}
        for k, v in skill_counter.most_common()
    ])
    # Сохранить CSV в data/ (родительский для data/processed/)
    data_dir = _ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    skills_df.to_csv(data_dir / "skill_counts.csv", index=False, encoding="utf-8")

    companies_df = pd.DataFrame([
        {"company": k, "count": v}
        for k, v in company_counter.most_common()
    ])
    companies_df.to_csv(data_dir / "company_counts.csv", index=False, encoding="utf-8")

    # ===== ГРАФИКИ =====

    # Топ-20 компаний
    top_c = company_counter.most_common(20)
    if top_c:
        fig, ax = plt.subplots(figsize=(10, 7))
        names = [c[0] for c in top_c]
        counts = [c[1] for c in top_c]
        ax.barh(range(len(names))[::-1], counts, color="steelblue", edgecolor="black")
        ax.set_yticks(range(len(names))[::-1])
        ax.set_yticklabels(names)
        ax.set_xlabel("Число упоминаний в вакансиях")
        ax.set_title("Топ-20 компаний по упоминаниям (2016–2026)")
        ax.grid(axis="x", alpha=0.3)
        for i, n in enumerate(counts):
            ax.text(n + max(counts) * 0.01, len(names) - 1 - i, str(n),
                    va="center", fontsize=9)
        fig.tight_layout()
        fig.savefig(FIG_DIR / "top_companies.png", dpi=100)
        plt.close(fig)

    # Топ-25 скиллов
    top_s = skill_counter.most_common(25)
    if top_s:
        fig, ax = plt.subplots(figsize=(10, 8))
        names = [s[0] for s in top_s]
        counts = [s[1] for s in top_s]
        ax.barh(range(len(names))[::-1], counts, color="seagreen", edgecolor="black")
        ax.set_yticks(range(len(names))[::-1])
        ax.set_yticklabels(names)
        ax.set_xlabel("Число упоминаний в вакансиях")
        ax.set_title("Топ-25 скиллов по упоминаниям (2016–2026)")
        ax.grid(axis="x", alpha=0.3)
        for i, n in enumerate(counts):
            ax.text(n + max(counts) * 0.01, len(names) - 1 - i, str(n),
                    va="center", fontsize=9)
        fig.tight_layout()
        fig.savefig(FIG_DIR / "top_skills.png", dpi=100)
        plt.close(fig)

    print(f"[OK] {out}")
    print(f"[OK] skill_counts.csv ({len(skills_df)} строк)")
    print(f"[OK] company_counts.csv ({len(companies_df)} строк)")
    print(f"[OK] 2 plots → {FIG_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())