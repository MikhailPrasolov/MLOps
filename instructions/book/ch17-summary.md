# Глава 17. Деревья решений

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/decision_trees.py`

> **Контекст:** нелинейная модель через жадное разбиение пространства признаков по критерию **information gain** (минимум энтропии). Глава строит дерево для задачи найма (`level, lang, tweets, phd → did_well`) алгоритмом **ID3**, классический и прозрачный.

## Ключевые концепции

- **Энтропия Шеннона** — `Σ -p·log₂(p)`; мера неопределённости; `H([1])=0`, `H([0.5,0.5])=1`
- **`partition_entropy`** — взвешенная сумма энтропий подмножеств после разбиения
- **ID3** — на каждом шаге выбираем атрибут, дающий **минимальную** `partition_entropy`
- **`Leaf(value)` / `Split(attribute, subtrees, default_value)`** — рекурсивная структура дерева через `NamedTuple` + `Union`
- **Рекурсивное построение** — если все метки одинаковы → `Leaf`; если атрибутов нет → `Leaf(most_common)`
- **`default_value`** в `Split` — на случай неизвестного значения атрибута в инференсе

## Код

```python
import math
from collections import Counter
from typing import NamedTuple, Union, Any

def entropy(class_probabilities):
    return sum(-p * math.log(p, 2) for p in class_probabilities if p > 0)

def data_entropy(labels):
    return entropy([c / len(labels) for c in Counter(labels).values()])

def partition_entropy(subsets):
    total = sum(len(s) for s in subsets)
    return sum(data_entropy(s) * len(s) / total for s in subsets)

class Leaf(NamedTuple):
    value: Any

class Split(NamedTuple):
    attribute: str
    subtrees: dict
    default_value: Any = None

DecisionTree = Union[Leaf, Split]

def build_tree_id3(inputs, split_attributes, target_attribute):
    label_counts = Counter(getattr(i, target_attribute) for i in inputs)
    most_common = label_counts.most_common(1)[0][0]
    if len(label_counts) == 1:    return Leaf(most_common)
    if not split_attributes:      return Leaf(most_common)
    best = min(split_attributes,
               key=lambda a: partition_entropy_by(inputs, a, target_attribute))
    partitions = partition_by(inputs, best)
    new_attrs = [a for a in split_attributes if a != best]
    subtrees = {v: build_tree_id3(subset, new_attrs, target_attribute)
                for v, subset in partitions.items()}
    return Split(best, subtrees, default_value=most_common)

def classify(tree, input):
    if isinstance(tree, Leaf): return tree.value
    key = getattr(input, tree.attribute)
    if key not in tree.subtrees: return tree.default_value
    return classify(tree.subtrees[key], input)
```

## Связанные главы

- [[ch16-summary]] — предыдущая
- [[ch18-summary]] — следующая
- [[ch13-summary]] — NB даёт вероятности, деревья — нет
- [[ch23-summary]] — деревья как компонент рекомендательных систем

## Краткие выводы

1. **ID3 жаден** — выбирает лучшее разбиение здесь и сейчас; не оптимально глобально
2. **Энтропия vs Gini** — выбор критерия редко меняет результат; ID3 использует энтропию, CART — Gini
3. **`default_value`** обязателен — на инференсе встретятся значения атрибутов, которых не было в обучении

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| Дерево решений | Интерпретируемые модели, baseline для табличных данных |
| ID3 / C4.5 / CART | Классические алгоритмы; XGBoost/LightGBM — их наследники |
| `Leaf` / `Split` | Простая структура для обучения/инференса |
| Энтропия | Выбор разбиений, feature importance |
