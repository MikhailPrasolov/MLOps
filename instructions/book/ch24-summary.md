# Глава 24. Базы данных и SQL

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/databases.py`

> **Контекст:** глава показывает, **что делает SQL «под капотом»** — реализует мини-движок реляционной БД на Python. После неё `SELECT/JOIN/GROUP BY/HAVING` перестают быть магией. На примере `users` и `user_interests` строятся все основные операции.

## Ключевые концепции

- **`Table`** — колонки + типы + список `Row` (dict'ов); типизация через `isinstance(value, type)` при `insert`
- **`select(keep_columns, additional_columns)`** — аналог `SELECT col, expr AS new_col FROM ...`
- **`where(predicate)`** — `WHERE`; предикат — `Callable[[Row], bool]`
- **`group_by(group_by_columns, aggregates, having)`** — `GROUP BY ... HAVING ...`; агрегаты через `__annotations__['return']`
- **`order_by(key_fn)`** — `ORDER BY ...`; минус в ключе = descending
- **`join(other, left_join=False)`** — INNER JOIN по общим колонкам; LEFT JOIN с None
- **`limit(n)`** — `LIMIT n`

## Код

```python
from typing import Callable, List, Dict, Any
from collections import defaultdict

Row = Dict[str, Any]
WhereClause = Callable[[Row], bool]
HavingClause = Callable[[List[Row]], bool]

class Table:
    def __init__(self, columns: List[str], types: List[type]):
        assert len(columns) == len(types)
        self.columns, self.types = columns, types
        self.rows: List[Row] = []

    def insert(self, values):
        if len(values) != len(self.types):
            raise ValueError(...)
        for v, t in zip(values, self.types):
            if not isinstance(v, t) and v is not None:
                raise TypeError(...)
        self.rows.append(dict(zip(self.columns, values)))

    def where(self, predicate=lambda r: True):
        t = Table(self.columns, self.types)
        for r in self.rows:
            if predicate(r):
                t.insert([r[c] for c in self.columns])
        return t

    def select(self, keep_columns=None, additional_columns=None):
        keep_columns = keep_columns or self.columns
        additional_columns = additional_columns or {}
        new_cols = keep_columns + list(additional_columns)
        new_t = Table(new_cols, [self.col2type(c) for c in keep_columns] +
                              [c.__annotations__['return']
                               for c in additional_columns.values()])
        for r in self.rows:
            new_t.insert([r[c] for c in keep_columns] +
                         [fn(r) for fn in additional_columns.values()])
        return new_t

    def group_by(self, group_cols, aggregates, having=lambda g: True):
        groups = defaultdict(list)
        for r in self.rows:
            key = tuple(r[c] for c in group_cols)
            groups[key].append(r)
        # ... формирует Table из key + agg_fn(group)

    def join(self, other, left_join=False):
        on = [c for c in self.columns if c in other.columns]
        add = [c for c in other.columns if c not in on]
        # ... для каждой строки self ищем совпадения в other

# Использование:
# users.where(lambda r: r['user_id'] > 1) \
#      .group_by([], {'sum_id': lambda rows: sum(r['user_id'] for r in rows)})
```

## Связанные главы

- [[ch23-summary]] — предыдущая
- [[ch25-summary]] — следующая (MapReduce как альтернатива БД для big data)
- [[ch09-summary]] — CSV/JSON как «до-БД» хранение

## Краткие выводы

1. **`__annotations__['return']`** — изящный способ узнать тип возврата функции без `inspect`
2. **`defaultdict(list)` для GROUP BY** — стандартный паттерн; ключ = tuple значений group-колонок
3. **JOIN = O(n·m)** в наивной реализации; реальные БД используют hash-индексы

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| Table.select/where/group_by | Понимание SQL — пишете запросы осознанно |
| `Callable[[Row], bool]` | Динамические фильтры в pandas (`df.query`) |
| LEFT JOIN с None | Подтягивание опциональных справочников |
| Aggregate через `__annotations__` | DSL поверх БД (pandas-стиль) |
