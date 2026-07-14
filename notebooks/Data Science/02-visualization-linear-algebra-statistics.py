"""
02 — Визуализация, линейная алгебра, статистика
================================================
Книга: «Data Science с нуля» — Джоэл Грасс (2-е издание, 2019)
Главы: 3 + 4 + 5
Источник: scratch/visualization.py, scratch/linear_algebra.py, scratch/statistics.py

Этот файл — конспект-компиляция ключевого кода из глав 3-5
с подробными русскими комментариями. Линейная алгебра (глава 4)
вынесена сюда локально, чтобы файл был самодостаточным — в самой
книге `statistics.py` импортирует её из `scratch.linear_algebra`.

Запуск:  python 02-visualization-linear-algebra-statistics.py
        (графики сохраняются в ../Data Science/_figures/)

Примечание: plt.show() заменён на plt.savefig() + plt.gca().clear()
как в оригинальном коде книги — чтобы скрипт можно было прогнать
в headless-режиме и не блокироваться на окне matplotlib.
"""

import math
import os
from collections import Counter
from typing import Callable, List, Tuple

import matplotlib

# 'Agg' — неинтерактивный backend: скрипт работает без дисплея.
# Если открываете в Jupyter — закомментируйте строку ниже.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Куда сохранять картинки
# В ноутбуке __file__ не определён, поэтому используем getcwd().
# В .py-скрипте os.path.dirname(__file__) даст папку скрипта.
try:
    _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _SCRIPT_DIR = os.getcwd()
_FIG_DIR = os.path.join(_SCRIPT_DIR, "_figures")
os.makedirs(_FIG_DIR, exist_ok=True)


# =============================================================================
# ГЛАВА 3. ВИЗУАЛИЗАЦИЯ ДАННЫХ
# =============================================================================
# Matplotlib в процедурном стиле (через pyplot) — стандарт в DS.
# Правила из главы:
#   • линейный график — для временных рядов и непрерывных трендов
#   • bar — для сравнения дискретных категорий
#   • гистограмма — для распределения ОДНОЙ числовой переменной
#   • scatter — для поиска связей между ДВУМЯ переменными
#   • ⚠️ НЕ обрезай ось Y с нулём — это обман
#   • ⚠️ СРАВНИВАЙ оси (plt.axis("equal")), если шкалы должны быть одинаковыми

# -----------------------------------------------------------------------------
# 3.1. Линейный график (line chart) — ВВП по годам
# -----------------------------------------------------------------------------
# Простейший кейс: годы по X, значение по Y. Сразу видно тренд.
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

plt.plot(years, gdp, color="green", marker="o", linestyle="solid")
plt.title("Nominal GDP")
plt.ylabel("Billions of $")
plt.savefig(os.path.join(_FIG_DIR, "viz_gdp.png"))
plt.gca().clear()


# -----------------------------------------------------------------------------
# 3.2. Столбчатая диаграмма (bar chart) — Оскары за фильмы
# -----------------------------------------------------------------------------
# Когда категории дискретны и их немного — bar нагляднее линии.
movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
num_oscars = [5, 11, 3, 8, 10]

# По X — индексы [0, 1, 2, 3, 4], высоты — из num_oscars
plt.bar(range(len(movies)), num_oscars)
plt.title("My Favorite Movies")
plt.ylabel("# of Academy Awards")
# Подписи по ЦЕНТРАМ столбцов (не по индексам!)
plt.xticks(range(len(movies)), movies)
plt.savefig(os.path.join(_FIG_DIR, "viz_movies.png"))
plt.gca().clear()


# -----------------------------------------------------------------------------
# 3.3. Гистограмма через бакетизацию — оценки за экзамен
# -----------------------------------------------------------------------------
# Настоящая гистограмма в matplotlib — plt.hist(). Здесь автор показывает
# «ручную» бакетизацию, чтобы подчеркнуть логику.
grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]

# Бакетизация по декадам, но 100 -> к баке «90-100»
histogram = Counter(min(grade // 10 * 10, 90) for grade in grades)

plt.bar(
    [x + 5 for x in histogram.keys()],     # сдвиг столбцов вправо на полбакета
    histogram.values(),                    # высоты
    10,                                    # ширина столбца
    edgecolor=(0, 0, 0),                   # чёрные границы
)
plt.axis([-5, 105, 0, 5])
plt.xticks([10 * i for i in range(11)])
plt.xlabel("Decile")
plt.ylabel("# of Students")
plt.title("Distribution of Exam 1 Grades")
plt.savefig(os.path.join(_FIG_DIR, "viz_grades.png"))
plt.gca().clear()


# -----------------------------------------------------------------------------
# 3.4. ⚠️ Манипулятивная ось Y (антипаттерн!)
# -----------------------------------------------------------------------------
# 500 → 505 за год = +1%. Без обрезки оси Y — это почти плоский график.
# С обрезкой [499, 506] — выглядит как «удвоение». Это манипуляция.
mentions = [500, 505]
years_short = [2017, 2018]

# Антипаттерн
plt.bar(years_short, mentions, 0.8)
plt.xticks(years_short)
plt.ylabel("# of times I heard someone say 'data science'")
plt.ticklabel_format(useOffset=False)      # отключает научную нотацию (2.013e3)
plt.axis([2016.5, 2018.5, 499, 506])        # ⚠️ обрезанная ось Y
plt.title("Look at the 'Huge' Increase!")
plt.savefig(os.path.join(_FIG_DIR, "viz_misleading_y_axis.png"))
plt.gca().clear()

# Корректный вариант — ось Y начинается с 0
plt.bar(years_short, mentions, 0.8)
plt.xticks(years_short)
plt.ylabel("# of times I heard someone say 'data science'")
plt.ticklabel_format(useOffset=False)
plt.axis([2016.5, 2018.5, 0, 550])           # ✅
plt.title("Not So Huge Anymore")
plt.savefig(os.path.join(_FIG_DIR, "viz_non_misleading_y_axis.png"))
plt.gca().clear()


# -----------------------------------------------------------------------------
# 3.5. Несколько серий + легенда — bias-variance tradeoff
# -----------------------------------------------------------------------------
# Идея: на одних осях показать 3 связанных величины.
# Форматы линий: 'g-' (зелёная сплошная), 'r-.' (красная штрихпунктир),
# 'b:' (синяя точечная). Метки через label=, легенда бесплатно.
variance     = [1, 2, 4, 8, 16, 32, 64, 128, 256]
bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]
total_error  = [x + y for x, y in zip(variance, bias_squared)]
xs = [i for i, _ in enumerate(variance)]

plt.plot(xs, variance,     "g-",  label="variance")
plt.plot(xs, bias_squared, "r-.", label="bias^2")
plt.plot(xs, total_error,  "b:",  label="total error")
plt.legend(loc=9)                            # 9 = "top center"
plt.xlabel("model complexity")
plt.xticks([])
plt.title("The Bias-Variance Tradeoff")
plt.savefig(os.path.join(_FIG_DIR, "viz_line_chart.png"))
plt.gca().clear()


# -----------------------------------------------------------------------------
# 3.6. Диаграмма рассеяния (scatter) с подписями точек
# -----------------------------------------------------------------------------
# Данные: друзья vs минуты на сайте, плюс буквенные метки a..i.
# plt.annotate ставит текст со смещением от точки.
friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels  = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

plt.scatter(friends, minutes)
for label, friend_count, minute_count in zip(labels, friends, minutes):
    plt.annotate(
        label,
        xy=(friend_count, minute_count),     # точка привязки
        xytext=(5, -5),                      # смещение текста
        textcoords="offset points",
    )
plt.title("Daily Minutes vs. Number of Friends")
plt.xlabel("# of friends")
plt.ylabel("daily minutes spent on the site")
plt.savefig(os.path.join(_FIG_DIR, "viz_scatterplot.png"))
plt.gca().clear()


# -----------------------------------------------------------------------------
# 3.7. Сравнимость осей (критично для scatter)
# -----------------------------------------------------------------------------
# Если оси НЕ сравнимы (разные шкалы) — корреляция выглядит обманчиво.
# plt.axis("equal") делает единичный отрезок по X и Y одинаковым.
test_1_grades = [99, 90, 85, 97, 80]
test_2_grades = [100, 85, 60, 90, 70]

# Несравнимые оси — искажение восприятия
plt.scatter(test_1_grades, test_2_grades)
plt.title("Axes Aren't Comparable")
plt.xlabel("test 1 grade")
plt.ylabel("test 2 grade")
plt.savefig(os.path.join(_FIG_DIR, "viz_scatterplot_axes_not_comparable.png"))
plt.gca().clear()

# Сравнимые оси — корректное восприятие
plt.scatter(test_1_grades, test_2_grades)
plt.title("Axes Are Comparable")
plt.axis("equal")                             # ✅ ключевая строка
plt.xlabel("test 1 grade")
plt.ylabel("test 2 grade")
plt.savefig(os.path.join(_FIG_DIR, "viz_scatterplot_axes_comparable.png"))
plt.gca().clear()


# =============================================================================
# ГЛАВА 4. ЛИНЕЙНАЯ АЛГЕБРА
# =============================================================================
# Минимальный набор для ML: вектор, матрица, dot product, distance.
# В книге этот код лежит в scratch/linear_algebra.py и переиспользуется
# в следующих главах (statistics, gradient_descent, neural_networks, ...).
# Здесь дублируем локально — для самодостаточности .py-файла.

Vector = List[float]

# -----------------------------------------------------------------------------
# 4.1. Вектор и примеры
# -----------------------------------------------------------------------------
# Вектор — упорядоченный список чисел фиксированной длины.
# Пример: один пользователь = точка в 3-мерном пространстве.
height_weight_age = [70, 170, 40]                # дюймы, фунты, годы
grades = [95, 80, 75, 62]                         # 4 экзамена

# -----------------------------------------------------------------------------
# 4.2. Поэлементные операции: add / subtract / scalar_multiply
# -----------------------------------------------------------------------------
def add(v: Vector, w: Vector) -> Vector:
    """Поэлементное сложение. Длины должны совпадать."""
    assert len(v) == len(w), "vectors must be the same length"
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def subtract(v: Vector, w: Vector) -> Vector:
    """Поэлементное вычитание."""
    assert len(v) == len(w), "vectors must be the same length"
    return [v_i - w_i for v_i, w_i in zip(v, w)]


def scalar_multiply(c: float, v: Vector) -> Vector:
    """Умножение вектора на скаляр."""
    return [c * v_i for v_i in v]


assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]
assert subtract([5, 7, 9], [4, 5, 6]) == [1, 2, 3]
assert scalar_multiply(2, [1, 2, 3]) == [2, 4, 6]


# -----------------------------------------------------------------------------
# 4.3. Покомпонентная сумма и среднее списка векторов
# -----------------------------------------------------------------------------
def vector_sum(vectors: List[Vector]) -> Vector:
    """Сложить все векторы поэлементно: result[i] = sum(v[i] for v in vectors)."""
    assert vectors, "no vectors provided!"
    num_elements = len(vectors[0])
    assert all(len(v) == num_elements for v in vectors), "different sizes!"
    return [sum(vector[i] for vector in vectors)
            for i in range(num_elements)]


def vector_mean(vectors: List[Vector]) -> Vector:
    """Среднее списка векторов (покомпонентно)."""
    n = len(vectors)
    return scalar_multiply(1 / n, vector_sum(vectors))


assert vector_sum([[1, 2], [3, 4], [5, 6], [7, 8]]) == [16, 20]
assert vector_mean([[1, 2], [3, 4], [5, 6]]) == [3, 4]


# -----------------------------------------------------------------------------
# 4.4. Скалярное произведение (dot product) — ГЛАВНАЯ операция
# -----------------------------------------------------------------------------
# dot(v, w) = v_1*w_1 + v_2*w_2 + ... + v_n*w_n
# Это скаляр. В ML — основа регрессий, нейросетей, косинусной меры.
def dot(v: Vector, w: Vector) -> float:
    assert len(v) == len(w), "vectors must be same length"
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v: Vector) -> float:
    """v_1^2 + v_2^2 + ... + v_n^2. = dot(v, v)."""
    return dot(v, v)


assert dot([1, 2, 3], [4, 5, 6]) == 32               # 1*4 + 2*5 + 3*6
assert sum_of_squares([1, 2, 3]) == 14                # 1 + 4 + 9


# -----------------------------------------------------------------------------
# 4.5. Магнитуда и евклидово расстояние
# -----------------------------------------------------------------------------
def magnitude(v: Vector) -> float:
    """||v|| = sqrt(v_1^2 + ... + v_n^2)."""
    return math.sqrt(sum_of_squares(v))


def distance(v: Vector, w: Vector) -> float:
    """Евклидово расстояние между двумя векторами."""
    return magnitude(subtract(v, w))


assert magnitude([3, 4]) == 5                          # 3-4-5 треугольник


# -----------------------------------------------------------------------------
# 4.6. Матрицы
# -----------------------------------------------------------------------------
Matrix = List[List[float]]                              # матрица = список строк

A = [[1, 2, 3],                                         # 2 строки × 3 столбца
     [4, 5, 6]]

B = [[1, 2],                                            # 3 строки × 2 столбца
     [3, 4],
     [5, 6]]


def shape(A: Matrix) -> Tuple[int, int]:
    """(число строк, число столбцов)."""
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols


def get_row(A: Matrix, i: int) -> Vector:
    return A[i]


def get_column(A: Matrix, j: int) -> Vector:
    return [A_i[j] for A_i in A]


assert shape([[1, 2, 3], [4, 5, 6]]) == (2, 3)


# -----------------------------------------------------------------------------
# 4.7. Конструкторы: identity_matrix, make_matrix
# -----------------------------------------------------------------------------
def make_matrix(num_rows: int,
                num_cols: int,
                entry_fn: Callable[[int, int], float]) -> Matrix:
    """Матрица, у которой entry (i,j) = entry_fn(i, j)."""
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]


def identity_matrix(n: int) -> Matrix:
    """Единичная матрица n×n (1 на диагонали, 0 везде)."""
    return make_matrix(n, n, lambda i, j: 1 if i == j else 0)


assert identity_matrix(5) == [
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
]


# -----------------------------------------------------------------------------
# 4.8. Практический кейс: матрица дружбы (взвешенный граф как матрица)
# -----------------------------------------------------------------------------
# friend_matrix[i][j] = 1 если i и j друзья, иначе 0.
# Это «матрица смежности» графа — мощная структура, т.к.
# friend_matrix[i][j] = 1 за O(1) (быстрее, чем список смежности).
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

assert friend_matrix[0][2] == 1, "0 и 2 — друзья"
assert friend_matrix[0][8] == 0, "0 и 8 — не друзья"

# Список друзей пользователя 5 — просто фильтр по строке
friends_of_five = [i for i, is_friend in enumerate(friend_matrix[5])
                   if is_friend]
# [4, 6, 7]


# =============================================================================
# ГЛАВА 5. СТАТИСТИКА
# =============================================================================
# Использует sum_of_squares и dot из главы 4 — заметьте, что они
# переиспользуются. Это и есть смысл «библиотеки scratch»: набор
# примитивов, поверх которого строятся ML-алгоритмы дальше.

# -----------------------------------------------------------------------------
# 5.1. Данные: число друзей и ежедневное время на сайте
# -----------------------------------------------------------------------------
num_friends = [100.0, 49, 41, 40, 25, 21, 21, 19, 19, 18,
               18, 16, 15, 15, 15, 15, 14, 14, 13, 13,
               13, 13, 12, 12, 11, 10, 10, 10, 10, 10,
               10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
               9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
               9, 9, 9, 9, 9, 9, 9, 9, 8, 8,
               8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
               8, 7, 7, 7, 7, 7, 7, 7, 7, 7,
               7, 7, 7, 7, 7, 7, 6, 6, 6, 6,
               6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
               6, 6, 6, 6, 6, 6, 6, 6, 5, 5,
               5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
               5, 5, 5, 5, 5, 4, 4, 4, 4, 4,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
               4, 4, 4, 4, 4, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1]
assert len(num_friends) == 204

# Время на сайте (минуты в день) — длинная строка, 204 значения
daily_minutes = [
    1, 68.77, 51.25, 52.08, 38.36, 44.54, 57.13, 51.4, 41.42, 31.22,
    34.76, 54.01, 38.79, 47.59, 49.1, 27.66, 41.03, 36.73, 48.65, 28.12,
    46.62, 35.57, 32.98, 35.0, 26.07, 23.77, 39.73, 40.57, 31.65, 31.21,
    36.32, 20.45, 21.93, 26.02, 27.34, 23.49, 46.94, 30.5, 33.8, 24.23,
    21.4, 27.94, 32.24, 40.57, 25.07, 19.42, 22.39, 18.42, 46.96, 23.72,
    26.41, 26.97, 36.76, 40.32, 35.02, 29.47, 30.2, 31.0, 38.11, 38.18,
    36.31, 21.03, 30.86, 36.07, 28.66, 29.08, 37.28, 15.28, 24.17, 22.31,
    30.17, 25.53, 19.85, 35.37, 44.6, 17.23, 13.47, 26.33, 35.02, 32.09,
    24.81, 19.33, 28.77, 24.26, 31.98, 25.73, 24.86, 16.28, 34.51, 15.23,
    39.72, 40.8, 26.06, 35.76, 34.76, 16.13, 44.04, 18.03, 19.65, 32.62,
    35.59, 39.43, 14.18, 35.24, 40.13, 41.82, 35.45, 36.07, 43.67, 24.61,
    20.9, 21.9, 18.79, 27.61, 27.21, 26.61, 29.77, 20.59, 27.53, 13.82,
    33.2, 25.0, 33.1, 36.65, 18.63, 14.87, 22.2, 36.81, 25.53, 24.62,
    26.25, 18.21, 28.08, 19.42, 29.79, 32.8, 35.99, 28.32, 27.79, 35.88,
    29.06, 36.28, 14.1, 36.63, 37.49, 26.9, 18.58, 38.48, 24.48, 18.95,
    33.55, 14.24, 29.04, 32.51, 25.63, 22.22, 19.0, 32.73, 15.16, 13.9,
    27.2, 32.01, 29.27, 33.0, 13.74, 20.42, 27.32, 18.23, 35.35, 28.48,
    9.08, 24.62, 20.12, 35.26, 19.92, 31.02, 16.49, 12.16, 30.7, 31.22,
    34.65, 13.13, 27.51, 33.2, 31.57, 14.1, 33.42, 17.44, 10.12, 24.42,
    9.82, 23.39, 30.93, 15.03, 21.67, 31.09, 33.29, 22.61, 26.89, 23.48,
    8.38, 27.81, 32.35, 23.84,
]

# Гистограмма распределения числа друзей — почти всегда полезно посмотреть
friend_counts = Counter(num_friends)
xs = range(101)
ys = [friend_counts[x] for x in xs]
plt.bar(xs, ys)
plt.axis([0, 101, 0, 25])
plt.title("Histogram of Friend Counts")
plt.xlabel("# of friends")
plt.ylabel("# of people")
plt.savefig(os.path.join(_FIG_DIR, "viz_hist_friend_counts.png"))
plt.gca().clear()


# -----------------------------------------------------------------------------
# 5.2. Меры центральной тенденции
# -----------------------------------------------------------------------------
def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)


assert 7.3333 < mean(num_friends) < 7.3334


def _median_odd(xs: List[float]) -> float:
    """Нечётное количество — серединный элемент."""
    return sorted(xs)[len(xs) // 2]


def _median_even(xs: List[float]) -> float:
    """Чётное количество — среднее двух серединных."""
    sorted_xs = sorted(xs)
    hi_midpoint = len(xs) // 2
    return (sorted_xs[hi_midpoint - 1] + sorted_xs[hi_midpoint]) / 2


def median(v: List[float]) -> float:
    return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)


assert median([1, 10, 2, 9, 5]) == 5
assert median([1, 9, 2, 10]) == (2 + 9) / 2
assert median(num_friends) == 6                # медиана = 6 друзьям


def quantile(xs: List[float], p: float) -> float:
    """p-й перцентиль (0 ≤ p ≤ 1). Упрощённый вариант из книги."""
    p_index = int(p * len(xs))
    return sorted(xs)[p_index]


assert quantile(num_friends, 0.10) == 1         # 10% имеют ≤ 1 друга
assert quantile(num_friends, 0.25) == 3         # 25% имеют ≤ 3
assert quantile(num_friends, 0.75) == 9         # 75% имеют ≤ 9
assert quantile(num_friends, 0.90) == 13        # 90% имеют ≤ 13


def mode(x: List[float]) -> List[float]:
    """Список мод (их может быть несколько — Counter знает все максимумы)."""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]


assert set(mode(num_friends)) == {1, 6}         # 1 и 6 встречаются чаще всего


# -----------------------------------------------------------------------------
# 5.3. Меры разброса (dispersion)
# -----------------------------------------------------------------------------
def data_range(xs: List[float]) -> float:
    return max(xs) - min(xs)


assert data_range(num_friends) == 99            # от 1 до 100


def de_mean(xs: List[float]) -> List[float]:
    """Сдвинуть xs так, чтобы среднее стало 0. Используется в variance/covariance."""
    x_bar = mean(xs)
    return [x - x_bar for x in xs]


def variance(xs: List[float]) -> float:
    """Выборочная дисперсия: сумма квадратов отклонений / (n-1)."""
    assert len(xs) >= 2, "variance requires at least two elements"
    n = len(xs)
    deviations = de_mean(xs)
    return sum_of_squares(deviations) / (n - 1)   # n-1 — поправка Бесселя


assert 81.54 < variance(num_friends) < 81.55


def standard_deviation(xs: List[float]) -> float:
    """Среднеквадратичное отклонение — sqrt дисперсии."""
    return math.sqrt(variance(xs))


assert 9.02 < standard_deviation(num_friends) < 9.04


def interquartile_range(xs: List[float]) -> float:
    """IQR = 75-й перцентиль − 25-й. Устойчив к выбросам."""
    return quantile(xs, 0.75) - quantile(xs, 0.25)


assert interquartile_range(num_friends) == 6    # 9 − 3


# -----------------------------------------------------------------------------
# 5.4. Ковариация и корреляция
# -----------------------------------------------------------------------------
# Ковариация показывает, В КАКУЮ СТОРОНУ xs и ys меняются вместе.
# Корреляция = ковариация, нормированная в [-1, 1].
# Корреляция 0.24 — слабая положительная связь «больше друзей ⇒ больше минут».

def covariance(xs: List[float], ys: List[float]) -> float:
    assert len(xs) == len(ys), "xs and ys must have same number of elements"
    return dot(de_mean(xs), de_mean(ys)) / (len(xs) - 1)


assert 22.42 < covariance(num_friends, daily_minutes) < 22.43

# В часах — ковариация делится на 60 (линейное преобразование)
daily_hours = [dm / 60 for dm in daily_minutes]
assert 22.42 / 60 < covariance(num_friends, daily_hours) < 22.43 / 60


def correlation(xs: List[float], ys: List[float]) -> float:
    """Нормализованная мера совместной изменчивости, ∈ [-1, 1]."""
    stdev_x = standard_deviation(xs)
    stdev_y = standard_deviation(ys)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(xs, ys) / stdev_x / stdev_y
    else:
        return 0                                # нет изменчивости → нет связи


assert 0.24 < correlation(num_friends, daily_minutes) < 0.25
assert 0.24 < correlation(num_friends, daily_hours)   < 0.25


# -----------------------------------------------------------------------------
# 5.5. ⚠️ Чувствительность корреляции к выбросам
# -----------------------------------------------------------------------------
# В наших данных есть один юзер с 100 друзьями — выброс.
# Если его убрать, корреляция ПРЫГАЕТ с 0.24 до 0.57!
# Это типичный DS-урок: «средние» и «корреляции» сильно зависят от хвостов.
outlier = num_friends.index(100)               # индекс юзера-выброса

num_friends_good = [x for i, x in enumerate(num_friends) if i != outlier]
daily_minutes_good = [x for i, x in enumerate(daily_minutes) if i != outlier]
daily_hours_good = [dm / 60 for dm in daily_minutes_good]

assert 0.57 < correlation(num_friends_good, daily_minutes_good) < 0.58
assert 0.57 < correlation(num_friends_good, daily_hours_good)   < 0.58

# Итог: один экстремальный объект сдвинул корреляцию с 0.57 до 0.24.
# Сначала смотрим scatter, считаем корреляцию, проверяем робастность —
# и только потом делаем выводы.


# =============================================================================
# ИТОГ ГЛАВ 3-5
# =============================================================================
# Визуализация (matplotlib) — основной инструмент «первого взгляда» на данные.
# Линейная алгебра (векторы, матрицы, dot) — фундамент всех ML-моделей.
# Статистика (mean, variance, correlation) — фундамент любого EDA.
#
# Дальше в книге:
#   гл. 6  — теория вероятностей
#   гл. 7  — гипотезы и статистические выводы
#   гл. 8  — градиентный спуск
#   гл. 9  — получение данных (scraping, API, файлы)
#   гл. 10 — работа с данными (pandas-подобный слой)
#   гл. 11 — машинное обучение
#   ...
print("\n[OK] Главы 3-5: все assert-ы пройдены, фигуры сохранены в", _FIG_DIR)
