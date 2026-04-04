# Django 博客系统 - 快速开始指南

5 分钟内将你的博客部署到公网！

## 🚀 推荐方案：CloudStudio（完全免费）

### 为什么选择 CloudStudio？
- ✅ 完全免费使用
- ✅ 无需安装任何软件
- ✅ 自动生成公网地址
- ✅ 在线编辑代码
- ✅ 适合学习和演示

---

## 📝 快速部署步骤

### 步骤 1：打开 CloudStudio（2 分钟）

1. 访问：https://cloud.tencent.com/developer/cloudstudio
2. 点击"登录"（使用腾讯云账号，如没有则免费注册）
3. 点击"新建工作空间"
4. 配置如下：
   - 工作空间名称：`my-django-blog`
   - 开发环境：选择 `Python`
   - Python 版本：`Python 3.9`
5. 点击"新建"，等待环境创建完成（约 30 秒）

### 步骤 2：上传代码（1 分钟）

**方式 A：使用 Git（推荐）**

在 CloudStudio 终端中输入：

```bash
cd /home/cloudstudio

# 如果你有 GitHub/GitLab 仓库
git clone https://github.com/your-username/BlogSystem.git
cd BlogSystem
```

**方式 B：手动上传**

1. 在本地将项目压缩为 `BlogSystem.zip`
2. 在 CloudStudio 左侧文件树，右键点击空白处
3. 选择"上传文件"
4. 选择并上传 `BlogSystem.zip`
5. 右键点击上传的 zip 文件，选择"解压"

### 步骤 3：一键部署（1 分钟）

在 CloudStudio 终端中，在项目目录下运行：

```bash
cd BlogSystem

# 方式 A：使用自动部署脚本（推荐）
bash deploy_cloudstudio.sh

# 方式 B：手动执行
pip install -r requirements.txt
rm -f db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### 步骤 4：配置公网访问（1 分钟）

1. 在 CloudStudio 界面左侧，找到"端口"选项卡
2. 点击"添加端口"
3. 输入端口：`8000`
4. 点击"确定"
5. 复制生成的公网地址，例如：`https://xxx.cloudstudio.net`

### 步骤 5：访问你的博客（立即生效）🎉

在浏览器中打开公网地址，你将看到：

- 博客首页
- 可以注册新用户
- 可以发布文章
- 可以查看热度排行榜

---

## 📸 截图预览

### 1. 注册页面
![注册](docs/signup.png)

### 2. 发布文章
![发布文章](docs/create_post.png)

### 3. 热度排行榜
![热度榜](docs/hot_posts.png)

---

## 🔧 自定义配置

### 修改网站标题

编辑 `BlogSystem/settings.py`：

```python
# 默认
LANGUAGE_CODE = 'zh-hans'

# 改为
LANGUAGE_CODE = 'en-us'  # 英文
```

### 修改管理员账号

```bash
python manage.py createsuperuser
# 输入新的用户名和密码
```

### 上传自己的 Logo

1. 将 logo 图片放到 `static/images/` 目录
2. 编辑 `blog/templates/blog/base.html`
3. 修改 `<a class="navbar-brand">` 部分

---

## 💡 功能演示

### 发布你的第一篇文章

1. 注册/登录账号
2. 点击导航栏"发布文章"
3. 填写标题和内容
4. （可选）上传封面图片
5. 点击"发布文章"

### 查看热度排行榜

1. 点击导航栏"🔥 热度榜"
2. 查看所有文章的热度排名
3. 点击文章标题查看详情

### 编辑个人资料

1. 点击导航栏你的用户名
2. 进入个人主页
3. 点击"编辑资料"
4. 上传头像，填写个人简介
5. 保存修改

---

## 🎨 界面美化

### 修改主题色

编辑 `static/css/style.css`：

```css
/* 修改导航栏颜色 */
.navbar {
    background-color: #your-color !important;
}
```

### 修改字体

编辑 `blog/templates/blog/base.html`：

```html
<!-- 在 <head> 中添加 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">

<!-- 修改 body 样式 -->
body {
    font-family: 'Noto Sans SC', sans-serif;
}
```

---

## 📱 测试功能清单

部署后，请测试以下功能：

- [ ] 首页显示正常
- [ ] 用户注册成功
- [ ] 用户登录成功
- [ ] 发布文章成功
- [ ] 查看文章详情
- [ ] 发表评论成功
- [ ] 热度排行榜显示
- [ ] 编辑个人资料
- [ ] 删除自己的评论
- [ ] 移动端访问正常

---

## 🔐 安全建议

### 生产环境部署

如果要用作正式网站，建议：

1. **使用自己的域名**
2. **配置 HTTPS**
3. **使用 PostgreSQL 数据库**
4. **关闭 DEBUG 模式**
5. **设置强密码**

参考 `DEPLOYMENT.md` 获取详细部署指南。

---

## ❓ 常见问题

### Q: CloudStudio 会自动关闭吗？
A: 免费版会自动休眠，但数据会保留。重新访问即可唤醒。

### Q: 如何保持网站一直在线？
A: 升级到付费版，或者使用 VPS 部署（参考 DEPLOYMENT.md）

### Q: 数据会丢失吗？
A: CloudStudio 重启可能会丢失数据，重要内容请定期备份或使用 Git 提交。

### Q: 如何更换域名？
A: 需要使用 VPS 部署，参考 `DEPLOYMENT.md` 中的 Docker 方式。

### Q: 如何添加更多功能？
A: 项目代码已开源，可以自由修改和扩展。

---

## 📚 下一步

### 学习 Django
- [Django 官方教程](https://docs.djangoproject.com/zh-hans/4.2/intro/tutorial01/)
- [Django Girls 教程](https://tutorial.djangogirls.org/zh/)

### 扩展功能
- 添加文章分类
- 添加标签系统
- 添加全文搜索
- 添加社交分享
- 添加评论回复

### 优化性能
- 使用 Redis 缓存
- 优化数据库查询
- 使用 CDN 加速
- 压缩静态文件

---

## 🎯 总结

你现在拥有：
- ✅ 一个可以公网访问的博客网站
- ✅ 完整的用户系统
- ✅ 文章管理功能
- ✅ 热度排行榜
- ✅ 响应式设计

**开始你的博客之旅吧！** 🚀

---

## 🆘 获取帮助

遇到问题？

1. 查看 [README.md](README.md)
2. 查看 [DEPLOYMENT.md](DEPLOYMENT.md)
3. 查看 [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
4. 提交 Issue 到 GitHub

---

**祝你使用愉快！** 🎉
