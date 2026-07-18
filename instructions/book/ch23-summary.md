# Глава 23. Рекомендательные системы

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/recommender_systems.py`

> **Контекст:** глава строит три классических подхода к рекомендациям на одних и тех же данных (`users_interests` — 15 пользователей × наборы интересов): **popularity-based**, **user-based CF** (через cosine similarity), **item-based CF** и завершает **matrix factorization** через эмбеддинги на MovieLens 100k.

## Ключевые концепции

- **«Что популярно»** — `Counter` по интересам → исключить свои → top-N
- **One-hot interest vector** — `[1 if interest in user_interests else 0 for interest in unique_interests]`
- **Cosine similarity** между пользователями — `dot / (||a||·||b||)` (из главы 21)
- **User-based CF** — найди похожих пользователей → суммируй их интересы с весом = similarity
- **Item-based CF** — симметрично: для каждого своего интереса — похожие интересы с весом similarity
- **Matrix factorization (MovieLens)** — случайные эмбеддинги `user_vectors[uid]`, `movie_vectors[mid]`; предсказание = `dot(u, m)`; loss = `(pred - rating)²`; обучение через SGD
- **PCA на эмбеддингах** — для визуализации кластеров похожих фильмов

## Код

```python
from collections import Counter, defaultdict
from scratch.nlp import cosine_similarity
from scratch.linear_algebra import dot

# 1. Популярное
popular_interests = Counter(i for ui in users_interests for i in ui)

# 2. User-based CF
unique_interests = sorted({i for ui in users_interests for i in ui})
user_vectors = [[1 if i in ui else 0 for i in unique_interests]
                for ui in users_interests]
user_sims = [[cosine_similarity(a, b) for b in user_vectors]
             for a in user_vectors]

def user_based_suggestions(user_id):
    suggestions = defaultdict(float)
    for other_id, sim in enumerate(user_sims[user_id]):
        if other_id != user_id and sim > 0:
            for interest in users_interests[other_id]:
                suggestions[interest] += sim
    return sorted(suggestions.items(), key=lambda x: -x[1])

# 3. Item-based CF — симметрично по интересам
interest_user_matrix = [[uv[j] for uv in user_vectors]
                        for j in range(len(unique_interests))]
interest_sims = [[cosine_similarity(a, b) for b in interest_user_matrix]
                 for a in interest_user_matrix]

# 4. Matrix factorization (MovieLens)
user_vectors = {uid: random_tensor(EMBEDDING_DIM) for uid in user_ids}
movie_vectors = {mid: random_tensor(EMBEDDING_DIM) for mid in movie_ids}

for epoch in range(20):
    for rating in train:
        pred = dot(user_vectors[rating.user_id], movie_vectors[rating.movie_id])
        err = pred - rating.rating
        # градиенты: err · m для u, err · u для m
        ...
```

## Связанные главы

- [[ch22-summary]] — предыдущая (графы; PageRank как рекомендация)
- [[ch24-summary]] — следующая (базы данных)
- [[ch12-summary]] — kNN на интересах = user-based CF lite
- [[ch21-summary]] — cosine similarity из NLP
- [[ch19-summary]] — Embedding слой из DL для матричной факторизации

## Краткие выводы

1. **User-based vs Item-based** — item-based стабильнее при росте числа пользователей
2. **Cosine similarity нормализует** — пользователь с 100 интересами не «забивает» пользователя с 3
3. **Matrix factorization — современный стандарт** — обучается SGD; даёт embeddings для downstream-задач

## Где пригодиться

| Концепция | Применение |
|-----------|-----------|
| Popularity baseline | Cold start, новые пользователи |
| User-based CF | Когда нужна интерпретируемость «похожие на тебя» |
| Item-based CF | Каталоги с ≫ пользователей (e-commerce) |
| Matrix factorization | Implicit feedback (просмотры), production-рекомендеры |
