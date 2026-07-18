# Глава 13. Наивный Байес

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/naive_bayes.py`

> **Контекст:** вероятностный классификатор на теореме Байеса с «наивным» предположением независимости признаков. В книге — на примере **spam detection**: токенизация текста → подсчёт частот слов в спаме/не-спаме → predict через log-вероятности.

## Ключевые концепции

- **`P(class | features) ∝ P(features | class) · P(class)`** — теорема Байеса; знаменатель одинаков для всех классов
- **«Наивность»** — признаки (слова) условно независимы при данном классе
- **Токенизация** — `re.findall("[a-z0-9']+", text.lower())` → `set(...)` (уникальные слова)
- **Сглаживание (Laplace, k=0.5)** — `(count + k) / (total + 2·k)` чтобы не было P=0 для редких слов
- **Логарифмические вероятности** — `sum(log p)` вместо `product(p)` — численная стабильность
- **`predict`** — `P(spam) / (P(spam) + P(ham))` ∈ [0, 1]

## Код

```python
import re, math
from collections import defaultdict
from typing import Set, NamedTuple, Dict, Iterable

def tokenize(text: str) -> Set[str]:
    return set(re.findall("[a-z0-9']+", text.lower()))

class Message(NamedTuple):
    text: str
    is_spam: bool

class NaiveBayesClassifier:
    def __init__(self, k: float = 0.5):
        self.k = k
        self.tokens: Set[str] = set()
        self.token_spam_counts: Dict[str, int] = defaultdict(int)
        self.token_ham_counts:  Dict[str, int] = defaultdict(int)
        self.spam_messages = self.ham_messages = 0

    def train(self, messages: Iterable[Message]) -> None:
        for m in messages:
            self.spam_messages += m.is_spam
            self.ham_messages  += not m.is_spam
            for t in tokenize(m.text):
                self.tokens.add(t)
                (self.token_spam_counts if m.is_spam else self.token_ham_counts)[t] += 1

    def _probabilities(self, token):
        s = self.token_spam_counts[token]; h = self.token_ham_counts[token]
        return ((s + self.k) / (self.spam_messages + 2*self.k),
                (h + self.k) / (self.ham_messages  + 2*self.k))

    def predict(self, text: str) -> float:
        text_tokens = tokenize(text)
        log_spam = log_ham = 0.0
        for t in self.tokens:
            p_spam, p_ham = self._probabilities(t)
            if t in text_tokens:
                log_spam += math.log(p_spam); log_ham += math.log(p_ham)
            else:
                log_spam += math.log(1 - p_spam); log_ham += math.log(1 - p_ham)
        p_s = math.exp(log_spam); p_h = math.exp(log_ham)
        return p_s / (p_s + p_h)
```

## Связанные главы

- [[ch11-summary]] — предыдущая (метрики, split)
- [[ch12-summary]] — kNN как альтернатива
- [[ch06-summary]] — теорема Байеса из главы о вероятности
- [[ch21-summary]] — NLP и токенизация (та же логика)

## Краткие выводы

1. **`set` токенов, а не список** — порядок слов не важен для bag-of-words NB
2. **Сглаживание `k=0.5`** — критично; без него один пример с редким словом обнулит вероятность
3. **`log + sum`** вместо `product` — обязательно, иначе 1000 слов → underflow до нуля

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| Spam-классификатор | Фильтрация email, комментариев, SMS |
| Multinomial NB | Тематическая классификация документов |
| Bernoulli NB | Бинарные признаки (присутствие/отсутствие слова) |
| Laplace smoothing | Любая модель с подсчётом частот (n-grams, HMM) |
