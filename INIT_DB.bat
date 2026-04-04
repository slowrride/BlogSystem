@echo off
chcp 65001 >nul
echo ============================================================
echo Django 数据库初始化脚本
echo ============================================================
echo.

cd /d %~dp0

echo 当前目录: %CD%
echo.

echo [步骤 1/3] 删除旧数据库...
if exist db.sqlite3 (
    del /f /q db.sqlite3
    echo ✓ 数据库文件已删除
) else (
    echo ⚠ 数据库文件不存在
)

echo.
echo [步骤 2/3] 生成迁移文件...
python manage.py makemigrations
if errorlevel 1 (
    echo ✗ 迁移文件生成失败
    pause
    exit /b 1
)

echo.
echo [步骤 3/3] 应用数据库迁移...
python manage.py migrate
if errorlevel 1 (
    echo ✗ 数据库迁移失败
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✓ 数据库初始化成功！
echo 现在运行: python manage.py createsuperuser
echo ============================================================
echo.
pause
