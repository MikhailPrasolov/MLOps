# Конспект: Главы 3–5

**Книга:** «Data Science с нуля» — Джоэл Грасс
**Источник:** второе издание (2019) — `scratch/visualization.py`, `scratch/linear_algebra.py`, `scratch/statistics.py`

> **Важно:** файл `Gras_Data_Science_Naytka_o_dannih_s_nylia_2017.pdf` — это **первое издание** (2017).
> Конспект ниже сверен с кодом **второго издания** из репозитория.
> Различия между изданиями описаны в конце файла.

---

## Глава 3. Визуализация данных

Matplotlib — де-факто стандарт визуализации в Python. В книге используется процедурный стиль через `pyplot`.

### 1. Линейный график (line chart)

```python
from matplotlib import pyplot as plt

years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

plt.plot(years, gdp, color='green', marker='o', linestyle='solid')
plt.title("Nominal GDP")
plt.ylabel("Billions of $")
plt.show()
```

### 2. Столбчатая диаграмма (bar chart)

```python
movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
num_oscars = [5, 11, 3, 8, 10]

plt.bar(range(len(movies)), num_oscars)
plt.title("My Favorite Movies")
plt.ylabel("# of Academy Awards")
plt.xticks(range(len(movies)), movies)   # подписи по центру столбцов
plt.show()
```

### 3. Гистограмма (histogram) через бакетизацию

```python
from collections import Counter

grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]

# Бакетизация: целые десятки, но 100 -> к 90-м
histogram = Counter(min(grade // 10 * 10, 90) for grade in grades)

plt.bar([x + 5 for x in histogram.keys()],   # сдвиг столбцов вправо
        histogram.values(),                  # высоты
        10,                                  # ширина
        edgecolor=(0, 0, 0))                 # чёрные грани

plt.axis([-5, 105, 0, 5])
plt.xticks([10 * i for i in range(11)])
plt.xlabel("Decile")
plt.ylabel("# of Students")
plt.title("Distribution of Exam 1 Grades")
plt.show()
```

### 4. ⚠️ Манипулятивная ось Y (антипаттерн)

```python
mentions = [500, 505]
years = [2017, 2018]

plt.bar(years, mentions, 0.8)
plt.xticks(years)
plt.ylabel("# of times I heard someone say 'data science'")
plt.ticklabel_format(useOffset=False)

# Обрезанная ось Y — разница 1% выглядит огромной
plt.axis([2016.5, 2018.5, 499, 506])
plt.title("Look at the 'Huge' Increase!")

# Правильный вариант — ось Y от 0
plt.axis([2016.5, 2018.5, 0, 550])
plt.title("Not So Huge Anymore")
```

### 5. Несколько серий на одном графике + легенда

```python
variance     = [1, 2, 4, 8, 16, 32, 64, 128, 256]
bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]
total_error  = [x + y for x, y in zip(variance, bias_squared)]
xs = [i for i, _ in enumerate(variance)]

plt.plot(xs, variance,     'g-',  label='variance')     # зелёная сплошная
plt.plot(xs, bias_squared, 'r-.', label='bias^2')       # красная штрихпунктир
plt.plot(xs, total_error,  'b:',  label='total error')  # синяя точечная

plt.legend(loc=9)        # loc=9 — «top center»
plt.xlabel("model complexity")
plt.xticks([])
plt.title("The Bias-Variance Tradeoff")
plt.show()
```

### 6. Диаграмма рассеяния (scatter plot) с подписями

```python
friends = [ 70,  65,  72,  63,  71,  64,  60,  64,  67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels  = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

plt.scatter(friends, minutes)

for label, friend_count, minute_count in zip(labels, friends, minutes):
    plt.annotate(label,
        xy=(friend_count, minute_count),
        xytext=(5, -5),
        textcoords='offset points')

plt.title("Daily Minutes vs. Number of Friends")
plt.xlabel("# of friends")
plt.ylabel("daily minutes spent on the site")
plt.show()
```

### 7. Сравнимость осей (критично!)

```python
test_1_grades = [ 99, 90, 85, 97, 80]
test_2_grades = [100, 85, 60, 90, 70]

plt.scatter(test_1_grades, test_2_grades)
plt.title("Axes Aren't Comparable")   # оси с разными диапазонами — искажение
plt.xlabel("test 1 grade")
plt.ylabel("test 2 grade")
plt.show()

# Правильный вариант: равные оси
plt.scatter(test_1_grades, test_2_grades)
plt.title("Axes Are Comparable")
plt.axis("equal")                     # ключевая строчка
plt.show()
```

---

## Глава 4. Линейная алгебра

Минимальный, но достаточный набор для понимания ML.

### 1. Вектор

```python
from typing import List

Vector = List[float]    # type alias — вектор это список float

height_weight_age = [70,  # inches,
                     170, # pounds,
                     40 ] # years

grades = [95, 80, 75, 62]
```

### 2. Операции над векторами

```python
def add(v: Vector, w: Vector) -> Vector:
    assert len(v) == len(w), "vectors must be the same length"
    return [v_i + w_i for v_i, w_i in zip(v, w)]

def subtract(v: Vector, w: Vector) -> Vector:
    assert len(v) == len(w), "vectors must be the same length"
    return [v_i - w_i for v_i, w_i in zip(v, w)]

def scalar_multiply(c: float, v: Vector) -> Vector:
    return [c * v_i for v_i in v]

def vector_sum(vectors: List[Vector]) -> Vector:
    assert vectors, "no vectors provided!"
    num_elements = len(vectors[0])
    assert all(len(v) == num_elements for v in vectors), "different sizes!"
    return [sum(vector[i] for vector in vectors)
            for i in range(num_elements)]

def vector_mean(vectors: List[Vector]) -> Vector:
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))
```

### 3. Скалярное произведение (dot product) — ГЛАВНАЯ операция

```python
def dot(v: Vector, w: Vector) -> float:
    assert len(v) == len(w), "vectors must be same length"
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

assert dot([1, 2, 3], [4, 5, 6]) == 32   # 1*4 + 2*5 + 3*6

def sum_of_squares(v: Vector) -> float:
    """v_1*v_1 + ... + v_n*v_n"""
    return dot(v, v)

assert sum_of_squares([1, 2, 3]) == 14
```

### 4. Магнитуда и расстояние

```python
import math

def magnitude(v: Vector) -> float:
    """||v|| = sqrt(v_1^2 + ... + v_n^2)"""
    return math.sqrt(sum_of_squares(v))

assert magnitude([3, 4]) == 5                # 3-4-5 треугольник

def distance(v: Vector, w: Vector) -> float:
    """Евклидово расстояние между v и w"""
    return magnitude(subtract(v, w))
```

### 5. Матрица

```python
Matrix = List[List[float]]

A = [[1, 2, 3],      # 2 строки × 3 столбца
     [4, 5, 6]]

B = [[1, 2],         # 3 строки × 2 столбца
     [3, 4],
     [5, 6]]

def shape(A: Matrix) -> tuple:
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols

assert shape([[1, 2, 3], [4, 5, 6]]) == (2, 3)

def get_row(A: Matrix, i: int) -> Vector:
    return A[i]

def get_column(A: Matrix, j: int) -> Vector:
    return [A_i[j] for A_i in A]
```

### 6. Конструкторы матриц

```python
from typing import Callable

def make_matrix(num_rows: int,
                num_cols: int,
                entry_fn: Callable[[int, int], float]) -> Matrix:
    """Матрица (i,j)-й элемент = entry_fn(i, j)"""
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]

def identity_matrix(n: int) -> Matrix:
    return make_matrix(n, n, lambda i, j: 1 if i == j else 0)

assert identity_matrix(5) == [[1,0,0,0,0],
                              [0,1,0,0,0],
                              [0,0,1,0,0],
                              [0,0,0,1,0],
                              [0,0,0,0,1]]
```

### 7. Практический кейс: матрица дружбы (взвешенный граф)

```python
#            user 0  1  2  3  4  5  6  7  8  9
friend_matrix = [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # user 0
                 [1, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # user 1
                 [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],  # user 2
                 [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],  # user 3
                 [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],  # user 4
                 [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],  # user 5
                 [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],  # user 6
                 [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],  # user 7
                 [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],  # user 8
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]  # user 9

# Проверка: 0 и 2 друзья
assert friend_matrix[0][2] == 1
# Список друзей пользователя 5
friends_of_five = [i for i, is_friend in enumerate(friend_matrix[5])
                   if is_friend]
```

---

## Глава 5. Статистика

### 1. Описательные статистики

```python
from typing import List
from collections import Counter
import matplotlib.pyplot as plt

num_friends = [100,49,41,40,25,...]   # 204 значения
assert len(num_friends) == 204

# Визуализация распределения
friend_counts = Counter(num_friends)
xs = range(101)
ys = [friend_counts[x] for x in xs]
plt.bar(xs, ys)
plt.axis([0, 101, 0, 25])
plt.title("Histogram of Friend Counts")
plt.show()
```

### 2. Меры центральной тенденции

```python
def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)

assert 7.3333 < mean(num_friends) < 7.3334

def _median_odd(xs: List[float]) -> float:
    return sorted(xs)[len(xs) // 2]

def _median_even(xs: List[float]) -> float:
    sorted_xs = sorted(xs)
    hi_midpoint = len(xs) // 2
    return (sorted_xs[hi_midpoint - 1] + sorted_xs[hi_midpoint]) / 2

def median(v: List[float]) -> float:
    return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)

assert median([1, 10, 2, 9, 5]) == 5
assert median([1, 9, 2, 10]) == (2 + 9) / 2
assert median(num_friends) == 6

def quantile(xs: List[float], p: float) -> float:
    """p-й перцентиль"""
    p_index = int(p * len(xs))
    return sorted(xs)[p_index]

assert quantile(num_friends, 0.10) == 1
assert quantile(num_friends, 0.25) == 3
assert quantile(num_friends, 0.75) == 9
assert quantile(num_friends, 0.90) == 13

def mode(x: List[float]) -> List[float]:
    """Список мод (их может быть несколько)"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]

assert set(mode(num_friends)) == {1, 6}    # 1 и 6 встречаются чаще всего
```

### 3. Меры разброса (dispersion)

```python
def data_range(xs: List[float]) -> float:
    return max(xs) - min(xs)

assert data_range(num_friends) == 99

# Сначала девиатация от среднего
def de_mean(xs: List[float]) -> List[float]:
    x_bar = mean(xs)
    return [x - x_bar for x in xs]

# Дисперсия: сумма квадратов девиаций / (n-1)
def variance(xs: List[float]) -> float:
    assert len(xs) >= 2, "variance requires at least two elements"
    n = len(xs)
    deviations = de_mean(xs)
    return sum_of_squares(deviations) / (n - 1)   # n-1 — выбор. исправленная

assert 81.54 < variance(num_friends) < 81.55

import math
def standard_deviation(xs: List[float]) -> float:
    return math.sqrt(variance(xs))

assert 9.02 < standard_deviation(num_friends) < 9.04

# Межквартильный размах: устойчив к выбросам
def interquartile_range(xs: List[float]) -> float:
    return quantile(xs, 0.75) - quantile(xs, 0.25)

assert interquartile_range(num_friends) == 6
```

### 4. Ковариация и корреляция

```python
def covariance(xs: List[float], ys: List[float]) -> float:
    """Мера совместной изменчивости xs и ys"""
    assert len(xs) == len(ys), "xs and ys must have same number of elements"
    return dot(de_mean(xs), de_mean(ys)) / (len(xs) - 1)

assert 22.42 < covariance(num_friends, daily_minutes) < 22.43

def correlation(xs: List[float], ys: List[float]) -> float:
    """Нормализованная ковариация: -1 ... +1"""
    stdev_x = standard_deviation(xs)
    stdev_y = standard_deviation(ys)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(xs, ys) / stdev_x / stdev_y
    else:
        return 0

assert 0.24 < correlation(num_friends, daily_minutes) < 0.25
```

### 5. ⚠️ Чувствительность корреляции к выбросам

```python
outlier = num_friends.index(100)    # у нас один юзер со 100 друзьями

num_friends_good = [x for i, x in enumerate(num_friends) if i != outlier]
daily_minutes_good = [x for i, x in enumerate(daily_minutes) if i != outlier]
daily_hours_good   = [dm / 60 for dm in daily_minutes_good]

# До удаления выброса: 0.24
# После удаления:        0.57
assert 0.57 < correlation(num_friends_good, daily_minutes_good) < 0.58
```

**Вывод:** корреляция может полностью поменять смысл из-за одного экстремального значения — нужна робастная визуализация (scatter) перед расчётом.

---

## Сверка изданий: 1-е (PDF) vs 2-е (репозиторий)

### Таблица различий для глав 3–5

| Аспект | 1-е издание (PDF 2017) | 2-е издание (репозиторий 2019) |
|--------|----------------------|-------------------------------|
| **Глава 3 (Viz)** | Базовый matplotlib, упор на простые `plot/bar` | Добавлены **scatter с подписями** через `plt.annotate`, **сравнимость осей** (`plt.axis("equal")`), акцент на **антипаттерны** (обрезанная ось Y) |
| **Глава 4 (LA)** | Только векторы и матрицы | Расширена: `vector_mean`, `identity_matrix`, `make_matrix` через `Callable`, матрица дружбы (взвешенный граф) |
| **Глава 5 (Stats)** | `mean`, `median`, `variance`, `correlation` | Добавлены: **`quantile`**, **`mode`** (возвращает список!), **`interquartile_range`**, улучшенный пример с **влиянием выброса** на корреляцию (0.24 → 0.57) |
| **Импорты** | `from scratch.linear_algebra import sum_of_squares, dot` — но модули первой версии лежат в `src/` | Те же импорты, но `scratch.linear_algebra` (новая структура) |
| **Визуальные данные** | Меньше примеров | Добавлен пример с **bias-variance tradeoff** (три серии на одном графике) |
| **Гистограммы** | Только `bar(Counter(...))` | Добавлен приём с **min(grade // 10 * 10, 90)** для корзинки «100 с 90-ми» |

### Что это значит для тебя

1. **Конспект выше актуален для 2-го издания.** В PDF (1-е) главы 3-5 короче и менее иллюстративны — меньше примеров с подписями точек, нет акцента на сравнимости осей.
2. **В 1-м издании** глава 5 (статистика) содержит базовые `mean/median/variance/correlation`, но **нет** `quantile`, `mode`, `interquartile_range` и примера с чувствительностью корреляции к выбросам — а это одни из самых практичных инструментов.
3. **Глава 4 в PDF** проще: меньше функций (нет `vector_mean`, `identity_matrix`), но концептуально тот же набор.
4. **Глава 3 в PDF** рисует те же графики, но без обсуждения **антипаттернов** визуализации (обрезанная ось Y, несравнимые оси).
5. **Практической разницы для базового понимания нет** — оба издания дают минимально необходимый набор. Рекомендую пользоваться **вторым изданием**.

---

## Практические выводы

| Что запомнить | Где пригодится |
|--------------|----------------|
| `plt.axis("equal")` — для сравнимых осей | Любой scatter двух метрик с одним масштабом |
| `plt.ticklabel_format(useOffset=False)` — отключает научную нотацию | Финансы, большие числа |
| **Никогда не обрезай ось Y с нулём** | Любая визуализация — это аргумент, а не декор |
| `Vector = List[float]` + `dot()` — база для ML | Нейросети, регрессия, рекомендации |
| Матрица `[[0,1,...],...]` — взвешенный граф | Соцсети, матрица схожести, корреляции |
| `mean` vs `median` — устойчивость к выбросам | Финансы, зарплаты, любые «длиннохвостые» данные |
| `variance` с `n-1` (а не `n`) | Выборочная дисперсия (Bessel's correction) |
| `correlation` ∈ `[-1, 1]`, но **чувствительна к выбросам** | A/B-тесты, поиск закономерностей |
| `quantile(p)` + `interquartile_range` | EDA, проверка распределения |
| `Counter` для гистограмм | Любой подсчёт частот |
| `mode()` возвращает **список** | Категориальные данные с несколькими пиками |
