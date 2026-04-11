from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型
    """
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 关注关系：用户可以关注多个用户，也可以被多个用户关注
    following = models.ManyToManyField(
        'self',
        through='Follow',
        through_fields=('follower', 'following'),
        related_name='followers',
        symmetrical=False,
        blank=True
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        """粉丝数量"""
        return self.followers.count()

    @property
    def following_count(self):
        """关注数量"""
        return self.following.count()


class Follow(models.Model):
    """
    关注关系模型
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows', verbose_name='关注者')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by', verbose_name='被关注者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    class Meta:
        verbose_name = '关注关系'
        verbose_name_plural = '关注关系'
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.username} 关注了 {self.following.username}'
