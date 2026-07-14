# Работа AI-агента с Jupyter-ноутбуками

> Протокол совместной работы с AI-агентом (Kilo, OpenCode) над `.ipynb` файлами.
> Запуск Jupyter — в `jupyter-guide.md`. Установка — в `setup-guide.md`.

---

## 1. Почему нельзя просто «открыть и править»

`.ipynb` — это **JSON**, а не текст. AI-агент работает с ним через программную правку (PowerShell + `ConvertFrom-Json` / `ConvertTo-Json`).

**Главная ловушка — гонка записи:**

```
Ты (Jupyter)         AI-агент
─────────────────     ──────────────────
Читаешь ноутбук
Редактируешь ячейку
                     Пишет в .ipynb через Write
Ctrl+S → Jupyter
перезаписывает файл  ❌ мои правки затёрты
```

В этой сессии так уже **потерялись** setup-ячейка `DATA_DIR` и 6 замен путей `read_csv`. После `Run All` обнаружилось, что агент «не помнит», что делал минуту назад. На самом деле Jupyter просто перезатёр.

---

## 2. Протокол «закрыть → править → открыть»

Единственный надёжный путь для больших правок:

| Шаг | Кто | Действие |
|-----|-----|----------|
| 1 | Ты | **Сохрани** ноутбук (`Ctrl+S`) |
| 2 | Ты | **Закрой** ноутбук в Jupyter / Lab / VS Code |
| 3 | Ты | Скажи агенту, что менять |
| 4 | Агент | Читает `.ipynb` как JSON, правит через PS, сохраняет, проверяет |
| 5 | Агент | Сообщает, что готово |
| 6 | Ты | **Открой** ноутбук заново |
| 7 | Ты | `Kernel → Restart & Run All` |
| 8 | Ты | Если есть ошибки — скинь traceback агенту |

**Правило:** пока агент правит файл, у тебя Jupyter **закрыт**. Никаких Ctrl+S посередине.

---

## 3. Параллельная работа через `.py` (рекомендуется)

Чтобы вообще не было гонки, держи **копию ноутбука в виде `.py`** и работай с ней.

### Конвертация `.ipynb` → `.py`

Агент может сконвертировать одной командой PowerShell (без зависимостей):

```powershell
# Читает .ipynb как JSON, пишет .py с маркерами # %%
# (полный скрипт — в jupyter-agent-workflow/scripts/ipynb-to-py.ps1)
& "C:\Users\Selecty\Desktop\GIT\MLOps\instructions\jupyter-agent-workflow\scripts\ipynb-to-py.ps1" `
  -InputIpynb "C:\Users\Selecty\Desktop\GIT\MLOps\notebooks\01-pandas-basics.ipynb" `
  -OutputPy   "C:\Users\Selecty\Desktop\GIT\MLOps\notebooks\01-pandas-basics.py"
```

Либо стандартный `nbconvert` (если установлен):

```powershell
jupyter nbconvert --to script "01-pandas-basics.ipynb" --output 01-pandas-basics
```

### Формат `.py` — маркеры `# %%`

```python
# -*- coding: utf-8 -*-
# Заголовок файла

# %%
import pandas as pd

# %% [markdown]
# # Заголовок раздела
# Текст, который в Jupyter был бы markdown-ячейкой

# %%
df = pd.read_csv(DATA_DIR / 'orders.csv')
df.head()
```

- **`# %%`** — граница code-ячейки (понимает Spyder, VS Code, Jupytext)
- **`# %% [markdown]`** — markdown-ячейка
- Открывается в **Spyder** как ноутбук (видны ячейки в Editor)
- В **VS Code** — `# %%` запускается через `# %%` cell в Jupyter extension
- В **Jupyter / Lab** — открой `.py` напрямую (Jupyter >= 7 / Lab >= 4) или через Jupytext

### Workflow с `.py`

```
┌──────────────────────────────────────────┐
│ .ipynb  ←───  run/visualize  ────  .py  │
│   ↑                                     │
│   │                                     │
│   └── nbconvert / ipynb-to-py.ps1 ──────┘
│                                         │
│  (агент правит ТОЛЬКО .py)              │
│  (ты читаешь/правишь .ipynb в Jupyter)  │
└──────────────────────────────────────────┘
```

**Плюсы `.py`:**
- ✅ Нет гонки с Jupyter (агент трогает только `.py`)
- ✅ Видно `git diff` — нормальный текст
- ✅ Линтер, форматтеры, type-checker работают
- ✅ Spyder воспринимает `# %%` как ячейки

**Минусы `.py`:**
- ❌ Теряются `Out[N]` (выводы ячеек)
- ❌ Теряются `execution_count`
- ❌ Magic-команды Jupyter работают, но при конвертации могут ломаться
- ❌ Markdown-разметка становится `# comment`

### Когда что использовать

| Задача | Файл |
|--------|------|
| Запустить / отладить / посмотреть выводы | `.ipynb` в Jupyter |
| Передать агенту на правку | `.py` (или `git diff` патч) |
| Code review | `.py` через `git diff` |
| Сохранить результаты эксперимента | `.ipynb` (там выводы) |
| Параллельная работа агент + человек | оба + `ipynb-to-py` синхронизация |

---

## 4. Как агент работает с `.ipynb` технически

### 4.1 Чтение

```powershell
$raw = [System.IO.File]::ReadAllText($path)
$json = $raw | ConvertFrom-Json
$json.cells      # массив всех ячеек
$json.cells[0].source    # source как массив строк
$json.cells[0].outputs   # массив выводов (с traceback, если был)
$json.cells[0].execution_count   # In[N]
```

### 4.2 Правка

Агент **не использует** `Edit` tool для JSON-файлов — это ненадёжно (нужен exact-match по байтам). Вместо этого:

```powershell
# 1. Прочитать
$json = [System.IO.File]::ReadAllText($path) | ConvertFrom-Json

# 2. Изменить конкретную ячейку по содержимому
foreach ($c in $json.cells) {
    if (($c.source -join "") -match "read_csv.*orders\.csv - orders") {
        $c.source = @("df = pd.read_csv(DATA_DIR / 'orders.csv')", "")
    }
}

# 3. Сохранить (depth ≥ 20 обязателен!)
$out = $json | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($path, $out, [System.Text.Encoding]::UTF8)
```

### 4.3 Верификация после правки

Агент всегда проверяет:
- `ConvertFrom-Json` парсит без ошибок
- `cells.Count` совпадает с ожидаемым
- Поиск плохих строк (например, `grep "/Users/mihail"` → должно быть 0)
- Если правка была в конкретной ячейке — напечатать её source для подтверждения

### 4.4 Потенциальные грабли

| Грабля | Симптом | Решение |
|--------|---------|---------|
| `ConvertTo-Json -Depth 4` (по умолчанию) | Обрезает вложенные `outputs` → JSON ломается | Всегда `-Depth 20` |
| `ConvertTo-Json` без `-Compress` | Переформатирует JSON, но файл растёт (~в 2 раза) | Либо принять, либо прогнать `jq` |
| Jupyter перезатёр правки | После `Ctrl+S` файл вернулся к старой версии | Закрыть Jupyter **до** правок |
| Edit tool exact-match fail | «oldString not found» | Не использовать Edit для `.ipynb`, только PS-JSON |
| `\r\n` vs `\n` | Windows-окончания строк ломают сравнение | Читать через `ReadAllText`, не `ReadAllLines` |
| **BOM + CRLF в `.ipynb`** | `NotJSONError: Notebook does not appear to be JSON: '\ufeff{\r\n ...'` | Использовать `UTF8Encoding($false)` при записи |

### 4.5 Критично: как НЕ сломать `.ipynb` кодировкой

**Проблема:** `[System.IO.File]::WriteAllText` в PowerShell по умолчанию пишет **UTF-8 с BOM** (`EF BB BF`). Плюс `ConvertTo-Json` использует **CRLF** (`\r\n`). Вместе это даёт `\ufeff{\r\n ...` в начале файла → Jupyter не парсит.

**Правильный шаблон записи:**

```powershell
# Читать можно как угодно
$raw = [System.IO.File]::ReadAllText($path)
$json = $raw | ConvertFrom-Json

# ... правки ...

# Писать ТОЛЬКО так:
$out = $json | ConvertTo-Json -Depth 20
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $out, $utf8NoBom)
```

**Если файл уже сломан** (агент записал с BOM):

```powershell
$bytes = [System.IO.File]::ReadAllBytes($path)
if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    $bytes = $bytes[3..($bytes.Length-1)]   # strip BOM
}
$text = [System.Text.Encoding]::UTF8.GetString($bytes) -replace "`r`n","`n" -replace "`r","`n"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $text, $utf8NoBom)
```

**Проверка после любой записи:**

```powershell
$firstBytes = [System.IO.File]::ReadAllBytes($path)[0..2]
if ($firstBytes[0] -eq 0xEF) { Write-Warning "BOM still present!" }
try { ([System.IO.File]::ReadAllText($path) | ConvertFrom-Json).cells.Count }
catch { Write-Error "JSON broken: $_" }
```

---

## 5. Чеклист перед большой правкой

Агент должен задать / ты должен подтвердить:

- [ ] Jupyter **закрыт** (или хотя бы ноутбук закрыт)
- [ ] Согласовано **что** именно меняется (список ячеек / строк)
- [ ] Агент знает, какие ячейки — code, какие — markdown
- [ ] Если будут удаления — агент спрашивает разрешения (по умолчанию **не удаляет**)
- [ ] После правки — `Kernel → Restart & Run All` и проверка, что всё ещё работает

---

## 6. Быстрые команды

### Конвертировать все ноутбуки проекта в `.py`

```powershell
Get-ChildItem "C:\Users\Selecty\Desktop\GIT\MLOps\notebooks\*.ipynb" | ForEach-Object {
    $py = $_.FullName -replace '\.ipynb$', '.py'
    # вызвать ipynb-to-py.ps1
}
```

### Сравнить .ipynb и .py на sync

```powershell
# Показывает ячейки, которые отличаются между двумя файлами
& "C:\...\instructions\jupyter-agent-workflow\scripts\diff-ipynb-py.ps1" `
  -Ipynb "01-pandas-basics.ipynb" -Py "01-pandas-basics.py"
```

### Восстановить .ipynb из .py

```powershell
# Вариант 1: jupytext (если установлен)
jupytext --to notebook "01-pandas-basics.py"

# Вариант 2: открыть .py в Jupyter 7+ / Lab 4+ (понимают нативно)
jupyter lab
# File → Open from Path → 01-pandas-basics.py
```

---

## 7. Генерация корректных `.ipynb` с нуля

> **Когда нужно:** обучающие ноутбуки по книге, туториалы, воспроизводимые примеры. Не «прогнал код и забыл», а **читаемая история с выполняемыми ячейками**.

### 7.1. Почему `jupytext --to notebook` в **light format** ломает ноутбуки

Если `.py` содержит обучающие комментарии в духе:

```python
def friends_of_friends(user):
    ...

# Пример: для Hero (id=0) — friends_of_friends({'id': 0}) = {3: 2}

def mean(xs): ...

# assert 7.33 < mean(num_friends) < 7.34
```

→ jupytext light format превращает строки `# Пример:` и `# assert X == Y` в **markdown-ячейки**. Функции определяются, но **никогда не вызываются**. Ноутбук в Jupyter выглядит «зелёным», никаких ошибок — но и никакого вывода. Тихая поломка.

**Симптомы:**

- `cells[5]` — markdown «Пример: для Hero...»
- `cells[7]` — markdown «assert 7.33 < mean(...)»
- `mean(num_friends)` нигде не вызывается → ничего не считается
- `plt.savefig()` сработал, но без `display(Image(...))` графики не встроены

Подробный разбор — в `30_Resources/Insights/jupytext-light-format-breaks-executable-comments.md` (Obsidian vault).

### 7.2. Два корректных подхода

| Подход | Когда | Sync | Контроль |
|--------|-------|------|----------|
| **percent format** (`# %%`) | Хочешь редактировать и `.py`, и `.ipynb` | ✅ автоматический через `jupytext --sync` | Средний (маркеры сам расставляешь) |
| **`nbformat` напрямую** | Строишь ноутбук программно (обучающие, воспроизводимые) | ❌ одна сторона (`.ipynb`) | Полный (каждая ячейка в коде) |

**Для обучающих ноутбуков (книга, туториал) рекомендую `nbformat`** — гарантирует, что вызовы будут.

### 7.3. Шаблон: `nbformat` для обучающего ноутбука

Каждая **секция = 3 ячейки** (markdown → def → call):

```python
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

nb = new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3 (mlops)",
                   "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.13"},
}

cells = []

# --- 1. Заголовок ---
cells.append(new_markdown_cell(
    "# Название ноутбука\n\n"
    "**Книга:** ...\n"
    "**Главы:** X + Y\n"
))

# --- 2. Setup ---
cells.append(new_code_cell(
    "import math\n"
    "import os\n"
    "import matplotlib\n"
    "matplotlib.use('Agg')   # headless backend для скриптов и CI\n"
    "import matplotlib.pyplot as plt\n"
    "from IPython.display import Image, display\n"
))

# --- 3. СЕКЦИЯ: X.Y ---
cells.append(new_markdown_cell(
    "### X.Y. Название секции\n\n"
    "Краткое пояснение (1-2 предложения)."
))

# Ячейка-определение
cells.append(new_code_cell(
    "def my_function(x):\n"
    "    \"\"\"Docstring.\"\"\"\n"
    "    return x * 2\n"
))

# Ячейка-вызов + проверка
cells.append(new_code_cell(
    "result = my_function(5)\n"
    "print(f\"my_function(5) = {result}\")\n"
    "\n"
    "assert result == 10\n"
    "print(\"[OK] X.Y\")\n"
))

# --- 4. ГРАФИКИ ---
cells.append(new_code_cell(
    "fig, ax = plt.subplots()\n"
    "ax.plot([1, 2, 3], [1, 4, 9])\n"
    "ax.set_title('Example')\n"
    "\n"
    "fpath = os.path.join(FIG_DIR, 'example.png')\n"
    "plt.savefig(fpath, dpi=80, bbox_inches='tight')\n"
    "plt.gca().clear()\n"
    "display(Image(filename=fpath))   # ← КРИТИЧНО для встраивания\n"
))

nb["cells"] = cells
nbf.write(nb, "out.ipynb")
```

### 7.4. Графики: `plt.savefig` + `display(Image(...))` (всегда оба)

```python
from IPython.display import Image, display

# matplotlib.use('Agg') ОБЯЗАТЕЛЬНО для headless-режима
# (если запускаешь через `jupyter nbconvert --execute`)

fpath = os.path.join(FIG_DIR, "plot.png")
plt.savefig(fpath, dpi=80, bbox_inches="tight")
plt.gca().clear()            # очистить ось, чтобы следующий график не наложился
display(Image(filename=fpath))   # ← без этого в ноутбуке будет пусто
```

**Где сохранять фигуры:**

```python
import os
FIG_DIR = os.path.join(os.getcwd(), "_figures")   # рядом с .ipynb
os.makedirs(FIG_DIR, exist_ok=True)
```

### 7.5. Шаблон: percent format (`# %%`)

Если всё-таки хочешь sync `.py` ↔ `.ipynb`:

```python
# %% [markdown]
# # Заголовок ноутбука
# Краткое описание

# %%
import math

# %% [markdown]
# ## Секция 1

# %%
def foo(x):
    """Определение."""
    return x + 1

# %%
# Ячейка-вызов (отдельный `# %%` блок)
result = foo(5)
print(result)
assert result == 6

# %%
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.show()    # в .ipynb отобразится inline
```

**Конвертация:**

```bash
# Установить jupytext (один раз)
pip install jupytext

# Установить формат и сконвертировать
jupytext --set-formats py:percent,ipynb my_notebook.py

# После правок — синхронизировать
jupytext --sync my_notebook.py
```

⚠️ **Не используй jupytext light format** (`jupytext --to notebook file.py` без `--from`) для обучающих ноутбуков — см. §8.1.

### 7.6. Валидация: всегда `jupyter nbconvert --execute`

```powershell
conda activate mlops
jupyter nbconvert --to notebook --execute my_notebook.ipynb `
                  --output my_notebook.ipynb
```

- Если есть `AssertionError`, `KeyError`, `NameError` — увидишь traceback в выводе
- Если всё OK — файл перезаписан с outputs (size растёт в ~2-4 раза)
- Занимает 10-60 сек в зависимости от объёма

### 7.7. Конкретный кейс: главы 1-5 книги «Data Science с нуля»

В `MLOps/notebooks/Data Science/`:

- `01-introduction-and-python-crash-course.ipynb` (54 cells) — гл. 1+2
- `02-visualization-linear-algebra-statistics.ipynb` (50 cells, 10 PNG) — гл. 3+4+5

**Как они были сделаны (и почему именно так):**

1. **Сначала через `jupytext`** (light format) — **получили сломанные** ноутбуки (см. §8.1)
2. **Перестроены через `nbformat`** в скрипте `build_nb0X.py` (полный контроль)
3. **Каждая секция:** markdown (пояснение) → code (def) → code (вызов+print+assert)
4. **Графики:** `plt.savefig()` + `display(Image(filename=...))` — встроены
5. **Валидация:** `jupyter nbconvert --execute` прошёл без ошибок

**Два бага, которые поймала валидация:**

1. `evens_below_20` (генератор) — после `sum()` исчерпывается → `list(...)`
2. `num_friends` (список) — моя копипаста имела 17 ones / 24 sixes (только 6 как mode), а книга — 22 / 22 (modes `{1, 6}`). Заменил на эталон из `scratch/statistics.py`.

### 7.8. Чеклист перед коммитом обучающего ноутбука

- [ ] Каждая функция **вызывается** в отдельной code-ячейке
- [ ] Все `assert` — **реальный код**, не комментарии
- [ ] Каждый `plt.savefig` сопровождается `display(Image(...))`
- [ ] `Kernel → Restart & Run All` отрабатывает без ошибок
- [ ] Размер ноутбука >50 КБ (значит outputs сохранены, графики встроены)
- [ ] Frontmatter `## Итог` в конце с ссылками на следующие главы/темы

---

## 8. Резюме

| Сценарий | Что делать |
|----------|------------|
| Большая правка > 5 ячеек | Закрыть Jupyter → агент правит `.ipynb` напрямую → открыть → Run All |
| Параллельная работа | Держать `.py`-копию, агент правит только её, ты — `.ipynb` |
| Мелкая правка (1-2 ячейки) | Скинуть текст ячейки агенту, он скажет, что вставить |
| Проверить, что не сломалось | `Kernel → Restart & Run All`, кинуть агенту traceback |
| Потерял правки агента | Спросить: «покажи что ты менял» — он прочитает JSON и повторит |
| **Строишь обучающий ноутбук с нуля** | **Сразу `nbformat` (§7). Не `jupytext --to notebook` в light format!** |

**Золотое правило:** пока агент правит файл — Jupyter закрыт. Это сэкономит 30 минут на отладку «почему у меня опять старый код».
