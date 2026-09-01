@echo off
chcp 65001 >nul 2>&1
title Google Text-to-Speech App

echo ============================================
echo   Google Text-to-Speech Application
echo   تطبيق تحويل النص إلى كلام
echo ============================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [✓] Python found / تم العثور على Python
    goto :run_app
)

where python3 >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [✓] Python3 found / تم العثور على Python3
    set PYTHON_CMD=python3
    goto :run_app
)

echo [!] Python not found. Installing Python 3.11...
echo [!] لم يتم العثور على Python. جاري تثبيت Python 3.11...
echo.

:: Download Python 3.11 installer
echo Downloading Python 3.11 installer...
curl -L -o python-3.11.9-amd64.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

if not exist python-3.11.9-amd64.exe (
    echo [ERROR] Failed to download Python installer.
    echo [خطأ] فشل تحميل مثبت Python.
    pause
    exit /b 1
)

:: Silent install with PATH
echo Installing Python 3.11 silently (this may take a few minutes)...
echo جاري تثبيت Python 3.11 بصمت (قد يستغرق بضع دقائق)...
python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Refresh PATH
set "PATH=%LocalAppData%\Programs\Python\Python311;%LocalAppData%\Programs\Python\Python311\Scripts;%PATH%"
set "PATH=%ProgramFiles%\Python311;%ProgramFiles%\Python311\Scripts;%PATH%"

:: Clean up installer
del python-3.11.9-amd64.exe 2>nul

:: Verify installation
where python >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [✓] Python 3.11 installed successfully!
    echo [✓] تم تثبيت Python 3.11 بنجاح!
) else (
    echo [ERROR] Python installation may require a restart.
    echo [خطأ] قد يتطلب تثبيت Python إعادة تشغيل الجهاز.
    pause
    exit /b 1
)

:run_app
echo.
echo Starting application... / جاري تشغيل التطبيق...
echo.

if defined PYTHON_CMD (
    %PYTHON_CMD% "%~dp0app.py"
) else (
    python "%~dp0app.py"
)

echo.
pause
