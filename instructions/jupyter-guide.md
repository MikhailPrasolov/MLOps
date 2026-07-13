# Jupyter Notebook и JupyterLab

> Запуск и использование. Установка — в `setup-guide.md`.

---

## 1. Запуск

### Стандартный способ (из PowerShell)

```powershell
# Активировать окружение
conda activate mlops

# Перейти в папку проекта
cd C:\Users\Selecty\Desktop\GIT\MLOps

# Запустить Jupyter Notebook (классический интерфейс)
jupyter notebook

# Или JupyterLab (более современный)
jupyter lab
```

Откроется в браузере на `http://localhost:8888/`.

### Альтернативы

```powershell
# Запуск без браузера (только сервер)
jupyter notebook --no-browser

# Запуск в конкретной папке
jupyter notebook C:\Users\Selecty\Desktop\GIT

# Сменить порт
jupyter notebook --port 8889
```

### Из Anaconda Navigator

**Пуск → Anaconda3 → Anaconda Navigator → Jupyter Notebook / JupyterLab**

---

## 2. Jupyter Notebook vs JupyterLab

| | Notebook | Lab |
|---|----------|-----|
| Интерфейс | Классический, простой | Современный, табы, multi-panel |
| Несколько ноутбуков | ❌ | ✅ (вкладки) |
| Просмотр файлов | Только текущая папка | Полноценный браузер |
| Расширения | Ограничено | Полная поддержка |
| **Рекомендация** | Для начинающих | **Для ежедневной работы** |

---

## 3. Структура ноутбука

```
┌─────────────────────────────────────────────┐
│ File  Edit  View  Insert  Cell  Kernel  Help │  ← меню
├─────────────────────────────────────────────┤
│ [▶ Run]  [■ Stop]  [↻ Restart]              │  ← toolbar
├─────────────────────────────────────────────┤
│ In [1]: import pandas as pd                 │  ← code cell
│         df = pd.read_csv('data/...csv')     │
│ Out[1]:      id  name   segment             │  ← output
│         0   1  Hero   Consumer              │
├─────────────────────────────────────────────┤
│ ## Heading (Markdown)                       │  ← markdown cell
│         **Жирный**, *курсив*, `код`         │
├─────────────────────────────────────────────┤
│ In [2]: df.head()                            │
└─────────────────────────────────────────────┘
```

---

## 4. Горячие клавиши

### В режиме редактирования (внутри ячейки)

| Клавиша | Действие |
|---------|----------|
| `Shift+Enter` | Выполнить ячейку и перейти к следующей |
| `Ctrl+Enter` | Выполнить ячейку и остаться на ней |
| `Alt+Enter` | Выполнить ячейку и вставить новую снизу |
| `Tab` | Автодополнение |
| `Shift+Tab` | Подсказка по функции (сигнатура + docstring) |
| `Ctrl+Shift+-` | Разделить ячейку по курсору |
| `Esc` | Выйти в командный режим |

### В командном режиме (ячейка выделена рамкой)

| Клавиша | Действие |
|---------|----------|
| `A` | Вставить ячейку выше |
| `B` | Вставить ячейку ниже |
| `D` + `D` | Удалить ячейку |
| `M` | Переключить в Markdown |
| `Y` | Переключить в Code |
| `R` | Переключить в Raw |
| `X` | Вырезать ячейку |
| `C` | Копировать ячейку |
| `V` | Вставить ниже |
| `Shift+Up/Down` | Выделить несколько ячеек |
| `Enter` | Войти в режим редактирования |
| `H` | Показать все горячие клавиши |

---

## 5. Типы ячеек

| Тип | Назначение |
|-----|-----------|
| **Code** | Python-код (по умолчанию) |
| **Markdown** | Текст, заголовки, списки, формулы LaTeX, ссылки |
| **Raw** | Необработанный текст (для nbconvert) |

### Пример Markdown-ячейки

```markdown
## Заголовок 2-го уровня

**Жирный**, *курсив*, `код`, ~~зачёркнутый~~.

- Список
- Список

1. Нумерованный
2. Нумерованный

[Ссылка](https://example.com)

$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

```python
print("код внутри markdown")
```
```

---

## 6. Магические команды (начинаются с `%` или `%%`)

```python
# Время выполнения одной строки
%timeit sum(range(1000))

# Время выполнения всей ячейки
%%time
total = 0
for i in range(10**6):
    total += i

# Запуск внешнего скрипта
%run scripts/my_script.py

# Загрузка файла в ячейку
%load script.py

# Список переменных
%who
%whos

# Показать matplotlib-графики в ячейке
%matplotlib inline

# История команд
%history

# Помощь
%magic
```

---

## 7. Быстрый старт: первый ноутбук

1. **Запустить Jupyter:**
   ```powershell
   conda activate mlops
   cd C:\Users\Selecty\Desktop\GIT\MLOps
   jupyter lab
   ```

2. **Создать ноутбук:** `File → New → Notebook` → Python 3

3. **Переименовать:** `File → Rename` → `02-first-eda.ipynb`

4. **В первую ячейку:**
   ```python
   import pandas as pd
   import matplotlib.pyplot as plt
   
   df = pd.read_csv('data/customers.csv')
   df.head()
   ```

5. **Shift+Enter** — выполнить

6. **Добавить ячейку с графиком:**
   ```python
   df['segment'].value_counts().plot(kind='bar')
   plt.title('Распределение по сегментам')
   plt.show()
   ```

7. **Сохранить:** `Ctrl+S`

---

## 8. Полезные приёмы

### Просмотр DataFrame в Jupyter

```python
import pandas as pd
df = pd.read_csv('data/customers.csv')

df.head()       # первые 5 строк
df.tail()        # последние 5 строк
df.info()        # инфо о колонках и типах
df.describe()    # статистики
df.sample(5)     # случайные 5 строк
```

### Прогресс-бар для долгих операций

```python
from tqdm.notebook import tqdm
import time

for i in tqdm(range(100)):
    time.sleep(0.1)
```

### Волшебная команда %autoreload (для своих модулей)

```python
%load_ext autoreload
%autoreload 2

# Теперь изменения в src/*.py подхватываются без перезапуска ядра
from src.loaders import load_customers
```

### Сброс ядра (если всё зависло)

**Kernel → Restart** или `Ctrl+M` (в Lab) / `00` (в Notebook)

---

## 9. Экспорт ноутбука

```powershell
# В HTML
jupyter nbconvert --to html notebook.ipynb

# В PDF (нужен LaTeX)
jupyter nbconvert --to pdf notebook.ipynb

# В .py-скрипт
jupyter nbconvert --to script notebook.ipynb
```

Из интерфейса: **File → Download as → HTML/PDF/Python**
