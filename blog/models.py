from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    """
    文章模型
    """
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    heat = models.PositiveIntegerField(default=0, verbose_name='热度')
    cover_image = models.ImageField(upload_to='post_covers/', blank=True, null=True, verbose_name='封面图片')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def calculate_heat(self):
        """
        计算热度：浏览量 * 1 + 评论数 * 3
        """
        comment_count = self.comments.count()
        self.heat = self.views * 1 + comment_count * 3
        self.save(update_fields=['heat'])
        return self.heat

    def save(self, *args, **kwargs):
        # 如果是新文章，初始化热度为 0
        if not self.pk:
            self.heat = 0
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    评论模型
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='作者')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} 在 {self.post.title} 上的评论'

    def save(self, *args, **kwargs):
        # 创建评论时更新文章热度
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            self.post.calculate_heat()
