# Глава 4. Линейная алгебра

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/linear_algebra.py`

> **Контекст:** минимальный векторно-матричный набор для понимания ML. Вектор = список `float`, матрица = список списков, без `numpy`. Главная операция — `dot product`, через которую выражаются почти все ML-формулы.

## Ключевые концепции

- **Vector** = `List[float]`; **Matrix** = `List[List[float]]` — type alias'ы
- **Операции над векторами** — `add`, `subtract`, `scalar_multiply`, `vector_sum`, `vector_mean`
- **Dot product** — `sum(v_i * w_i)`; через него — `sum_of_squares`, `magnitude`, `squared_distance`
- **Матрица** — `shape`, `get_row`, `get_column`, `make_matrix(num_rows, num_cols, entry_fn)`
- **Identity matrix** — `make_matrix(n, n, lambda i, j: 1 if i == j else 0)`
- **Матрица смежности** — взвешенный граф, `friend_matrix[i][j] == 1` ⇔ друзья

## Код

```python
from typing import List, Callable
import math

Vector = List[float]
Matrix = List[List[float]]

def add(v: Vector, w: Vector) -> Vector:
    return [v_i + w_i for v_i, w_i in zip(v, w)]

def dot(v: Vector, w: Vector) -> float:
    """Главная операция ML: v_1*w_1 + ... + v_n*w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def magnitude(v: Vector) -> float:
    return math.sqrt(sum_of_squares(v))     # ||v||

def distance(v: Vector, w: Vector) -> float:
    return magnitude(subtract(v, w))        # евклидово расстояние

def make_matrix(num_rows, num_cols, entry_fn: Callable[[int, int], float]):
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]

# Матрица дружбы — взвешенный граф
friend_matrix = [[0,1,1,0,0,...], ...]
friends_of_five = [i for i, is_friend in enumerate(friend_matrix[5])
                   if is_friend]
```

## Связанные главы

- [[ch03-summary]] — предыдущая
- [[ch05-summary]] — следующая (использует `dot`)
- [[ch18-summary]] — нейросети (умножение матриц)
- [[ch15-summary]] — множественная регрессия (формула через матрицы)

## Краткие выводы

1. **`dot(v, v) = sum_of_squares`** — фундамент для дисперсии, корреляции, нейросетей
2. **Матрица `friend_matrix`** — общий паттерн: смежность графа, корреляционная матрица, one-hot encoding
3. **`make_matrix(n, n, lambda i, j: ...)`** — идиоматичный способ строить матрицы по формуле `(i,j)`

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `dot(v, w)` | Корреляция, косинусное сходство, линейная регрессия |
| `magnitude` / `distance` | KNN, кластеризация, anomaly detection |
| `Matrix` как `List[List]` | Графы, изображения (пиксели = матрица) |
| `friend_matrix` паттерн | Соцсети, рекомендации, PageRank |
