#!/bin/bash
# CloudStudio 快速部署脚本

echo "==================================="
echo "Django 博客系统 - CloudStudio 部署"
echo "==================================="

# 检查是否在正确的目录
if [ ! -f "manage.py" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

echo ""
echo "[1/5] 安装 Python 依赖..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "错误: 依赖安装失败"
    exit 1
fi

echo ""
echo "[2/5] 数据库初始化..."
rm -f db.sqlite3
python manage.py makemigrations
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "错误: 数据库迁移失败"
    exit 1
fi

echo ""
echo "[3/5] 创建超级用户..."
echo "请按照提示输入管理员账号信息："
python manage.py createsuperuser

if [ $? -ne 0 ]; then
    echo "警告: 超级用户创建失败，稍后可以手动创建"
fi

echo ""
echo "[4/5] 收集静态文件..."
python manage.py collectstatic --noinput

echo ""
echo "[5/5] 启动服务..."
echo "服务正在启动，访问 http://localhost:8000"
echo ""
echo "==================================="
echo "部署完成！"
echo "==================================="
echo ""
echo "下一步："
echo "1. 在 CloudStudio 左侧添加 8000 端口映射"
echo "2. 使用生成的公网地址访问网站"
echo ""

python manage.py runserver 0.0.0.0:8000
