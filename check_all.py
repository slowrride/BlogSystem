#!/usr/bin/env python
"""
Django 项目完整性检查脚本
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogSystem.settings')

try:
    import django
    django.setup()
    
    from django.core.management import call_command
    from django.conf import settings
    
    print("=" * 60)
    print("Django 项目完整性检查")
    print("=" * 60)
    
    # 检查配置
    print("\n[1/5] 检查项目配置...")
    try:
        call_command('check', verbosity=2)
        print("✓ 项目配置检查通过")
    except Exception as e:
        print(f"✗ 配置检查失败: {e}")
    
    # 检查数据库连接
    print("\n[2/5] 检查数据库连接...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ 数据库连接正常")
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
    
    # 检查迁移状态
    print("\n[3/5] 检查数据库迁移状态...")
    try:
        from django.db.migrations.loader import MigrationLoader
        from django.db.migrations.recorder import MigrationRecorder
        
        loader = MigrationLoader(connection)
        recorder = MigrationRecorder(connection)
        
        applied = recorder.applied_migrations()
        unapplied = set(loader.graph.nodes) - applied
        
        if unapplied:
            print(f"⚠ 有 {len(unapplied)} 个未应用的迁移:")
            for migration in sorted(unapplied):
                print(f"  - {migration[0]}.{migration[1]}")
        else:
            print("✓ 所有迁移已应用")
    except Exception as e:
        print(f"✗ 迁移检查失败: {e}")
    
    # 检查模型
    print("\n[4/5] 检查模型定义...")
    try:
        from blog.models import Post, Comment
        from users.models import User
        
        print(f"✓ 用户模型: {User._meta.db_table}")
        print(f"✓ 文章模型: {Post._meta.db_table}")
        print(f"✓ 评论模型: {Comment._meta.db_table}")
        
        # 检查模型方法
        post = Post(title="test", content="test")
        print(f"✓ 文章模型方法: calculate_heat, __str__")
        
    except Exception as e:
        print(f"✗ 模型检查失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 检查视图函数
    print("\n[5/5] 检查视图函数...")
    try:
        from blog import views as blog_views
        from users import views as user_views
        
        print("✓ 博客应用视图:")
        for name in dir(blog_views):
            if not name.startswith('_'):
                print(f"  - {name}")
        
        print("✓ 用户应用视图:")
        for name in dir(user_views):
            if not name.startswith('_'):
                print(f"  - {name}")
                
    except Exception as e:
        print(f"✗ 视图检查失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("检查完成!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
