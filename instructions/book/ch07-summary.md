# Глава 7. Гипотезы и статистические выводы

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/inference.py`

> **Контекст:** глава превращает нормальное распределение из главы 6 в **p-value**, доверительные интервалы и A/B-тесты. Ключевая мысль: «отклонить H₀» = наше наблюдение **настолько экстремально**, что при верной H₀ его вероятность < α (обычно 5%).

## Ключевые концепции

- **Null hypothesis H₀** vs **Alternative H₁** — p-value считается в предположении H₀
- **Type I (α)** vs **Type II (β) error**; **power = 1 − β** — вероятность поймать эффект, если он есть
- **Доверительный интервал 95%** — `normal_two_sided_bounds(0.95, mu, sigma)` → симметричный интервал вокруг μ
- **p-value** — `2 * normal_probability_above(x, mu, sigma)` для двустороннего теста
- **A/B test** — `a_b_test_statistic(N_A, n_A, N_B, n_B)` через z-статистику `(p_B - p_A) / sqrt(σ²_A + σ²_B)`
- **Beta distribution** — распределение на [0,1] для параметра `p`; `B(α,β)` — нормировка через `math.gamma`

## Код

```python
from typing import Tuple
import math
from scratch.probability import normal_cdf, inverse_normal_cdf

def normal_approximation_to_binomial(n, p):
    """μ и σ для биномиального через нормальное"""
    return (p * n, math.sqrt(p * (1 - p) * n))

def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """Симметричные bounds вокруг μ, содержащие нужную вероятность"""
    tail = (1 - probability) / 2
    upper = inverse_normal_cdf(1 - tail, mu, sigma)
    lower = inverse_normal_cdf(tail, mu, sigma)
    return lower, upper

def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu: return 2 * (1 - normal_cdf(x, mu, sigma))
    else:        return 2 * normal_cdf(x, mu, sigma)

# A/B test
def a_b_test_statistic(N_A, n_A, N_B, n_B):
    p_A = n_A / N_A;  sigma_A = math.sqrt(p_A * (1 - p_A) / N_A)
    p_B = n_B / N_B;  sigma_B = math.sqrt(p_B * (1 - p_B) / N_B)
    return (p_B - p_A) / math.sqrt(sigma_A**2 + sigma_B**2)

# Пример: разница 200 vs 150 на 1000 = z ≈ -2.94, p ≈ 0.003 → отвергаем H₀
z = a_b_test_statistic(1000, 200, 1000, 150)
assert two_sided_p_value(z) < 0.01
```

## Связанные главы

- [[ch06-summary]] — предыдущая (`normal_cdf`, `inverse_normal_cdf`)
- [[ch08-summary]] — следующая (статистика → оптимизация)
- [[ch14-summary]] — регрессия как стат. вывод с другими H₀/H₁

## Краткие выводы

1. **p-value ≠ P(H₀ | data)** — это `P(data | H₀)`, ловушка для новичков
2. **Доверительный интервал ≠ вероятность попадания в него** — при повторении эксперимента 95% таких интервалов накроют истинный параметр
3. **Power растёт** с размером выборки и эффектом — рассчитывайте sample size заранее

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `a_b_test_statistic` | A/B-тесты в продукте, маркетинге |
| `normal_two_sided_bounds` | 95% доверительные интервалы для метрик |
| `two_sided_p_value` | Проверка гипотез, регрессионные коэффициенты |
| `beta_pdf` | Байесовский аналог A/B-теста |
