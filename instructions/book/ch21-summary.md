# Глава 21. Обработка естественного языка

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/nlp.py`

> **Контекст:** глава про «классическое» NLP до трансформеров — n-граммы, грамматики, **LDA-топик моделирование** и **word2vec-эмбеддинги** через свою нейросеть. Самый большой файл в книге (700+ строк) — здесь действительно много идей.

## Ключевые концепции

- **N-граммы** — `defaultdict(list)` с переходами `prev → [next_candidates]`; генерация текста через `random.choice`
- **Грамматики** — `_S → _NP _VP`; `expand()` рекурсивно заменяет нетерминалы
- **Gibbs sampling** — для топик-моделирования; каждый шаг: убрать текущее назначение, выбрать новое по `p_topic_given_doc · p_word_given_topic`
- **LDA (Latent Dirichlet Allocation)** — каждый документ = смесь тем, каждая тема = распределение слов
- **Cosine similarity** — `dot(a, b) / sqrt(dot(a,a) · dot(b,b))` ∈ [-1, 1]
- **`Vocabulary`** — `word ↔ id`; `one_hot_encode(word)` → вектор
- **Word embeddings** — `Embedding` layer учит плотный вектор на слово (word2vec-подобный подход)
- **`sample_from(weights)`** — выбор индекса с вероятностями пропорциональными `weights`

## Код

```python
from collections import defaultdict, Counter
import random, re, math

# 1. N-граммы (bigram)
transitions = defaultdict(list)
for prev, current in zip(document, document[1:]):
    transitions[prev].append(current)

def generate_using_bigrams():
    current = "."
    result = []
    while True:
        current = random.choice(transitions[current])
        result.append(current)
        if current == ".":
            return " ".join(result)

# 2. Грамматика
grammar = {
    "_S":  ["_NP _VP"],
    "_NP": ["_N", "_A _NP _P _A _N"],
    "_VP": ["_V", "_V _NP"],
    "_N":  ["data science", "Python", "regression"],
    "_A":  ["big", "linear", "logistic"],
}

def expand(grammar, tokens):
    for i, token in enumerate(tokens):
        if token[0] != "_": continue  # терминал
        replacement = random.choice(grammar[token])
        if replacement[0] == "_":
            tokens = tokens[:i] + replacement.split() + tokens[i+1:]
        else:
            tokens[i] = replacement
        return expand(grammar, tokens)
    return tokens

# 3. LDA через Gibbs sampling
def p_topic_given_document(topic, d, alpha=0.1):
    return (document_topic_counts[d][topic] + alpha) / (document_lengths[d] + K*alpha)

def p_word_given_topic(word, topic, beta=0.1):
    return (topic_word_counts[topic][word] + beta) / (topic_counts[topic] + W*beta)

# На каждой итерации для каждого (doc, word):
#   убираем вклад текущей темы → выбираем новую тему → возвращаем вклад

# 4. Cosine similarity
def cosine_similarity(v1, v2):
    return dot(v1, v2) / math.sqrt(dot(v1, v1) * dot(v2, v2))
```

## Связанные главы

- [[ch20-summary]] — предыдущая (кластеризация документов = LDA light)
- [[ch22-summary]] — следующая (графы)
- [[ch13-summary]] — NB на текстах
- [[ch19-summary]] — нейросеть как backbone для word2vec

## Краткие выводы

1. **N-граммы дают «локальный» язык** — работает для коротких текстов, но не улавливает дальние зависимости
2. **LDA — unsupervised-метод**; количество тем `K` — гиперпараметр
3. **Word embeddings** — основа современного NLP; в книге показано через свой `Embedding` слой, сегодня это `word2vec`/`BERT`

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| N-граммы | Автодополнение, простые чат-боты, статистические spell-checker'ы |
| Грамматики | Парсинг команд DSL, простые конфиги |
| LDA | Тематическое моделирование коллекций документов |
| Cosine similarity | Поиск похожих текстов, рекомендации |
| Embedding | Любая задача NLP — baseline перед трансформерами |
