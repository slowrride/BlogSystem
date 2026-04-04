import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

# 测试配置
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogSystem.settings')
    import django
    django.setup()
    
    from django.conf import settings
    print("Django 配置加载成功!")
    print(f"AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
    print(f"数据库: {settings.DATABASES['default']['NAME']}")
    print(f"调试模式: {settings.DEBUG}")
    
    # 检查用户模型
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print(f"用户模型: {User}")
    print(f"用户表名: {User._meta.db_table}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
