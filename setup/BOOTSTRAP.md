# 🚀 Bootstrap на новом ПК

## Быстрый способ (1 команда)

1. **Установи Anaconda3** (если ещё нет):
   - Ссылка: https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Windows-x86_64.exe
   - При установке **отметь** `Add Anaconda3 to my PATH environment variable`

2. **Склонируй оба репозитория** рядом:
   ```powershell
   cd C:\Users\Selecty\Desktop\GIT
   git clone https://github.com/joelgrus/data-science-from-scratch
   git clone <твой_MLOps_url>  MLOps
   ```

3. **Двойной клик** по `C:\Users\Selecty\Desktop\GIT\MLOps\setup\bootstrap.bat`

Скрипт автоматически:
- ✅ Настроит PowerShell Execution Policy
- ✅ Запустит `conda init`
- ✅ Создаст окружение `mlops` из `environment.yml`
- ✅ Поставит `scratch` (книжный пакет) через `pip install -e`
- ✅ Проверит, что всё работает

## Ручной способ (если bootstrap не подходит)

См. `instructions/setup-guide.md` — там пошаговая инструкция.

## Что НЕ переносится между ПК

| Что | Переносится? |
|-----|------|
| Код, ноутбуки, инструкции | ✅ (в git) |
| `environment.yml` | ✅ (в git) — declarative |
| Conda-окружение | ❌ — создаётся через `conda env create` |
| Anaconda3 (700 МБ) | ❌ — устанавливается отдельно |
| PATH, Execution Policy | ❌ — настраивается через bootstrap |
| Книжный PDF | ✅ (если коммитнуть; 21.8 МБ) |

## Принцип

`environment.yml` — **декларативное описание** окружения, а не бинарный снимок. В нём перечислены только явно поставленные пакеты (`numpy`, `pandas` и т. д.), а все транзитивные зависимости conda вытянет сама. Это надёжнее, чем `conda env export` (где ~300 пакетов с привязкой к версиям).
