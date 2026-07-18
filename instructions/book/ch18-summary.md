# Глава 18. Нейронные сети

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/neural_networks.py`

> **Контекст:** глава показывает, что нейросеть — это стек логистических регрессий (neuron), скомпонованных в слои. Два культовых примера: **XOR** (доказывает, что одного нейрона мало — нужен скрытый слой) и **FizzBuzz** (шуточный, но учит 10-битному входу → 4-классовому выходу).

## Ключевые концепции

- **Perceptron** — `step(dot(w, x) + bias)`; может выучить AND/OR/NOT, **но не XOR**
- **Sigmoid neuron** — заменяем step на `σ(z) = 1/(1+e^-z)` → дифференцируемость
- **`feed_forward(network, input)`** — проход по слоям; bias добавляется как `+[1]` к входу
- **XOR — двухслойная сеть** — 2 нейрона в скрытом слое: AND + OR-NOT
- **Backprop** — `output * (1 - output) * (output - target)` для дельты; затем по цепочке назад
- **`binary_encode(x)` → `fizz_buzz_encode(y)`** — 10 бит → 4 класса через 25 скрытых нейронов

## Код

```python
import math
from scratch.linear_algebra import dot, Vector

def sigmoid(t): return 1 / (1 + math.exp(-t))

def neuron_output(weights, inputs):
    """weights включает bias, inputs включает 1"""
    return sigmoid(dot(weights, inputs))

def feed_forward(neural_network, input_vector):
    outputs = []
    for layer in neural_network:
        input_with_bias = input_vector + [1]    # bias
        output = [neuron_output(neuron, input_with_bias) for neuron in layer]
        outputs.append(output)
        input_vector = output                  # выход → вход следующего слоя
    return outputs

def sqerror_gradients(network, input_vector, target_vector):
    hidden_outputs, outputs = feed_forward(network, input_vector)
    # Дельта выходного слоя
    output_deltas = [output * (1 - output) * (output - target)
                     for output, target in zip(outputs, target_vector)]
    # Градиенты выходного слоя
    output_grads = [[d * h for h in hidden_outputs + [1]]
                    for d in output_deltas]
    # Дельта скрытого слоя через backprop
    hidden_deltas = [hidden * (1 - hidden) *
                      dot(output_deltas, [n[i] for n in network[-1]])
                     for i, hidden in enumerate(hidden_outputs)]
    # Градиенты скрытого слоя
    hidden_grads = [[d * x for x in input_vector + [1]]
                    for d in hidden_deltas]
    return [hidden_grads, output_grads]

# XOR — ручная сеть:
xor_network = [[ [20., 20, -30],     # AND-нейрон
                 [20., 20, -10]],    # OR-нейрон
                [[-60., 60, -30]]]   # "2nd but not 1st"
# feed_forward(xor_network, [1, 0])[-1][0] > 0.99 — XOR!
```

## Связанные главы

- [[ch17-summary]] — предыдущая
- [[ch19-summary]] — следующая (глубокое обучение = та же идея, но слоёв > 2)
- [[ch16-summary]] — neuron ≈ логрегрессия
- [[ch08-summary]] — backprop = GD + chain rule

## Краткие выводы

1. **XOR требует скрытого слоя** — главный мотиватор для многослойных сетей
2. **Bias подаётся как фиктивный вход `+[1]`** — стандартный трюк, упрощает формулы
3. **Backprop = chain rule + GD** — никакой магии, просто последовательное применение производных

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| feed_forward | Прямой проход в любой нейросети |
| sqerror_gradients | Backprop вручную для понимания (PyTorch делает то же) |
| XOR-пример | Доказательство необходимости скрытых слоёв |
| sigmoid | Активация для бинарного выхода; внутри скрытых слоёв чаще ReLU/Tanh |
