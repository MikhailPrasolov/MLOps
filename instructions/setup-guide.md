# Установка и развёртывание среды

> Инструкция по установке Anaconda, созданию окружения и подготовке к работе.
> После установки см. `jupyter-guide.md` (Jupyter) и `spyder-guide.md` (Spyder).

---

## 1. Скачать и установить Anaconda

**Ссылка:** https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Windows-x86_64.exe
(размер ~700 МБ, версия 2025.12, Python 3.13)

**Шаги установки:**
1. Запустить скачанный `Anaconda3-2025.12-2-Windows-x86_64.exe`
2. **Next >**
3. **I Agree** (принять лицензию)
4. **Just Me** (рекомендуется)
5. Папка: `C:\Users\Selecty\anaconda3` (по умолчанию)
6. **ВАЖНО:** отметить **Add Anaconda3 to my PATH environment variable**
7. **Install** (5–10 минут)
8. **Next → Finish**

**Что внутри:**
- Python 3.13
- numpy, pandas, scipy, matplotlib, seaborn
- Jupyter Notebook / JupyterLab
- Spyder IDE
- scikit-learn
- ~300+ пакетов

---

## 2. Проверка установки

**Открыть НОВЫЙ PowerShell** (обязательно, чтобы PATH обновился):

```powershell
python --version
# → Python 3.13.x

conda --version
# → conda 25.x.x

python -c "import numpy, pandas, sklearn; print('OK')"
# → OK
```

**Если `conda` не находится:**

1. Проверить, что Anaconda в PATH:
   ```powershell
   $env:Path -split ';' | Select-String -Pattern 'anaconda'
   ```
2. Если нет — добавить вручную в **User PATH** (через `Система → О переменных среды`):
   ```
   C:\Users\Selecty\anaconda3
   C:\Users\Selecty\anaconda3\Scripts
   C:\Users\Selecty\anaconda3\Library\bin
   ```
3. Отключить Microsoft Store python-псевдоним:
   **Параметры Windows → Приложения → Псевдонимы выполнения приложений → отключить python.exe и python3.exe**

---

## 3. Разрешить выполнение скриптов PowerShell

Без этого `conda init` не загрузится:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

---

## 4. Инициализация conda

```powershell
conda init powershell
```

**Закрыть и заново открыть PowerShell** — теперь префикс `(base)` будет в начале строки.

---

## 5. Создание окружения `mlops`

```powershell
# Создать окружение
conda create --name mlops --yes python=3.13 numpy pandas matplotlib seaborn scikit-learn

# Активировать
conda activate mlops

# Доустановить jupyter и spyder (через pip — пакет jupyterlab_widgets в conda-репозитории битый)
python -m pip install jupyter ipykernel spyder

# Доустановить книжный пакет scratch
python -m pip install -e C:\Users\Selecty\Desktop\GIT\data-science-from-scratch

# Проверка
python -c "import numpy, pandas, sklearn, matplotlib, seaborn; from scratch.linear_algebra import dot; print('OK', dot([1,2,3],[4,5,6]))"
# → OK 32
```

---

## 6. Альтернатива: чистый venv (если conda не подходит)

```powershell
cd C:\Users\Selecty\Desktop\GIT\MLOps
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install numpy pandas matplotlib seaborn scikit-learn jupyter spyder
pip install -r ..\data-science-from-scratch\requirements.txt
pip install -e ..\data-science-from-scratch
```

---

## 7. Структура проектов

```
C:\Users\Selecty\Desktop\GIT\
├── MLOps/                          ← песочница
│   ├── data/                       ← датасеты
│   ├── notebooks/                  ← Jupyter-ноутбуки
│   ├── src/                        ← переиспользуемые модули
│   ├── instructions/               ← инструкции
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
└── data-science-from-scratch/      ← код книги Джоэла Грасса
    ├── scratch/                    ← модули по главам
    ├── first-edition/
    ├── requirements.txt
    └── setup.py
```

---

## 8. Полезные команды conda

```powershell
# Список окружений
conda env list

# Активировать / деактивировать
conda activate mlops
conda deactivate

# Установить пакет в текущее окружение
conda install <package>
pip install <package>      # если в conda нет

# Удалить окружение
conda env remove --name mlops

# Обновить все пакеты
conda update --all
```

---

## 9. Импорт книжных модулей

После `pip install -e ..\data-science-from-scratch` импорты работают из любой папки:

```python
from scratch.linear_algebra import dot, Vector
from scratch.statistics import mean, median
from scratch.probability import normal_cdf
from scratch.working_with_data import rescale

print(dot([1, 2, 3], [4, 5, 6]))   # → 32
print(normal_cdf(0))                # → 0.5
```

---

## Что дальше

- **Jupyter Notebook / Lab** → см. `jupyter-guide.md`
- **Spyder IDE** → см. `spyder-guide.md`
