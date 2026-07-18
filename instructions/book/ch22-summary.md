# Глава 22. Анализ социальных сетей

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/network_analysis.py`

> **Контекст:** возврат к «DataSciencester», но теперь как граф. Глава вводит три центральные метрики центральности (**betweenness**, **closeness**), собственный вектор через power iteration и **PageRank** как итеративный алгоритм.

## Ключевые концепции

- **Граф дружбы** — `Dict[int, List[int]]` (adjacency list); ненаправленный
- **`shortest_paths_from`** — BFS через `deque`; возвращает **все** кратчайшие пути от вершины
- **Betweenness centrality** — сколько раз узел лежит на кратчайших путях между другими парами (1/n_paths на каждый)
- **Closeness centrality** — `1 / sum(len(shortest_paths))`; «средняя близость ко всем»
- **Eigenvector centrality** — power iteration: `guess ← A·guess / ||A·guess||` до сходимости
- **PageRank** — итерация `next_pr[target] += damping · pr[source] / outgoing_counts[source]` + базовая часть `(1-d)/N`
- **Damping = 0.85** — телепортация, чтобы случайный блуждатель не застрял

## Код

```python
from typing import NamedTuple
from collections import deque, Counter
import random, tqdm

class User(NamedTuple):
    id: int; name: str

# BFS — все кратчайшие пути от from_user
def shortest_paths_from(from_user_id, friendships):
    shortest_paths_to = {from_user_id: [[]]}
    frontier = deque((from_user_id, f) for f in friendships[from_user_id])
    while frontier:
        prev, user = frontier.popleft()
        new_paths = [p + [user] for p in shortest_paths_to[prev]]
        old_paths = shortest_paths_to.get(user, [])
        min_len = len(old_paths[0]) if old_paths else float('inf')
        new_paths = [p for p in new_paths
                     if len(p) <= min_len and p not in old_paths]
        shortest_paths_to[user] = old_paths + new_paths
        frontier.extend((user, f) for f in friendships[user]
                        if f not in shortest_paths_to)
    return shortest_paths_to

# Betweenness centrality
betweenness = {u.id: 0.0 for u in users}
for src in users:
    for tgt, paths in shortest_paths[src.id].items():
        if src.id < tgt.id:
            contrib = 1 / len(paths)
            for path in paths:
                for mid in path:
                    if mid not in (src.id, tgt):
                        betweenness[mid] += contrib

# PageRank
def page_rank(users, endorsements, damping=0.85, num_iters=100):
    outgoing = Counter(t for s, t in endorsements)
    pr = {u.id: 1 / len(users) for u in users}
    base_pr = (1 - damping) / len(users)
    for _ in tqdm.trange(num_iters):
        next_pr = {u.id: base_pr for u in users}
        for s, t in endorsements:
            next_pr[t] += damping * pr[s] / outgoing[s]
        pr = next_pr
    return pr
```

## Связанные главы

- [[ch21-summary]] — предыдущая (n-граммы)
- [[ch23-summary]] — следующая (рекомендации)
- [[ch01-summary]] — начало DataSciencester-цикла
- [[ch20-summary]] — community detection как кластеризация графа

## Краткие выводы

1. **BFS даёт shortest paths** — фундамент для betweenness/closeness centrality
2. **Power iteration = eigenvector centrality** — сходится для большинства реальных графов
3. **PageRank с damping** — простая итерация, решает проблему «ловушек» (висячих узлов)

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| BFS shortest paths | Любая задача «расстояние в графе» |
| Betweenness centrality | Поиск узких мест в сетях, инфлюенсеров |
| PageRank | Ранжирование веб-страниц, рекомендации, fraud detection |
| Eigenvector centrality | Важность узла с учётом важности соседей |
