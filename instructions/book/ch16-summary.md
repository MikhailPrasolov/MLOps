# Глава 16. Логистическая регрессия

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/logistic_regression.py`

> **Контекст:** линейная регрессия + сигмоида = классификатор. Глава строит модель `P(y=1|x) = σ(β·x)` через максимизацию правдоподобия (= минимизация negative log-likelihood) и gradient descent. На данных `experience, salary → paid_account` достигается precision=0.75, recall=0.8.

## Ключевые концепции

- **`logistic(x) = 1 / (1 + e^(-x))`** — сигмоида, сжимает `R → (0, 1)`
- **`logistic_prime(x) = σ(x) · (1 - σ(x))`** — для backprop / градиентов
- **Negative log-likelihood** — функция потерь для классификации: `-Σ [y·log p + (1-y)·log(1-p)]`
- **Gradient** — `-(y - σ(β·x)) · x_j` — на удивление похож на MSE
- **Predict threshold 0.5** — если `σ(β·x) ≥ 0.5` → класс 1
- **Обязательный `rescale(xs)`** — иначе GD не сходится (как в главе 10)

## Код

```python
import math
from scratch.linear_algebra import dot, vector_sum

def logistic(x: float) -> float:
    return 1.0 / (1 + math.exp(-x))

def _negative_log_likelihood(x, y, beta):
    if y == 1:
        return -math.log(logistic(dot(x, beta)))
    return -math.log(1 - logistic(dot(x, beta)))

def _negative_log_gradient(x, y, beta):
    """Похож на MSE-градиент, но через сигмоиду"""
    err = y - logistic(dot(x, beta))
    return [err * x_j for x_j in x]

def negative_log_gradient(xs, ys, beta):
    return vector_sum([_negative_log_gradient(x, y, beta)
                       for x, y in zip(xs, ys)])

# Predict
def predict(x, beta):
    return logistic(dot(beta, x))   # ∈ [0, 1]

# Цикл обучения (batch GD):
# beta = gradient_step(beta, negative_log_gradient(xs, ys, beta), -learning_rate)
# predict >= 0.5 → класс 1
```

## Связанные главы

- [[ch15-summary]] — предыдущая (множественная регрессия)
- [[ch17-summary]] — следующая (деревья — нелинейная альтернатива)
- [[ch18-summary]] — нейросеть = стек логистических регрессий
- [[ch11-summary]] — precision/recall/F1 для оценки

## Краткие выводы

1. **Логрегрессия = линейная регрессия + sigmoid** — но loss другой (NLL, не MSE)
2. **Градиент NLL = `-(y - σ(β·x)) · x`** — формально такой же, как у MSE для линейной регрессии
3. **`rescale(xs)` обязателен** — без нормализации GD расходится или сходится медленно

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| Логрегрессия | Бинарная классификация (churn, fraud, клик) |
| `predict >= 0.5` threshold | Подбирайте по бизнес-метрике (PR-кривая) |
| NLL loss | Любая задача с вероятностным выходом |
| Градиент через `sigmoid_prime` | Backprop в нейросетях |
