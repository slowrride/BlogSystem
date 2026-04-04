"""
项目初始化脚本
"""
import os
import subprocess

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"命令执行失败，返回码: {result.returncode}")
        return False
    return True

def main():
    print("=" * 50)
    print("Django 博客系统初始化")
    print("=" * 50)
    
    # 步骤1: 删除旧的数据库文件
    print("\n步骤1: 清理旧数据库...")
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"已删除: {db_path}")
    else:
        print("没有找到旧的数据库文件")
    
    # 步骤2: 删除迁移文件
    print("\n步骤2: 清理迁移文件...")
    migration_files = []
    for root, dirs, files in os.walk('.'):
        if 'migrations' in dirs:
            migrations_dir = os.path.join(root, 'migrations')
            for file in files:
                if file != '__init__.py' and not file.startswith('.'):
                    file_path = os.path.join(migrations_dir, file)
                    try:
                        os.remove(file_path)
                        print(f"已删除: {file_path}")
                    except Exception as e:
                        print(f"删除失败 {file_path}: {e}")
    
    # 步骤3: 生成迁移文件
    if not run_command('python manage.py makemigrations', '步骤3: 生成迁移文件'):
        print("迁移文件生成失败!")
        return
    
    # 步骤4: 应用迁移
    if not run_command('python manage.py migrate', '步骤4: 应用迁移'):
        print("数据库迁移失败!")
        return
    
    # 步骤5: 创建超级用户
    print("\n" + "=" * 50)
    print("步骤5: 创建超级用户")
    print("=" * 50)
    run_command('python manage.py createsuperuser', '创建超级用户')
    
    print("\n" + "=" * 50)
    print("初始化完成!")
    print("现在可以运行: python manage.py runserver")
    print("=" * 50)

if __name__ == '__main__':
    main()
