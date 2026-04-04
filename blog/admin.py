from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views', 'heat', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('views', 'heat', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content_preview', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'post__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = '评论内容'
