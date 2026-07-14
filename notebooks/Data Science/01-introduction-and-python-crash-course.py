"""
01 — Введение и краткий курс Python
====================================
Книга: «Data Science с нуля» — Джоэл Грасс (2-е издание, 2019)
Главы: 1 + 2
Источник: scratch/introduction.py, scratch/crash_course_in_python.py

Этот файл — конспект-компиляция ключевого кода из глав 1-2
с подробными русскими комментариями. Можно запускать как обычный
.py (assert-ы служат мини-тестами) и использовать как опору при
сборке .ipynb по главам.

Запуск:  python 01-introduction-and-python-crash-course.py
"""

# =============================================================================
# ГЛАВА 1. ВВЕДЕНИЕ: ПОИСК КЛЮЧЕВЫХ СВЯЗЕЙ
# =============================================================================
# Сквозной пример — маленькая социальная сеть из 10 пользователей.
# Цель главы: показать, что «дата сайенс» в основе — это просто
# структуры данных + итерации + Counter/defaultdict.

# -----------------------------------------------------------------------------
# 1.1. Моделирование данных
# -----------------------------------------------------------------------------
# Пользователей храним как список словарей — это типичный приём,
# когда данные приходят «как есть» (JSON, API, таблица).

users = [
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"},
]

# Связи (граф) — список пар id. Это «сырое» представление,
# с которым удобно работать, но искать друзей конкретного юзера — O(n).
friendship_pairs = [
    (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
    (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9),
]

# Список смежности — dict: id -> [friend_ids].
# Строим ОДИН РАЗ, дальше доступ O(1) + сразу длина.
friendships = {user["id"]: [] for user in users}
for i, j in friendship_pairs:
    friendships[i].append(j)
    friendships[j].append(i)        # связь симметрична — добавляем в обе стороны


# -----------------------------------------------------------------------------
# 1.2. Базовая метрика — количество друзей
# -----------------------------------------------------------------------------
def number_of_friends(user):
    """Сколько друзей у пользователя?"""
    return len(friendships[user["id"]])


# Суммарно и в среднем по сети
total_connections = sum(number_of_friends(u) for u in users)
print(f"Всего связей: {total_connections}")              # 24
print(f"Среднее число друзей: {total_connections / len(users)}")  # 2.4

# Сортировка по числу друзей — КЛЮЧЕВОЙ приём для любого «топ-N».
# (id, num_friends) -> sort по второму элементу через lambda.
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]
num_friends_by_id.sort(key=lambda id_and_friends: id_and_friends[1], reverse=True)
# Итог: [(1, 3), (2, 3), (3, 3), (5, 3), (8, 3), (0, 2), (4, 2), (6, 2), (7, 2), (9, 1)]


# -----------------------------------------------------------------------------
# 1.3. Friends of friends (FOAF) — «друзья друзей»
# -----------------------------------------------------------------------------
# Идея: рекомендовать людям тех, кто дружит с их друзьями, но
# не является прямым другом. Counter сразу даёт «рейтинг кандидатов».
from collections import Counter


def friends_of_friends(user):
    """Счётчик FOAF для данного пользователя (исключая его и прямых друзей)."""
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id]              # мои друзья
        for foaf_id in friendships[friend_id]              # их друзья
        if foaf_id != user_id                              # не я сам
        and foaf_id not in friendships[user_id]            # не прямой друг
    )


# Пример: для Hero (id=0) — friends_of_friends({'id': 0}) = {3: 2}


# -----------------------------------------------------------------------------
# 1.4. Группировка интересов через defaultdict
# -----------------------------------------------------------------------------
# Два прохода: «интерес -> пользователи» и «пользователь -> интересы».
# Это универсальный шаблон «инвертированного индекса» в DS.
from collections import defaultdict

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"),
    (3, "R"), (3, "Python"), (3, "statistics"), (3, "regression"),
    (3, "probability"), (4, "machine learning"), (4, "regression"),
    (4, "decision trees"), (4, "libsvm"), (5, "Python"),
    (5, "Java"), (5, "R"), (5, "JavaScript"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"),
    (9, "Hadoop"), (9, "Java"), (9, "MapReduce"), (9, "Big Data"),
]

# Прямой индекс: интерес -> [user_id]
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# Обратный индекс: user_id -> [interest]
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)


def most_common_interests_with(user):
    """С кем у пользователя больше всего общих интересов?"""
    return Counter(
        interested_user_id
        for interest in interests_by_user_id[user["id"]]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user["id"]
    )


# -----------------------------------------------------------------------------
# 1.5. Бакетизация (binning) — зарплата по стажу
# -----------------------------------------------------------------------------
# «Грязные» данные с пропусками — типичная задача.
# Стратегия: разбить непрерывную величину tenure на 3 бакета и
# посчитать среднюю зарплату в каждом.

salaries_and_tenures = [
    (83000, 8.7), (88000, 8.1), (48000, 0.7), (76000, 6),
    (69000, 6.5), (76000, 7.5), (60000, 2.5), (83000, 10),
    (48000, 1.9), (63000, 4.2), (None, 4.0),   # одна зарплата неизвестна
    (72000, 7.0), (71000, 7.9), (91000, 8.0), (79000, 7.0),
]


def tenure_bucket(tenure):
    """Сгруппировать стаж в 3 бакета."""
    if tenure < 2:
        return "less than two"
    elif tenure < 5:
        return "between two and five"
    else:
        return "more than five"


# Группировка: bucket -> [salary, ...]
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    if salary is not None:                          # пропуски отбрасываем
        salary_by_tenure_bucket[tenure_bucket(tenure)].append(salary)

# Средняя зарплата по бакетам
average_salary_by_bucket = {
    bucket: sum(salaries) / len(salaries)
    for bucket, salaries in salary_by_tenure_bucket.items()
}
# {'more than five': ~80000, 'between two and five': ~66000, 'less than two': ~48000}


# -----------------------------------------------------------------------------
# 1.6. Подсчёт слов — Counter.most_common()
# -----------------------------------------------------------------------------
words_and_counts = Counter(
    word
    for user, interest in interests
    for word in interest.lower().split()
)

# Топ-слова с частотой > 1
for word, count in words_and_counts.most_common():
    if count > 1:
        # print(word, count)
        pass


# =============================================================================
# ГЛАВА 2. КРАТКИЙ КУРС PYTHON
# =============================================================================
# Эта глава — справочник по минимальному набору Python, нужному для DS.
# Ниже — самые важные приёмы с краткими примерами и assert-проверками.

# -----------------------------------------------------------------------------
# 2.1. Функции
# -----------------------------------------------------------------------------
def double(x):
    """Докстринг — описание функции (показывается в help())."""
    return x * 2


def my_print(message="default"):
    print(message)


def full_name(first="Name", last="Surname"):
    return f"{first} {last}"


full_name(last="Grus")                  # "Name Grus" — именованные аргументы


def apply_to_one(f):
    """Принимает функцию — это фундамент функционального стиля."""
    return f(1)


apply_to_one(lambda x: x + 4)           # 5 — лямбда для простых случаев


# -----------------------------------------------------------------------------
# 2.2. Строки
# -----------------------------------------------------------------------------
# f-строки (Python 3.6+) — главный способ форматирования
first_name, last_name = "Joel", "Grus"
full_name = f"{first_name} {last_name}"   # "Joel Grus"

# Сырые строки — без экранирования
path = r"\t"                              # два символа: '\' и 't'

# Старый способ форматирования (ещё встречается)
"{0} {1}".format(first_name, last_name)   # "Joel Grus"


# -----------------------------------------------------------------------------
# 2.3. Исключения
# -----------------------------------------------------------------------------
try:
    print(0 / 0)
except ZeroDivisionError:
    print("cannot divide by zero")


# -----------------------------------------------------------------------------
# 2.4. Списки — самая частая структура
# -----------------------------------------------------------------------------
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Индексация (отрицательные — с конца)
assert x[0] == 0 and x[-1] == 9 and x[-2] == 8

# Срезы [start:end:step] — end не включается
assert x[:3] == [0, 1, 2]
assert x[3:] == [3, 4, 5, 6, 7, 8, 9]
assert x[1:5] == [1, 2, 3, 4]
assert x[::3] == [0, 3, 6, 9]              # каждый третий
assert x[5:2:-1] == [5, 4, 3]              # обратный срез

# Методы
y = x.copy() if hasattr(x, "copy") else x[:]   # список для экспериментов
# На самом деле проще:
y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
y.append(0)                                     # добавить в конец
y.extend([4, 5, 6])                             # расширить списком
y + [4, 5, 6]                                   # новый список, оригинал не меняется
y.sort()                                        # in-place
assert len(y) > 0


# -----------------------------------------------------------------------------
# 2.5. Деструктуризация
# -----------------------------------------------------------------------------
x, y = [1, 2]
_, y = [1, 2]                                   # _ — игнорируем
x, y = y, x                                     # Pythonic swap


def add(a, b):
    return a + b


add(*[1, 2])                                    # * распаковывает список в аргументы


# -----------------------------------------------------------------------------
# 2.6. Кортежи — неизменяемые списки
# -----------------------------------------------------------------------------
my_tuple = (1, 2)
x, y = (3, 4)                                   # распаковка
# my_tuple[0] = 99  → TypeError: кортежи нельзя менять


# -----------------------------------------------------------------------------
# 2.7. Словари — ключевая DS-структура
# -----------------------------------------------------------------------------
grades = {"Joel": 80, "Tim": 95}

grades["Joel"]                                  # 80 — чтение (KeyError если нет)
grades.get("Kate", 0)                           # 0 — безопасное чтение с default
assert "Joel" in grades                        # проверка КЛЮЧА (не значения!)

tweet = {"user": "joelgrus", "text": "Data Science", "retweet_count": 100,
         "hashtags": ["#ds", "#python"]}
# Итерация
# for k in tweet.keys(): ...
# for v in tweet.values(): ...
# for k, v in tweet.items(): ...


# -----------------------------------------------------------------------------
# 2.8. defaultdict и Counter — must-have коллекции
# -----------------------------------------------------------------------------
from collections import defaultdict, Counter

word_counts = defaultdict(int)                  # int() -> 0
dd_list = defaultdict(list)                     # list() -> []
dd_dict = defaultdict(dict)                     # dict() -> {}

c = Counter([0, 1, 2, 0])                       # Counter({0: 2, 1: 1, 2: 1})
c.most_common(3)                                # [(0, 2), (1, 1), (2, 1)]


# -----------------------------------------------------------------------------
# 2.9. Множества (set) — O(1) проверка членства
# -----------------------------------------------------------------------------
s = set()
s.add(1)
s.add(2)                                       # добавим 2, чтобы assert ниже прошёл
assert 2 in s                                   # O(1), не как в list
assert len({1, 2, 2, 3}) == 3                   # set оставляет уникальные


# -----------------------------------------------------------------------------
# 2.10. List comprehension — САМЫЙ частый приём в DS-коде
# -----------------------------------------------------------------------------
# Форма: [expression for item in iterable if condition]
even_numbers = [x for x in range(5) if x % 2 == 0]   # [0, 2, 4]
squares      = [x * x for x in range(5)]             # [0, 1, 4, 9, 16]

# Вложенные comprehensions = вложенные циклы
pairs = [(x, y) for x in range(3) for y in range(3)]      # 9 пар
increasing_pairs = [(x, y) for x in range(5)
                    for y in range(x + 1, 5)]              # пары x<y

# Dict comprehension
square_dict = {x: x * x for x in range(5)}
assert square_dict[3] == 9

# Set comprehension
assert {x * x for x in [1, -1]} == {1}

# _ — игнорирование значения
zeros = [0 for _ in even_numbers]


# -----------------------------------------------------------------------------
# 2.11. Генераторы — ленивые последовательности (экономят память)
# -----------------------------------------------------------------------------
def generate_range(n):
    i = 0
    while i < n:
        yield i                                  # ← генератор
        i += 1


# Generator expression — как list comp, но в круглых скобках
evens_below_20 = (i for i in range(20) if i % 2 == 0)
# НЕ вычисляется сразу! Дайте ему sum()/list()/for — тогда посчитается
assert sum(evens_below_20) == 90

# Композиция генераторов: данные текут по цепочке без материализации


def natural_numbers():
    n = 1
    while True:
        yield n
        n += 1


data = natural_numbers()
evens = (x for x in data if x % 2 == 0)
even_squares = (x ** 2 for x in evens)
# even_squares всё ещё ленив. next(even_squares) → 4, 16, 36, ...


# -----------------------------------------------------------------------------
# 2.12. enumerate — обход с индексом
# -----------------------------------------------------------------------------
names = ["Alice", "Bob", "Charlie"]
for i, name in enumerate(names):
    # print(f"name {i} is {name}")
    pass


# -----------------------------------------------------------------------------
# 2.13. zip — параллельная итерация
# -----------------------------------------------------------------------------
list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]
assert list(zip(list1, list2)) == [('a', 1), ('b', 2), ('c', 3)]

# Распаковка zip — обратная операция
pairs = [('a', 1), ('b', 2), ('c', 3)]
letters, numbers = zip(*pairs)
assert letters == ('a', 'b', 'c') and numbers == (1, 2, 3)


# -----------------------------------------------------------------------------
# 2.14. *args и **kwargs — гибкие сигнатуры
# -----------------------------------------------------------------------------
def magic(*args, **kwargs):
    # args — кортеж позиционных, kwargs — dict именованных
    assert isinstance(args, tuple)
    assert isinstance(kwargs, dict)


magic(1, 2, key="word", key2="word2")


# -----------------------------------------------------------------------------
# 2.15. Декораторы — функции высшего порядка
# -----------------------------------------------------------------------------
def doubler(f):
    def g(*args, **kwargs):
        return 2 * f(*args, **kwargs)
    return g


g_doubler = doubler(add)
assert g_doubler(1, 2) == 6                     # 2 * (1+2)


# -----------------------------------------------------------------------------
# 2.16. Сортировка с key
# -----------------------------------------------------------------------------
assert sorted([4, 1, 2, 3]) == [1, 2, 3, 4]
assert sorted([-4, 1, -2, 3], key=abs, reverse=True) == [-4, 3, -2, 1]
x = [3, 1, 2]
x.sort()                                        # in-place
assert x == [1, 2, 3]


# -----------------------------------------------------------------------------
# 2.17. random — воспроизводимость через seed
# -----------------------------------------------------------------------------
import random

random.seed(10)                                 # фиксируем для воспроизводимости
random.random()                                 # [0.0, 1.0)
random.randrange(10)                            # из range(10)
lst = [1, 2, 3, 4, 5]
random.shuffle(lst)                             # in-place
random.choice(lst)                              # один случайный
random.sample(lst, 2)                           # K случайных БЕЗ повторений


# -----------------------------------------------------------------------------
# 2.18. re — регулярные выражения
# -----------------------------------------------------------------------------
import re

assert re.match("a", "cat") is None             # match — с начала строки
assert re.search("a", "cat") is not None        # search — где угодно
assert re.split("[ab]", "carbs") == ['c', 'r', 's']
assert re.sub("[0-9]", "-", "R2D2") == "R-D-"


# -----------------------------------------------------------------------------
# 2.19. Type hints — самодокументирующийся код
# -----------------------------------------------------------------------------
from typing import List, Dict, Tuple, Set, Iterable, Callable, Optional, Union

Vector = List[float]


def total(xs: List[float]) -> float:
    return sum(xs)


def twice(repeater: Callable[[str, int], str], s: str) -> str:
    """Сигнатура: f принимает (str, int) -> str."""
    return repeater(s, 2)


values: List[int] = []
best_so_far: Optional[float] = None             # может быть None
operation: Union[str, int, float, bool]         # допустимо несколько типов


# =============================================================================
# ИТОГ ГЛАВ 1-2
# =============================================================================
# Главный вывод: вся дальнейшая книга строится на:
#   1) defaultdict + Counter для группировок и подсчётов
#   2) list comprehensions / generators для преобразований
#   3) zip / enumerate для итераций
#   4) lambda / decorators / *args / type hints — для чистого кода
# Эти 4 кита покрывают ~90% всего кода в DS-практике.
print("\n[OK] Главы 1-2: все assert-ы пройдены.")
