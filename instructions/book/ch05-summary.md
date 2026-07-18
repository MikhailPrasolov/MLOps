# Глава 5. Статистика

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/statistics.py`

> **Контекст:** глава — про описательную статистику как способ «разглядеть» данные до применения моделей. Ключевая мысль: одна метрика (среднее) часто врёт — нужны медиана, квантили, IQR и проверка корреляции на выбросах.

## Ключевые концепции

- **Меры центра** — `mean`, `median` (для нечётных/чётных отдельно), `quantile(xs, p)`, `mode` (возвращает **список** — мод может быть несколько!)
- **Меры разброса** — `data_range`, `variance` (с `n-1`, Bessel's correction), `standard_deviation`, `interquartile_range`
- **Совместная изменчивость** — `covariance(xs, ys) = dot(de_mean(xs), de_mean(ys)) / (n-1)`
- **Корреляция** — нормированная ковариация ∈ `[-1, 1]`; **крайне чувствительна к выбросам** (0.24 → 0.57 после удаления одного)

## Код

```python
from collections import Counter
import math
from scratch.linear_algebra import dot, sum_of_squares

def mean(xs): return sum(xs) / len(xs)
def median(v): return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)
def quantile(xs, p): return sorted(xs)[int(p * len(xs))]
def mode(x):    # возвращает СПИСОК мод
    counts = Counter(x)
    m = max(counts.values())
    return [xi for xi, c in counts.items() if c == m]

def de_mean(xs):
    x_bar = mean(xs); return [x - x_bar for x in xs]

def variance(xs):
    n = len(xs); return sum_of_squares(de_mean(xs)) / (n - 1)

def correlation(xs, ys):
    stdev_x = standard_deviation(xs); stdev_y = standard_deviation(ys)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(xs, ys) / stdev_x / stdev_y
    return 0

# ⚠️ Удаление выброса переворачивает корреляцию
assert 0.24 < correlation(num_friends, daily_minutes) < 0.25
# Удаляем юзера со 100 друзьями:
assert 0.57 < correlation(num_friends_good, daily_minutes_good) < 0.58
```

## Связанные главы

- [[ch04-summary]] — предыдущая (`dot`, `sum_of_squares`)
- [[ch06-summary]] — следующая (вероятность)
- [[ch07-summary]] — статистический вывод поверх этих мер

## Краткие выводы

1. **`mode()` возвращает список** — не путайте с «единственным» значением
2. **`variance` делит на `n-1`** — выборочная (исправленная) дисперсия, не `n`
3. **Корреляция ломается на выбросах** — всегда смотрите scatter до того, как верить числу

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `mean` vs `median` | Длиннохвостые распределения (зарплаты, latency) |
| `quantile` / IQR | EDA, детекция выбросов по 1.5×IQR правилу |
| `correlation` | A/B-тесты, feature selection, EDA-отчёты |
| `covariance` через `dot` | Основа для PCA, ковариационная матрица |
