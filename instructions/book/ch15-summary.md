# Глава 15. Множественная регрессия

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/multiple_regression.py`

> **Контекст:** расширение до `y = β·x = β₀ + β₁x₁ + β₂x₂ + ...`. Вектор `x` всегда начинается с 1 (для intercept). Глава добавляет три продвинутых приёма: **bootstrap** для оценки ошибок коэффициентов, **p-value** через `normal_cdf` и **регуляризацию** (ridge / lasso) против переобучения.

## Ключевые концепции

- **Дизайн-матрица** — `x = [1, x₁, x₂, ..., xₙ]`; первый элемент всегда 1 для β₀ (intercept)
- **`predict(x, β) = dot(x, β)`** — вся модель = одно скалярное произведение
- **`sqerror_gradient(x, y, β) = [2·err·x_i for x_i in x]`** — градиент для SGD
- **Bootstrap** — `bootstrap_sample` с повторениями; оценивает стандартные ошибки без формул
- **p-value коэффициента** — `2 * (1 - normal_cdf(beta_hat / sigma_hat))` — значим ли признак
- **Ridge-регуляризация** — `+ α · Σ βᵢ²` в loss; штрафует большие коэффициенты
- **Lasso-регуляризация** — `+ α · Σ |βᵢ|`; обнуляет незначимые коэффициенты → feature selection

## Код

```python
from scratch.linear_algebra import Vector, dot, add
from scratch.statistics import correlation, standard_deviation, mean

def predict(x: Vector, beta: Vector) -> float:
    """Первый элемент x = 1 для intercept"""
    return dot(x, beta)

def error(x, y, beta):
    return predict(x, beta) - y

def sqerror_gradient(x, y, beta):
    err = error(x, y, beta)
    return [2 * err * x_i for x_i in x]

def least_squares_fit(xs, ys, learning_rate=0.001, num_steps=1000, batch_size=1):
    guess = [random.random() for _ in xs[0]]
    for _ in range(num_steps):
        for s in range(0, len(xs), batch_size):
            batch = list(zip(xs[s:s+batch_size], ys[s:s+batch_size]))
            grad = vector_mean([sqerror_gradient(x, y, guess) for x, y in batch])
            guess = gradient_step(guess, grad, -learning_rate)
    return guess

# Ridge
def ridge_penalty(beta, alpha):
    return alpha * dot(beta[1:], beta[1:])

def ridge_penalty_gradient(beta, alpha):
    return [0.] + [2 * alpha * b_j for b_j in beta[1:]]

# Пример: на 4 признаках (friends, work_hours, phd, ...) R² ≈ 0.68
# β_friends ≈ 0.97, β_work_hours ≈ -1.85, β_phd ≈ 0.91
```

## Связанные главы

- [[ch14-summary]] — предыдущая (один β, аналитическое решение)
- [[ch16-summary]] — следующая (логистическая регрессия для классификации)
- [[ch07-summary]] — p-value из статистического вывода
- [[ch18-summary]] — нейросеть = регрессия с нелинейностями

## Краткие выводы

1. **`x[0] = 1`** — стандартный трюк для встраивания intercept в ту же формулу
2. **Bootstrap вместо формул** — работает для **любых** моделей, не только линейных
3. **Ridge vs Lasso** — Ridge сжимает, Lasso обнуляет; Lasso лучше для интерпретируемости

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| Множественная регрессия | Базовая табличная модель, маркетинг-микс моделирование |
| Bootstrap стандартных ошибок | Оценка uncertainty без аналитических формул |
| p-value коэффициентов | Feature selection, проверка гипотез о признаках |
| Ridge/Lasso | Борьба с переобучением, feature selection (Lasso) |
