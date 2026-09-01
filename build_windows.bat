@echo off
chcp 65001 >nul 2>&1
title Build Google TTS - Windows EXE

echo ============================================
echo   Building Google TTS for Windows (.exe)
echo   بناء التطبيق لنظام Windows
echo ============================================
echo.

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is required. Run run.bat first to install it.
    echo [خطأ] Python مطلوب. شغّل run.bat أولاً لتثبيته.
    pause
    exit /b 1
)

:: Install PyInstaller
echo [1/3] Installing PyInstaller...
echo [1/3] جاري تثبيت PyInstaller...
pip install pyinstaller gTTS pygame

:: Build EXE
echo.
echo [2/3] Building executable...
echo [2/3] جاري بناء الملف التنفيذي...
pyinstaller ^
    --onefile ^
    --name "GoogleTTS" ^
    --icon "NONE" ^
    --add-data "README.md;." ^
    --hidden-import "gtts" ^
    --hidden-import "pygame" ^
    --hidden-import "gtts.tokenizer" ^
    --hidden-import "gtts.tokenizer.pre_processors" ^
    --hidden-import "gtts.tokenizer.tokenizer_cases" ^
    --console ^
    app.py

:: Check result
echo.
if exist "dist\GoogleTTS.exe" (
    echo [3/3] ============================================
    echo   [✓] Build successful! / تم البناء بنجاح!
    echo   Output: dist\GoogleTTS.exe
    echo   Size: 
    for %%A in ("dist\GoogleTTS.exe") do echo     %%~zA bytes
    echo ============================================
) else (
    echo [ERROR] Build failed! Check the output above.
    echo [خطأ] فشل البناء! تحقق من المخرجات أعلاه.
)

echo.
echo [INFO] You can distribute dist\GoogleTTS.exe as a standalone app.
echo [INFO] No Python installation needed on the target machine.
echo [معلومة] يمكنك توزيع dist\GoogleTTS.exe كتطبيق مستقل.
echo [معلومة] لا حاجة لتثبيت Python على الجهاز المستهدف.
echo.
pause
