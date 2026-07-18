# Глава 25. MapReduce

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/mapreduce.py`

> **Контекст:** глава вводит паттерн **MapReduce** как способ распараллелить любую агрегацию. Главная мысль: `mapper` производит `(key, value)`, `reducer` сворачивает все `value` для одного `key`. На одном Python-процессе — линейная имитация; в Hadoop/Spark — настоящий параллелизм.

## Ключевые концепции

- **`Mapper`** — `Callable[..., Iterable[KV]]` — генератор `(key, value)` пар
- **`Reducer`** — `Callable[[key, Iterable[values]], KV]` — агрегация по ключу
- **`map_reduce(inputs, mapper, reducer)`** — общий исполнитель; `defaultdict(list)` как «shuffle»
- **`values_reducer(fn)`** — фабрика reducer'ов: `sum_reducer`, `max_reducer`, `min_reducer`, `count_distinct_reducer`
- **`wc_mapper`** — `yield (word, 1)` для каждого слова документа
- **`wc_reducer`** — `yield (word, sum(counts))`
- **Matrix multiplication через MapReduce** — `A[i][j]` идёт во все `C[i][y]` с коэффициентом `B[j][y]`; reducer перемножает совпадающие индексы
- **Use cases** — word count, top-word per user, distinct likers per user, анализ статусов

## Код

```python
from collections import defaultdict
from typing import Callable, Iterable, Any, Tuple

KV = Tuple[Any, Any]
Mapper = Callable[..., Iterable[KV]]
Reducer = Callable[[Any, Iterable], KV]

def map_reduce(inputs, mapper, reducer):
    collector = defaultdict(list)
    for input in inputs:
        for key, value in mapper(input):
            collector[key].append(value)
    return [output for key, values in collector.items()
            for output in reducer(key, values)]

# Word count
def wc_mapper(document):
    for word in document.split():
        yield (word, 1)

def wc_reducer(word, counts):
    yield (word, sum(counts))

# Фабрика reducer'ов
def values_reducer(values_fn):
    def reduce(key, values):
        return (key, values_fn(values))
    return reduce

sum_reducer  = values_reducer(sum)
max_reducer  = values_reducer(max)
min_reducer  = values_reducer(min)
count_distinct_reducer = values_reducer(lambda v: len(set(v)))

# Matrix multiplication: C = A · B через MapReduce
def matrix_multiply_mapper(num_rows_a, num_cols_b):
    def mapper(entry):
        if entry.name == "A":
            for y in range(num_cols_b):
                yield ((entry.i, y), (entry.j, entry.value))
        else:  # B
            for x in range(num_rows_a):
                yield ((x, entry.j), (entry.i, entry.value))
    return mapper
```

## Связанные главы

- [[ch24-summary]] — предыдущая (SQL — альтернативный подход к агрегации)
- [[ch26-summary]] — следующая (этика данных)
- [[ch09-summary]] — работа с большими файлами до MapReduce
- [[ch21-summary]] — большие текстовые корпуса

## Краткие выводы

1. **MapReduce = shuffle + reduce** — параллелизм достигается на shuffle-фазе между машинами
2. **Reducer-фабрика** — `values_reducer(sum)` — избавляет от boilerplate
3. **Matrix multiply через MapReduce** — неэффективно для одной машины, но масштабируется на кластер

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| MapReduce паттерн | Spark, Hadoop, даже pandas `groupby().agg()` |
| `wc_mapper`/`wc_reducer` | ETL-пайплайны, логирование, подсчёт событий |
| Matrix multiply MR | Распределённые рекомендательные системы (ALS) |
| `count_distinct_reducer` | Метрики уникальных пользователей (DAU) |
