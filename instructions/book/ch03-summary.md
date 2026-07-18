# Глава 3. Визуализация данных

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/visualization.py`

> **Контекст:** глава — про matplotlib как инструмент аргументации, а не декора. Вводит четыре базовых графика (line, bar, histogram, scatter) и подчёркивает антипаттерны: обрезанная ось Y, несравнимые оси.

## Ключевые концепции

- **Line chart** — тренды во времени (`plt.plot(xs, ys, color=..., marker=..., linestyle=...)`)
- **Bar chart** — сравнение категорий (`plt.bar`, `plt.xticks(range(...), labels)`)
- **Histogram** — бакетизация через `Counter(min(grade // 10 * 10, 90) for grade in grades)` — приём «100 → в 90-е»
- **Scatter** — `plt.scatter(x, y)` + `plt.annotate` для подписей точек
- **Bias-variance tradeoff** — три серии на одном графике + `plt.legend(loc=9)`

## Код

```python
from matplotlib import pyplot as plt
from collections import Counter

# 1. Линейный график (тренд)
plt.plot(years, gdp, color='green', marker='o', linestyle='solid')
plt.title("Nominal GDP"); plt.ylabel("Billions of $"); plt.show()

# 2. Гистограмма с бакетизацией
histogram = Counter(min(g // 10 * 10, 90) for g in grades)
plt.bar([x + 5 for x in histogram.keys()], histogram.values(), 10,
        edgecolor=(0, 0, 0))
plt.axis([-5, 105, 0, 5]); plt.show()

# 3. Scatter + подписи
plt.scatter(friends, minutes)
for label, fc, mc in zip(labels, friends, minutes):
    plt.annotate(label, xy=(fc, mc), xytext=(5, -5),
                 textcoords='offset points')

# 4. ⚠️ Антипаттерн: обрезанная ось Y
plt.axis([2016.5, 2018.5, 499, 506])   # 1% разница выглядит огромной
plt.axis([2016.5, 2018.5, 0, 550])     # правильный вариант

# 5. Сравнимость осей — критично для scatter
plt.axis("equal")    # без неё искажается корреляция визуально
```

## Связанные главы

- [[ch02-summary]] — предыдущая
- [[ch04-summary]] — следующая
- [[ch05-summary]] — статистика поверх графиков

## Краткие выводы

1. **`plt.axis("equal")`** — обязательно для scatter двух метрик одного масштаба
2. **Никогда не обрезайте ось Y с нулём** — это пропаганда, не визуализация
3. **`Counter(min(grade // 10 * 10, 90))`** — стандартный приём бакетизации с «приклеиванием» 100 к 90-м

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `plt.bar` + `xticks` | Категориальные отчёты, KPI |
| `Counter` бакетизация | Построение гистограмм вручную |
| Scatter + `annotate` | Разметка выбросов, объяснение точек |
| `plt.axis("equal")` | Любые scatter-визуализации |
| Bias-variance chart | Объяснение компромисса сложности модели |
