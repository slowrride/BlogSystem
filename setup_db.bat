@echo off
chcp 65001 >nul
echo ============================================================
echo Django Database Initialization Script
echo ============================================================
echo.

cd /d %~dp0

echo Current directory: %CD%
echo.

echo [Step 1/3] Delete old database...
if exist db.sqlite3 (
    del /f /q db.sqlite3
    echo [OK] Database file deleted
) else (
    echo [INFO] Database file does not exist
)

echo.
echo [Step 2/3] Generate migration files...
python manage.py makemigrations
if errorlevel 1 (
    echo [ERROR] Migration file generation failed
    pause
    exit /b 1
)

echo.
echo [Step 3/3] Apply database migrations...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Database migration failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [SUCCESS] Database initialization completed!
echo Now run: python manage.py createsuperuser
echo ============================================================
echo.
pause
