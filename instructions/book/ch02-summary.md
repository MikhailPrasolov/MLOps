# Глава 2. Краткий курс Python

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/crash_course_in_python.py`

> **Контекст:** не учебник Python, а плотная шпаргалка по идиомам, на которых строится вся книга — comprehensions, генераторы, `zip`/`enumerate`, `defaultdict`/`Counter`, `*args`/`**kwargs`. Если вы пишете на Python — многое будет знакомо, но автор местами даёт «правильный питонический» способ.

## Ключевые концепции

- **Comprehensions** — `[f(x) for x in xs]` и `{k: v for ...}`; «Pythonic way» вместо `map`/`filter`
- **Generators** — `yield` для ленивых последовательностей; экономят память на больших потоках
- **Структуры** — `list` (изменяемая), `tuple` (нет), `set` (уникальные), `dict` (маппинг)
- **`*args` / `**kwargs`** — произвольные позиционные и именованные аргументы; основа гибких API
- **`zip` / `enumerate`** — параллельная итерация по нескольким спискам / с индексом

## Код

```python
# 1. List/dict/set comprehensions
even_numbers = [x for x in range(10) if x % 2 == 0]
squares      = {x: x*x for x in range(5)}
unique_tags  = {tag for tag in tags}

# 2. Генератор (ленивый)
def lazy_range(n):
    i = 0
    while i < n:
        yield i
        i += 1

# 3. zip + enumerate — главный паттерн книги
for i, (xs_i, ys_i) in enumerate(zip(xs, ys)):
    ...

# 4. *args / **kwargs
def doubler(f):
    def g(x): return 2 * f(x)
    return g

def magic(*args, **kwargs):
    print("positional:", args)
    print("keyword:",   kwargs)

# 5. Counter / defaultdict
from collections import Counter, defaultdict
c = Counter([1, 1, 2, 3, 3, 3])         # Counter({3: 3, 1: 2, 2: 1})
d = defaultdict(int)                    # отсутствующий ключ → 0
```

## Связанные главы

- [[ch01-summary]] — предыдущая (использует эти идиомы)
- [[ch03-summary]] — следующая
- [[ch04-summary]] — векторы/матрицы через comprehensions

## Краткие выводы

1. **Предпочитайте comprehensions** — короче, быстрее и «правильнее», чем `map`/`filter`
2. **Генераторы для потоков данных** — никогда не материализуйте гигантские списки, если можно `yield`
3. **`Counter` + `defaultdict`** — две структуры, на которых держится весь «Data Science с нуля»

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| Comprehensions | Любая трансформация списков/словарей |
| `Counter` | Подсчёт частот, гистограммы, top-N |
| `defaultdict(list)` | Группировка, инвертированные индексы |
| Generators | Чтение CSV/JSON построчно, ETL-пайплайны |
| `*args`/`**kwargs` | Декораторы, обёртки, конфигурируемые функции |
