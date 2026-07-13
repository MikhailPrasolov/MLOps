# MLOps — Data Analytics Sandbox

> Python + Pandas: пространство для дата-аналитики, экспериментов и восстановления навыков.
>
> **Книга:** Джоэл Грасс «Data Science с нуля» (2-е издание) — изучаем и применяем на практике.

---

## Цель

Этот репозиторий — **песочница** для:
- Восстановления и развития навыков **Python**, **Pandas**, **NumPy**, **Matplotlib / Seaborn**
- Параллельного изучения книги «Data Science с нуля» (код из `scratch/`)
- ETL-экспериментов: загрузка, очистка, трансформация данных
- Аналитических исследований: EDA, когортный анализ, RFM-сегментация
- Визуализации данных и построения отчётов
- Проб ML-моделей (sklearn)

---

## Структура

```
MLOps/                              ← твоя песочница
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/                           ← датасеты
│   ├── customers.csv               — клиенты (id, name, segment, state, city)
│   ├── orders.csv                  — заказы (id, order_date, ship_mode, customer_id, sales)
│   └── Top_N_Sales.csv             — ~87 МБ, детальные продажи
│
├── notebooks/                      ← Jupyter-ноутбуки
│   └── 01-pandas-basics.ipynb      — основы Series/DataFrame
│
├── src/                            ← переиспользуемые модули
│   ├── loaders.py                  — загрузка данных
│   ├── cleaners.py                 — очистка
│   ├── analytics.py                — аналитические утилиты
│   └── visualizers.py              — визуализация
│
├── instructions/                   ← документация и конспекты
│   ├── setup-guide.md              — установка Anaconda, Jupyter, Spyder
│   ├── ch01-02-summary.md          — конспект глав 1–2
│   └── Gras_Data_Science_....pdf   — книга (1-е издание, для справки)
│
└── tests/                          ← pytest
    └── test_loaders.py

../data-science-from-scratch/       ← companion repo (код книги)
    ├── scratch/                    — модули по главам (introduction, linear_algebra, …)
    ├── first-edition/              — код 1-го издания
    ├── setup.py                    — для pip install -e .
    └── requirements.txt
```

---

## Данные

| Файл | Размер | Описание | Колонки |
|------|--------|----------|---------|
| `data/customers.csv` | ~43 КБ | Информация о клиентах | id, name, segment, state, city |
| `data/orders.csv` | ~216 КБ | Заказы клиентов | id, order_date, ship_mode, customer_id, sales |
| `data/Top_N_Sales.csv` | ~87 МБ | Детальные продажи | TrDte, BCode, ClientID, Item, ItemGroup, Quantity, Amount |

---

## Изучение книги

| Глава | Тема | Файл в `scratch/` | Статус |
|-------|------|-------------------|--------|
| 1 | Введение | `introduction.py` | ✅ Прочитано |
| 2 | Python Crash Course | `crash_course_in_python.py` | ✅ Прочитано |
| 3 | Визуализация данных | `visualization.py` | ⏳ |
| 4 | Линейная алгебра | `linear_algebra.py` | ⏳ |
| 5 | Статистика | `statistics.py` | ⏳ |
| … | … | … | … |

Полная таблица — в `instructions/ch01-02-summary.md`.

---

## Быстрый старт

### Вариант A — Anaconda (рекомендуется)

```powershell
# Скачать и установить:
# https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Windows-x86_64.exe

# Создать и активировать окружение
conda create --name mlops python=3.12 numpy pandas matplotlib seaborn scikit-learn jupyter spyder -y
conda activate mlops

# Установить книжные зависимости
pip install -r ..\data-science-from-scratch\requirements.txt
pip install -e ..\data-science-from-scratch

# Запустить Jupyter
jupyter notebook
```

### Вариант B — чистый Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r ..\data-science-from-scratch\requirements.txt
pip install -e ..\data-science-from-scratch
jupyter notebook
```

Подробная инструкция по установке — **`instructions/setup-guide.md`**.

---

## Зависимости

Основной стек:

- `pandas`, `numpy` — работа с данными
- `matplotlib`, `seaborn` — визуализация
- `scikit-learn` — ML-модели
- `jupyter`, `ipykernel` — интерактивная среда
- `pytest` — тестирование

Полный список — в `requirements.txt`.

---

## Правила работы

- **Данные** — только `data/`, файлы в gitignore при большом объёме
- **Ноутбуки** — `notebooks/`, именование: `NN-description.ipynb`
- **Код** — переиспользуемые функции в `src/`
- **Коммиты** — осмысленные сообщения на русском или английском
- **Не коммитить**: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, большие файлы (>100 МБ)

---

## Полезные ссылки

- `instructions/setup-guide.md` — полная инструкция по установке и запуску
- `instructions/ch01-02-summary.md` — конспект глав 1–2 книги + сверка изданий
- `../data-science-from-scratch/scratch/` — код всех глав книги
