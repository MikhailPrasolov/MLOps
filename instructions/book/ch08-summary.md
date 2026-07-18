# Глава 8. Градиентный спуск

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/gradient_descent.py`

> **Контекст:** фундамент всей оптимизации в ML. Глава показывает, как численно оценить градиент через `difference_quotient`, затем использовать аналитический градиент (`2*v_i` для sum_of_squares), и три варианта спуска — batch / mini-batch / stochastic — на примере подбора `slope=20, intercept=5`.

## Ключевые концепции

- **Difference quotient** — `(f(x+h) − f(x)) / h` — численная оценка производной
- **Gradient** — вектор частных производных; направление наискорейшего роста функции
- **Gradient step** — `v = v + step_size * gradient` (с минусом — минимизация)
- **Batch GD** — на каждом шаге по **всей** выборке; стабильно, дорого
- **Stochastic GD (SGD)** — по **одному** примеру; шумно, дёшево, может «выбить» из локального минимума
- **Mini-batch** — компромисс: пачка из N примеров → батч-генератор через `yield`
- **Step size (learning rate)** — критический гиперпараметр; слишком большой → расходимость

## Код

```python
import random
from scratch.linear_algebra import Vector, dot, distance, scalar_multiply

def gradient_step(v, gradient, step_size):
    """v_new = v - step_size * gradient (для минимизации)"""
    return [v_i - step_size * g_i for v_i, g_i in zip(v, gradient)]

def sum_of_squares_gradient(v):
    """Аналитический градиент f(v) = ||v||² → ∇f = 2v"""
    return [2 * v_i for v_i in v]

# Линейная регрессия: подбираем slope, intercept
def linear_gradient(x, y, theta):
    slope, intercept = theta
    predicted = slope * x + intercept
    error = predicted - y
    return [2 * error * x, 2 * error]      # ∇MSE

# Mini-batch генератор
def minibatches(dataset, batch_size, shuffle=True):
    starts = list(range(0, len(dataset), batch_size))
    if shuffle: random.shuffle(starts)
    for start in starts:
        yield dataset[start:start + batch_size]

# Пример: 5000 эпох batch-GD дают slope≈20, intercept≈5
```

## Связанные главы

- [[ch07-summary]] — предыдущая
- [[ch09-summary]] — следующая
- [[ch14-summary]] — линейная регрессия через GD
- [[ch16-summary]] — логистическая регрессия через GD
- [[ch18-summary]] — backpropagation как частный случай chain rule + GD

## Краткие выводы

1. **`gradient_step` со знаком «минус»** — всегда двигаемся **против** градиента для минимизации
2. **SGD выигрывает на больших данных** — не нужно держать всю выборку в памяти
3. **Аналитический градиент >> численный** — `difference_quotient` только для отладки/проверки

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `gradient_step` | Любая ML-модель с дифференцируемой функцией потерь |
| `linear_gradient` | Основа для линейной/логистической регрессии |
| `minibatches` | Все нейросети — `torch.utils.data.DataLoader` делает то же |
| SGD vs batch | На больших данных SGD быстрее сходится и обобщает лучше |
