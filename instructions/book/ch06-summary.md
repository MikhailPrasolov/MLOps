# Глава 6. Теория вероятностей

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/probability.py`

> **Контекст:** плотность и распределение — `pdf`/`cdf` — как мост между данными и вероятностью. Глава вводит равномерное и нормальное распределение, биномиальное как сумму bernoulli trials, и обратную `cdf` через бинарный поиск (нужна для A/B-тестов в следующей главе).

## Ключевые концепции

- **PDF** (`normal_pdf`) — плотность в точке; площадь под кривой = 1
- **CDF** (`normal_cdf`) — `P(X ≤ x)`; использует `math.erf`
- **Inverse normal CDF** — бинарный поиск по z для заданной вероятности (z-таблица наоборот)
- **Bernoulli trial / Binomial(n, p)** — подбрасывание монеты; `binomial(n, p) = sum(bernoulli_trial(p))`
- **Normal approximation to binomial** — при большом n биномиальное → нормальное (μ=np, σ=√(np(1−p)))
- **Условная вероятность** — `P(both | older) ≈ 1/2`, `P(both | either) ≈ 1/3` (две девочки в семье)

## Код

```python
import math
import random

SQRT_TWO_PI = math.sqrt(2 * math.pi)

def normal_pdf(x, mu=0, sigma=1):
    return math.exp(-(x-mu)**2 / 2 / sigma**2) / (SQRT_TWO_PI * sigma)

def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """Бинарный поиск: какой z даёт P(Z <= z) == p?"""
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)
    low_z, hi_z = -10.0, 10.0
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2
        mid_p = normal_cdf(mid_z)
        if mid_p < p: low_z = mid_z
        else:         hi_z = mid_z
    return mid_z

def bernoulli_trial(p):
    return 1 if random.random() < p else 0

def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))
```

## Связанные главы

- [[ch05-summary]] — предыдущая (статистика как предтеча)
- [[ch07-summary]] — следующая (гипотезы строятся поверх normal_cdf / inverse)
- [[ch15-summary]] — регрессия использует normal approximation

## Краткие выводы

1. **CDF — это «таблица z»** в коде; `inverse_normal_cdf` через бинарный поиск — бесценно для доверительных интервалов
2. **Binomial — сумма Bernoulli**; центральная предельная теорема гарантирует нормальную аппроксимацию при n>30
3. **Условная вероятность ≠ совместная** — `P(both | either) ≈ 1/3`, а не 1/4

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `normal_cdf` | Расчёт p-values, доверительных интервалов |
| `inverse_normal_cdf` | Подбор порога для A/B-теста по уровню значимости |
| `bernoulli_trial` / `binomial` | Симуляции, монте-карло, нагрузочное тестирование |
| Normal approximation | Быстрая оценка для больших n без биномиальной формулы |
