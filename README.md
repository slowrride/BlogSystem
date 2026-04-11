# Django 个人博客系统

一个功能完善的基于 Django 4.2 的个人博客系统，具备现代化的用户界面和丰富的互动功能。

## 📸 项目截图

<div align="center">
  <img src="docs/screenshot_home.png" alt="首页" width="800">
  <br>
  <em>博客首页</em>
</div>

## ✨ 核心功能

### 用户功能
- 🔐 **用户认证系统**
  - 用户注册（支持用户名、邮箱验证）
  - 安全登录/登出
  - 个人资料管理（头像、个人简介）
  - 权限控制（仅作者可编辑/删除自己的内容）

### 博客功能
- 📝 **文章管理**
  - 发布新文章（支持封面图片）
  - 编辑和删除文章
  - 文章浏览量统计
  - 分页显示（每页 10 篇）

### 互动功能
- 💬 **评论系统**
  - 发表文章评论
  - 删除自己的评论
  - 评论时间戳显示

### 排行榜
- 🔥 **热度排行榜**
  - 实时热度计算：浏览量 × 1 + 评论数 × 3
  - 热度排序展示（Top 20）
  - 热度自动更新机制

## 🛠 技术栈

### 后端
- **Python 3.9+**
- **Django 4.2.7** - Web 框架
- **SQLite 3** - 数据库（开发环境）

### 前端
- **Bootstrap 5.3** - 响应式 UI 框架
- **Django Templates** - 模板引擎
- **Crispy Forms** - 表单美化

### 核心依赖
```
Django==4.2.7
Pillow==10.1.0
django-crispy-forms==2.0
crispy-bootstrap5==0.7
```

## 📁 项目结构

```
BlogSystem/
├── BlogSystem/              # 项目主配置目录
│   ├── settings.py          # 项目设置（数据库、模板、静态文件）
│   ├── urls.py             # 主路由配置
│   └── wsgi.py            # WSGI 配置
├── users/                 # 用户应用
│   ├── models.py           # 自定义用户模型（头像、个人简介）
│   ├── views.py            # 注册、登录、个人主页视图
│   ├── forms.py           # 注册、个人资料表单
│   ├── urls.py            # 用户路由
│   └── templates/users/   # 用户模板
├── blog/                  # 博客应用
│   ├── models.py           # 文章、评论模型（含热度计算）
│   ├── views.py            # 文章列表、详情、创建、删除、热度榜
│   ├── forms.py           # 文章、评论表单
│   ├── urls.py            # 博客路由
│   └── templates/blog/    # 博客模板
├── static/                # 静态文件
│   └── css/
│       └── style.css      # 自定义样式
├── media/                 # 用户上传文件（头像、文章封面）
├── manage.py             # Django 管理脚本
├── requirements.txt       # 项目依赖
└── README.md            # 项目说明
```

## 🚀 快速开始

### 环境要求
- Python 3.9 或更高版本
- pip 包管理器

### 快速启动（Windows）

运行数据库初始化脚本：
```bash
setup_db.bat
```

然后创建超级用户：
```bash
python manage.py createsuperuser
```

### 手动安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd BlogSystem
```

2. **创建虚拟环境**（推荐）
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **数据库初始化**
```bash
# 删除旧数据库（如果存在）
del db.sqlite3  # Windows
# rm db.sqlite3  # Linux/Mac

# 生成迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

按照提示输入：
- 用户名
- 邮箱地址
- 密码

6. **启动开发服务器**
```bash
python manage.py runserver
```

7. **访问应用**
- 博客首页: http://127.0.0.1:8000/
- 管理后台: http://127.0.0.1:8000/admin/

## 📚 使用指南

### 功能演示

1. **用户注册**
   - 访问 `/users/register/`
   - 填写用户名、邮箱和密码
   - 点击"注册"完成注册

2. **发布文章**
   - 登录后点击"发布文章"
   - 填写标题、内容（可选封面图片）
   - 提交发布

3. **发表评论**
   - 点击任意文章查看详情
   - 在评论框输入内容
   - 点击"发表评论"

4. **查看热度榜**
   - 点击导航栏"🔥 热度榜"
   - 查看热度最高的文章排名

5. **编辑个人资料**
   - 点击导航栏用户名进入个人主页
   - 点击"编辑资料"
   - 上传头像、修改个人简介

### 常见问题

**Q: 如何快速重新初始化数据库？**
A: Windows 用户运行 `setup_db.bat`，Linux/Mac 用户手动删除 `db.sqlite3` 后运行迁移命令。

**Q: 忘记管理员密码怎么办？**
A: 运行 `python manage.py createsuperuser` 创建新的超级用户，或在数据库中修改密码。

**Q: 如何更换数据库（如使用 PostgreSQL）？**
A: 参考 [DEPLOYMENT.md](DEPLOYMENT.md) 中的生产环境配置章节。

## 🌐 公网部署

详细的部署指南请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

### 快速部署（推荐新手）

#### CloudStudio 部署（5 分钟，免费）

1. **访问 CloudStudio**
   - 打开 https://cloud.tencent.com/developer/cloudstudio
   - 使用腾讯云账号登录

2. **创建工作空间**
   - 点击"新建工作空间"
   - 选择"Python"模板，Python 3.9
   - 创建工作空间

3. **上传代码**
   ```bash
   # 方式1：使用 Git（推荐）
   git clone <your-repository-url>
   cd BlogSystem

   # 方式2：手动上传
   # 将项目文件拖拽到 CloudStudio 编辑器中
   ```

4. **安装依赖并初始化**
   ```bash
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver 0.0.0.0:8000
   ```

5. **配置端口**
   - 在 CloudStudio 端口设置中添加 8000 端口
   - 系统会提供公网访问地址

### 其他部署方式

- **PythonAnywhere**：适合个人博客，支持免费套餐和自定义域名
- **Docker + VPS**：适合生产环境，高性能和完全控制
- **Heroku**：快速部署，自动扩展

详细步骤请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔧 配置说明

### 生产环境设置

在生产环境中，请修改 `BlogSystem/settings.py`：

```python
# 安全设置
DEBUG = False
SECRET_KEY = 'your-secret-key-here'
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# 数据库（推荐使用 PostgreSQL）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 静态文件
STATIC_ROOT = '/var/www/static/'
```

## 📊 热度计算算法

**热度公式：**
```
热度 = 浏览量 × 1 + 评论数 × 3
```

**示例：**
- 文章 A：浏览 100，评论 10 → 热度 = 100×1 + 10×3 = 130
- 文章 B：浏览 200，评论 5 → 热度 = 200×1 + 5×3 = 215
- 文章 B 排名更高

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

- **Wangxinyu** - 项目开发者

## 🙏 致谢

- Django 团队 - 优秀的 Web 框架
- Bootstrap - 响应式 UI 框架
- Crispy Forms - 表单美化工具

## 📮 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至 [2010806610@qq.com]

---

## 📚 文档

| 文档 | 描述 |
|-----|------|
| [README.md](README.md) | 项目介绍和使用指南（本文件） |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 详细部署指南（CloudStudio、PythonAnywhere、Docker 等） |

---

**享受你的博客之旅！** 🎉
