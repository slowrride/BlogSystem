# Django 博客系统部署指南

本文档提供了多种部署方式，从简单的免费部署到专业的生产环境部署。

## 📋 部署方式对比

| 部署方式 | 难度 | 成本 | 适用场景 | 推荐度 |
|---------|------|------|---------|--------|
| CloudStudio | ⭐ | 免费 | 快速测试、学习 | ⭐⭐⭐⭐⭐ |
| PythonAnywhere | ⭐⭐ | 免费/付费 | 个人博客、小型项目 | ⭐⭐⭐⭐ |
| Docker + VPS | ⭐⭐⭐ | 付费 | 专业生产环境 | ⭐⭐⭐⭐⭐ |
| Heroku | ⭐⭐ | 付费 | 快速部署、自动扩展 | ⭐⭐⭐ |

---

## 方式一：CloudStudio 部署（最简单，推荐新手）

### 优势
- ✅ 完全免费
- ✅ 无需本地安装任何东西
- ✅ 自动生成公网访问地址
- ✅ 支持在线编辑代码

### 步骤

#### 1. 访问 CloudStudio
打开浏览器访问：https://cloud.tencent.com/developer/cloudstudio

#### 2. 登录并创建工作空间
1. 使用腾讯云账号登录
2. 点击"新建工作空间"
3. 选择以下配置：
   - 工作空间名称：`django-blog`
   - 开发环境：`Python`
   - Python 版本：`3.9`
4. 点击"新建"

#### 3. 上传项目代码
方式 A：使用 Git（推荐）
```bash
# 在 CloudStudio 终端中执行
cd /home/cloudstudio
git clone <your-repository-url>
cd BlogSystem
```

方式 B：手动上传
1. 将本地项目压缩为 zip 文件
2. 在 CloudStudio 左侧文件管理器中右键
3. 选择"上传文件"
4. 解压 zip 文件

#### 4. 安装依赖
```bash
cd BlogSystem
pip install -r requirements.txt
```

#### 5. 配置数据库
```bash
# 删除旧数据库（如果存在）
rm -f db.sqlite3

# 生成迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate
```

#### 6. 创建超级用户
```bash
python manage.py createsuperuser
# 按提示输入用户名、邮箱、密码
```

#### 7. 启动服务
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 8. 配置端口映射
1. 在 CloudStudio 界面左侧找到"端口"选项
2. 点击"添加端口"
3. 输入端口：`8000`
4. 点击"确定"
5. 系统会提供公网访问地址，例如：`https://xxx.cloudstudio.net`

### 注意事项
- CloudStudio 免费版会自动休眠，需要定期访问保持在线
- 使用 SQLite 数据库，适合测试但生产环境建议用 PostgreSQL
- 数据不会持久化保存，重启后可能丢失

---

## 方式二：PythonAnywhere 部署（个人博客首选）

### 优势
- ✅ 提供免费套餐
- ✅ 专为 Django 优化
- ✅ 自定义域名支持
- ✅ 自动 SSL 证书

### 步骤

#### 1. 注册账号
访问 https://www.pythonanywhere.com/ 创建免费账户

#### 2. 创建 Web 应用
1. 登录后点击 Dashboard
2. 点击 "Web" → "Add a new web app"
3. 选择配置方式：`Manual configuration`
4. 选择 Python 版本：`Python 3.9`
5. 点击 Next

#### 3. 上传项目代码
在 PythonAnywhere 的 Bash 控制台中执行：

```bash
# 使用 Git（推荐）
git clone <your-repository-url>
cd BlogSystem

# 或使用 ZIP 上传
# 先在本地压缩项目，然后上传到 PythonAnywhere
```

#### 4. 创建虚拟环境
```bash
cd BlogSystem
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. 配置数据库
```bash
# 保留 SQLite（免费套餐推荐）
python manage.py makemigrations
python manage.py migrate
```

#### 6. 配置 WSGI 文件
在 Web 应用设置页面，找到 WSGI configuration file，点击编辑：

```python
import os
import sys

path = '/home/yourusername/BlogSystem'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'BlogSystem.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

将 `yourusername` 替换为你的 PythonAnywhere 用户名。

#### 7. 配置静态文件
```bash
# 在项目中
python manage.py collectstatic
```

然后在 Web 应用设置中配置：
- Static files URL: `/static/`
- Static files directory: `/home/yourusername/BlogSystem/staticfiles`

#### 8. 重启应用
在 Web 应用设置页面点击 "Reload" 按钮

#### 9. 访问你的网站
你的网站地址是：`http://yourusername.pythonanywhere.com`

### 自定义域名（可选）
1. 购买域名
2. 在域名注册商处设置 CNAME 记录指向 `yourusername.pythonanywhere.com`
3. 在 PythonAnywhere 中配置域名

---

## 方式三：Docker + VPS 部署（生产环境推荐）

### 优势
- ✅ 完全控制
- ✅ 高性能
- ✅ 支持高并发
- ✅ 易于扩展

### 步骤

#### 1. 准备 VPS
推荐云服务商：
- 腾讯云（推荐，国内访问快）
- 阿里云
- 华为云
- AWS
- DigitalOcean

最低配置：1核2GB内存

#### 2. 安装 Docker 和 Docker Compose
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 3. 上传项目
```bash
# 在本地打包
git push <your-repository>

# 在服务器上拉取
git clone <your-repository-url>
cd BlogSystem
```

#### 4. 配置环境变量
```bash
cp .env.example .env
nano .env  # 编辑配置
```

#### 5. 启动服务
```bash
docker-compose up -d
```

#### 6. 配置 Nginx
项目已包含 Nginx 配置文件 `nginx.conf`

#### 7. 配置域名
在你的域名服务商处添加 A 记录指向服务器 IP

#### 8. 配置 SSL（使用 Let's Encrypt）
```bash
# 安装 Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d yourdomain.com
```

---

## 方式四：Heroku 部署（快速部署）

### 步骤

#### 1. 安装 Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# 下载安装器：https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. 登录 Heroku
```bash
heroku login
```

#### 3. 创建 Procfile
在项目根目录创建 `Procfile`：
```
web: gunicorn BlogSystem.wsgi --log-file -
```

#### 4. 修改 requirements.txt
添加：
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

#### 5. 创建应用
```bash
heroku create your-blog-name
```

#### 6. 配置环境变量
```bash
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set DJANGO_ALLOWED_HOSTS=your-blog-name.herokuapp.com
```

#### 7. 推送代码
```bash
git push heroku master
```

#### 8. 运行迁移
```bash
heroku run python manage.py migrate
```

#### 9. 创建超级用户
```bash
heroku run python manage.py createsuperuser
```

---

## 🛡️ 安全配置建议

### 1. 生成安全的 SECRET_KEY
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 2. 配置 ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-ip-address']
```

### 3. 启用 HTTPS
- 使用 Let's Encrypt 免费证书
- 配置强制 HTTPS 重定向

### 4. 数据库备份
```bash
# SQLite 备份
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL 备份
pg_dump -U bloguser blogdb > backup.sql
```

---

## 📊 性能优化建议

### 1. 使用生产级数据库
- PostgreSQL（推荐）
- MySQL

### 2. 配置缓存
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. 使用 Gunicorn
```bash
pip install gunicorn
gunicorn BlogSystem.wsgi:application --bind 0.0.0.0:8000
```

### 4. 静态文件 CDN
- 使用 Cloudflare
- 或使用 AWS CloudFront

---

## 🔍 故障排查

### 问题 1：502 Bad Gateway
**解决方案**：检查 Docker 容器是否运行
```bash
docker-compose ps
docker-compose logs
```

### 问题 2：静态文件 404
**解决方案**：
```bash
python manage.py collectstatic
```

### 问题 3：数据库连接失败
**解决方案**：检查数据库配置和网络连接

---

## 📚 更多资源

- Django 官方文档：https://docs.djangoproject.com/
- Django Girls 教程：https://tutorial.djangogirls.org/
- Docker 文档：https://docs.docker.com/
- Nginx 文档：https://nginx.org/en/docs/

---

**祝你部署成功！** 🎉
