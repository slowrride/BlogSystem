from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

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

    # 一篇文章可以被多个用户点赞，一个用户也可以点赞多个文章
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name='点赞用户')

    # 附件（最多3个）
    attachment1 = models.FileField(upload_to='post_attachments/', blank=True, null=True, verbose_name='附件1')
    attachment2 = models.FileField(upload_to='post_attachments/', blank=True, null=True, verbose_name='附件2')
    attachment3 = models.FileField(upload_to='post_attachments/', blank=True, null=True, verbose_name='附件3')

    # 是否公开：True为公开，False为仅个人可见
    is_public = models.BooleanField(default=True, verbose_name='是否公开')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        获取文章的绝对URL
        """
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def like_count(self):
        """
        获取点赞数量
        """
        return self.likes.count()

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


class Notification(models.Model):
    """
    通知模型
    """
    NOTIFICATION_TYPES = (
        ('like', '点赞'),
        ('comment', '评论'),
        ('message', '私信'),
        ('follow', '关注'),
        ('new_post', '新文章'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='接收者')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', verbose_name='发送者')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='通知类型')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, verbose_name='文章')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, verbose_name='评论')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']

    def __str__(self):
        if self.notification_type == 'like':
            return f'{self.sender.username} 给你的文章《{self.post.title}》点了赞'
        elif self.notification_type == 'comment':
            return f'{self.sender.username} 评论了你的文章《{self.post.title}》'
        elif self.notification_type == 'message':
            return f'{self.sender.username} 给你发送了私信'
        elif self.notification_type == 'follow':
            return f'{self.sender.username} 关注了你'
        elif self.notification_type == 'new_post':
            return f'{self.sender.username} 发布了新文章《{self.post.title}》'
        return f'{self.sender.username} 的通知'


class Message(models.Model):
    """
    私信消息模型
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')
    content = models.TextField(verbose_name='消息内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = '私信'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}: {self.content[:50]}'

    def save(self, *args, **kwargs):
        # 保存消息时更新通知
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            # 创建新消息通知
            Notification.objects.create(
                recipient=self.recipient,
                sender=self.sender,
                notification_type='message',
                post=None,
                comment=None
            )
