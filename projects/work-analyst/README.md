# Work Analyst — Telegram вакансии → CSV

Парсер Telegram web export чата **«Работа ищет аналитиков // Вакансии»** в плоский CSV.

## Назначение

Извлекает только сообщения-вакансии (по тегам `#vacancy` / `#вакансия` / `#естьработа`) из HTML-экспорта чата и сохраняет в `data/processed/vacancies.csv` для последующего анализа (EDA, NLP, ML).

## Структура проекта

```
projects/work-analyst/
├── src/
│   ├── __init__.py
│   ├── loader.py            # list_html_files(), iter_messages_html()
│   ├── parser.py            # parse_message() → Message dataclass
│   ├── filter.py            # is_vacancy(), filter_vacancies()
│   └── pipeline.py          # run() — оркестрация
├── notebooks/
│   └── parse_run.py         # CLI entry-point (Phase 1: ETL)
├── analytics/               # Phase 2: EDA — прогресс и выводы
│   ├── 01_profile.py
│   ├── 02_time_trends.py
│   ├── 03_geo_seniority.py
│   ├── 04_salary.py
│   ├── 05_companies_skills.py
│   ├── findings.md          # ← главный отчёт: TL;DR + 6 разделов + план
│   ├── vacancies_with_salary.csv   # 28 МБ, с распарсенными зарплатами
│   ├── skill_counts.csv
│   ├── company_counts.csv
│   └── figures/             # 14 PNG графиков
├── tests/
│   └── test_parser.py       # pytest (25 тестов)
├── data/
│   └── processed/           # vacancies.csv (output, 28 МБ)
├── logs/                    # parsing.log (WARNING+)
├── README.md
└── requirements.txt
```

## Запуск

### Установка зависимостей

```powershell
conda activate mlops
pip install -r requirements.txt
```

### Сэмпл (10 файлов, для разработки)

```powershell
cd C:\Users\Selecty\Desktop\GIT\MLOps\projects\work-analyst
python notebooks/parse_run.py --in ../../data/Telegram/ChatExport_2026-07-18 --out data/processed/vacancies.csv --limit 10 --log logs/parsing.log
```

### Полный прогон (196 файлов, 226 МБ)

```powershell
python notebooks/parse_run.py --in ../../data/Telegram/ChatExport_2026-07-18 --out data/processed/vacancies.csv --log logs/parsing.log
```

### Тесты

```powershell
pytest tests/ -v
```

## Схема CSV

| Поле | Тип | Описание |
|---|---|---|
| `date` | ISO 8601 UTC | `2016-09-21T13:35:02+00:00` |
| `message_id` | int | ID из Telegram (`message12345`) |
| `author` | str | Имя отправителя (из `from_name`) |
| `text` | str | Чистый текст, `<br>` → пробел, ссылки сохранены как `[видимый](URL)` |
| `links` | str | URL через `;`, дедуплицированы |
| `tags` | str | Хештеги через `;`, lowercase, без `#go_to_message` якорей |
| `source_file` | str | Имя исходного HTML-файла |

## Selection criteria

Вакансия = сообщение, у которого **есть хотя бы один** тег из:
- `#vacancy` (английский, основной)
- `#вакансия` (русский, основной)
- `#vacancies` (редкая форма множественного числа)
- `#вакансиям` (дательный падеж)
- `#естьработа` (исторический тег из правил чата)

Service-сообщения (смена названия, конвертация supergroup) и `joined`-сообщения без автора сохраняются, но без `author` (None → пустая строка в CSV).

## Что сделано

- **Phase 1 ✅ (ETL)**: парсер Telegram-экспорта → 10 095 вакансий в `data/processed/vacancies.csv` (279 сек)
- **Phase 2 ✅ (EDA)**: 5 скриптов анализа + 14 графиков + `findings.md` с TL;DR
- **Phase 3 (следующая)**: word boundaries, NER для зарплат, кластеризация вакансий, прогноз трендов

### Главные выводы (Phase 2)

| # | Вывод | Цифра |
|---|---|---|
| 1 | Рынок вакансий сжимается 4 года | -78% от пика 2021 (2719 → 595) |
| 2 | Зарплаты растут на фоне спада | 95k → 250k ₽ (+163% за 8 лет) |
| 3 | Рынок = удалёнка | 47% вакансий remote |
| 4 | SQL — абсолютный лидер | 6453 упоминания (64% вакансий) |
| 5 | R всё ещё > Python | 5216 vs 3363 |

Подробнее — в `analytics/findings.md`.

## Lessons learned

- Telegram web export делит историю на пейджинговые HTML (`messages.html`, `messages2.html`, ...). Парсер обрабатывает каждый файл отдельно, склеивает в общий CSV.
- `#go_to_message12345` — это **не** тег, а внутренний якорь Telegram для cross-reference. Фильтруем при парсинге тегов.
- Для больших файлов (226 МБ) BeautifulSoup с `lxml` парсит ~1.2 МБ за ~1 сек. Полный прогон ≈ 3-5 мин на средней машине.
- **Regex для зарплат** требует контекста (₽/зарплата/Salary рядом) иначе захватывает телефоны/ID. Обязательно фильтровать по диапазону [15k–1.5M ₽].
- **Substring search** для компаний без `\b` даёт false positives (VK → «вклады»). Использовать word boundaries для точной статистики.
- **Тег coverage** = 23-50% для большинства тегов — НЕЛЬЗЯ судить о структуре только по ним. Нужна NLP-разметка или ручная классификация.