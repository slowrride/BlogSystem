@echo off
chcp 65001 >nul
echo ============================================================
echo Django 数据库重新初始化
echo ============================================================

echo.
echo [1/4] 删除数据库文件...
if exist db.sqlite3 (
    del /f /q db.sqlite3
    echo ✓ 已删除数据库文件: db.sqlite3
) else (
    echo ⚠ 数据库文件不存在，跳过删除步骤
)

echo.
echo [2/4] 清理迁移文件...
if exist users\migrations\0001_initial.py del /f /q users\migrations\0001_initial.py
if exist blog\migrations\0001_initial.py del /f /q blog\migrations\0001_initial.py
echo ✓ 迁移文件已清理

echo.
echo [3/4] 生成迁移文件...
python manage.py makemigrations

echo.
echo [4/4] 应用数据库迁移...
python manage.py migrate

echo.
echo ============================================================
echo 数据库重新初始化完成！
echo 现在可以运行: python manage.py createsuperuser
echo ============================================================
pause
