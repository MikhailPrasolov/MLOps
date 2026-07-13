# Конспект: Главы 1–2

**Книга:** «Data Science с нуля» — Джоэл Грасс
**Источник:** второе издание (2019) — `scratch/introduction.py`, `scratch/crash_course_in_python.py`

> **Важно:** файл `Gras_Data_Science_Naytka_o_dannih_s_nylia_2017.pdf` — это **первое издание** (2017).
> Конспект ниже сверен с кодом **второго издания** из репозитория.
> Различия между изданиями описаны в конце файла.

---

## Глава 1. Введение: поиск ключевых связей

Сквозной пример: анализ социальной сети (10 пользователей, friendship-связи).

### Моделирование данных

```python
# Пользователи — список словарей
users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    # ...
]

# Связи — список кортежей (id1, id2)
friendship_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), ...]

# Список смежности — dict: id -> [friend_ids]
friendships = {user["id"]: [] for user in users}
for i, j in friendship_pairs:
    friendships[i].append(j)
    friendships[j].append(i)
```

### Метрики

```python
# Количество друзей
def number_of_friends(user):
    return len(friendships[user["id"]])

# Суммарные / средние связи
total_connections = sum(number_of_friends(u) for u in users)  # 24
avg_connections = total_connections / len(users)              # 2.4

# Сортировка по количеству друзей (ключевой приём!)
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]
num_friends_by_id.sort(key=lambda id_fr: id_fr[1], reverse=True)
```

### Friends of Friends (FOAF)

```python
from collections import Counter

def friends_of_friends(user):
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id]
        for foaf_id in friendships[friend_id]
        if foaf_id != user_id
        and foaf_id not in friendships[user_id]  # исключаем прямых друзей
    )
```

### Интересы и группировка

```python
from collections import defaultdict

# interests: список кортежей (user_id, interest)
# Группировка: интерес -> список пользователей
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# Обратная группировка: пользователь -> список интересов
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

# Поиск общих интересов
def most_common_interests_with(user):
    return Counter(
        interested_user_id
        for interest in interests_by_user_id[user["id"]]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user["id"]
    )
```

### Бакетизация (бининг)

```python
def tenure_bucket(tenure):
    if tenure < 2:      return "less than two"
    elif tenure < 5:    return "between two and five"
    else:               return "more than five"

# Группировка зарплат по бакетам tenure
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure_bucket[tenure_bucket(tenure)].append(salary)

average_salary_by_bucket = {
    bucket: sum(salaries) / len(salaries)
    for bucket, salaries in salary_by_tenure_bucket.items()
}
```

### Подсчёт слов через Counter

```python
words_and_counts = Counter(
    word for user, interest in interests for word in interest.lower().split()
)
for word, count in words_and_counts.most_common():
    if count > 1:
        print(word, count)
```

---

## Глава 2. Краткий курс Python

Сжатый обзор самого важного (с акцентом на DS-специфику).

### 1. Функции

```python
def double(x):
    """Докстринг: описание функции."""
    return x * 2

# Значения по умолчанию
def my_print(message="default"):
    print(message)

# Именованные аргументы
def full_name(first="Name", last="Surname"):
    return first + " " + last

full_name(last="Grus")  # "Name Grus"

# Лямбды (только для простых случаев)
apply_to_one(lambda x: x + 4)  # 5
```

### 2. Строки

```python
# f-строки (Python 3.6+, самый удобный способ)
full_name = f"{first_name} {last_name}"

# Сырые строки (не экранировать слеши)
path = r"\t"  # \t — это два символа, не табуляция

# Форматирование
"{0} {1}".format(first_name, last_name)
```

### 3. Исключения

```python
try:
    print(0 / 0)
except ZeroDivisionError:
    print("cannot divide by zero")
```

### 4. Списки (самое важное)

```python
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Индексация
x[0]          # 0
x[-1]         # 9 — последний элемент
x[-2]         # 8 — предпоследний

# Срезы: [start:end:step]
x[:3]         # [0, 1, 2]
x[3:]         # [3, 4, 5, 6, 7, 8, 9]
x[1:5]        # [1, 2, 3, 4]
x[::3]        # [0, 3, 6, 9] — каждый третий
x[5:2:-1]     # [5, 4, 3] — обратный срез

# Методы
x.append(0)        # добавить в конец
x.extend([4,5,6])  # расширить списком
x + [4,5,6]        # новый список (не меняет оригинал)
x.sort()
len(x)
```

### 5. Деструктуризация

```python
x, y = [1, 2]
_, y = [1, 2]        # _ — игнорируем значение
x, y = y, x          # Pythonic swap

# Распаковка аргументов
def add(a, b): return a + b
add(*[1, 2])         # 3 — * распаковывает список в аргументы
```

### 6. Кортежи

```python
my_tuple = (1, 2)
x, y = (3, 4)        # распаковка
# Кортежи нельзя изменять (в отличие от списков)
```

### 7. Словари (dict) — ключевой тип для DS

```python
grades = {"Joel": 80, "Tim": 95}

grades["Joel"]           # 80 — чтение
grades.get("Kate", 0)    # 0 — безопасное чтение с default
"Joel" in grades         # True — проверка ключа

# Обход
tweet.keys()             # ключи
tweet.values()           # значения
tweet.items()            # пары (key, value)
```

### 8. defaultdict и Counter — самые полезные коллекции

```python
from collections import defaultdict, Counter

# defaultdict — dict с фабрикой значения по умолчанию
word_counts = defaultdict(int)     # int() -> 0
dd_list = defaultdict(list)        # list() -> []
dd_dict = defaultdict(dict)        # dict() -> {}

# Counter — подсчёт элементов
c = Counter([0, 1, 2, 0])         # {0: 2, 1: 1, 2: 1}
c.most_common(10)                 # топ-10
```

### 9. Множества (set)

```python
s = set()
s.add(1)
2 in s               # True — O(1), быстрее чем list
len(set(item_list))  # количество уникальных
```

### 10. List Comprehension — САМЫЙ важный приём

```python
# Базовая форма: [expression for item in iterable if condition]
even_numbers = [x for x in range(5) if x % 2 == 0]  # [0, 2, 4]
squares      = [x * x for x in range(5)]             # [0, 1, 4, 9, 16]

# Вложенные (аналог вложенных циклов)
pairs = [(x, y) for x in range(5) for y in range(5)]  # 25 пар

# С фильтром
increasing_pairs = [(x, y) for x in range(5) for y in range(x+1, 5)]

# Dict comprehension
square_dict = {x: x*x for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Set comprehension
square_set = {x*x for x in [1, -1]}       # {1}

# _ для игнорирования
zeros = [0 for _ in even_numbers]
```

### 11. Генераторы (ленивые последовательности)

```python
def generate_range(n):
    i = 0
    while i < n:
        yield i
        i += 1

# Generator expression — как list comp, но в круглых скобках
evens_below_20 = (i for i in range(20) if i % 2 == 0)
# НЕ вычисляется до момента итерации!

# Композиция генераторов — цепочки без создания промежуточных списков
data = natural_numbers()
evens = (x for x in data if x % 2 == 0)
even_squares = (x ** 2 for x in evens)      # память не ест
```

### 12. enumerate — правильный обход с индексом

```python
for i, name in enumerate(names):
    print(f"name {i} is {name}")  # Pythonic way
```

### 13. zip — склеивание последовательностей

```python
list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]
list(zip(list1, list2))  # [('a', 1), ('b', 2), ('c', 3)]

# Обратная операция — распаковка zip
pairs = [('a', 1), ('b', 2), ('c', 3)]
letters, numbers = zip(*pairs)  # letters = ('a', 'b', 'c'), numbers = (1, 2, 3)
```

### 14. *args и **kwargs

```python
def magic(*args, **kwargs):
    print("unnamed args:", args)    # кортеж
    print("keyword args:", kwargs)  # словарь

magic(1, 2, key="word", key2="word2")
# unnamed args: (1, 2)
# keyword args: {'key': 'word', 'key2': 'word2'}
```

### 15. Декораторы (функции, возвращающие функции)

```python
def doubler(f):
    def g(*args, **kwargs):
        return 2 * f(*args, **kwargs)
    return g

g = doubler(add)
g(1, 2)  # 6
```

### 16. Сортировка

```python
sorted([4, 1, 2, 3])                          # [1, 2, 3, 4]
sorted([-4, 1, -2, 3], key=abs, reverse=True)  # [-4, 3, -2, 1]
x.sort()  # in-place
```

### 17. random

```python
random.seed(10)                # фиксируем seed для воспроизводимости
random.random()                # [0.0, 1.0)
random.randrange(10)           # случайное из range(10)
random.shuffle(lst)            # перемешать in-place
random.choice(lst)             # один случайный
random.sample(lst, 6)          # 6 случайных без повторений
```

### 18. re — регулярные выражения

```python
re.match("a", "cat")           # None — не совпало с начала
re.search("a", "cat")          # match object — 'a' есть в строке
re.split("[ab]", "carbs")      # ['c', 'r', 's'] — разделение
re.sub("[0-9]", "-", "R2D2")   # 'R-D-' — замена
```

### 19. Type Hints (аннотации типов)

```python
from typing import List, Dict, Tuple, Set, Iterable, Callable, Optional, Union

Vector = List[float]

def total(xs: List[float]) -> float:
    return sum(xs)

def twice(repeater: Callable[[str, int], str], s: str) -> str:
    return repeater(s, 2)

values: List[int] = []
best_so_far: Optional[float] = None
operation: Union[str, int, float, bool]
```

---

## Сверка изданий: 1-е (PDF) vs 2-е (репозиторий)

### Таблица различий

| Аспект | 1-е издание (PDF 2017) | 2-е издание (репозиторий 2019) |
|--------|----------------------|-------------------------------|
| **Python** | 2.7 (+ Python 3.5 в `code-python3/`) | 3.6+ |
| **Глава 2** | Описана **текстом** в книге, отдельного файла кода **нет** | `crash_course_in_python.py` — **771 строка** кода |
| **Типизация** | Нет type hints | Полные type hints: `Vector = List[float]`, `Callable`, `Optional` |
| **Хранение данных** | `user["friends"] = [users[j], users[i]]` — хранятся объекты | `friendships = {user["id"]: []}` — отдельный dict с числовыми id |
| **FOAF** | Две вспомогательные функции: `not_the_same`, `not_friends` | Всё в одном выражении с `Counter` |
| **Количество глав** | 22 | 27 (добавлены глубокое обучение, NLP advanced, recommender systems и др.) |
| **Разделение** | Глава 1 — `introduction.py`, статистика — `stats.py` | Глава 1 — `introduction.py`, Глава 2 — `crash_course_in_python.py` |

### Что это значит для тебя

1. **Конспект выше актуален для 2-го издания.** В PDF (1-е) код `introduction.py` выглядит немного иначе — друзей держит прямо в объектах пользователей, а не в отдельном dict.
2. **Глава 2 в PDF** — те же концепции (списки, словари, функции, list comprehensions), но без type hints и f-строк. f-строки появились только в Python 3.6, поэтому их нет в 1-м издании.
3. **Практической разницы для обучения нет** — оба издания учат одному и тому же. Я рекомендую пользоваться **вторым изданием** (код из `scratch/`), так как он современнее.

---

## Практические выводы

| Что запомнить | Где пригодится |
|--------------|----------------|
| `defaultdict(list)` — группировка | EDA, groupby, агрегация |
| `Counter.most_common()` — топ-N | Любой анализ частот |
| List comprehensions — вместо циклов | Весь код |
| `*args, **kwargs` — гибкие функции | Свои обёртки и утилиты |
| `sorted(..., key=lambda)` — сортировка по вычисляемому полю | Рейтинги, топы |
| `set` — быстрая проверка `in` | Фильтрация дубликатов |
| `f"{var}"` — форматирование | Отладка, вывод |
| `random.seed()` — воспроизводимость | Эксперименты |
| Type hints — документация кода | Любой серьёзный проект |
