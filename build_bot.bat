@echo off
echo.
echo 🛠️  Starting build process for mybot...

:: تفعيل البيئة الافتراضية (إذا موجودة)
call .venv\Scripts\activate

:: تنفيذ التحزيم باستخدام PyInstaller وملف mybot.spec
pyinstaller mybot.spec

echo.
echo ✅ Build completed. Check the dist\mybot folder.
pause
