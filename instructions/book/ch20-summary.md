# Глава 20. Кластеризация

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/clustering.py`

> **Контекст:** unsupervised-задача — найти группы похожих объектов без меток. Глава вводит два семейства: **K-means** (центроиды, итеративно) и **иерархическую кластеризацию** (binary tree через `Leaf`/`Merged`). Кейс — группировка пользователей по геолокации и **квантование цветов** изображения.

## Ключевые концепции

- **K-means** — случайные назначения → пересчёт средних → переназначение → до сходимости
- **`cluster_means(k, inputs, assignments)`** — среднее по кластеру; пустой кластер → `random.choice(inputs)`
- **`classify(input)`** — к какому кластеру относится новая точка (ближайший по `squared_distance`)
- **Elbow method** — график `total_squared_error vs k` для выбора числа кластеров
- **Hierarchical (bottom-up)** — начинаем с n кластеров-листьев; на каждом шаге объединяем два ближайших
- **`distance_agg = min` vs `max`** — single-linkage (чувствителен к шуму) vs complete-linkage
- **`generate_clusters(base, num_clusters)`** — «разрезает» дерево по `merge_order`
- **Image recoloring** — k-means по пикселям → 5 цветов → «постеризация» изображения

## Код

```python
import random, itertools, tqdm
from scratch.linear_algebra import squared_distance, vector_mean, distance

class KMeans:
    def __init__(self, k):
        self.k = k; self.means = None

    def classify(self, input):
        return min(range(self.k),
                   key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):
        assignments = [random.randrange(self.k) for _ in inputs]
        with tqdm.tqdm(itertools.count()) as t:
            for _ in t:
                self.means = cluster_means(self.k, inputs, assignments)
                new_assignments = [self.classify(i) for i in inputs]
                num_changed = num_differences(assignments, new_assignments)
                if num_changed == 0: return
                assignments = new_assignments
                self.means = cluster_means(self.k, inputs, assignments)
                t.set_description(f"changed: {num_changed} / {len(inputs)}")

# Иерархическая кластеризация
from typing import NamedTuple, Union
class Leaf(NamedTuple):    value: list
class Merged(NamedTuple):  children: tuple; order: int

def bottom_up_cluster(inputs, distance_agg=min):
    clusters = [Leaf(inp) for inp in inputs]
    while len(clusters) > 1:
        c1, c2 = min(((a, b)
                      for i, a in enumerate(clusters)
                      for b in clusters[:i]),
                     key=lambda p: cluster_distance(p[0], p[1], distance_agg))
        clusters = [c for c in clusters if c != c1 and c != c2]
        clusters.append(Merged((c1, c2), order=len(clusters)))
    return clusters[0]

def generate_clusters(base_cluster, num_clusters):
    clusters = [base_cluster]
    while len(clusters) < num_clusters:
        next_cluster = min(clusters, key=get_merge_order)
        clusters = [c for c in clusters if c != next_cluster]
        clusters.extend(get_children(next_cluster))
    return clusters
```

## Связанные главы

- [[ch19-summary]] — предыдущая
- [[ch21-summary]] — следующая (кластеризация текстов)
- [[ch12-summary]] — KNN как supervised-аналог K-means
- [[ch22-summary]] — community detection = кластеризация на графе

## Краткие выводы

1. **K-means требует нормализации** — иначе признак с большим масштабом доминирует
2. **Elbow method** для выбора k — смотрите на излом графика ошибки
3. **Bottom-up кластеризация даёт «даendrogramm»** — можно выбрать любое число кластеров постфактум

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| K-means | Сегментация клиентов, квантование цветов, кластеризация документов |
| Elbow method | Выбор числа кластеров |
| Hierarchical | Таксономии, дендрограммы, small data |
| Image recoloring | Постеризация, сжатие палитры |
