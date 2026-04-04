import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogSystem.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.core.management import call_command
from django.db import connection
from django.conf import settings

print("=" * 60)
print("Django 配置检查")
print("=" * 60)

print(f"\nDjango 版本: {django.VERSION}")
print(f"数据库引擎: {settings.DATABASES['default']['ENGINE']}")
print(f"数据库名称: {settings.DATABASES['default']['NAME']}")
print(f"自定义用户模型: {settings.AUTH_USER_MODEL}")

print("\n已安装的应用:")
for app in settings.INSTALLED_APPS:
    print(f"  - {app}")

print("\n" + "=" * 60)
print("尝试创建数据库表")
print("=" * 60)

try:
    # 创建数据库表
    call_command('migrate', '--no-input', verbosity=2)
    print("\n✓ 数据库迁移成功完成！")
except Exception as e:
    print(f"\n✗ 数据库迁移失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("检查数据库表")
print("=" * 60)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\n数据库中的表:")
        for table in tables:
            print(f"  - {table[0]}")
except Exception as e:
    print(f"\n✗ 检查数据库表失败: {e}")

print("\n" + "=" * 60)
print("现在可以创建超级用户: python manage.py createsuperuser")
print("=" * 60)
