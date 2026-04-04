#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogSystem.settings')

try:
    import django
    django.setup()
    
    from django.core.management import call_command
    from django.db import connection
    
    print("=" * 60)
    print("开始数据库迁移")
    print("=" * 60)
    
    # 检查数据库连接
    print("\n检查数据库连接...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"当前数据库表: {len(tables)} 个")
        for table in tables:
            print(f"  - {table[0]}")
    
    # 运行迁移
    print("\n运行数据库迁移...")
    call_command('migrate', verbosity=2)
    
    # 检查迁移后的表
    print("\n检查迁移后的数据库表...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"迁移后数据库表: {len(tables)} 个")
        for table in tables:
            print(f"  - {table[0]}")
    
    # 检查用户表是否存在
    print("\n检查用户表...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_user';")
        user_table = cursor.fetchone()
        if user_table:
            print("✓ 用户表 users_user 已创建")
        else:
            print("✗ 用户表 users_user 不存在")
    
    print("\n" + "=" * 60)
    print("迁移完成!")
    print("现在可以运行: python manage.py createsuperuser")
    print("=" * 60)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
