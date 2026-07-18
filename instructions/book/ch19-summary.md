# Глава 19. Глубокое обучение

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/deep_learning.py`

> **Контекст:** «правильная» реализация нейросети в ООП-стиле: `Layer` базовый класс с `forward`/`backward`/`params`/`grads`, наследники `Linear`, `Sigmoid`, `Tanh`, `Relu`, `Dropout`. Глава обучает глубокую сеть на **MNIST** (60000 изображений 28×28 → 10 цифр) и вводит центральный приём — **`SoftmaxCrossEntropy` loss**.

## Ключевые концепции

- **`Layer` абстракция** — `forward(input)`, `backward(grad)`, `params()`, `grads()` — контракт для всех слоёв
- **`Tensor = list`** — вложенные списки любой размерности
- **`Linear(input_dim, output_dim)`** — `y = Wx + b`; сохраняет `self.input` для backward
- **`Sequential(layers)`** — контейнер; forward по порядку, backward в обратном порядке
- **Активации** — `Sigmoid` (бинарный выход), `Tanh` (скрытые слои), `Relu` (быстрее Tanh, без vanishing gradient)
- **`SoftmaxCrossEntropy`** — `(p - y)` — самый простой градиент в DL; категориальная кроссэнтропия
- **`Dropout(p)`** — зануление `p` доли входов в train-режиме; масштабирование в eval-режиме
- **Оптимизаторы** — `GradientDescent`, `Momentum` (бегущее среднее градиентов)
- **Xavier init** — `variance = len(dims) / sum(dims)` — стабилизирует дисперсию

## Код

```python
import math, random
from typing import List

class Layer:
    def forward(self, x):  raise NotImplementedError
    def backward(self, g):  raise NotImplementedError
    def params(self):       return ()
    def grads(self):        return ()

class Linear(Layer):
    def __init__(self, in_d, out_d, init='xavier'):
        self.w = random_tensor(out_d, in_d, init=init)
        self.b = random_tensor(out_d, init=init)
    def forward(self, x):
        self.input = x
        return [dot(x, self.w[o]) + self.b[o] for o in range(self.output_dim)]
    def backward(self, grad):
        self.w_grad = [[self.input[i] * grad[o]
                        for i in range(self.input_dim)]
                       for o in range(self.output_dim)]
        self.b_grad = grad
        return [sum(self.w[o][i] * grad[o] for o in range(self.output_dim))
                for i in range(self.input_dim)]

class SoftmaxCrossEntropy(Loss):
    def loss(self, predicted, actual):
        probs = softmax(predicted)
        return -sum(math.log(p + 1e-30) * a for p, a in zip(probs, actual))
    def gradient(self, predicted, actual):
        return [p - a for p, a in zip(softmax(predicted), actual)]

# MNIST классификатор: Linear(784, 30) → Tanh → Linear(30, 10) → SoftmaxCrossEntropy
# С dropout и momentum optimizer — лучше 95% accuracy
```

## Связанные главы

- [[ch18-summary]] — предыдущая (ручной backprop)
- [[ch20-summary]] — следующая (unsupervised)
- [[ch21-summary]] — NLP на рекуррентных сетях

## Краткие выводы

1. **`Layer` абстракция** — единый контракт делает композицию тривиальной (`Sequential`)
2. **`SoftmaxCrossEntropy.gradient = p - y`** — самый «приятный» градиент в ML
3. **Dropout + Momentum** — два главных трюка 2014-2017; сегодня Adam + BatchNorm

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `Layer` / `Sequential` | Архитектура PyTorch/Keras/JAX под капотом |
| `Linear` + активация | Любой MLP, табличные данные, простые задачи |
| `SoftmaxCrossEntropy` | Multi-class классификация |
| `Dropout` | Регуляризация нейросетей |
| MNIST pipeline | Baseline для CV-задач |
