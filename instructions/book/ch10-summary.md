# Глава 10. Работа с данными

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/working_with_data.py`

> **Контекст:** глава — про «причёсывание» сырых данных: `NamedTuple` для структурированных записей, `Optional` для безопасного парсинга, `defaultdict` для группировки, `rescale` для нормализации и **PCA** для понижения размерности.

## Ключевые концепции

- **`NamedTuple`** — `class StockPrice(NamedTuple): symbol, date, closing_price` — typed dict без наследования
- **`Optional[T]`** — `try_parse_row` возвращает `None` при ошибке (вместо exception)
- **`Counter` для бакетизации** — `bucketize(point, bucket_size) = bucket_size * math.floor(point / bucket_size)`
- **`correlation_matrix`** — `make_matrix(n, n, lambda i, j: correlation(data[i], data[j]))`
- **Rescale** — `(x - mean) / stdev` для каждого измерения → mean=0, stdev=1
- **PCA** — поиск направления максимальной дисперсии через `directional_variance` + GD
- **`de_mean`** — центрирование (вычитание среднего) — обязательный шаг перед PCA

## Код

```python
from typing import NamedTuple, Optional, List, Dict
from collections import Counter, defaultdict
import datetime
import re
from dateutil.parser import parse

# 1. NamedTuple
class StockPrice(NamedTuple):
    symbol: str
    date: datetime.date
    closing_price: float

# 2. Безопасный парсер
def try_parse_row(row: List[str]) -> Optional[StockPrice]:
    symbol, date_, price_ = row
    if not re.match(r"^[A-Z]+$", symbol): return None
    try:
        date = parse(date_).date()
        price = float(price_)
    except ValueError:
        return None
    return StockPrice(symbol, date, price)

# 3. Rescale (стандартизация)
def rescale(data: List[Vector]) -> List[Vector]:
    means, stdevs = scale(data)
    rescaled = [v[:] for v in data]
    for v in rescaled:
        for i in range(len(v)):
            if stdevs[i] > 0:
                v[i] = (v[i] - means[i]) / stdevs[i]
    return rescaled

# 4. PCA: первая главная компонента через GD
def first_principal_component(data, n=100, step_size=0.1):
    guess = [1.0 for _ in data[0]]
    for _ in range(n):
        grad = directional_variance_gradient(data, guess)
        guess = gradient_step(guess, grad, step_size)
    return direction(guess)

def pca(data, num_components):
    components = []
    for _ in range(num_components):
        comp = first_principal_component(data)
        components.append(comp)
        data = remove_projection(data, comp)
    return components
```

## Связанные главы

- [[ch09-summary]] — предыдущая (откуда данные)
- [[ch11-summary]] — следующая (что с ними делать)
- [[ch17-summary]] — деревья решений используют rescale-подобные операции
- [[ch18-summary]] — нейросети требуют нормализованных входов

## Краткие выводы

1. **`NamedTuple` лучше dict** — типизация + иммутабельность + `.field` доступ
2. **Rescale обязателен** для нейросетей и PCA; без него признак с большим масштабом «задавит» остальные
3. **PCA через GD на directional variance** — прототип того, что делает `sklearn.decomposition.PCA`

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `NamedTuple` | DTO, строки таблиц, протоколы обмена |
| `Optional[T]` | Парсинг «грязных» внешних данных |
| `defaultdict(list)` | Группировка по ключу, инвертированный индекс |
| `rescale` | Подготовка данных для нейросетей, KNN, SVM |
| PCA | Визуализация, устранение мультиколлинеарности, фичи для downstream-моделей |
