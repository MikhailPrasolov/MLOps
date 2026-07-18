# Глава 14. Простая линейная регрессия

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/simple_linear_regression.py`

> **Контекст:** y = α + β·x + ε. Глава показывает **два способа** найти α и β: (1) аналитически через `correlation`, `standard_deviation`, `mean`; (2) итеративно через gradient descent из главы 8. На данных `num_friends → daily_minutes` β ≈ 0.9, R² ≈ 0.33.

## Ключевые концепции

- **Модель** — `predict(alpha, beta, x_i) = beta * x_i + alpha`
- **Error** = `predicted - actual` (со знаком!)
- **Least squares fit** — аналитическое решение: `β = corr(x,y) · σ_y / σ_x`, `α = ȳ - β · x̄`
- **Gradient descent** — `grad_α = Σ 2·error`, `grad_β = Σ 2·error·x_i`
- **R² (коэффициент детерминации)** — `1 - SSE/SST`, доля объяснённой дисперсии ∈ [0, 1]
- **Total sum of squares (SST)** — `Σ (y_i - ȳ)²` — общий разброс y

## Код

```python
from scratch.linear_algebra import Vector
from scratch.statistics import correlation, standard_deviation, mean

def predict(alpha, beta, x_i):
    return beta * x_i + alpha

def error(alpha, beta, x_i, y_i):
    return predict(alpha, beta, x_i) - y_i

def least_squares_fit(x: Vector, y: Vector):
    """Аналитическое решение — мгновенно, без GD"""
    beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
    alpha = mean(y) - beta * mean(x)
    return alpha, beta

def total_sum_of_squares(y):
    return sum(v ** 2 for v in de_mean(y))

def r_squared(alpha, beta, x, y):
    """1 - (sum of squared errors) / (total sum of squares)"""
    return 1.0 - sum_of_sqerrors(alpha, beta, x, y) / total_sum_of_squares(y)

# Пример на num_friends → daily_minutes (без выброса):
# alpha ≈ 22.95, beta ≈ 0.903, R² ≈ 0.329
# GD даёт те же значения за ~10000 эпох
```

## Связанные главы

- [[ch13-summary]] — предыдущая
- [[ch15-summary]] — следующая (множественная регрессия = больше β)
- [[ch08-summary]] — gradient descent для оптимизации
- [[ch05-summary]] — correlation, standard_deviation, mean

## Краткие выводы

1. **Аналитическое решение vs GD** — для простой регрессии формула работает мгновенно и точно; GD нужен для нелинейных случаев
2. **R² ∈ [0, 1]** — но **0.33 «плохо»** в общем случае; смотрите ещё на остатки
3. **Intercept α = ȳ − β·x̄** — линия всегда проходит через точку средних `(x̄, ȳ)`

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `least_squares_fit` | Базовая линейная модель, тренды, прогноз |
| R² | Сравнение моделей, отчёт руководству |
| Gradient descent на MSE | Numpy/SciPy `curve_fit`, обучение нейросетей |
| `error` без квадрата | Анализ остатков, выбросы |
