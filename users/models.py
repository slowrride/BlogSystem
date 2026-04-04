from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型
    """
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
