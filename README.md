# MLOps — Data Analytics Sandbox

> Python + Pandas: пространство для дата-аналитики, экспериментов и восстановления навыков.
>
> **Книга:** Джоэл Грасс «Data Science с нуля» (2-е изд.) — изучаем и применяем на практике.

---

## Цель

- Восстановление и развитие навыков **Python**, **Pandas**, **NumPy**, **Matplotlib / Seaborn**
- Параллельное изучение книги «Data Science с нуля» (код из `../data-science-from-scratch/scratch/`)
- ETL-эксперименты: загрузка, очистка, трансформация данных
- Аналитические исследования: EDA, когортный анализ, RFM-сегментация
- Визуализация и построение отчётов
- Пробы ML-моделей (sklearn)
- Прикладные мини-проекты в `projects/` (парсинг, EDA, mini-pipeline)

---

## Среда

| Компонент | Значение |
|-----------|----------|
| Anaconda3 | 2025.12 (Python 3.13) — `C:\Users\Selecty\anaconda3` |
| Conda env | `mlops` (Python 3.13.14) |
| numpy / pandas / sklearn | 2.5.1 / 3.0.3 / 1.9.0 |
| matplotlib / seaborn | 3.11.0 / 0.13.2 |
| Jupyter | Notebook + Lab (через pip) |
| Spyder IDE | 6.1.5 |
| Книжный пакет `scratch` | `pip install -e ../data-science-from-scratch` |

Декларативное описание окружения — `setup/environment.yml` (для переноса на другой ПК).

```powershell
conda activate mlops
```

---

## Структура

```
MLOps/                              ← твоя песочница
├── README.md                       ← этот файл
├── requirements.txt                ← pip-зависимости
├── .gitignore
│
├── setup/                          ← развёртывание на новом ПК
│   ├── BOOTSTRAP.md                — инструкция
│   ├── bootstrap.bat               — автоустановка (идемпотентный)
│   └── environment.yml             — декларативное описание conda-окружения
│
├── data/                           ← датасеты
│   ├── customers.csv               — клиенты (id, name, segment, state, city)
│   ├── orders.csv                  — заказы (id, order_date, ship_mode, customer_id, sales)
│   ├── Top_N_Sales.csv             — ~83 МБ, детальные продажи
│   └── Telegram/
│       └── ChatExport_2026-07-18/  ← web-export чата «Работа ищет аналитиков»
│           ├── messages.html … messages196.html   — 196 пейджинговых HTML
│           ├── css/, js/, images/                 — служебные ресурсы Telegram
│           └── *.html — основной вход для парсера в projects/work-analyst
│
├── notebooks/                      ← Jupyter-ноутбуки
│   ├── 01-pandas-basics.ipynb      — основы Series/DataFrame
│   ├── 01-pandas-basics.py         ← .py-экспорт ноутбука
│   └── Data Science/               ← конспекты по книге Грасса
│       ├── 01-introduction-and-python-crash-course.ipynb
│       ├── 02-visualization-linear-algebra-statistics.ipynb
│       ├── 01-… .py, 02-… .py     ← .py-зеркала для Spyder
│       └── _figures/               ← PNG-графики из ноутбуков
│
├── src/                            ← переиспользуемые модули
│   ├── __init__.py
│   ├── loaders.py                  — загрузка данных
│   ├── cleaners.py                 — очистка
│   ├── analytics.py                — аналитические утилиты
│   └── visualizers.py              — визуализация
│
├── tests/                          ← pytest
│   ├── __init__.py
│   └── test_loaders.py
│
├── instructions/                   ← документация и конспекты
│   ├── setup-guide.md              — установка и развёртывание
│   ├── jupyter-guide.md            — Jupyter Notebook и Lab
│   ├── jupyter-agent-workflow.md   — протокол работы AI-агента с .ipynb
│   ├── spyder-guide.md             — Spyder IDE
│   └── book/                       ← материалы по книге
│       ├── Gras_Data_Science_..._2017.pdf   — книга (рус. перевод 1-го изд.)
│       ├── ch01-summary.md … ch27-summary.md  ← 27 конспектов по главам
│
└── projects/                       ← прикладные мини-проекты (см. projects/README.md)
    └── work-analyst/               ← парсер вакансий из Telegram-экспорта + EDA

../data-science-from-scratch/       ← companion repo (код книги, рядом)
    ├── scratch/                    — модули по главам
    ├── first-edition/              — код 1-го издания
    ├── setup.py                    — для `pip install -e .`
    └── requirements.txt
```

---

## Данные

| Файл | Размер | Записей | Колонки |
|------|--------|---------|---------|
| `data/customers.csv` | ~43 КБ | ~800 | id, name, segment, state, city |
| `data/orders.csv` | ~216 КБ | ~5K | id, order_date, ship_mode, customer_id, sales |
| `data/Top_N_Sales.csv` | ~83 МБ | ~500K+ | TrDte, BCode, ClientID, Item, ItemGroup, Quantity, Amount |
| `data/Telegram/ChatExport_2026-07-18/messages*.html` | ~226 МБ суммарно | 196 файлов | HTML web-export Telegram-чата |

Разделитель: `customers.csv` / `orders.csv` — запятая, `Top_N_Sales.csv` — точка с запятой.

> ⚠️ Файлы в `data/` большого размера исключены через `.gitignore` (`data/*.csv`). Для версионирования использовать git-lfs или DVC.

---

## Проекты

В каталоге `projects/` лежат самостоятельные мини-проекты со своим `src/`, `tests/`, `notebooks/`, `data/`, `requirements.txt`. Главный репозиторий предоставляет окружение и общий код в `src/`.

| Проект | Что делает | Статус |
|--------|-----------|--------|
| [`work-analyst`](projects/work-analyst/) | Парсер Telegram web-export → CSV + EDA рынка вакансий | Phase 1+2 ✅, Phase 3 ⏳ |

Подробнее и правила добавления новых проектов — `projects/README.md`.

---

## Изучение книги

Конспекты по всем 27 главам в `instructions/book/chNN-summary.md` (формат: краткое содержание + ключевые формулы + ссылки на код в `../data-science-from-scratch/scratch/`).

| # | Тема | Файл в `scratch/` | Конспект |
|---|------|-------------------|----------|
| 1 | Введение | `introduction.py` | `ch01-summary.md` ✅ |
| 2 | Python Crash Course | `crash_course_in_python.py` | `ch02-summary.md` ✅ |
| 3 | Визуализация | `visualization.py` | `ch03-summary.md` ✅ |
| 4 | Линейная алгебра | `linear_algebra.py` | `ch04-summary.md` ✅ |
| 5 | Статистика | `statistics.py` | `ch05-summary.md` ✅ |
| 6 | Вероятность | `probability.py` | `ch06-summary.md` ✅ |
| 7 | Гипотезы и инференс | `inference.py` | `ch07-summary.md` ✅ |
| 8 | Градиентный спуск | `gradient_descent.py` | `ch08-summary.md` ✅ |
| 9 | Получение данных | `getting_data.py` | `ch09-summary.md` ✅ |
| 10 | Работа с данными | `working_with_data.py` | `ch10-summary.md` ✅ |
| 11 | ML введение | `machine_learning.py` | `ch11-summary.md` ✅ |
| 12 | k ближайших соседей | `k_nearest_neighbors.py` | `ch12-summary.md` ✅ |
| 13 | Наивный Байес | `naive_bayes.py` | `ch13-summary.md` ✅ |
| 14 | Простая линейная регрессия | `simple_linear_regression.py` | `ch14-summary.md` ✅ |
| 15 | Множественная регрессия | `multiple_regression.py` | `ch15-summary.md` ✅ |
| 16 | Логистическая регрессия | `logistic_regression.py` | `ch16-summary.md` ✅ |
| 17 | Деревья решений | `decision_trees.py` | `ch17-summary.md` ✅ |
| 18 | Нейронные сети | `neural_networks.py` | `ch18-summary.md` ✅ |
| 19 | Глубокое обучение | `deep_learning.py` | `ch19-summary.md` ✅ |
| 20 | Кластеризация | `clustering.py` | `ch20-summary.md` ✅ |
| 21 | NLP | `natural_language_processing.py` | `ch21-summary.md` ✅ |
| 22 | Анализ соцсетей | `social_network_analysis.py` | `ch22-summary.md` ✅ |
| 23 | Рекомендательные системы | `recommender_systems.py` | `ch23-summary.md` ✅ |
| 24 | Базы данных и SQL | `databases.py` | `ch24-summary.md` ✅ |
| 25 | MapReduce | `mapreduce.py` | `ch25-summary.md` ✅ |
| 26 | Этика данных | (нет) | `ch26-summary.md` ✅ |
| 27 | Что дальше | (нет) | `ch27-summary.md` ✅ |

Все 27 глав имеют конспекты. Прогресс по воспроизведению кода в ноутбуках `notebooks/Data Science/` — см. соответствующие `.ipynb` файлы (ch01–02 объединены в `01-introduction-and-python-crash-course.ipynb`).

---

## Быстрый старт

### На новом ПК (с нуля)

1. Установить Anaconda3 (галочка «Add to PATH»)
2. Склонировать `MLOps` и `data-science-from-scratch` рядом
3. Двойной клик по `setup/bootstrap.bat`
4. Подробнее — `setup/BOOTSTRAP.md`

### На текущем ПК (уже всё стоит)

```powershell
conda activate mlops
cd C:\Users\User\Desktop\GIT\MLOps
jupyter lab        # или jupyter notebook / spyder
```

Подробности:
- `setup/BOOTSTRAP.md` — что переносится между ПК и почему
- `instructions/setup-guide.md` — ручная установка
- `instructions/jupyter-guide.md` — Jupyter Notebook и Lab
- `instructions/spyder-guide.md` — Spyder IDE

---

## Проверка работоспособности

```powershell
conda activate mlops
python -c "
import numpy, pandas, sklearn, matplotlib, seaborn
from scratch.linear_algebra import dot
from scratch.statistics import mean
print(f'numpy {numpy.__version__}')
print(f'pandas {pandas.__version__}')
print(f'sklearn {sklearn.__version__}')
print(f'scratch OK: dot([1,2,3],[4,5,6]) = {dot([1,2,3],[4,5,6])}')
"
```

Ожидаемый вывод:
```
numpy 2.5.1
pandas 3.0.3
sklearn 1.9.0
scratch OK: dot([1,2,3],[4,5,6]) = 32
```

---

## Безопасность: коммиты и окружение

| Действие | Влияние на conda-окружение |
|----------|---------------------------|
| `git commit` / `push` / `pull` | Никакого |
| Изменения в `src/`, `notebooks/`, `instructions/`, `projects/` | Никакого |
| Изменения в `setup/environment.yml` | Никакого, пока не запустишь `bootstrap.bat` или `conda env update` |
| Двойной клик `bootstrap.bat` повторно | **Безопасно** — `env update` (добавит только новые пакеты) |
| `data_science_from_scratch/` — `git pull` | Через `pip install -e` изменения подхватываются автоматически |

**Conda-окружение `mlops` живёт в `C:\Users\Selecty\anaconda3\envs\mlops\` — за пределами репозитория.** Git про него не знает.

---

## Правила работы

- **Данные** — только в `data/` (`.gitignore` уже исключает `data/*.csv`)
- **Ноутбуки** — в `notebooks/`, именование `NN-description.ipynb`
- **Код** — переиспользуемые функции в `src/`, проектный код — в `projects/<project>/src/`
- **Самостоятельные проекты** — в `projects/<project>/` со своим `README.md`, `requirements.txt`, `src/`, `tests/`, `notebooks/` (см. `projects/README.md`)
- **Коммиты** — осмысленные сообщения на русском или английском
- **Не коммитить**: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `build/`, `*.egg-info/`, файлы >100 МБ

---

## Полезные ссылки

- `setup/BOOTSTRAP.md` — перенос на новый ПК
- `instructions/setup-guide.md` — ручная установка
- `instructions/jupyter-guide.md` — Jupyter Notebook и Lab
- `instructions/jupyter-agent-workflow.md` — протокол AI-агента с .ipynb
- `instructions/spyder-guide.md` — Spyder IDE
- `instructions/book/chNN-summary.md` — 27 конспектов книги
- `projects/README.md` — правила оформления проектов
- `../data-science-from-scratch/scratch/` — код всех глав книги
