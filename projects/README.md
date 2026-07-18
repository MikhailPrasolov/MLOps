# MLOps / projects

> Каталог прикладных мини-проектов на базе общего окружения `MLOps`.
> Каждый проект самодостаточен: свой `src/`, `tests/`, `notebooks/`, `data/`, `requirements.txt`, `README.md`.

---

## Назначение

`projects/` отделяет **экспериментальные песочницы** (корневой `MLOps/` — ноутбуки, конспекты, общие модули) от **прикладных задач** со своим жизненным циклом: парсинг → очистка → анализ → отчёт.

Общий код из корневого `src/` (`loaders.py`, `analytics.py`, `visualizers.py`) доступен из проектов через `PYTHONPATH` conda-окружения `mlops`.

---

## Текущие проекты

| Проект | Что делает | Фазы | Статус |
|--------|-----------|-------|--------|
| [`work-analyst/`](work-analyst/) | Парсер Telegram web-export чата «Работа ищет аналитиков» → плоский CSV вакансий + EDA рынка | Phase 1 ETL ✅, Phase 2 EDA ✅, Phase 3 NLP/ML ⏳ | активный |

---

## Структура каталога

```
projects/
├── README.md                       ← этот файл
└── <project-name>/                 ← самостоятельный проект
    ├── README.md                   ← описание + инструкции запуска
    ├── requirements.txt            ← зависимости проекта (pip)
    ├── src/                        ← модули проекта (loader, parser, pipeline, …)
    ├── tests/                      ← pytest
    ├── notebooks/                  ← CLI entry-points и ad-hoc ноутбуки
    ├── data/                       ← входные и выходные данные проекта
    │   ├── raw/                    ← неизменяемые исходники (опц.)
    │   └── processed/              ← результат ETL
    ├── analytics/                  ← EDA: NN_<тема>.py + NN_<тема>.txt отчёт + findings.md + figures/
    └── logs/                       ← WARNING+ логи парсеров
```

---

## Правила оформления нового проекта

1. **Изоляция**: каждый проект живёт в своей подпапке, не трогает корень `MLOps/`.
2. **Именование**: kebab-case (`work-analyst`, `sales-forecast`, …).
3. **`README.md`** обязателен и должен содержать:
   - краткое описание задачи (1–2 предложения),
   - структуру каталога проекта,
   - инструкции запуска (CLI-команды),
   - схему выходных данных (CSV/Parquet/JSON — какие колонки, типы),
   - ссылку на основной отчёт (`analytics/findings.md` для EDA-проектов).
4. **`requirements.txt`** — только то, чего нет в корневом `requirements.txt` (чтобы `pip install -r` работал идемпотентно).
5. **Код**: переиспользуемая логика в `src/`, разовые скрипты — в `notebooks/`.
6. **Данные**: всё, что >1 МБ, исключить через `.gitignore` (`data/<project>/processed/*.csv`) или версионировать через git-lfs/DVC.
7. **Тесты**: `pytest tests/` должен проходить без сетевого доступа и зависеть только от фикстур в `tests/fixtures/` (если нужны большие тестовые данные).
8. **EDA-проекты** (по конвенции `work-analyst`):
   - скрипты анализа лежат в `analytics/` с `NN_` префиксом (`01_profile.py`, `02_time_trends.py`, …);
   - рядом с каждым `.py` сохраняется текстовый отчёт `.txt` с тем же префиксом (`01_profile.txt`);
   - агрегированные табличные CSV — в `data/processed/`;
   - графики — в `analytics/figures/`;
   - главный итоговый отчёт — `analytics/findings.md` (TL;DR + разделы).

---

## Совместное использование с корневым окружением

Все проекты работают в общем conda-env `mlops` (см. корень `MLOps/README.md`). Чтобы из проекта импортировать общие модули:

```powershell
conda activate mlops
$env:PYTHONPATH = "C:\Users\Selecty\Desktop\GIT\MLOps;$env:PYTHONPATH"
cd C:\Users\Selecty\Desktop\GIT\MLOps\projects\<project>
python -c "from src.loaders import load_customers; print(load_customers().shape)"
```

Или установить корневой пакет в editable-режиме (если появится `setup.py` в корне).

---

## Добавление нового проекта (быстрый чек-лист)

- [ ] Создать `projects/<name>/` со структурой выше
- [ ] `pip install -r requirements.txt` (относительно проекта)
- [ ] Написать `README.md` по шаблону из существующего `work-analyst/`
- [ ] Если EDA — следовать layout-конвенции (NN_скрипт → NN_отчёт → findings.md)
- [ ] Зафиксировать в git отдельным коммитом «projects: init <name>»
- [ ] Добавить строку в таблицу «Текущие проекты» в этом файле
