# Глава 11. Машинное обучение

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/machine_learning.py`

> **Контекст:** короткая глава-«мост» между предобработкой данных и моделями. Вводит три ключевых инструмента ML: **train/test split**, базовые **метрики классификации** (accuracy, precision, recall, F1) и **confusion matrix** — фундамент оценки любой модели.

## Ключевые концепции

- **Train/test split** — `split_data(data, prob)` делит выборку в пропорции `[prob, 1-prob]` после shuffle
- **TypeVar `X`, `Y`** — обобщённые типы для пары (признаки, целевая переменная)
- **`train_test_split(xs, ys, test_pct)`** — синхронная разбивка фич и таргетов по одним индексам
- **Confusion matrix** — счётчик `(predicted, actual)` пар
- **Precision = TP / (TP + FP)** — из предсказанных положительных сколько верных
- **Recall = TP / (TP + FN)** — из реальных положительных сколько поймали
- **F1 = 2·P·R / (P+R)** — гармоническое среднее, баланс precision/recall
- **Accuracy может вводить в заблуждение** на несбалансированных классах (98% при 99% негативов — бесполезно)

## Код

```python
import random
from typing import TypeVar, List, Tuple

X = TypeVar('X'); Y = TypeVar('Y')

def split_data(data: List[X], prob: float) -> Tuple[List[X], List[X]]:
    data = data[:]               # shallow copy — shuffle мутирует
    random.shuffle(data)
    cut = int(len(data) * prob)
    return data[:cut], data[cut:]

def train_test_split(xs, ys, test_pct):
    idxs = list(range(len(xs)))
    train_idxs, test_idxs = split_data(idxs, 1 - test_pct)
    return ([xs[i] for i in train_idxs], [xs[i] for i in test_idxs],
            [ys[i] for i in train_idxs], [ys[i] for i in test_idxs])

# Confusion matrix
def accuracy(tp, fp, fn, tn):  return (tp + tn) / (tp + fp + fn + tn)
def precision(tp, fp, fn, tn): return tp / (tp + fp)
def recall(tp, fp, fn, tn):    return tp / (tp + fn)
def f1_score(tp, fp, fn, tn):
    p, r = precision(tp, fp, fn, tn), recall(tp, fp, fn, tn)
    return 2 * p * r / (p + r)
```

## Связанные главы

- [[ch10-summary]] — предыдущая (подготовка данных)
- [[ch12-summary]] — следующая (KNN как первая модель)
- [[ch13-summary]] — Наивный Байес (другая модель, те же метрики)
- [[ch15-summary]] — R² для регрессии (аналог accuracy)

## Краткие выводы

1. **Всегда делайте train/test split** до любой модели — иначе переобучение невидимо
2. **Accuracy врёт на дисбалансе** — для fraud 1/10000 accuracy=99.99% ничего не значит
3. **F1 vs accuracy** — выбирайте F1/Precision/Recall под бизнес-метрику (recall для диагностики, precision для рекламы)

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `split_data` / `train_test_split` | Любой ML-пайплайн; аналог `sklearn.model_selection.train_test_split` |
| Precision/Recall/F1 | Классификация с дисбалансом (fraud, churn, диагностика) |
| Confusion matrix | Отладка модели: где чаще ошибается — на каком классе |
| Random shuffle | Не забывайте `random.seed()` для воспроизводимости |
