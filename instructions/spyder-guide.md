# Spyder IDE

> Установка и использование. Установка окружения — в `setup-guide.md`.

---

## 1. Установка

Если Spyder не установлен в окружении `mlops`:

```powershell
conda activate mlops
conda install -n mlops spyder -y
```

Или через pip:

```powershell
python -m pip install spyder
```

---

## 2. Запуск

```powershell
# Активировать окружение
conda activate mlops

# Запустить
spyder
```

Или из меню **Пуск → Anaconda3 → Spyder** (запустит в базовой среде).

---

## 3. Интерфейс

```
┌──────────────────────────────────────────────────────────┐
│ File  Edit  Search  Source  Run  Debug  Consoles  Help  │  ← меню
├─────────────────────┬────────────────────────┬───────────┤
│ Editor (слева)      │ Variable Explorer     │           │
│                     │ ┌────────────────────┐ │           │
│ def dot(v, w):      │ │ Name  Type  Size  │ │           │
│   return sum(...)   │ │ x     list  3     │ │           │
│                     │ │ df    DataFrame 5  │ │           │
│ # F5 - запустить    │ └────────────────────┘ │           │
├─────────────────────┴────────────────────────┴───────────┤
│ IPython Console (внизу)                                  │
│ In [1]: import numpy as np                               │
│ In [2]: np.array([1,2,3]).mean()                          │
│ Out[2]: 2.0                                              │
├──────────────────────────────────────────────────────────┤
│ Plots / Help / History                                   │
└──────────────────────────────────────────────────────────┘
```

### Основные панели

| Панель | Что показывает |
|--------|---------------|
| **Editor** | Код `.py`-файлов |
| **Variable Explorer** | Все переменные текущей сессии (тип, размер, превью) |
| **IPython Console** | Интерактивный REPL с подсветкой вывода |
| **Plots** | Все matplotlib-графики (с историей) |
| **Help** | Документация под курсором |
| **File Explorer** | Дерево файлов (открыть через `View → Panes`) |

---

## 4. Настройка (один раз при первом запуске)

**Tools → Preferences:**

### Editor
- **Font:** Consolas, 11 (моноширинный, читаемый)
- **Show line numbers:** включено
- **Highlight current line:** включено
- **Tab width:** 4 (стандарт Python)
- **Convert tabs to spaces:** включено
- **Auto-indent:** включено

### IPython console
- **Graphics backend:** **Inline** (графики в консоли, не отдельные окна)
- **Automatic insertion of parentheses:** включено

### Run
- **Working directory:** **The directory of the file being executed**
- **Clear all variables before execution:** на свой вкус (удобно при отладке)

### Appearance
- **Theme:** Dark / Light (на вкус)
- **Syntax highlighting scheme:** Spyder Dark / Monokai

---

## 5. Рабочий процесс

### Способ A: Выполнить выделенное (основной)

1. Открыть файл: **File → Open** → выбрать `.py` из `scratch/` или `MLps/src/`
2. Написать код в редакторе
3. **Выделить** нужный блок (или просто кликнуть в строку)
4. **F9** — выполнить выделенное в IPython-консоли
5. Результат смотрим в Variable Explorer / Plots / Console

### Способ B: Запустить весь файл

1. Открыть файл
2. **F5** — выполнить скрипт целиком
3. Все переменные появятся в Variable Explorer
4. Графики — в Plots

### Способ C: Интерактивно в консоли

Курсор в **IPython Console** → писать код построчно:

```python
import pandas as pd
df = pd.read_csv('data/customers.csv')
df.head()
df['segment'].value_counts()
```

`Tab` — автодополнение. `Shift+Tab` внутри скобок — подсказка по аргументам.

---

## 6. Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| `F5` | Запустить весь файл |
| `F9` | Выполнить выделенное (или текущую строку) |
| `Ctrl+Enter` | Выполнить ячейку (если есть `#%%` разделители) |
| `Ctrl+S` | Сохранить |
| `Ctrl+Shift+S` | Сохранить как |
| `Ctrl+F` | Найти |
| `Ctrl+H` | Заменить |
| `Ctrl+G` | Перейти к строке |
| `Ctrl+/` | Закомментировать / раскомментировать |
| `Tab` | Автодополнение |
| `Shift+Tab` | Подсказка по функции |
| `Ctrl+I` | Помощь по объекту под курсором |
| `F2` | Переименовать переменную (рефакторинг) |

---

## 7. Cells (ячейки) — удобный аналог Jupyter

В Spyder можно разбить файл на ячейки через комментарии:

```python
#%%
import pandas as pd
df = pd.read_csv('data/customers.csv')

#%%
df.head()

#%%
df['segment'].value_counts().plot(kind='bar')
```

`Ctrl+Enter` — выполнить текущую ячейку. Удобно для exploratory-анализа, как в Jupyter, но с сохранением в `.py`-файле.

---

## 8. Отладка (debugger)

1. **Поставить breakpoint:** кликнуть слева от номера строки (появится красная точка)
2. **F5** — запустить в режиме отладки
3. Выполнение остановится на breakpoint
4. Использовать:

| Клавиша | Действие |
|---------|----------|
| `F10` | Step Over (следующая строка) |
| `F11` | Step Into (войти в функцию) |
| `Shift+F11` | Step Out (выйти из функции) |
| `Ctrl+Shift+F5` | Continue (до следующего breakpoint) |
| `Ctrl+Shift+F10` | Stop debugger |

Слева в панели **Debug** видно: текущую строку, локальные переменные, call stack.

---

## 9. Частые сценарии

### EDA на своих CSV

```python
import pandas as pd
import matplotlib.pyplot as plt

# F9 на каждом блоке
df = pd.read_csv('data/customers.csv')
df.info()                       # в Variable Explorer появится df
df.head()                       # в Console
df['segment'].value_counts().plot(kind='bar')   # в Plots
```

### Подключение книжного кода

```python
# После pip install -e ..\data-science-from-scratch
from scratch.linear_algebra import dot
from scratch.statistics import mean
from scratch.probability import normal_cdf

dot([1, 2, 3], [4, 5, 6])   # → 32
```

### Проверка своего модуля

```python
import sys
sys.path.insert(0, r'C:\Users\Selecty\Desktop\GIT\MLOps\src')

from loaders import load_customers, load_orders
from analytics import top_n
from visualizers import plot_distribution

df = load_customers()
print(df.head())
```

---

## 10. Решение проблем

| Проблема | Решение |
|----------|---------|
| `spyder` не находится | `conda activate mlops`, затем `spyder` |
| Spyder запускается в base, а не в mlops | Запускай через `conda run -n mlops spyder` или из `Anaconda Prompt (mlops)` |
| Графики не отображаются | `Preferences → IPython console → Graphics backend: Inline` |
| Variable Explorer пуст | Убедись, что код выполняется (F9), а не просто написан |
| Зависло ядро | **Consoles → Restart kernel** или `Ctrl+.` |
| Медленно работает | Закрой ненужные ноутбуки, не держи большие DataFrame в памяти |

---

## 11. Spyder vs Jupyter: что выбрать

| Задача | Лучший инструмент |
|--------|-------------------|
| Разведочный анализ данных (EDA) | **Jupyter** — быстрые эксперименты |
| Написание переиспользуемых функций | **Spyder** — автодополнение, рефакторинг |
| Отладка сложной логики | **Spyder** — debugger с breakpoints |
| Презентация результатов | **Jupyter** — текст + графики + код |
| Чтение/правка `.py`-файлов | **Spyder** — нормальный редактор |
| Обучающие материалы (книга) | **Jupyter** — пошаговое выполнение |

**Рекомендация:** используй оба. Jupyter для EDA и обучения, Spyder для разработки модулей в `src/`.
