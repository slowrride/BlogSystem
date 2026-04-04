"""
Django 数据库重新初始化脚本

使用方法：python reinit_db.py
"""

import os
import sys
import shutil

def main():
    print("=" * 60)
    print("Django 数据库重新初始化")
    print("=" * 60)

    # 1. 删除数据库文件
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ 已删除数据库文件: {db_path}")
    else:
        print("⚠ 数据库文件不存在，跳过删除步骤")

    # 2. 删除迁移文件（保留 __init__.py）
    print("\n清理迁移文件...")
    for app in ['users', 'blog']:
        migrations_dir = os.path.join(os.path.dirname(__file__), app, 'migrations')
        if os.path.exists(migrations_dir):
            for filename in os.listdir(migrations_dir):
                if filename.startswith('00') and filename.endswith('.py'):
                    file_path = os.path.join(migrations_dir, filename)
                    try:
                        os.remove(file_path)
                        print(f"✓ 已删除: {file_path}")
                    except Exception as e:
                        print(f"✗ 删除失败 {file_path}: {e}")
        else:
            print(f"⚠ {app}/migrations 目录不存在")

    # 3. 创建迁移文件
    print("\n生成迁移文件...")
    os.system('python manage.py makemigrations')

    # 4. 应用迁移
    print("\n应用数据库迁移...")
    os.system('python manage.py migrate')

    # 5. 创建超级用户
    print("\n" + "=" * 60)
    print("现在可以创建超级用户了！")
    print("运行: python manage.py createsuperuser")
    print("=" * 60)

if __name__ == '__main__':
    main()
