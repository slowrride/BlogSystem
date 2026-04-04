# Django 个人博客系统

一个基于 Django 的个人博客系统，包含以下功能：
- 用户注册和登录
- 发布博客文章
- 文章评论功能
- 文章热度统计（基于浏览量和评论数）
- 热度排行榜

## 功能特点
- 完整的用户认证系统
- 富文本文章编辑
- 实时热度计算
- 响应式设计

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行数据库迁移：
```bash
python manage.py makemigrations
python manage.py migrate
```

3. 创建超级用户：
```bash
python manage.py createsuperuser
```

4. 运行服务器：
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 即可使用。
