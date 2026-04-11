from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    文章表单
    """
    class Meta:
        model = Post
        fields = ('title', 'content', 'cover_image', 'attachment1', 'attachment2', 'attachment3')
        labels = {
            'title': '标题',
            'content': '内容',
            'cover_image': '封面图片（可选）',
            'attachment1': '附件1（可选）',
            'attachment2': '附件2（可选）',
            'attachment3': '附件3（可选）',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'id': 'content-editor'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment1': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment2': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment3': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    """
    评论表单
    """
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': '评论内容',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
