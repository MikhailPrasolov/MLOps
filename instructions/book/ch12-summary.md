# Глава 12. Метод k ближайших соседей

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/k_nearest_neighbors.py`

> **Контекст:** самая интуитивная модель — «посмотри на k похожих объектов и пусть они проголосуют». Глава использует классический датасет Iris (3 класса ирисов, 4 признака), показывает **curse of dimensionality** — на высокоразмерных данных расстояния теряют смысл.

## Ключевые концепции

- **`LabeledPoint`** = `NamedTuple(point: Vector, label: str)` — пара «фичи + метка»
- **kNN classify** — `sorted(by distance)[:k]` → `majority_vote` среди k ближайших
- **`majority_vote` с tie-breaking** — если ничья, отбросить самого дальнего (`labels[:-1]`) и переголосовать
- **Iris dataset** — 150 записей, 4 числовых признака, 3 класса; классика для примеров
- **Curse of dimensionality** — в высоких размерностях min-distance ≈ avg-distance, соседи теряют смысл
- **`confusion_matrix`** — счётчик пар `(predicted, actual)` через `defaultdict(int)`

## Код

```python
from typing import NamedTuple, List
from collections import Counter
from scratch.linear_algebra import Vector, distance

class LabeledPoint(NamedTuple):
    point: Vector
    label: str

def majority_vote(labels: List[str]) -> str:
    """При ничье — отбрасываем самого дальнего"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = sum(1 for c in vote_counts.values() if c == winner_count)
    if num_winners == 1:
        return winner
    return majority_vote(labels[:-1])    # рекурсия

def knn_classify(k: int, labeled_points: List[LabeledPoint], new_point: Vector) -> str:
    by_distance = sorted(labeled_points,
                         key=lambda lp: distance(lp.point, new_point))
    k_nearest_labels = [lp.label for lp in by_distance[:k]]
    return majority_vote(k_nearest_labels)

# Пример: на Iris с k=5 получаем ~96% accuracy
predicted = knn_classify(5, iris_train, iris.point)
```

## Связанные главы

- [[ch11-summary]] — предыдущая (split, confusion matrix)
- [[ch13-summary]] — следующая (другая модель)
- [[ch04-summary]] — `distance()` из линейной алгебры — ядро kNN
- [[ch10-summary]] — нормализация обязательна для kNN (без неё признак с большим масштабом доминирует)

## Краткие выводы

1. **kNN — ленивый ученик**: вся «модель» это **сама выборка**; предсказание = `O(n)` lookup
2. **`majority_vote` с отбрасыванием дальнего** — простой и надёжный tie-breaker
3. **Curse of dimensionality**: для kNN нормализация признаков **обязательна**, иначе расстояния бессмысленны

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| kNN классификация | Baseline для табличных данных, рекомендации «похожих пользователей» |
| kNN регрессия | Среднее по k соседям для непрерывных таргетов |
| `LabeledPoint` | Паттерн для любой supervised-задачи без модели |
| `majority_vote` | Ансамбли, soft-voting в RandomForest, бустинге |
