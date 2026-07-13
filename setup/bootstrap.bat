@echo off
REM ===============================================================
REM   MLOps Bootstrap Script
REM   Одноразовая настройка среды на новом ПК
REM   Использование: двойной клик по bootstrap.bat
REM ===============================================================

setlocal enabledelayedexpansion
chcp 65001 > nul

echo.
echo ============================================================
echo   MLOps - Bootstrap
echo ============================================================
echo.

REM ---- 1. Проверка Anaconda ----
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Anaconda ne najdena v PATH.
    echo Ustanovi Anaconda3:
    echo   https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Windows-x86_64.exe
    echo Pervym shagom pri ustanovke otmet' "Add Anaconda3 to my PATH".
    echo.
    pause
    exit /b 1
)
echo [OK] Anaconda najdena:
conda --version

REM ---- 2. PowerShell Execution Policy ----
echo.
echo [STEP] PowerShell Execution Policy - RemoteSigned
powershell -NoProfile -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" >nul 2>nul
echo [OK] Gotovo

REM ---- 3. conda init ----
echo.
echo [STEP] conda init powershell
powershell -NoProfile -Command "conda init powershell" >nul 2>nul
echo [OK] Gotovo (peremotay PowerShell posle ustanovki)

REM ---- 4. Sozdaem ili obnovlyaem okruzhenie mlops iz environment.yml ----
echo.
echo [STEP] Proveryaem okruzhenie 'mlops'
call conda env list | findstr /C:"mlops " >nul 2>nul
if %errorlevel% neq 0 (
    echo [STEP] Sozdaem conda okruzhenie 'mlops' iz environment.yml
    echo       (mozhet zanyat 5-10 minut)
    call conda env create --name mlops --file environment.yml
    if !errorlevel! neq 0 (
        echo [ERROR] Nevozmozhno sozdat' okruzhenie
        pause
        exit /b 1
    )
    echo [OK] Okruzhenie 'mlops' sozdano
) else (
    echo [OK] Okruzhenie 'mlops' uzhe sushchestvuet
    echo [STEP] Obnovlyaem (dobavlyayutsya tol'ko novye pakety, sushchestvuyushchie ne trogayutsya)
    call conda env update --name mlops --file environment.yml
    if !errorlevel! neq 0 (
        echo [WARN] Obnovlenie ne udalos' - vozmozhno, versii ne sovpadayut
    ) else (
        echo [OK] Okruzhenie obnovleno
    )
)

REM ---- 5. Aktiviruem i stavim scratch (kniga) ----
echo.
echo [STEP] Stavitsya knizhnyj paket scratch
call conda activate mlops

REM Proverka, chto data-science-from-scratch ryadom
if not exist "..\data-science-from-scratch\setup.py" (
    echo [WARN] ..\data-science-from-scratch ne najden.
    echo        Skloniruj repo ryadom:
    echo        git clone https://github.com/joelgrus/data-science-from-scratch ..\data-science-from-scratch
    echo.
    set /p SKIP="Prodolzhit' bez scratch? (y/n): "
    if /i not "!SKIP!"=="y" (
        echo.
        pause
        exit /b 1
    )
) else (
    pip install -e "..\data-science-from-scratch" --quiet
    if !errorlevel! neq 0 (
        echo [WARN] scratch ne ustanovilsya. Vypolni vruchnuyu:
        echo        pip install -e ..\data-science-from-scratch
    ) else (
        echo [OK] scratch ustanovlen
    )
)

REM ---- 6. Proverka ----
echo.
echo ============================================================
echo   PROVERKA
echo ============================================================
python --version
python -c "import numpy, pandas, sklearn, matplotlib, seaborn; print('packages: OK')"
python -c "from scratch.linear_algebra import dot; print(f'scratch: dot([1,2,3],[4,5,6]) = {dot([1,2,3],[4,5,6])}')"

echo.
echo ============================================================
echo   GOTOVO!
echo ============================================================
echo.
echo Sleduyushchie shagi:
echo   1. Zakroj i zanovo otkroy PowerShell
echo   2. conda activate mlops
echo   3. jupyter lab    (ili jupyter notebook)
echo.
pause
