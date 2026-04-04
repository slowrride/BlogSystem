-- 初始化数据库脚本

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 使用数据库
USE blog;

-- 3. 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    avatar VARCHAR(255),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. 创建文章表
CREATE TABLE IF NOT EXISTS blog_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INT NOT NULL,
    views INT DEFAULT 0,
    heat INT DEFAULT 0,
    cover_image VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. 创建评论表
CREATE TABLE IF NOT EXISTS blog_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    post_id INT NOT NULL,
    author_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES blog_posts(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. 插入测试数据
INSERT INTO users (username, email, password, is_staff, is_superuser) 
VALUES ('admin', 'admin@example.com', 'pbkdf2_sha256$150000$iA9dLk8e3hRw$4gqJ8k9mP8l8n2p6v3r7t8w2q4y5u8i0o2p3l4k5j6h7g8f9d0s1a2z3x4c5v6b7n8m9', TRUE, TRUE);

INSERT INTO blog_posts (title, content, author_id, views, heat) 
VALUES 
('第一篇博客文章', '这是我发布的第一篇博客文章，欢迎大家评论！', 1, 100, 100),
('Django 开发教程', 'Django 是一个强大的 Python Web 框架，本文将介绍 Django 的基本用法。', 1, 200, 200),
('Python 编程技巧', '分享一些实用的 Python 编程技巧，帮助大家提高开发效率。', 1, 150, 150);

INSERT INTO blog_comments (content, post_id, author_id) 
VALUES 
('写得不错，学习了！', 1, 1),
('很有帮助的文章', 2, 1),
('期待更多内容', 3, 1);
