# Инструкция по установке и настройке

## 1. Скачать и установить Anaconda

**Ссылка:** https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Windows-x86_64.exe
(размер ~700 МБ, версия 2025.12, Python 3.12)

**Установка:**
1. Запустить скачанный `Anaconda3-2025.12-2-Windows-x86_64.exe`
2. Нажать **Next >**
3. Принять лицензию (**I Agree**)
4. Выбрать **Just Me** (рекомендуется)
5. Папка установки: оставить по умолчанию `C:\Users\Selecty\anaconda3`
6. **ВАЖНО:** отметить галочку **Add Anaconda3 to my PATH environment variable** (иначе команды не будут работать из терминала)
7. Нажать **Install** (5–10 минут)
8. После завершения — **Next > Finish**

**Что внутри:**
- Python 3.12
- numpy, pandas, scipy, matplotlib, seaborn
- Jupyter Notebook / JupyterLab
- Spyder IDE
- scikit-learn
- ~300+ предустановленных пакетов

---

## 2. Проверка установки

После установки **открыть НОВЫЙ терминал PowerShell** (обязательно, чтобы PATH обновился):

```powershell
# Проверить Python
python --version
# → Python 3.12.x

# Проверить conda
conda --version
# → conda 24.x.x

# Проверить ключевые пакеты
python -c "import numpy; print(f'numpy {numpy.__version__}')"
python -c "import pandas; print(f'pandas {pandas.__version__}')"
python -c "import sklearn; print(f'scikit-learn {sklearn.__version__}')"
```

---

## 3. Настройка окружения для проектов

### 3.1. Виртуальное окружение для MLOps

```powershell
cd C:\Users\Selecty\Desktop\GIT\MLOps

# Создать виртуальное окружение через conda (рекомендуется)
conda create --name mlops python=3.12 numpy pandas matplotlib seaborn scikit-learn jupyter spyder -y

# Активировать
conda activate mlops

# Установить доп. зависимости из requirements.txt книги
pip install -r ..\data-science-from-scratch\requirements.txt

# Установить книжный пакет scratch (чтобы import работал)
pip install -e ..\data-science-from-scratch
```

### 3.2. Или через стандартный venv (если conda не ставится)

```powershell
cd C:\Users\Selecty\Desktop\GIT\MLOps

# Создать venv
python -m venv .venv

# Активировать
.venv\Scripts\Activate.ps1

# Установить всё через pip
pip install --upgrade pip setuptools wheel
pip install numpy pandas matplotlib seaborn scikit-learn jupyter spyder
pip install -r ..\data-science-from-scratch\requirements.txt
pip install -e ..\data-science-from-scratch
```

---

## 4. Запуск Jupyter Notebook

### Из командной строки

```powershell
# Способ 1 — из папки MLOps (ноутбуки сохранятся рядом)
cd C:\Users\Selecty\Desktop\GIT\MLOps
conda activate mlops
jupyter notebook

# Способ 2 — из корня GIT (будут видны оба репозитория)
cd C:\Users\Selecty\Desktop\GIT
jupyter notebook
```

После запуска откроется браузер с файловым менеджером Jupyter:
- Заходишь в `MLOps/notebooks/` для своих экспериментов
- Заходишь в `data-science-from-scratch/scratch/` для кода книги

### JupyterLab (более современный интерфейс)

```powershell
jupyter lab
```

### Горячие клавиши Jupyter

| Клавиша | Действие |
|---------|----------|
| `Shift+Enter` | Выполнить ячейку и перейти к следующей |
| `Ctrl+Enter` | Выполнить ячейку и остаться на ней |
| `Alt+Enter` | Выполнить ячейку и вставить новую снизу |
| `Esc` + `A` | Вставить ячейку выше |
| `Esc` + `B` | Вставить ячейку ниже |
| `Esc` + `D` + `D` | Удалить ячейку |
| `Esc` + `M` | Переключить в Markdown |
| `Esc` + `Y` | Переключить в Code |
| `Tab` | Автодополнение (внутри ячейки) |
| `Shift+Tab` | Подсказка по функции |

---

## 5. Запуск Spyder

```powershell
# Из командной строки
conda activate mlops
spyder
```

Или через меню **Пуск → Anaconda3 → Spyder**.

**Настройка Spyder:**
1. `Tools → Preferences → Editor`:
   - Font: Consolas 11
   - Show line numbers — включено
2. `Tools → Preferences → IPython console`:
   - Graphics backend: **Inline** (графики будут в консоли)
3. `Tools → Preferences → Run`:
   - Working directory: **The directory of the file being executed**

**Рабочий процесс в Spyder:**
1. Открыть файл: `File → Open` → выбрать `.py` из `scratch/` или `MLOps/`
2. Написать код в редакторе (слева)
3. Выделить и нажать `F9` — выполнить выделенное
4. `F5` — запустить весь файл
5. Переменные и графики — в панелях справа

---

## 6. Структура проектов

```
C:\Users\Selecty\Desktop\GIT\
├── MLOps/                          ← твоя песочница
│   ├── data/                       ← датасеты
│   ├── notebooks/                  ← Jupyter-ноутбуки
│   ├── src/                        ← переиспользуемые модули
│   ├── instructions/               ← инструкции (этот файл)
│   ├── tests/                      ← тесты
│   ├── requirements.txt
│   └── README.md
│
└── data-science-from-scratch/      ← код книги Джоэла Грасса
    ├── scratch/                    ← модули по главам
    ├── requirements.txt
    └── setup.py
```

---

## 7. Полезные команды conda

```powershell
# Список окружений
conda env list

# Активировать окружение
conda activate mlops

# Деактивировать
conda deactivate

# Удалить окружение
conda env remove --name mlops

# Установить новый пакет в текущее окружение
conda install <package>
# или через pip (если в conda нет)
pip install <package>

# Обновить все пакеты
conda update --all
```

---

## 8. Импорт scratch из книги

После `pip install -e ..\data-science-from-scratch` импорты работают откуда угодно:

```python
from scratch.linear_algebra import dot, Vector
from scratch.statistics import mean, median
from scratch.working_with_data import rescale

# Пример
result = dot([1, 2, 3], [4, 5, 6])
print(result)  # → 32
```

---

## 9. Быстрый старт: первый ноутбук

```powershell
cd C:\Users\Selecty\Desktop\GIT\MLOps
conda activate mlops
jupyter notebook
```

В браузере:
1. `New → Notebook (Python 3.12)` — создать ноутбук
2. Переименовать: `File → Rename` → `02-first-eda.ipynb`
3. В первую ячейку:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/customers.csv')
df.head()
```

4. `Shift+Enter` — выполнить
