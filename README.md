# MLOps — Data Analytics Sandbox

> Python + Pandas: пространство для дата-аналитики, экспериментов и восстановления навыков.
>
> **Книга:** Джоэл Грасс «Data Science с нуля» (2-е изд.) — изучаем и применяем на практике.

---

## Цель

Этот репозиторий — **песочница** для:
- Восстановления и развития навыков **Python**, **Pandas**, **NumPy**, **Matplotlib / Seaborn**
- Параллельного изучения книги «Data Science с нуля» (код из `../data-science-from-scratch/scratch/`)
- ETL-экспериментов: загрузка, очистка, трансформация данных
- Аналитических исследований: EDA, когортный анализ, RFM-сегментация
- Визуализации данных и построения отчётов
- Проб ML-моделей (sklearn)

---

## Среда

| Компонент | Версия / Значение |
|-----------|-------------------|
| Anaconda3 | 2025.12 (Python 3.13) — `C:\Users\Selecty\anaconda3` |
| Conda env | `mlops` (Python 3.13) |
| numpy / pandas / sklearn | 2.5.1 / 3.0.3 / 1.9.0 |
| matplotlib / seaborn | 3.11.0 / 0.13.2 |
| Jupyter | Notebook + Lab (через pip) |
| Spyder IDE | 6.1.5 |
| Книжный пакет `scratch` | `pip install -e ../data-science-from-scratch` |

**Активация окружения:**
```powershell
conda activate mlops
```

---

## Структура

```
MLOps/                              ← твоя песочница
├── README.md                       ← этот файл
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
└── instructions/                   ← документация и конспекты
    ├── setup-guide.md              — установка и развёртывание
    ├── jupyter-guide.md            — Jupyter Notebook и Lab
    ├── spyder-guide.md             — Spyder IDE
    └── book/                       ← материалы по книге
        ├── Gras_Data_Science_..._2017.pdf  — книга (1-е изд., для справки)
        └── ch01-02-summary.md      — конспект глав 1–2 + сверка изданий

../data-science-from-scratch/       ← companion repo (код книги)
    ├── scratch/                    — модули по главам (introduction, linear_algebra, …)
    ├── first-edition/              — код 1-го издания
    ├── setup.py                    — для pip install -e .
    └── requirements.txt
```

---

## Данные

| Файл | Размер | Записей | Колонки |
|------|--------|---------|---------|
| `data/customers.csv` | ~43 КБ | ~800 | id, name, segment, state, city |
| `data/orders.csv` | ~216 КБ | ~5K | id, order_date, ship_mode, customer_id, sales |
| `data/Top_N_Sales.csv` | ~87 МБ | ~500K+ | TrDte, BCode, ClientID, Item, ItemGroup, Quantity, Amount |

Разделитель: `customers.csv` / `orders.csv` — запятая, `Top_N_Sales.csv` — точка с запятой.

---

## Изучение книги

| # | Тема | Файл в `scratch/` | Статус |
|---|------|-------------------|--------|
| 1 | Введение | `introduction.py` | ✅ |
| 2 | Python Crash Course | `crash_course_in_python.py` | ✅ |
| 3 | Визуализация | `visualization.py` | ⏳ |
| 4 | Линейная алгебра | `linear_algebra.py` | ⏳ |
| 5 | Статистика | `statistics.py` | ⏳ |
| 6 | Вероятность | `probability.py` | ⏳ |
| 7 | Гипотезы и инференс | `inference.py` | ⏳ |
| 8 | Градиентный спуск | `gradient_descent.py` | ⏳ |
| 9–10 | Данные | `getting_data.py`, `working_with_data.py` | ⏳ |
| 11 | Машинное обучение | `machine_learning.py` | ⏳ |
| 12–17 | ML-модели | `k_nearest_neighbors.py` … `decision_trees.py` | ⏳ |
| 18–19 | Нейросети, deep learning | `neural_networks.py`, `deep_learning.py` | ⏳ |
| 20–25 | Кластеризация, NLP, сети, рекомендации, SQL, MapReduce | `clustering.py` … `mapreduce.py` | ⏳ |

Конспект глав 1–2 — в `instructions/book/ch01-02-summary.md`.

---

## Быстрый старт

```powershell
# 1. Активировать окружение
conda activate mlops

# 2. Перейти в проект
cd C:\Users\Selecty\Desktop\GIT\MLOps

# 3. Запустить Jupyter
jupyter notebook          # классический
jupyter lab                # современный (рекомендуется)

# 4. Или запустить Spyder
spyder
```

После установки читай подробные гайды в `instructions/`:
- `setup-guide.md` — установка среды
- `jupyter-guide.md` — Jupyter Notebook / Lab
- `spyder-guide.md` — Spyder IDE

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

## Зависимости

- `pandas`, `numpy` — работа с данными
- `matplotlib`, `seaborn` — визуализация
- `scikit-learn` — ML-модели
- `jupyter`, `ipykernel` — интерактивная среда
- `pytest` — тестирование

Полный список — в `requirements.txt`.

---

## Правила работы

- **Данные** — только в `data/`
- **Ноутбуки** — в `notebooks/`, именование `NN-description.ipynb`
- **Код** — переиспользуемые функции в `src/`
- **Коммиты** — осмысленные сообщения на русском или английском
- **Не коммитить**: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, файлы >100 МБ

---

## Полезные ссылки

- `instructions/setup-guide.md` — установка и развёртывание
- `instructions/jupyter-guide.md` — Jupyter Notebook и Lab
- `instructions/spyder-guide.md` — Spyder IDE
- `instructions/book/ch01-02-summary.md` — конспект глав 1–2
- `../data-science-from-scratch/scratch/` — код всех глав книги
