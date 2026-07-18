# Глава 1. Введение: поиск ключевых связей

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/introduction.py`

> **Контекст:** глава задаёт мотивацию через сквозной пример «DataSciencester» — соцсеть для дата-сайентистов. Показывает, как «вручную» решать типовые задачи DS (рекомендации друзей, общие интересы, зарплатные бакеты) без библиотек — на чистом Python.

## Ключевые концепции

- **«Ключевые связи» (Key Connectors)** — пользователи, через которых идёт наибольший поток информации; пример друзей-друзей (`friends_of_friends`) и `Counter` для подсчёта пересечений
- **Инвертированный индекс** — `defaultdict(list)` для маппинга `interest → [user_ids]`, основа поиска и рекомендаций
- **Бакетизация (binning)** — превращение непрерывной величины (стаж) в категории (`<2`, `2–5`, `>5`) для робастной агрегации
- **«Чистый Python»-подход** — без `pandas`/`scikit-learn`, всё через `list`/`dict`/`Counter`/`defaultdict`

## Код

```python
from collections import Counter, defaultdict

# 1. Друзья-друзья (рекомендации друзей)
def friends_of_friends(user):
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id]
        for foaf_id in friendships[friend_id]
        if foaf_id != user_id
        and foaf_id not in friendships[user_id]
    )

# 2. Инвертированный индекс: интерес → пользователи
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# 3. Бакетизация зарплат по стажу
def tenure_bucket(tenure):
    if tenure < 2:   return "less than two"
    elif tenure < 5: return "between two and five"
    else:            return "more than five"

# Итог: <2 → 48k, 2-5 → 61.5k, >5 → 79.2k — опытные получают больше
```

## Связанные главы

- [[ch02-summary]] — синтаксис Python, который нужен для понимания примеров
- [[ch22-summary]] — анализ социальных сетей (продолжение идей «DataSciencester»)
- [[ch23-summary]] — рекомендательные системы (развитие «общих интересов»)

## Краткие выводы

1. **`Counter` + `defaultdict(list)`** — основа для почти всех задач подсчёта и индексации в «чистом Python»
2. **`foaf` (friend-of-a-friend)** — простейший коллаборативный фильтр: рекомендуй тех, кто дружит с друзьями
3. **Бакетизация спасает** от разреженности: 10 точек данных лучше превратить в 3 осмысленные категории

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `Counter` для foaf | Любые рекомендательные системы «по соседям» |
| `defaultdict(list)` индекс | Поиск документов, тегирование, группировка |
| Бакетизация tenure→salary | A/B-анализ по сегментам, когортный анализ |
